#!/usr/bin/env python3

from flask import Flask, request, render_template_string
import re
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
<style>
  @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
  body {
    background: #121212;
    color: #00ff99;
    font-family: 'Share Tech Mono', monospace;
    padding: 30px;
    user-select: none;
  }
  h1 { text-align:center; font-size: 3em; margin-bottom: 5px; text-shadow: 0 0 10px #00ff99;}
  p {text-align:center; margin-top:0; margin-bottom:20px;}
  form {max-width: 600px; margin:auto; display:flex; gap:10px;}
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
    border:none;
    border-radius: 5px;
    font-weight: bold;
    cursor: pointer;
    color:#111;
    text-shadow: 0 0 3px #006633;
  }
  .response {
    max-width: 600px;
    margin: 20px auto 0;
    background: #111;
    border: 2px solid #00ff99;
    border-radius: 7px;
    padding: 15px;
    white-space: pre-wrap;
    box-shadow: 0 0 12px #00ff99;
    min-height: 100px;
  }
</style>
</head>
<body>
  <h1>Ghost_in_the_Jail</h1>
  <p>Python version: {{ version }}</p>
  <p>What would you like to say? (2 tries max)</p>
  <form method="POST" autocomplete="off" spellcheck="false">
    <input name="user_input" type="text" autofocus placeholder=">>> tape ton code ici ..." />
    <input type="submit" value="Envoyer" />
  </form>
  {% if response %}
  <div class="response">{{ response }}</div>
  {% endif %}
  {% if tries_left is not none %}
  <p style="text-align:center; margin-top:20px; color:#00cc66;">Tries left: {{ tries_left }}</p>
  {% endif %}
</body>
</html>
"""

# On stocke le nombre de tentatives restantes par session (simplifié ici)
# Pour démo rapide on le fait en variable globale (attention: pas thread-safe en vrai)

user_tries = 2

def process_input(text):
    global user_tries
    text = text.lower()
    check = search_func(banned)(''.join(text.split("__")))
    if check:
        return f"Nope, we ain't letting you use {check.group(0)}!", True
    if re.match("^(_?[A-Za-z0-9])*[A-Za-z](_?[A-Za-z0-9])*$", text):
        return "You aren't getting through that easily, come on.", True
    else:
        try:
            exec(text, {'globals': globals(), '__builtins__': {}}, {'print':print})
        except Exception as e:
            return f"Error: {e}", True

@app.route("/", methods=["GET", "POST"])
def index():
    global user_tries
    response = None
    stop = False
    if request.method == "POST":
        if user_tries <= 0:
            response = "Sorry, you have no tries left."
            stop = True
        else:
            user_input = request.form.get("user_input", "")
            response, stop = process_input(user_input)
            if stop:
                user_tries = 0
            else:
                user_tries -= 1
    else:
        user_tries = 2  # reset tries on GET

    return render_template_string(template, response=response, version=version, tries_left=user_tries if not stop else 0)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
