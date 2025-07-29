#!/usr/bin/env python3

from flask import Flask, request, render_template_string
import re
import io, sys
from sys import version

app = Flask(__name__)

banned = "import|chr|os|sys|system|builtin|exec|eval|subprocess|pty|popen|read|get_data"
search_func = lambda word: re.compile(r"\b({0})\b".format(word), flags=re.IGNORECASE).search

template = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Ghost_in_the_Jail - Challenge</title>
  <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
  <style>
    body {
      background: #121212;
      color: #00ff99;
      font-family: 'Share Tech Mono', monospace;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 30px;
      min-height: 100vh;
      margin: 0;
    }
    h1 {
      font-size: 3em;
      margin-bottom: 5px;
      text-shadow: 0 0 10px #00ff99;
    }
    p {
      margin-top: 0;
      margin-bottom: 20px;
      text-align: center;
    }
    form {
      display: flex;
      gap: 10px;
      max-width: 600px;
      width: 100%;
      margin-bottom: 20px;
    }
    input[type=text] {
      flex-grow: 1;
      padding: 12px;
      font-size: 1.1em;
      background: #111;
      border: 2px solid #00ff99;
      border-radius: 5px;
      color: #00ff99;
    }
    input[type=submit] {
      padding: 12px 25px;
      background: #00ff99;
      border: none;
      border-radius: 5px;
      font-weight: bold;
      cursor: pointer;
      color: #111;
      text-shadow: 0 0 3px #006633;
    }
    .response {
      background: #111;
      border: 2px solid #00ff99;
      border-radius: 7px;
      padding: 15px;
      white-space: pre-wrap;
      box-shadow: 0 0 12px #00ff99;
      min-height: 100px;
      max-width: 600px;
      width: 100%;
      margin-top: 10px;
    }
    #hint-container {
      position: fixed;
      bottom: 30px;
      right: 30px;
      text-align: right;
      z-index: 1000;
    }
    #hint-toggle {
      background: #00ff99;
      color: #111;
      border: none;
      border-radius: 20px;
      padding: 10px 15px;
      font-size: 1em;
      cursor: pointer;
      box-shadow: 0 0 8px #00ff99;
      transition: background 0.3s ease;
    }
    #hint-toggle:hover {
      background: #00cc77;
    }
    #hint-message {
      display: none;
      margin-top: 10px;
      background: #111;
      color: #00ff99;
      padding: 10px 15px;
      border: 1px solid #00ff99;
      border-radius: 10px;
      box-shadow: 0 0 10px #00ff99;
      font-family: 'Share Tech Mono', monospace;
      animation: fadeIn 0.5s ease;
    }
    .ghost {
      font-size: 3em;
      animation: float 2.5s ease-in-out infinite;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(5px); }
      to { opacity: 1; transform: translateY(0); }
    }
    @media (max-width: 600px) {
      form {
        flex-direction: column;
      }
      input[type=submit] {
        width: 100%;
      }
    }
  </style>
</head>
<body>
  <div class=\"ghost\">👻</div>
  <h1>Ghost_in_the_Jail</h1>
  <p>Python version: {{ version }}</p>
  <p>What would you like to say?</p>
  <form method="POST" autocomplete="off" spellcheck="false">
    <input name="user_input" type="text" autofocus placeholder=">>> tape ton code ici ..." />
    <input type="submit" value="Envoyer" />
  </form>
  {% if response %}
  <div class="response">{{ response }}</div>
  {% endif %}
  {% if tries_left is not none %}
  {% endif %}

  <div id="hint-container">
    <button id="hint-toggle">💡 Hint ?</button>
    <div id="hint-message">exec function is different from eval. Go and check it</div>
  </div>

  <script>
    document.getElementById("hint-toggle").addEventListener("click", function () {
      const hint = document.getElementById("hint-message");
      hint.style.display = hint.style.display === "block" ? "none" : "block";
    });
  </script>
</body>
</html>
"""

# Simple gestion du nombre d'essais (non thread-safe)
user_tries = 5

def process_input(text):
    global user_tries
    text = text.lower()
    check = search_func(banned)(''.join(text.split("__")))
    if check:
        return f"Nope, we ain't letting you use {check.group(0)}!", True
    if re.match("^(_?[A-Za-z0-9])*[A-Za-z](_?[A-Za-z0-9])*$", text):
        return "You aren't getting through that easily, come on.", True
    try:
      buffer = io.StringIO()
      sys_stdout = sys.stdout
      sys.stdout = buffer
      exec(text, {'globals': globals(), '__builtins__': {}}, {'print': print})
      sys.stdout = sys_stdout
      return buffer.getvalue(), False
    except Exception as e:
      sys.stdout = sys_stdout
      return f"Error: {e}", True

@app.route("/", methods=["GET", "POST"])
def index():
    global user_tries
    response = None
    stop = False
    if request.method == "POST":
      user_input = request.form.get("user_input", "")
      response, stop = process_input(user_input)
    else:
        user_tries = 5

    return render_template_string(template, response=response, version=version, tries_left=user_tries if not stop else 0)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
