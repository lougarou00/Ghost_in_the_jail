from flask import Flask, request, render_template_string
import re

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
        body { font-family: Arial, sans-serif; background: #121212; color: #eee; padding: 20px; }
        input[type=text] { width: 80%; padding: 10px; margin: 10px 0; background: #222; border: none; color: #eee; }
        input[type=submit] { padding: 10px 20px; background: #007bff; border: none; color: white; cursor: pointer; }
        .response { margin-top: 20px; padding: 15px; background: #222; border-radius: 5px; white-space: pre-wrap; }
    </style>
</head>
<body>
    <h1>Ghost_in_the_Jail</h1>
    <p>Dis quelque chose au challenge :</p>
    <form method="POST">
        <input name="user_input" autocomplete="off" autofocus />
        <input type="submit" value="Envoyer" />
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
            # On capture le print dans une liste pour afficher ensuite
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
