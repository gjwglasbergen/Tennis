from flask import Flask
from uuid import uuid4, UUID

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    return "Welcome to the Tennis App!"


@app.route("/matches", methods=["GET"])
def matches():
    return "List of tennis matches will be displayed here."


@app.route("/matches/<uuid:id>", methods=["GET"])
def match_detail(id: UUID):
    return f"Details of match with UUID {id} will be displayed here."


@app.route("/matches/<uuid:id>/viewer", methods=["GET"])
def match_viewer(id: UUID):
    return f"Viewer for match with UUID {id} will be displayed here."


@app.route("/matches/<uuid:id>/edit", methods=["GET", "POST"])
def match_edit(id: UUID):
    return f"Edit form for match with UUID {id} will be displayed here."


if __name__ == "__main__":
    app.run(debug=True)
