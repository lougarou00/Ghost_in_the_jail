from flask import Flask, request, render_template_string
import re
from sys import modules

modules.clear()
del modules

app = Flask(__name__)

banned = "import|chr|os|sys|system|builtin|exec|eval|subprocess|pty|popen|read|get_data|for|in|join|chr"
search_func = lambda word: re.compile(r"\b({0})\b".format(word), flags=re.IGNORECASE).search

template = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8" />
<title>Ghost_in_the_Jail - Challenge</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

  body {
    margin: 0; padding: 30px;
    font-family: 'Share Tech Mono', monospace;
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    color: #00ff99;
    user-select: none;
  }

  h1 {
    text-align: center;
    font-size: 3em;
    letter-spacing: 0.1em;
    text-shadow: 0 0 10px #00ff99, 0 0 20px #00ff99;
    margin-bottom: 10px;
  }

  p {
    text-align: center;
    font-size: 1.2em;
    margin-top: 0;
    margin-bottom: 30px;
  }

  form {
    max-width: 600px;
    margin: 0 auto;
    display: flex;
    gap: 15px;
  }

  input[type="text"] {
    flex-grow: 1;
    padding: 12px 15px;
    font-size: 1.1em;
    background: #111;
    border: 2px solid #00ff99;
    border-radius: 5px;
    color: #00ff99;
    box-shadow: 0 0 8px #00ff99 inset;
    transition: border-color 0.3s ease;
  }

  input[type="text"]:focus {
    outline: none;
    border-color: #00cc66;
    box-shadow: 0 0 12px #00cc66 inset;
  }

  input[type="submit"] {
    padding: 12px 25px;
    font-size: 1.1em;
    background: #00ff99;
    color: #111;
    font-weight: bold;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    text-shadow: 0 0 3px #006633;
    transition: background 0.3s ease;
  }

  input[type="submit"]:hover {
    background: #00cc66;
  }

  .response {
    max-width: 600px;
    margin: 30px auto 0 auto;
    background: #111;
    border: 2px solid #00ff99;
    border-radius: 7px;
    padding: 20px;
    white-space: pre-wrap;
    font-size: 1em;
    box-shadow: 0 0 12px #00ff99;
    min-height: 80px;
  }
</style>
</head>
<body>
  <h1>Ghost_in_the_Jail</h1>
  <p>Entrez votre commande, esprit hacker :</p>
  <form method="POST" autocomplete="off" spellcheck="false">
    <input name="user_input" type="text" autofocus placeholder=">>> tape ton code ici ..." />
    <input type="submit" value="Exécuter" />
  </form>
  {% if response %}
    <div class="response">{{ response }}</div>
  {% endif %}
</body>
</html>
"""

def process_input(text):
    text = text.lower()
    check = search_func(banned)(''.join(text.split("__")))
    if check:
        return f"Stupid, you can't use {check.group(0)}!"
    if re.match("^(_?[A-Za-z0-9])*[A-Za-z](_?[A-Za-z0-9])*$", text):
        return "You aren't getting through that easily, come on."
    else:
        try:
            output = []
            exec(text, {'globals': globals(), '__builtins__': {}}, {'print': lambda x: output.append(str(x))})
            return "\n".join(output) if output else "(rien à afficher)"
        except Exception as e:
            return f"Error: {e}"

@app.route("/", methods=["GET", "POST"])
def index():
    response = None
    if request.method == "POST":
        user_input = request.form.get("user_input", "")
        response = process_input(user_input)
    return render_template_string(template, response=response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
