
from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = "cliniccare-development-key"
@app.route("/")
def home():
    return "Welcome to ClinicCare-Lite!"


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form["full_name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        # Hash the password
        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )

        connection = sqlite3.connect("cliniccare.db")
        cursor = connection.cursor()

        try:
            cursor.execute("""
                INSERT INTO users (full_name, email, password_hash, role)
                VALUES (?, ?, ?, ?)
            """, (
                full_name,
                email,
                password_hash.decode("utf-8"),
                role
            ))

            connection.commit()

            return "Registration successful!"

        except sqlite3.IntegrityError:
            return "That email is already registered."

        finally:
            connection.close()
    return render_template("register.html")
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = sqlite3.connect("cliniccare.db")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT user_id, full_name, password_hash, role FROM users WHERE email = ?",
            (email,)
        )

        user = cursor.fetchone()
        connection.close()

        if not user:
            return "No account found with that email."

        password_matches = bcrypt.checkpw(
            password.encode("utf-8"),
            user[2].encode("utf-8")
        )

        if not password_matches:
            return "Incorrect password."

        session["user_id"] = user[0]
        session["full_name"] = user[1]
        session["role"] = user[3]

        print("Logged in user:", user[1])
        print("User role:", repr(user[3]))

        if user[3] == "Patient":
            return redirect(url_for("patient_dashboard"))

        elif user[3] == "Clinician":
            return redirect(url_for("clinician_dashboard"))

        else:
            return "Unknown user role: " + repr(user[3])

    return render_template("login.html")
  
    

@app.route("/patient-dashboard")
def patient_dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "Patient":
        return "Access denied."

    return render_template(
    "patient_dashboard.html",
    full_name=session["full_name"]
)

@app.route("/clinician-dashboard")
def clinician_dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "Clinician":
        return "Access denied."

    return render_template(
        "clinician_dashboard.html",
        full_name=session["full_name"]
    )

@app.route("/create-task", methods=["GET", "POST"])
def create_task():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "Clinician":
        return "Access denied."

    connection = sqlite3.connect("cliniccare.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    if request.method == "POST":

        patient_id = request.form["patient_id"]
        title = request.form["title"]
        instructions = request.form["instructions"]
        due_date = request.form["due_date"]

        cursor.execute("""
            INSERT INTO health_tasks
            (clinician_id, patient_id, title, instructions, due_date)
            VALUES (?, ?, ?, ?, ?)
        """, (
            session["user_id"],
            patient_id,
            title,
            instructions,
            due_date
        ))

        connection.commit()
        connection.close()

        return "Health task assigned successfully!"

    cursor.execute("""
        SELECT user_id, full_name, email
        FROM users
        WHERE role = 'Patient'
    """)

    patients = cursor.fetchall()

    connection.close()

    return render_template(
        "create_task.html",
        patients=patients
    )

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)

