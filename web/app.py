import os
import html
import sqlite3
from flask import Flask, request, make_response, redirect

app = Flask(__name__)
DB_PATH = "web/gradebook.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    return conn


@app.route("/")
def index():
    return (
        "<h1>CSCI 4178 Hall of Fame</h1>"
        "<ul>"
        "<li><a href='/login'>Login and view grades</a></li>"
        "<li><a href='/comments'>View course comments</a></li>"
        "<li><a href='/diag/ping?host=127.0.0.1'>Diagnostic ping</a></li>"
        "</ul>"
    )


# -------------------- Login (intentionally vulnerable) -------------------- #

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return """
        <h1>Login</h1>
        <form method="POST">
            Username: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <input type="submit" value="Login">
        </form>
        <p>Example users: alice, bob, prof.</p>
        """

    username = request.form.get("username", "")
    password = request.form.get("password", "")

    # Intentionally vulnerable: string concatenation with untrusted input
    query = (
        "SELECT username, role FROM users "
        f"WHERE username = '{username}' AND password = '{password}'"
    )

    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute(query)
        row = cur.fetchone()
    except Exception as e:
        conn.close()
        return f"<p>Database error: {e}</p>"

    conn.close()

    if row:
        resp = make_response(
            f"<p>Welcome {row[0]} (role: {row[1]})</p>"
            f"<p><a href='/grades?student={row[0]}'>View your grades</a></p>"
            "<p><a href='/comments'>View comments</a></p>"
        )
        # Very naive "session" using cookies
        resp.set_cookie("username", row[0])
        resp.set_cookie("role", row[1])
        return resp
    else:
        return "<p>Login failed</p><p><a href='/login'>Try again</a></p>"


# -------------------- Grades view (intentionally vulnerable) -------------------- #

@app.route("/grades")
def grades():
    username = request.cookies.get("username")
    if not username:
        return redirect("/login")

    # User can override the student parameter in the URL
    student = request.args.get("student", username)

    # Intentionally vulnerable: SQL concatenation
    query = f"SELECT course, grade FROM grades WHERE student = '{student}'"

    conn = get_db()
    cur = conn.cursor()
    rows = cur.execute(query).fetchall()
    conn.close()

    html_out = f"<h1>Grades for {html.escape(student)}</h1><ul>"
    for course, grade in rows:
        html_out += f"<li>{html.escape(course)}: {html.escape(grade)}</li>"
    html_out += "</ul>"

    html_out += """
    <p>Try exploring the <code>student</code> parameter in the URL.</p>
    <p><a href="/comments">View comments</a></p>
    """
    return html_out


# -------------------- Comments (stored XSS) -------------------- #

@app.route("/comments", methods=["GET"])
def comments():
    conn = get_db()
    cur = conn.cursor()
    rows = cur.execute("SELECT author, text FROM comments").fetchall()
    conn.close()

    html_out = "<h1>Course comments</h1>"
    html_out += """
    <form method="POST" action="/comment">
        Name: <input name="author"><br>
        Comment: <textarea name="text"></textarea><br>
        <input type="submit" value="Post comment">
    </form>
    <p>Note: Instructors may also read this page while logged in.</p>
    """

    # Intentionally vulnerable: text is injected directly into HTML
    for author, text in rows:
        safe_author = html.escape(author)
        # Deliberately omit escaping of text to demonstrate XSS
        html_out += f"<p><b>{safe_author}</b>: {text}</p>"

    html_out += "<p><a href='/'>Back to home</a></p>"
    return html_out


@app.route("/comment", methods=["POST"])
def add_comment():
    author = request.form.get("author", "anonymous")
    text = request.form.get("text", "")

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO comments(author, text) VALUES (?, ?)",
        (author, text),
    )
    conn.commit()
    conn.close()

    return redirect("/comments")


# -------------------- Naive grade update (for Browser Key) -------------------- #

@app.route("/update_grade", methods=["POST"])
def update_grade():
    username = request.cookies.get("username")
    role = request.cookies.get("role")
    if role != "instructor":
        return "<p>Only instructors can update grades.</p>"

    student = request.form.get("student")
    course = request.form.get("course")
    grade = request.form.get("grade")

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE grades SET grade = ? WHERE student = ? AND course = ?",
        (grade, student, course),
    )
    conn.commit()
    conn.close()

    return (
        f"<p>Grade updated for {html.escape(student)} in "
        f"{html.escape(course)} to {html.escape(grade)}</p>"
        '<p><a href="/grades?student=' + html.escape(student) + '">Back to grades</a></p>'
    )


# -------------------- Diagnostic ping (command injection) -------------------- #

@app.route("/diag/ping")
def diag_ping():
    host = request.args.get("host", "127.0.0.1")

    # Intentionally vulnerable: host is passed directly to a shell command
    cmd = f"ping -c 1 {host}"
    stream = os.popen(cmd)
    output = stream.read()

    safe_host = html.escape(host)
    safe_output = html.escape(output[:800])

    return (
        f"<h1>Ping {safe_host}</h1>"
        f"<pre>{safe_output}</pre>"
        "<p><a href='/'>Back to home</a></p>"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
