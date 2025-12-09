# CSCI 4178 – Cyber Escape: Hall of Fame Edition

**Time**: 1 hour 20 minutes
**Teams**: 3 students per team

---

## 1. Story

The Faculty has launched the **CSCI 4178 Hall of Fame** portal. Through this portal, students can:

* Log in and view their grades
* Leave public comments about the course
* Use a small “diagnostic” page that support staff left enabled

The portal was developed quickly and deployed without a proper security review. Your team has been asked to investigate before this system is exposed to the outside world.

Inside this system there are three serious weaknesses, each at a different layer:

* The **database layer**
* The **browser layer**
* The **system layer**

Your mission is to discover **three “keys”**:

* **Database Key**: you can use the portal to access database content that should not be visible to a normal user.
* **Browser Key**: you can make the browser of a logged in user execute JavaScript that you fully control, and use it to affect sensitive data.
* **System Key**: you can make a diagnostic feature run operating system commands of your choice and reveal internal information from the server.

For each key, you must demonstrate what you did and explain how to fix it.

---

## 2. Environment and setup

You will run a small vulnerable lab environment inside Docker on your own laptop.

### Step 1 – Get the lab files

You will clone or download the repository from https://github.com/samerlahoud/hall-of-fame-escape-lab including the following files:

```text
hall-of-fame-escape-lab/
├── Dockerfile
├── requirements.txt
└── web/
    ├── app.py
    ├── schema.sql
    ├── init_db.py
    └── system_secret.txt
```

Open a terminal inside the downloaded folder. For example:

```bash
cd ~/Downloads/hall-of-fame-escape-lab
ls
```

You should see the `Dockerfile` and the `web` directory.

### Step 2 – Build the Docker image

In the same folder, build the image:

```bash
docker build -t hall-of-fame-escape-lab .
```

This creates a local image that contains the vulnerable web application and its SQLite database.

### Step 3 – Run the container

Start the environment:

```bash
docker run --rm -it -p 5000:5000 hall-of-fame-escape-lab
```

Leave this terminal window open. The web application is now available at:

```text
http://localhost:5000
```

Open this URL in your browser.

To stop everything at the end, press `Ctrl + C` in the terminal where `docker run` is running.

---

## 3. Your three keys

Work in your team of three and try to achieve **all three keys**.

You are allowed to:

* Browse the application and click on links
* Modify URLs manually in the address bar
* Use browser developer tools and network tab
* Use any local HTTP tools if you wish (for example curl, Postman)

You are **not** supposed to modify the application source code or the database files directly. Think of yourself as an external attacker who can only interact with the running system.

---

### 3.1 Database Key

Explore the login and grades features:

* There is a login page with some example users (for example `alice`, `bob`, `prof`).
* After logging in, there is a page that shows grades, and it uses a `student` parameter in the URL.

Your goal for the **Database Key** is to show that you can use the application to read database content that should not be available to you. Examples that would count:

* Seeing grades for another student while logged in as yourself.
* Extracting data from a table that is not meant to be visible through the interface.

You will need to link this to database level vulnerabilities discussed in the course and explain how to fix the problem.

---

### 3.2 Browser Key

Explore the comments feature:

* There is a page where users can submit comments about the course.
* Comments are displayed back to any visitor of that page.

You are told that instructors may also read this page while logged in with higher privileges.

Your goal for the **Browser Key** is to show that you can:

* Inject a comment that makes the browser execute JavaScript when the comments page is loaded, and
* Use that code to have an effect on something sensitive, for example submitting a request that changes a grade when an instructor views the page.

Explain how a real system should defend itself.

---

### 3.3 System Key

Explore the diagnostic page:

* There is a link on the home page to a simple “ping” diagnostic endpoint.
* It takes a `host` parameter and shows you the result of a command on the server.

Your goal for the **System Key** is to show that you can use this diagnostic feature to execute operating system commands of your choice and reveal internal information from the server that should not be exposed. For example, you may try to:

* List files on the server
* Read the contents of a file under `web/` such as `system_secret.txt`

You will need to connect this to command injection and unsafe use of shell commands, and explain how to write such diagnostics safely.

---

## 4. What to record

For each key your team finds, write down the following (brief bullet points are enough):

1. **What you achieved**

   * A short description of what you did and what changed or what you saw.
   * For example, “We were logged in as Alice but saw Bob’s grades,” or “When the instructor opens the comments page, Alice’s grade is automatically changed.”

2. **How you did it**

   * Enough detail so that you could repeat it later.
   * For example, a specific URL you used, an HTTP request body, or a comment payload.

3. **Why it worked (course concept)**

   * Which vulnerability or concept from CSCI 4178 explains the behaviour.
   * For example, SQL injection, stored XSS, missing output encoding, command injection, missing input validation, missing CSRF protection.

4. **How to fix it**

   * At least one realistic countermeasure for that vulnerability.
   * For example:

     * Using parameterized queries instead of string concatenation in SQL.
     * Escaping or sanitizing untrusted output in HTML.
     * Adding CSRF tokens on sensitive POST requests.
     * Avoiding shell calls with concatenated user input and using safe APIs instead.

---

## 5. Debrief

At the end of the session, each team will briefly present one or two of its findings:

* Which key you obtained
* What you did
* Which vulnerability it demonstrates
* How a real defender should fix or prevent it

The aim of this final lab is not to have the most clever exploit, but to show that you can:

* Recognise important classes of vulnerabilities
* Turn them into concrete, observable effects
* Reason about realistic mitigations

You are encouraged to share ideas within your team and to focus on understanding and explanation.
