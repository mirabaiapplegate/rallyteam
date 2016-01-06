"""Task List."""

from flask import Flask, render_template, redirect, request, json, jsonify
from model import Task, connect_to_db, db
from flask_debugtoolbar import DebugToolbarExtension
import os
import json

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = os.environ.get("FLASK_SECRET_KEY","ABC")


@app.route('/')
def root_route():
    """ Homepage """

    return render_template("task_list.html")


@app.route('/tasks', methods=["GET"])
def tasks_index():
    """ List all the tasks. """
    task_models = Task.query.order_by(Task.task_id.asc())
    tasks = []

    for task in task_models:
        task_data = { "id": task.task_id, "title": task.title, "completed": task.completed }
        tasks.append(task_data)

    return json.dumps(tasks)


@app.route('/tasks', methods=['POST'])
def create_task():
    """ Create task. """

    json = request.get_json()
    title = json["title"]
    completed = json["completed"]

    new_task = Task(title, completed)

    db.session.add(new_task)
    db.session.commit()

    return jsonify({ "id": new_task.task_id, "title": new_task.title, "completed": new_task.completed })

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """ Update task. """

    json = request.get_json()
    title = json["title"]
    completed = json["completed"]

    db.session.query(Task).filter(Task.task_id==task_id).update({ "title": title, "completed": completed })
    db.session.commit()

    return jsonify({ "id": task_id, "title": title, "completed": completed })



@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """ Delete task. """


if __name__ == "__main__":
    from doctest import testmod
    if testmod().failed == 0:
        app.debug = True
        connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    PORT = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=PORT)
