from fastapi import FastAPI, UploadFile, File, Form

from llm_chain import chat_with_resume
from parser import extract_text
import json

app = FastAPI()


@app.post("/chat")
async def chat(
    file: UploadFile = File(...),              # binary resume
    user_input: str = Form(...),               # user message
    chat_history: str = Form("[]")             # stringified JSON
):
    try:
        chat_history = json.loads(chat_history)
        resume_text = extract_text(file)

        if not resume_text.strip():
            return {"reply": "Could not extract text from resume"}

        reply = chat_with_resume(
            resume_text,
            chat_history,
            user_input
        )

        return {"reply": reply}

    except Exception as e:
        print("ERROR:", str(e))
        return {"reply": f"Backend error: {str(e)}"}