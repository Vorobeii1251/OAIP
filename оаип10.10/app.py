from flask import Flask, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "change-me-in-production"


@app.route("/")
def index():
    if "visits" not in session:
        session["visits"] = 0

    session["visits"] += 1

    return render_template("index.html", visits=session["visits"])


@app.route("/reset", methods=["POST"])
def reset():
    session["visits"] = 0
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)