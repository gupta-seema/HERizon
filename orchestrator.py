#!/usr/bin/env python3
"""
Simple orchestrator for the Shadow IT multi-agent pipeline.

Flow:
  1) Call SaaS Detector
  2) Call Risk Scoring
  3) Call Policy Mapping
  4) Call Automation Agent
  5) Conditionally call Human Security Agent
"""

import os
import time
import json
import uuid
import logging
from typing import Any, Dict, Optional
import requests
from dotenv import load_dotenv

load_dotenv()

# CONFIG (from env)
API_KEY = os.getenv("AGENT_API_KEY", "")
AGENT_DETECTOR_URL = os.getenv("AGENT_DETECTOR_URL", "")
AGENT_RISK_URL = os.getenv("AGENT_RISK_URL", "")
AGENT_POLICY_URL = os.getenv("AGENT_POLICY_URL", "")
AGENT_AUTOMATION_URL = os.getenv("AGENT_AUTOMATION_URL", "")
AGENT_HUMAN_URL = os.getenv("AGENT_HUMAN_URL", "")
LOG_FILE = os.getenv("LOG_FILE", "orchestrator.log")

# Basic logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger("orchestrator")


# === Helper HTTP function to call an agent endpoint ===
def call_agent(url: str, payload: Dict[str, Any], retries: int = 2, timeout: int = 20) -> Dict[str, Any]:
    """
    Call an agent endpoint using HTTP POST and return parsed JSON response.
    Expects the agent endpoint to accept and return JSON.
    """
    if not url:
        raise ValueError("Agent URL not configured.")
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    last_exc = None
    for attempt in range(1, retries + 2):
        try:
            logger.info("Calling agent %s (attempt %d). Payload keys: %s", url, attempt, list(payload.keys()))
            resp = requests.post(url, json=payload, headers=headers, timeout=timeout)
            resp.raise_for_status()
            data = resp.json()
            logger.info("Agent %s returned status %s", url, resp.status_code)
            return data
        except Exception as e:
            last_exc = e
            logger.warning("Agent call to %s failed on attempt %d: %s", url, attempt, str(e))
            time.sleep(1 * attempt)
    # all retries failed
    logger.error("All attempts to call agent %s failed: %s", url, last_exc)
    raise last_exc


# === Normalizers / validators ===
def ensure_event_id(payload: Dict[str, Any]) -> str:
    if "event_id" in payload and payload["event_id"]:
        return payload["event_id"]
    eid = str(uuid.uuid4())
    payload["event_id"] = eid
    return eid


def normalize_detector_output(output: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert outputs from SaaS Detector into the canonical shape expected by downstream agents.
    """
    # Minimal canonical fields we expect downstream
    canonical = {
        "event_id": output.get("event_id"),
        "detected_app": output.get("detected_app"),
        "category": output.get("category"),
        "reason_detected": output.get("reason_detected"),
        "permissions": output.get("permissions", []),
        "vendor": output.get("vendor"),
        "user": output.get("user"),
        "evidence": output.get("evidence", []),
        "needs_risk_scoring": output.get("needs_risk_scoring", True)
    }
    return canonical


# === The pipeline ===
def run_pipeline(initial_payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run the SaaS Detector -> Risk Scoring -> Policy Mapping -> Automation -> Human Security pipeline.
    Returns the final result dict (the human agent result if escalated, otherwise the automation result).
    """
    # ensure event id
    ensure_event_id(initial_payload)

    # Step 1: SaaS Detector
    logger.info("Step 1: calling SaaS Detector")
    detector_resp = call_agent(AGENT_DETECTOR_URL, initial_payload)
    detector_canonical = normalize_detector_output(detector_resp)

    # If nothing detected, finish early
    if detector_canonical.get("detected_app") is None:
        logger.info("No detected app found; finishing pipeline.")
        return {"stage": "detection_none", "result": detector_canonical}

    # Step 2: Risk Scoring
    logger.info("Step 2: calling Risk Scoring for event %s", detector_canonical["event_id"])
    risk_input = {
        "event_id": detector_canonical["event_id"],
        "detected_app": detector_canonical["detected_app"],
        "category": detector_canonical.get("category"),
        "permissions": detector_canonical.get("permissions"),
        "vendor": detector_canonical.get("vendor"),
        "user": detector_canonical.get("user"),
        "evidence": detector_canonical.get("evidence"),
    }
    risk_resp = call_agent(AGENT_RISK_URL, risk_input)
    logger.info("Risk response keys: %s", list(risk_resp.keys()))

    # Validate risk_resp
    risk_score = risk_resp.get("risk_score") or risk_resp.get("score") or 0
    risk_level = risk_resp.get("risk_level") or "Unknown"

    # Step 3: Policy Mapping
    logger.info("Step 3: calling Policy Mapping")
    policy_input = {
        "event_id": detector_canonical["event_id"],
        "detected_app": detector_canonical["detected_app"],
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_factors": risk_resp.get("risk_factors", []),
        "vendor": detector_canonical.get("vendor"),
        "permissions": detector_canonical.get("permissions"),
        "user": detector_canonical.get("user"),
    }
    policy_resp = call_agent(AGENT_POLICY_URL, policy_input)
    logger.info("Policy response: %s", {k: policy_resp.get(k) for k in ("policy_action", "policy_status", "suggested_alternatives")})

    # Step 4: Automation Agent
    logger.info("Step 4: calling Automation Agent")
    automation_input = {
        "event_id": detector_canonical["event_id"],
        "detected_app": detector_canonical["detected_app"],
        "risk_score": risk_score,
        "risk_level": risk_level,
        "policy_result": policy_resp,
        "user": detector_canonical.get("user"),
    }
    automation_resp = call_agent(AGENT_AUTOMATION_URL, automation_input)
    logger.info("Automation response keys: %s", list(automation_resp.keys()))

    # Decide whether to escalate to human
    escalate_flag = False
    # check explicit flags first
    if automation_resp.get("needs_human_security_agent") or policy_resp.get("escalate_to_human") or risk_resp.get("escalate_to_human"):
        escalate_flag = True
    else:
        # fallback rules based on risk or policy
        if (isinstance(risk_score, (int, float)) and risk_score >= 85) or (policy_resp.get("policy_status") and policy_resp.get("policy_status").lower() in ("blocked", "needs_review")):
            escalate_flag = True

    # Step 5: Human Security Agent (if needed)
    final_result = {
        "event_id": detector_canonical["event_id"],
        "detector": detector_canonical,
        "risk": risk_resp,
        "policy": policy_resp,
        "automation": automation_resp
    }

    if escalate_flag:
        logger.info("Escalation required - calling Human Security Agent")
        human_input = {
            "event_id": detector_canonical["event_id"],
            "context": final_result,
            "requested_action": automation_resp.get("automation_action", "review"),
        }
        human_resp = call_agent(AGENT_HUMAN_URL, human_input)
        final_result["human_review"] = human_resp
        final_result["stage"] = "escalated_to_human"
        logger.info("Human review complete for event %s", detector_canonical["event_id"])
    else:
        final_result["stage"] = "automated"
        logger.info("No human escalation required for event %s", detector_canonical["event_id"])

    # persist log entry (simple file)
    try:
        with open(LOG_FILE, "a") as fh:
            fh.write(json.dumps(final_result) + "\n")
    except Exception as e:
        logger.exception("Failed to append final result to log file: %s", e)

    return final_result


# === Example / test run ===
if __name__ == "__main__":
    # Sample payload to test the pipeline (paste your actual telemetry sample here)
    sample_payload = {
        "user": "jane.doe@company.com",
        "cloudAppUsed": "Notion",
        "domain": "notion.so",
        "timestamp": "2025-11-18T13:04:00Z",
        "permissions": ["files.readwrite", "offline_access"],
        "approvedApps": ["Microsoft 365", "Slack", "Jira", "Figma"]
    }

    try:
        result = run_pipeline(sample_payload)
        print("Pipeline result:")
        print(json.dumps(result, indent=2))
    except Exception as exc:
        logger.exception("Pipeline run failed: %s", exc)
        print("Pipeline error:", str(exc))
