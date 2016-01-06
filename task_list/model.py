"""Models adn database functions for Task List project."""

import os
from flask_sqlalchemy import SQLAlchemy

# Connect to the SQLite database
db = SQLAlchemy()

##############################################################################
# Model definitions

class Task(db.Model):
    """Tasks of task list website."""

    __tablename__ = "tasks"

    task_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(64), nullable=True)
    completed = db.Column(db.Boolean(), nullable=False)


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Task task_id=%s title=%s>" % (self.task_id, self.title)

    def __init__(self, title, completed):
        """Construct Task objects"""

        self.title = title
        self.completed = False


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", 'sqlite:///tasks.db')
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
