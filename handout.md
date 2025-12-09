# CSCI 4178 – Cyber Escape: Hall of Fame Edition

**Time**: 1 hour
**Teams**: 3 students per team (flexible)

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

Explore the diagnostic page linked from the home screen. It takes a host parameter and displays some output based on that value.

For this System Key, your team should investigate whether this feature exposes more of the underlying system than intended. Pay attention to how changes in the host parameter affect the output, and whether you can and reveal internal information from the server that should not be exposed.

In your explanation, relate your findings to course topics such as safe use of diagnostic tools, handling user controlled parameters, and separating application behaviour from underlying operating system details.

---

## 4. What to Share

During the lab, your team should keep brief notes for each key: what you managed to do, how you did it (including any important input, URL, or sequence of steps), and which CSCI 4178 concepts explain why it worked. Each team will be invited to share these findings with the instructor on Teams, focusing on a clear description of the vulnerability and at least one realistic way to fix it.
