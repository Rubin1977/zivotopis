"""
Jednorazový skript na vytvorenie izolovanej SQL playground databázy.
Spusti raz z koreňového priečinka projektu: python create_playground_db.py

Vytvorí súbor sql_playground.sqlite3 vedľa db.sqlite3 - úplne oddelený
od produkčných dát. Tento súbor je bezpečné commitnúť do gitu (obsahuje
len neškodné demo dáta), aby sa objavil aj na produkcii po `git pull`.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sql_playground.sqlite3")

if os.path.exists(DB_PATH):
    print(f"Súbor {DB_PATH} už existuje. Ak ho chceš prepísať, najprv ho zmaž a spusti znova.")
    exit(0)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    subject TEXT NOT NULL
);

CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    teacher_id INTEGER,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id)
);

CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    course_id INTEGER,
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

CREATE TABLE sql_playground (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    note TEXT
);
""")

cur.executemany(
    "INSERT INTO teachers (id, name, subject) VALUES (?, ?, ?)",
    [
        (1, "Mgr. Kováčová", "Biológia"),
        (2, "Ing. Novák", "Informatika"),
        (3, "Dr. Horváth", "Chémia"),
    ],
)

cur.executemany(
    "INSERT INTO courses (id, name, teacher_id) VALUES (?, ?, ?)",
    [
        (1, "Genetika", 1),
        (2, "Programovanie v Pythone", 2),
        (3, "Organická chémia", 3),
    ],
)

cur.executemany(
    "INSERT INTO students (id, name, age, course_id) VALUES (?, ?, ?, ?)",
    [
        (1, "Ján Malý", 21, 1),
        (2, "Eva Veselá", 22, 2),
        (3, "Peter Krátky", 20, 2),
        (4, "Zuzana Biela", 23, 3),
        (5, "Tomáš Dlhý", 21, 1),
    ],
)

cur.execute(
    "INSERT INTO sql_playground (id, note) VALUES (?, ?)",
    (1, "Vitaj v SQL playgrounde! Skús napríklad: SELECT * FROM students;"),
)

conn.commit()
conn.close()

print(f"Hotovo. Vytvorená databáza: {DB_PATH}")
