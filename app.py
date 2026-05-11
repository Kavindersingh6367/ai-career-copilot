from flask import Flask, render_template, request, redirect, session
from ai import analyze_resume
from db import Base, engine, SessionLocal
import model
import PyPDF2
import docx
import json
from dotenv import load_dotenv
import os
app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")
Base.metadata.create_all(bind=engine)


# HOME
@app.route('/')
def home():

    if "user" in session:
        return redirect('/dashboard')

    return redirect('/login')


# SIGNUP
@app.route("/signup", methods=["GET", "POST"])
def signup():

    db = SessionLocal()

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = db.query(model.user).filter_by(
            email=email
        ).first()

        if existing_user:
            return "User already exists"

        user = model.user(
            email=email,
            password=password
        )

        db.add(user)
        db.commit()

        return redirect('/login')

    return render_template("signup.html")


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    db = SessionLocal()

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = db.query(model.user).filter_by(
            email=email,
            password=password
        ).first()

        if user:

            session["user"] = user.email

            return redirect('/dashboard')

        else:
            return "Invalid email or password"

    return render_template("login.html")


# DASHBOARD
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():

    if "user" not in session:
        return redirect('/login')

    result = None

    if request.method == "POST":

        user_goal = request.form.get("role")
        resume_text = request.form.get("resume", "")

        file = request.files.get("resume_file")

        # FILE HANDLING

        if file and file.filename != "":

            # PDF
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

            # DOCX
            elif file.filename.endswith(".docx"):

                try:

                    doc = docx.Document(file)

                    text = ""

                    for para in doc.paragraphs:
                        text += para.text + "\n"

                    resume_text = text

                except Exception as e:

                    result = {
                        "error": f"DOCX Error: {str(e)}"
                    }

        # AI ANALYSIS
        if resume_text and user_goal:

            try:

                result = analyze_resume(
                    resume_text,
                    user_goal
                )

                # SAVE TO DATABASE

                db = SessionLocal()

                user = db.query(model.user).filter_by(
                    email=session["user"]
                ).first()

                report = model.Report(
                    user_id=user.id,
                    resume_text=resume_text,
                    results=json.dumps(result)
                )

                db.add(report)
                db.commit()

            except Exception as e:

                result = {
                    "error": f"AI Analysis Error: {str(e)}"
                }

    return render_template(
        "dashboard.html",
        user=session["user"],
        result=result
    )


# HISTORY
@app.route("/history")
def history():

    if "user" not in session:
        return redirect('/login')

    db = SessionLocal()

    user = db.query(model.user).filter_by(
        email=session["user"]
    ).first()

    reports = db.query(model.Report).filter_by(
        user_id=user.id
    ).all()

    parsed_reports = []

    for r in reports:

        try:
            parsed_result = json.loads(r.results)

        except:
            parsed_result = {}

        parsed_reports.append({
            "resume_text": r.resume_text,
            "results": parsed_result
        })

    return render_template(
        "history.html",
        reports=parsed_reports
    )


# LOGOUT
@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect('/login')


if __name__ == "__main__":
    app.run(debug=True)