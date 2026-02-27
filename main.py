from typing import List, Optional

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Basic String Store")


class StringItem(BaseModel):
    text: str


strings: List[str] = []


@app.get("/", response_class=HTMLResponse)
async def root() -> str:
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <title>Basic FastAPI String App</title>
        <style>
            body {
                font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
                background: #f5f5f5;
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                margin: 0;
            }
            .card {
                background: #ffffff;
                padding: 24px 28px;
                border-radius: 12px;
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.06);
                max-width: 420px;
                width: 100%;
            }
            h1 {
                margin-top: 0;
                font-size: 20px;
                margin-bottom: 12px;
            }
            p {
                margin-top: 0;
                margin-bottom: 16px;
                color: #555;
                font-size: 14px;
            }
            label {
                display: block;
                font-size: 14px;
                margin-bottom: 6px;
                font-weight: 500;
            }
            input[type="text"] {
                width: 100%;
                padding: 10px 12px;
                border-radius: 8px;
                border: 1px solid #ccc;
                font-size: 14px;
                box-sizing: border-box;
                outline: none;
                transition: border-color 0.15s ease, box-shadow 0.15s ease;
            }
            input[type="text"]:focus {
                border-color: #2563eb;
                box-shadow: 0 0 0 1px rgba(37, 99, 235, 0.2);
            }
            .buttons {
                margin-top: 14px;
                display: flex;
                gap: 8px;
            }
            button {
                flex: 1;
                padding: 10px 0;
                border-radius: 999px;
                border: none;
                cursor: pointer;
                font-size: 14px;
                font-weight: 500;
                transition: background-color 0.15s ease, transform 0.05s ease;
            }
            button#get-btn {
                background: #e5e7eb;
                color: #111827;
            }
            button#post-btn {
                background: #2563eb;
                color: #ffffff;
            }
            button:active {
                transform: translateY(1px);
            }
            .output {
                margin-top: 16px;
                padding: 10px 12px;
                border-radius: 8px;
                background: #f9fafb;
                border: 1px solid #e5e7eb;
                min-height: 40px;
                font-size: 14px;
                white-space: pre-wrap;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Basic String Store</h1>
            <p>Type a string and use <strong>Get</strong> to look it up or <strong>Post</strong> to add it to the in-memory list.</p>
            <label for="text-input">String</label>
            <input id="text-input" type="text" placeholder="Enter a string..." />
            <div class="buttons">
                <button id="get-btn" type="button">Get</button>
                <button id="post-btn" type="button">Post</button>
            </div>
            <div id="output" class="output"></div>
        </div>
        <script>
            function getInputAndOutput() {
                const input = document.getElementById("text-input");
                const output = document.getElementById("output");
                return { input, output };
            }

            async function callGet(text) {
                const { output } = getInputAndOutput();
                if (!output) return;
                output.textContent = "Fetching...";
                try {
                    const res = await fetch(`/strings?text=${encodeURIComponent(text)}`);
                    const data = await res.json();
                    output.textContent = data.message;
                } catch (err) {
                    output.textContent = "Error calling GET endpoint.";
                }
            }

            async function callPost(text) {
                const { output } = getInputAndOutput();
                if (!output) return;
                output.textContent = "Posting...";
                try {
                    const res = await fetch("/strings", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ text })
                    });
                    const data = await res.json();
                    output.textContent = data.message;
                } catch (err) {
                    output.textContent = "Error calling POST endpoint.";
                }
            }

            document.getElementById("get-btn").addEventListener("click", () => {
                const { input, output } = getInputAndOutput();
                if (!input || !output) return;
                const text = input.value.trim();
                if (!text) {
                    output.textContent = "Please enter a string first.";
                    return;
                }
                callGet(text);
            });

            document.getElementById("post-btn").addEventListener("click", () => {
                const { input, output } = getInputAndOutput();
                if (!input || !output) return;
                const text = input.value.trim();
                if (!text) {
                    output.textContent = "Please enter a string first.";
                    return;
                }
                callPost(text);
            });
        </script>
    </body>
    </html>
    """


@app.get("/strings")
async def get_string(text: Optional[str] = Query(None, description="String to look up")):
    if text is None:
        return {
            "message": "No string provided. The current list is: "
            + (", ".join(strings) if strings else "(empty)")
        }

    if text in strings:
        return {"message": f"Here is your string: '{text}'. It was found in our list!"}
    return {"message": f"Sorry, the string '{text}' is not in the list yet."}


@app.post("/strings")
async def add_string(item: StringItem):
    strings.append(item.text)
    return {
        "message": f"Your string '{item.text}' was added successfully! Total items: {len(strings)}"
    }


