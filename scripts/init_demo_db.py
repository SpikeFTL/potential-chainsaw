import sqlite3
from pathlib import Path

DB=Path("data/sample.db")
DB.parent.mkdir(exist_ok=True)

if DB.exists():
    DB.unlink()

with sqlite3.connect(DB) as c:
    c.executescript("""
    CREATE TABLE students(id INTEGER PRIMARY KEY,name TEXT NOT NULL,year INTEGER NOT NULL,branch TEXT NOT NULL);
    CREATE TABLE courses(id INTEGER PRIMARY KEY,code TEXT NOT NULL,name TEXT NOT NULL,credits INTEGER NOT NULL);
    CREATE TABLE marks(id INTEGER PRIMARY KEY,student_id INTEGER,course_id INTEGER,score REAL,exam TEXT);
    CREATE TABLE attendance(id INTEGER PRIMARY KEY,student_id INTEGER,course_id INTEGER,attended INTEGER,total INTEGER);
    CREATE TABLE fees(id INTEGER PRIMARY KEY,student_id INTEGER,amount_due REAL,amount_paid REAL,due_date TEXT);
    """)
    c.executemany("INSERT INTO students VALUES(?,?,?,?)",[
        (1,"Aarav Sharma",3,"IT"),(2,"Riya Mehra",2,"CSE"),(3,"Kabir Khan",3,"IT"),
        (4,"Ananya Singh",1,"ECE"),(5,"Vihaan Patel",4,"IT")
    ])
    c.executemany("INSERT INTO courses VALUES(?,?,?,?)",[
        (1,"DB301","Database Systems",4),(2,"AI401","Artificial Intelligence",4),(3,"CN302","Computer Networks",3)
    ])
    c.executemany("INSERT INTO marks VALUES(?,?,?,?,?)",[
        (1,1,1,91,"final"),(2,2,1,84,"final"),(3,3,2,95,"final"),
        (4,4,3,72,"midterm"),(5,5,1,88,"final"),(6,1,2,89,"final"),(7,2,2,79,"midterm")
    ])
    c.executemany("INSERT INTO attendance VALUES(?,?,?,?,?)",[
        (1,1,1,24,26),(2,2,1,21,26),(3,3,2,25,26),(4,4,3,18,26),(5,5,1,23,26)
    ])
    c.executemany("INSERT INTO fees VALUES(?,?,?,?,?)",[
        (1,1,1200,1200,"2026-07-15"),(2,2,1000,600,"2026-07-20"),
        (3,3,1300,1300,"2026-07-15"),(4,4,900,500,"2026-08-01"),(5,5,1500,1000,"2026-07-25")
    ])
print(f"Created {DB}")
