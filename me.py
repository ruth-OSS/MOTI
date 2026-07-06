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
@app.route("/data")
def data():
    conn = sqlite3.connect("proposal.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM responses ORDER BY id DESC")
    rows = cursor.fetchall()

    conn.close()

    html = "<h2>SQLite Data</h2><hr>"

    for r in rows:
        html += f"""
        <p>
        <b>ID:</b> {r[0]} <br>
        <b>Message:</b> {r[1]} <br>
        <b>Date:</b> {r[2]} <br>
        <b>Time:</b> {r[3]} <br>
        <b>IP:</b> {r[4]} <br>
        <b>Browser:</b> {r[5]}
        </p><hr>
        """

    return html
@app.route("/headers")
def headers():
    html = "<h2>Request Headers</h2><hr>"

    for key, value in request.headers.items():
        html += f"<b>{key}</b>: {value}<br>"

    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

