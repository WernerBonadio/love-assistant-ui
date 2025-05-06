import os
from flask import Flask, request, jsonify, render_template
from openai import OpenAI
#from dotenv import load_dotenv, find_dotenv

#dotenv_path = find_dotenv()
#print("📄 Loading .env from:", dotenv_path)
#load_dotenv(dotenv_path, override=True)
#print("🔐 FINAL OPENAI_API_KEY =", os.getenv("OPENAI_API_KEY"))

import os
api_key = os.getenv("OPENAI_API_KEY")
print("✅ Loaded API key starts with:", api_key[:10] if api_key else "❌ Not found")

openai_client = OpenAI(api_key=api_key)
assistant_id = os.getenv("OPENAI_ASSISTANT_ID")
print("🧪 Loaded Assistant ID:", assistant_id if assistant_id else "❌ NOT FOUND")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    import time
    try:
        user_input = request.json.get("message")
        print(f"🔵 User said: {user_input}")

        thread = openai_client.beta.threads.create()
        openai_client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input
        )
        run = openai_client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        while run.status not in ["completed", "failed", "cancelled"]:
            print(f"⏳ Waiting... run status: {run.status}")
            time.sleep(1)
            run = openai_client.beta.threads.runs.retrieve(run_id=run.id, thread_id=thread.id)

        if run.status != "completed":
            raise Exception(f"Run failed. Status: {run.status}")

        messages = openai_client.beta.threads.messages.list(thread_id=thread.id)
        answer = messages.data[0].content[0].text.value
        print(f"🟢 Assistant replied: {answer}")

        return jsonify({"response": answer})

    except Exception as e:
        print(f"❌ FULL ERROR: {e}")
        return jsonify({"response": "Server error: " + str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

