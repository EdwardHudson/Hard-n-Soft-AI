import tkinter as tk
import requests
import json

API_KEY = "AIzaSyB3p77XJVhMwJ6zB64H15i7iN50ycHR1PY"
MODEL = "gemini-2.5-flash"
URL = f"https://generativelanguage.googleapis.com/v1/models/{MODEL}:generateContent?key={API_KEY}"

chat_history = []  # Stores the full convo

def ask_gemini():
    user_input = entry.get()
    entry.delete(0, tk.END)

    if not user_input.strip():
        return

    chat_log.insert(tk.END, f"You: {user_input}\n")
    chat_history.append({"role": "user", "parts": [{"text": user_input}]})

    payload = {
        "contents": chat_history
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(URL, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            data = response.json()
            reply = data["candidates"][0]["content"]["parts"][0]["text"]
            chat_log.insert(tk.END, f"Hard'n'Soft AI: {reply}\n\n")
            chat_history.append({"role": "model", "parts": [{"text": reply}]})
        else:
            chat_log.insert(tk.END, f"Error {response.status_code}: {response.text}\n\n")
    except Exception as e:
        chat_log.insert(tk.END, f"Exception: {str(e)}\n\n")

# GUI setup
root = tk.Tk()
root.title("Hard'n'Soft AI")

chat_log = tk.Text(root, height=25, width=70, wrap=tk.WORD)
chat_log.pack(padx=10, pady=10)

entry = tk.Entry(root, width=60)
entry.pack(padx=10, side=tk.LEFT, expand=True, fill=tk.X)

send_btn = tk.Button(root, text="Send", command=ask_gemini)
send_btn.pack(padx=10, pady=5, side=tk.RIGHT)

root.mainloop()
