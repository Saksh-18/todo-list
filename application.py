from flask import Flask, render_template, request, redirect, url_for
import json, os

application = Flask(__name__)
TODO_FILE = "todos.json"

def load_todos():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE) as f:
            return json.load(f)
    return []

def save_todos(todos):
    with open(TODO_FILE, "w") as f:
        json.dump(todos, f)

@application.route("/")
def index():
    todos = load_todos()
    filter_by = request.args.get("filter", "all")
    if filter_by == "active":
        visible = [t for t in todos if not t["done"]]
    elif filter_by == "done":
        visible = [t for t in todos if t["done"]]
    else:
        visible = todos
    active_count = sum(1 for t in todos if not t["done"])
    return render_template("index.html", todos=visible, filter=filter_by, count=active_count)

@application.route("/add", methods=["POST"])
def add():
    text = request.form.get("task", "").strip()
    if text:
        todos = load_todos()
        todos.insert(0, {"text": text, "done": False})
        save_todos(todos)
    return redirect(url_for("index"))

@application.route("/toggle/<int:index>")
def toggle(index):
    todos = load_todos()
    if 0 <= index < len(todos):
        todos[index]["done"] = not todos[index]["done"]
        save_todos(todos)
    return redirect(request.referrer or url_for("index"))

@application.route("/delete/<int:index>")
def delete(index):
    todos = load_todos()
    if 0 <= index < len(todos):
        todos.pop(index)
        save_todos(todos)
    return redirect(request.referrer or url_for("index"))

@application.route("/clear")
def clear():
    todos = [t for t in load_todos() if not t["done"]]
    save_todos(todos)
    return redirect(url_for("index"))

if __name__ == "__main__":
    application.run(debug=True)
```

---

**`requirements.txt`**
```
flask