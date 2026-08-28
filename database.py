
import sqlite3

DATABASE = "cliniccare.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('Clinician', 'Patient'))
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS health_tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            clinician_id INTEGER NOT NULL,
            patient_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            instructions TEXT NOT NULL,
            due_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            FOREIGN KEY (clinician_id) REFERENCES users(user_id),
            FOREIGN KEY (patient_id) REFERENCES users(user_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            submission_id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER NOT NULL,
            patient_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            submitted_at TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Submitted',
            FOREIGN KEY (task_id) REFERENCES health_tasks(task_id),
            FOREIGN KEY (patient_id) REFERENCES users(user_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            review_id INTEGER PRIMARY KEY AUTOINCREMENT,
            submission_id INTEGER NOT NULL,
            clinician_id INTEGER NOT NULL,
            outcome TEXT NOT NULL,
            notes TEXT,
            reviewed_at TEXT NOT NULL,
            FOREIGN KEY (submission_id) REFERENCES submissions(submission_id),
            FOREIGN KEY (clinician_id) REFERENCES users(user_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            message_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            read_status INTEGER DEFAULT 0,
            FOREIGN KEY (sender_id) REFERENCES users(user_id),
            FOREIGN KEY (receiver_id) REFERENCES users(user_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            clinician_id INTEGER NOT NULL,
            appointment_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Scheduled',
            FOREIGN KEY (patient_id) REFERENCES users(user_id),
            FOREIGN KEY (clinician_id) REFERENCES users(user_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL,
            read_status INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)
 
    connection.commit()
    connection.close()
    print("ClinicCare database created successfully")

if __name__ == "__main__":
    create_tables()
