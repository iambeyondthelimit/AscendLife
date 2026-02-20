import sqlite3
import os
import time
import random
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress

console = Console()
DB_PATH = "db/player_progress.db"

if not os.path.exists("db"):
    os.makedirs("db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # PROFILE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            mbti TEXT,
            discipline INTEGER DEFAULT 50,
            strategy INTEGER DEFAULT 50
        )
    ''')

    # NUTRITION
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nutrition (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal TEXT,
            calories INTEGER,
            protein INTEGER
        )
    ''')

    # ACADEMICS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS academics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            subject TEXT,
            score INTEGER
        )
    ''')

    # TO-DO
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT
        )
    ''')

    # GYM
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gym (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exercise TEXT,
            sets INTEGER,
            reps INTEGER,
            weight REAL
        )
    ''')

    # SKILLS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill TEXT,
            level INTEGER
        )
    ''')

    # QUOTES
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote TEXT
        )
    ''')

    # SIDE QUESTS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS side_quests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            challenge TEXT,
            solved INTEGER DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()

init_db()

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def slow_print(text, delay=0.02):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(delay)
    print()

def pause():
    input("\nPress Enter to continue...")

def loading_animation(message="Loading", seconds=2):
    with Progress() as progress:
        task = progress.add_task(f"[cyan]{message}...", total=seconds)
        for i in range(seconds):
            time.sleep(1)
            progress.update(task, advance=1)

def load_or_register_profile():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profile LIMIT 1")
    profile = cursor.fetchone()

    if profile:
        console.print(f"[green]Welcome back, {profile[1]}![/green]")
        conn.close()
        return profile
    else:
        clear()
        console.print(Panel.fit("[bold orange1]Register Player[/bold orange1]", border_style="red"))
        name = input("Name: ")
        age = int(input("Age: "))
        mbti = input("MBTI: ")
        cursor.execute("INSERT INTO profile (name, age, mbti) VALUES (?, ?, ?)", (name, age, mbti))
        conn.commit()
        cursor.execute("SELECT * FROM profile LIMIT 1")
        profile = cursor.fetchone()
        conn.close()
        console.print(f"[green]Registration complete! Welcome, {name}![/green]")
        pause()
        return profile

def game_intro(profile):
    clear()
    Entry()
    Start()
    slow_print("Initializing AscendLife ...", 0.05)
    loading_animation("Booting your path operating system", 3)
    clear()
    console.print(Panel.fit(f"[bold red]WELCOME, {profile[1].upper()}, USELESS PLAYER[/bold red]", border_style="orange1"))
    slow_print(
        f"{profile[1]}, even in your uselessness, a spark of potential exists.\n"
        "Most humans have exponential ability, yet fail due to lack of discipline, strategy, and action.\n"
        "Will you rise… or remain forgotten?"
    )
    pause()

def Entry(): 
    entry = r"""
💀💀💀WELCOME TO THE GAME💀💀💀💀WELCOME TO THE GAME💀💀💀
💀💀💀WELCOME TO THE GAME💀💀💀💀WELCOME TO THE GAME💀💀💀
💀💀💀WELCOME TO THE GAME💀💀💀💀WELCOME TO THE GAME💀💀💀
💀💀💀WELCOME TO THE GAME💀💀💀💀WELCOME TO THE GAME💀💀💀
💀💀💀WELCOME TO THE GAME💀💀💀💀WELCOME TO THE GAME💀💀💀
💀💀💀WELCOME TO THE GAME💀💀💀💀WELCOME TO THE GAME💀💀💀
💀💀💀WELCOME TO THE GAME💀💀💀💀WELCOME TO THE GAME💀💀💀
💀💀💀WELCOME TO THE GAME💀💀💀💀WELCOME TO THE GAME💀💀💀
💀💀💀WELCOME TO THE GAME💀💀💀💀WELCOME TO THE GAME💀💀💀
💀💀💀WELCOME TO THE GAME💀💀💀💀WELCOME TO THE GAME💀💀💀
"""


    for i in range(16):          
        clear()
        print("\n" * i + entry)
        time.sleep(0.08)

    for i in range(16, -1, -1): 
        clear()
        print("\n" * i + entry)
        time.sleep(0.08)

def Start():
    start = "               " + "ARE YOU READY, PLAYER?"
    clear()
    for i in start:
        print(i, end="",flush=True)
        time.sleep(0.03)
    
    time.sleep (1)

    for i in start:
        time.sleep (0.01)
        print("\b \b", end="", flush = True)
        
def nutrition_module():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    while True:
        clear()
        console.print(Panel.fit("[bold orange1]Nutrition Tracker[/bold orange1]", border_style="red"))
        table = Table(title="Meals")
        table.add_column("ID")
        table.add_column("Meal")
        table.add_column("Calories", justify="right")
        table.add_column("Protein", justify="right")
        total_calories = 0
        total_protein = 0
        
        cursor.execute("SELECT * FROM nutrition")
        rows = cursor.fetchall()
        for row in rows:
            table.add_row(str(row[0]), row[1], str(row[2]), str(row[3]))
            total_calories += row[2]
            total_protein += row[3]
        
        table.add_row("[bold]TOTAL[/bold]", "-", f"[bold]{total_calories}[/bold]", f"[bold]{total_protein}[/bold]")
        console.print(table)
        console.print("\n1. Add Meal  2. Back to Dashboard")
        choice = input("Choose: ")
        if choice=="1":
            meal = input("Meal Name: ")
            calories = int(input("Calories: "))
            protein = int(input("Protein: "))
            cursor.execute("INSERT INTO nutrition (meal, calories, protein) VALUES (?, ?, ?)", (meal, calories, protein))
            conn.commit()
        elif choice=="2":
            break
    conn.close()

def academics_module():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    while True:
        clear()
        console.print(Panel.fit("[bold orange1]Academic Records[/bold orange1]", border_style="red"))
        table = Table(title="Records")
        table.add_column("ID")
        table.add_column("Type")
        table.add_column("Subject")
        table.add_column("Score")
        cursor.execute("SELECT * FROM academics")
        for row in cursor.fetchall():
            table.add_row(str(row[0]), row[1], row[2], str(row[3]))
        console.print(table)
        console.print("\n1. Add Record  2. Back to Dashboard")
        choice = input("Choose: ")
        if choice=="1":
            type_ = input("Type (Quiz/Exam/Activity): ")
            subject = input("Subject: ")
            score = int(input("Score: "))
            cursor.execute("INSERT INTO academics (type, subject, score) VALUES (?, ?, ?)", (type_, subject, score))
            conn.commit()
        elif choice=="2":
            break
    conn.close()

def todo_module():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    while True:
        clear()
        console.print(Panel.fit("[bold orange1]To-Do Manager[/bold orange1]", border_style="red"))
        table = Table(title="Tasks")
        table.add_column("ID")
        table.add_column("Task")
        cursor.execute("SELECT * FROM todos")
        for row in cursor.fetchall():
            table.add_row(str(row[0]), row[1])
        console.print(table)
        console.print("\n1. Add Task  2. Delete Task  3. Back to Dashboard")
        choice = input("Choose: ")
        if choice=="1":
            task = input("Task: ")
            cursor.execute("INSERT INTO todos (task) VALUES (?)", (task,))
            conn.commit()
        elif choice=="2":
            tid = int(input("Task ID to delete: "))
            cursor.execute("DELETE FROM todos WHERE id=?", (tid,))
            conn.commit()
        elif choice=="3":
            break
    conn.close()

def gym_module():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    while True:
        clear()
        console.print(Panel.fit("[bold orange1]Gym Tracker[/bold orange1]", border_style="red"))
        table = Table(title="Exercises")
        table.add_column("ID")
        table.add_column("Exercise")
        table.add_column("Sets")
        table.add_column("Reps")
        table.add_column("Weight")
        cursor.execute("SELECT * FROM gym")
        for row in cursor.fetchall():
            table.add_row(str(row[0]), row[1], str(row[2]), str(row[3]), str(row[4]))
        console.print(table)
        console.print("\n1. Add Exercise  2. Back to Dashboard")
        choice = input("Choose: ")
        if choice=="1":
            ex = input("Exercise Name: ")
            sets = int(input("Sets: "))
            reps = int(input("Reps: "))
            weight = float(input("Weight: "))
            cursor.execute("INSERT INTO gym (exercise, sets, reps, weight) VALUES (?, ?, ?, ?)", (ex, sets, reps, weight))
            conn.commit()
        elif choice=="2":
            break
    conn.close()

def skills_module():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    while True:
        clear()
        console.print(Panel.fit("[bold orange1]Skills / Talents[/bold orange1]", border_style="red"))
        table = Table(title="Skills")
        table.add_column("ID")
        table.add_column("Skill")
        table.add_column("Level")
        cursor.execute("SELECT * FROM skills")
        for row in cursor.fetchall():
            table.add_row(str(row[0]), row[1], str(row[2]))
        console.print(table)
        console.print("\n1. Add Skill  2. Back to Dashboard")
        choice = input("Choose: ")
        if choice=="1":
            skill = input("Skill Name: ")
            level = int(input("Level: "))
            cursor.execute("INSERT INTO skills (skill, level) VALUES (?, ?)", (skill, level))
            conn.commit()
        elif choice=="2":
            break
    conn.close()

def about_me_module(profile):
    clear()
    console.print(Panel.fit("[bold orange1]About Me[/bold orange1]", border_style="red"))
    console.print(f"Name: {profile[1]}")
    console.print(f"Age: {profile[2]}")
    console.print(f"MBTI: {profile[3]}")
    console.print(f"Discipline: {profile[4]}")
    console.print(f"Strategy: {profile[5]}")
    # display random motivational quotes
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quotes")
    quotes = cursor.fetchall()
    if quotes:
        q = random.choice(quotes)
        console.print(f"\nQuote: {q[1]}")
    conn.close()
    pause()

def side_quests_module():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    clear()
    cursor.execute("SELECT * FROM side_quests")
    challenges = cursor.fetchall()
    if challenges:
        q = random.choice(challenges)
        console.print(Panel.fit(f"[bold magenta]Side Quest[/bold magenta]\n{q[1]}", border_style="magenta"))
        solve = input("Did you solve it? (y/n): ")
        if solve.lower() == "y":
            cursor.execute("UPDATE side_quests SET solved=1 WHERE id=?", (q[0],))
            conn.commit()
    else:
        console.print("[cyan]No side quests yet.[/cyan]")
    conn.close()
    pause()

def dashboard(profile):
    while True:
        clear()
        console.print(Panel.fit("[bold orange1]PLAYER - Life OS Dashboard[/bold orange1]", border_style="red"))
        console.print("1. Nutrition Tracker")
        console.print("2. Academic Records")
        console.print("3. To-Do Manager")
        console.print("4. Gym Tracker")
        console.print("5. Skills / Talents")
        console.print("6. About Me")
        console.print("7. Side Quests")
        console.print("0. Exit")
        choice = input("Choose: ")
        if choice=="1":
            nutrition_module()
        elif choice=="2":
            academics_module()
        elif choice=="3":
            todo_module()
        elif choice=="4":
            gym_module()
        elif choice=="5":
            skills_module()
        elif choice=="6":
            about_me_module(profile)
        elif choice=="7":
            side_quests_module()
        elif choice=="0":
            console.print("[cyan]Exiting PLAYER. Stay disciplined![/cyan]")
            break
        else:
            console.print("[red]Invalid choice[/red]")
            time.sleep(1)

if __name__=="__main__":
    profile = load_or_register_profile()
    game_intro(profile)
    dashboard(profile)
