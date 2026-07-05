from flask import Flask, render_template, request
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)


# ---------- DATABASE ----------
def create_database():

    conn = sqlite3.connect("proposal.db")
    cursor = conn.cursor()

    cursor.execute("""
CREATE TABLE IF NOT EXISTS responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT,
    date TEXT,
    time TEXT,
    ip_address TEXT,
    browser TEXT
)
""")

    conn.commit()
    conn.close()


create_database()



# ---------- ROUTES ----------

@app.route("/")
def proposal():
    return render_template("proposal.html")


@app.route("/main")
def main():
    return render_template("main.html")


@app.route("/main2")
def main2():
    return render_template("main2.html")


@app.route("/no")
def no():
    return render_template("no.html")


@app.route("/kissi")
def kissi():
    return render_template("kissi.html")

#---------first track--------

# ---------- FORM ----------

@app.route("/submit", methods=["POST"])
def submit():

    message = request.form.get("message")

    now = datetime.now()
    date = now.strftime("%d-%m-%Y")
    time = now.strftime("%I:%M:%S %p")

    ip_address = request.remote_addr
    browser = request.user_agent.string

    conn = sqlite3.connect("proposal.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO responses
        (message, date, time, ip_address, browser)
        VALUES (?, ?, ?, ?, ?)
          """, (message, date, time, ip_address, browser))

    conn.commit()
    conn.close()

    return render_template("thnku.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

