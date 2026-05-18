from flask import Flask, request, render_template, redirect, session
from db import Base, engine, SessionLocal
from ai import analyze_resume
import models
import PyPDF2
import docx
import json
import os
import bcrypt
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

app = Flask(__name__)

# Secret key from .env
app.secret_key = os.getenv("SECRET_KEY")

Base.metadata.create_all(bind=engine)


@app.route('/')
def home():
    if "user" in session:
        return redirect("/dashboard")

    return redirect("/login")


@app.route('/signup', methods=["GET", "POST"])
def signup():

    db = SessionLocal()

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = db.query(models.User).filter_by(
            email=email
        ).first()

        if existing_user:
            return "User already exists"
        
        # Hash password
        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode('utf-8')

        user = models.User(
            email=email,
            password=hashed_password
        )

        db.add(user)
        db.commit()

        return redirect("/login")

    return render_template("signup.html")


@app.route('/login', methods=["GET", "POST"])
def login():

    db = SessionLocal()

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = db.query(models.User).filter_by(
            email=email,
        ).first()

        # Debug prints
        print("Entered password:", password)

        if user:
            print("Stored password:", user.password)

        if bcrypt.checkpw(
            password.encode("utf-8"),
            user.password.encode("utf-8")
        ):
            session["user"] = user.email
            return redirect("/dashboard")

        return "Invalid Credentials"

    return render_template("login.html")


@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():

    if "user" not in session:
        return redirect("/login")

    result = None

    if request.method == "POST":

        user_goal = request.form.get("role")
        resume_text = request.form.get("resume")

        file = request.files.get("file")

        # PDF/DOCX handling

        if file and file.filename != "":

            if file.filename.endswith(".pdf"):

                try:
                    pdf_reader = PyPDF2.PdfReader(file)

                    text = ""

                    for page in pdf_reader.pages:
                        text += page.extract_text() or ""

                    resume_text = text

                except Exception as e:
                    result = {
                        "error": f"PDF Error: {str(e)}"
                    }

            elif file.filename.endswith(".docx"):

                try:
                    document = docx.Document(file)

                    text = ""

                    for para in document.paragraphs:
                        text += para.text + "\n"

                    resume_text = text

                except Exception as e:
                    result = {
                        "error": f"DOCX Error: {str(e)}"
                    }

        # AI analysis

        if resume_text and user_goal:

            try:

                result = analyze_resume(
                    resume_text,
                    user_goal
                )

                db = SessionLocal()

                user = db.query(models.User).filter_by(
                    email=session["user"]
                ).first()

                report = models.Reports(
                    user_id=user.id,
                    resume_text=resume_text,
                    result=json.dumps(result)
                )

                db.add(report)
                db.commit()

            except Exception as e:

                result = {
                    "error": f"AI Error: {str(e)}"
                }

    return render_template(
        "dashboard.html",
        user=session["user"],
        result=result
    )


@app.route('/history')
def history():

    if "user" not in session:
        return redirect("/login")

    db = SessionLocal()

    user = db.query(models.User).filter_by(
        email=session["user"]
    ).first()

    reports = db.query(models.Reports).filter_by(
        user_id=user.id
    ).all()

    parsed_reports = []

    for r in reports:

        try:
            parsed_result = json.loads(r.result)

        except:
            parsed_result = {}

        parsed_reports.append({
            "resume": r.resume_text,
            "result": parsed_result
        })

    return render_template(
        "history.html",
        reports=parsed_reports
    )


@app.route('/logout')
def logout():

    session.pop("user", None)

    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)