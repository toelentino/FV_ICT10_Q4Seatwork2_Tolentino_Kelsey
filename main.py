from dataclasses import dataclass
import random
from flask import Flask, jsonify, render_template, request


app = Flask(__name__)


@dataclass
class Classmate:
    name: str
    section: str
    favorite_subject: str

    def introduce(self) -> str:
        return (
            f"Hi! I am {self.name} from section {self.section}. "
            f"My favorite subject is {self.favorite_subject}."
        )


name_pool = [
    "Carriena",
    "Lorenzo",
    "Sasha",
    "Michael",
    "Liam",
    "Miko",
    "Matthew",
    "Alfiona",
    "Cas",
    "Rafa",
    "Sammy",
    "David",
]

section_pool = ["SAPPHIRE", "SAPPHIRE 2", "SAPPHIRE 3", "SAPPHIRE 4", "SAPPHIRE 5"]
subject_pool = ["Science", "Math", "English", "SS", "ICT", "Music and ARTS"]

random.shuffle(name_pool)
classmates = [
    Classmate(name_pool[i], random.choice(section_pool), random.choice(subject_pool))
    for i in range(5)
]


def classmates_payload():
    return [
        {
            "name": c.name,
            "section": c.section,
            "favorite_subject": c.favorite_subject,
            "introduction": c.introduce(),
        }
        for c in classmates
    ]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/classmates", methods=["GET"])
def get_classmates():
    return jsonify({"classmates": classmates_payload()})


@app.route("/add_classmate", methods=["POST"])
def add_classmate():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    section = (data.get("section") or "").strip()
    favorite_subject = (data.get("favorite_subject") or "").strip()

    if not name or not section or not favorite_subject:
        return jsonify({"error": "Please fill out all fields."}), 400

    classmates.append(Classmate(name, section, favorite_subject))
    return jsonify({"classmates": classmates_payload()})


if __name__ == "__main__":
    app.run(debug=True)
