from flask import Flask, render_template

app = Flask(__name__)

BATTERY = 42

SUBSYSTEMS = [
    {"id": 1, "name": "Двигательная установка", "value": 87,  "unit": "%",  "status": "ok"},
    {"id": 2, "name": "Солнечные панели", "value": 42,  "unit": "%",  "status": "warning"},
    {"id": 3, "name": "Система связи", "value": 12,  "unit": "мс", "status": "ok"},
    {"id": 4, "name": "Бортовой компьютер", "value": 65,  "unit": "°C", "status": "ok"},
    {"id": 5, "name": "Терморегуляция", "value": 94,  "unit": "°C", "status": "critical"},
    {"id": 6, "name": "Камера MASTCAM", "value": 30,  "unit": "%",  "status": "ok"},
    {"id": 7, "name": "Манипулятор", "value": 92,  "unit": "%",  "status": "warning"},
    {"id": 8, "name": "Гидравлика", "value": 55,  "unit": "%",  "status": "ok"},
]


@app.route("/")
def index():
    return render_template(
        "index.html",
        battery=BATTERY,
        subsystems=SUBSYSTEMS,
    )


if __name__ == "__main__":
    app.run(debug=True)