# Phase 0 Setup: From Zero to Your First Claude Call

Each step says what to do and why. Platform: Windows 11.

## 1. Install the tools

| Tool | Why | How |
|---|---|---|
| **Python 3.12** | The language everything is written in | Download from python.org. During install, **tick "Add python.exe to PATH"** |
| **VS Code** | Where you write code | Already installed. Add the **Python** extension by Microsoft |
| **Git** | Saves versions of your code | Already installed (this repo uses it) |
| **GitHub account** | Online backup and portfolio | github.com, free |

Check that it worked by opening a VS Code terminal (`` Ctrl+` ``) and running:

```powershell
python --version
git --version
```

## 2. Create a virtual environment

A virtual environment keeps this project's libraries separate from everything else on your computer.

```powershell
cd C:\Users\rojas\Downloads\stouponsAgents
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

You should now see `(.venv)` at the start of the terminal line. Run the `Activate` command every time you open a new terminal.

> If PowerShell says scripts are disabled, run this once:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

## 3. Install the libraries

```powershell
pip install -r requirements.txt
```

## 4. Get a Claude API key

1. Go to **console.anthropic.com** and sign up.
2. Add a small amount of credit ($5 is plenty to start).
3. **Set a monthly spend limit** under Settings → Limits.
4. Create an API key and copy it.
5. In this folder, copy `.env.example` to a new file named `.env`, then paste in your key:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```

`.env` is listed in `.gitignore`, so Git will never upload it. **Never** paste your key into code or chat.

## 5. Your first Claude call

Type this out yourself (don't copy-paste; typing it is how you learn it) into a new file named `hello_claude.py`:

```python
from dotenv import load_dotenv
import anthropic

load_dotenv()                    # reads ANTHROPIC_API_KEY from .env
client = anthropic.Anthropic()   # creates the connection to Claude

response = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=16000,
    system="You are the friendly Stoupons assistant for water-treatment services.",
    messages=[
        {"role": "user", "content": "Hello! What does a water softener do?"}
    ],
)

for block in response.content:
    if block.type == "text":
        print(block.text)

print("Tokens used:", response.usage.input_tokens, "in /", response.usage.output_tokens, "out")
```

Run it:

```powershell
python hello_claude.py
```

You should see Claude's answer and the token count.

### What each part means
- `load_dotenv()`: loads your secret key from `.env`
- `client.messages.create(...)`: sends one request to Claude
- `model`: which Claude model answers. Try changing it to `claude-haiku-5-5` and compare speed and cost
- `system`: the agent's job description. **This is where every agent's personality and rules live**
- `messages`: the conversation so far
- `response.usage`: how many tokens you used, which is how you'll track cost

## 6. Practice exercises (Phase 0)

1. Change the `system` prompt so Claude only answers water-treatment questions and politely declines anything else. Try to break it.
2. Turn `hello_claude.py` into a loop: read input with `input()`, append each turn to `messages`, and keep chatting until the user types `quit`.
3. Load `data/mock/products.json` with Python's `json` module and print each product name.
4. Commit your work:
   ```powershell
   git add .
   git commit -m "Phase 0: first Claude call"
   git push
   ```

When the Phase 0 exit checklist in [ROADMAP.md](ROADMAP.md) is done, you're ready for **Agent #1: Knowledge Agent**.
