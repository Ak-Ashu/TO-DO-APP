from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

FILE = "tasks.json"

# Load tasks
def load_tasks():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)

# Save tasks
def save_tasks(tasks):
    with open(FILE, "w") as f:
        json.dump(tasks, f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_tasks")
def get_tasks():
    return jsonify(load_tasks())

@app.route("/add_task", methods=["POST"])
def add_task():
    data = request.json
    tasks = load_tasks()
    tasks.append({"text": data["text"], "done": False})
    save_tasks(tasks)
    return jsonify({"status": "success"})

@app.route("/delete_task", methods=["POST"])
def delete_task():
    index = request.json["index"]
    tasks = load_tasks()
    tasks.pop(index)
    save_tasks(tasks)
    return jsonify({"status": "deleted"})

@app.route("/toggle_task", methods=["POST"])
def toggle_task():
    index = request.json["index"]
    tasks = load_tasks()
    tasks[index]["done"] = not tasks[index]["done"]
    save_tasks(tasks)
    return jsonify({"status": "updated"})

# AI Suggestion (simple logic, can upgrade to OpenAI)
@app.route("/ai_suggest")
def ai_suggest():
    suggestions = [
        "Practice DSA for 1 hour",
        "Work on Flask project",
        "Revise DBMS concepts",
        "Apply for internships",
        "Build portfolio website"
    ]
    import random
    return jsonify({"task": random.choice(suggestions)})

if __name__ == "__main__":
    app.run(debug=True)