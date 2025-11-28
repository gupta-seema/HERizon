import time
from flask import Flask, render_template, request, redirect, url_for
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import ListSortOrder
import os
import sys

# Setting a low timeout for demonstration; adjust as necessary
# This helps the connection attempt fail fast if the environment isn't set up.
API_TIMEOUT = 30 

app = Flask(__name__)

# ------------------------
# Azure AI Foundry Project Configuration
# ------------------------

try:
    # 1. Initialize AIProjectClient
    project = AIProjectClient(
        credential=DefaultAzureCredential(),
        endpoint="https://herizon-resource.services.ai.azure.com/api/projects/herizon",
        timeout=API_TIMEOUT
    )

    # 2. Fetch your main orchestrator agent
    # REPLACE THIS ID if your agent ID has changed!
    MAIN_AGENT_ID = "asst_23qYh19ZTPuQcPpwY3FARopi" 
    main_agent = project.agents.get_agent(MAIN_AGENT_ID)
    print(f"Successfully connected to Azure AI Project and fetched agent {MAIN_AGENT_ID}.")

except Exception as e:
    print("-" * 50)
    print("FATAL ERROR: Failed to connect to Azure AI.")
    print(f"Error: {e}")
    print("Please ensure you have run 'az login' and that the endpoint/ID are correct.")
    print("-" * 50)
    # Exiting the application if the connection fails at startup
    sys.exit(1)


# Global state for the chat session
conversation_history = []
thread = None

def wait_for_thread_ready(thread_id):
    """Waits until the thread is free from any active runs to prevent thread locking errors."""
    max_wait_time = 60 # seconds
    start_time = time.time()
    
    while time.time() - start_time < max_wait_time:
        try:
            # List the most recent run for this thread
            runs = project.agents.runs.list(thread_id=thread_id, limit=1)
            
            # Check if the thread is free (no runs, or the latest one is a final state)
            if not runs or runs[0].status in [
                "completed", "failed", "cancelled", "expired", "deleted"
            ]:
                return True  # Thread is ready
            
            # If a run is still active, wait
            print(f"Thread busy (Run {runs[0].id}, Status: {runs[0].status}). Waiting...")
            time.sleep(1)
            
        except Exception as e:
            # Handle temporary API issues gracefully
            print(f"Error checking run status: {e}. Retrying in 1 second...")
            time.sleep(1)
            
    print(f"WARNING: Thread {thread_id} timed out waiting for run to complete.")
    return True # Proceed anyway, accepting a potential thread-locking error


@app.route("/", methods=["GET", "POST"])
def chat():
    global conversation_history, thread

    if request.method == "POST":
        user_message = request.form["message"]
        # Add user message to history immediately for display
        conversation_history.append({"role": "user", "text": user_message})

        # 1. Initialize Thread
        if thread is None:
            thread = project.agents.threads.create()
            print(f"New Thread Created: {thread.id}")

        # 2. Wait for Thread to be Ready (The fix for the HttpResponseError)
        wait_for_thread_ready(thread.id)

        try:
            # 3. Send User Message
            project.agents.messages.create(
                thread_id=thread.id,
                role="user",
                content=user_message
            )

            # 4. Run the Main Orchestrator Agent
            # NOTE: Removed the 'Run' type hint to fix the ImportError
            run = project.agents.runs.create_and_process(
                thread_id=thread.id,
                agent_id=main_agent.id
            )
            print(f"Run Started: {run.id}")

            # 5. Wait until the run completes
            while run.status not in ["completed", "failed", "cancelled", "expired", "deleted"]:
                time.sleep(0.5)
                # Re-fetch the run status
                run = project.agents.runs.get(run.id)
            
            print(f"Run Finished with Status: {run.status}")

            # 6. Fetch and Rebuild History
            if run.status == "completed":
                messages = project.agents.messages.list(
                    thread_id=thread.id,
                    order=ListSortOrder.ASCENDING
                )
                
                conversation_history = []
                for msg in messages:
                    # Filter for messages with actual text content
                    if msg.text_messages:
                        role = "user" if msg.role == "user" else "agent"
                        conversation_history.append({
                            "role": role,
                            "text": msg.text_messages[-1].text.value
                        })
            else:
                # Add a failure message if the run did not complete successfully
                conversation_history.append({
                    "role": "agent",
                    "text": f"Error: The agent run failed with status: {run.status}. Please check your agent's logs in Azure AI Studio."
                })

        except Exception as e:
            # General error handling for API calls
            error_message = f"A critical error occurred while communicating with Azure AI: {e}"
            print(error_message)
            conversation_history.append({
                "role": "agent",
                "text": error_message
            })


        return redirect(url_for("chat"))

    # GET request: render the chat page
    return render_template("chat.html", conversation=conversation_history)


if __name__ == "__main__":
    app.run(debug=True)