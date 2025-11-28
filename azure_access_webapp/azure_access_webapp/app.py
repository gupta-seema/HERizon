import time
from flask import Flask, render_template, request, redirect, url_for
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import ListSortOrder

app = Flask(__name__)

# ---------- Azure AI Foundry Client ----------
project = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint="https://access-agent-resource.services.ai.azure.com/api/projects/access-agent"
)

main_agent = project.agents.get_agent("asst_emDqOSy5n3OFGlU6YEpVw7R6")

# Create a persistent thread once
thread = project.agents.threads.create()

conversation_history = []


def wait_for_run(thread_id, run_id):
    """Poll the run until it completes."""
    while True:
        run = project.agents.runs.get(thread_id=thread_id, run_id=run_id)

        if run.status in ["completed", "failed", "cancelled"]:
            return run

        time.sleep(1)


@app.route("/", methods=["GET", "POST"])
def chat():
    global conversation_history, thread

    if request.method == "POST":
        user_message = request.form["message"].strip()

        if not user_message:
            return redirect(url_for("chat"))

        # Store in UI
        conversation_history.append({"role": "user", "text": user_message})

        # ---------- 1. Add user message to Azure thread ----------
        project.agents.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_message
        )

        # ---------- 2. Start a new run ----------
        run = project.agents.runs.create(
            thread_id=thread.id,
            agent_id=main_agent.id
        )

        # ---------- 3. Wait for run to finish ----------
        wait_for_run(thread.id, run.id)

        # ---------- 4. Read ALL messages in thread ----------
        messages = project.agents.messages.list(
            thread_id=thread.id,
            order=ListSortOrder.ASCENDING
        )

        # Build conversation
        conversation_history = []
        for msg in messages:
            if msg.text_messages:
                text = msg.text_messages[-1].text.value
                role = "user" if msg.role == "user" else "access-agent"
                conversation_history.append({"role": role, "text": text})

        return redirect(url_for("chat"))

    return render_template("chat.html", conversation=conversation_history)


if __name__ == "__main__":
    app.run(debug=True)
