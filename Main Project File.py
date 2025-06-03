import customtkinter as ctk
import sqlite3

# Set up SQLite database
conn = sqlite3.connect("mood_tracker.db")
cursor = conn.cursor()

# Create Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# Create Mood entries table
cursor.execute("""
CREATE TABLE IF NOT EXISTS moods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    emotion_strength INTEGER NOT NULL,
    mood_quality INTEGER NOT NULL,
    selected_emotion TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

conn.commit()
conn.close()

# Global variables
label_result = None
user_id = None  # To keep track of logged-in user

# Create Login Page
def login_page():
    global label_result
    # Username entry
    label_username = ctk.CTkLabel(app, text="Username:")
    label_username.pack(pady=(20, 5))
    entry_username = ctk.CTkEntry(app)
    entry_username.pack(pady=5)

    # Password entry
    label_password = ctk.CTkLabel(app, text="Password:")
    label_password.pack(pady=5)
    entry_password = ctk.CTkEntry(app, show="*")
    entry_password.pack(pady=5)

    # Login button
    button_login = ctk.CTkButton(app, text="Login", command=lambda: validate_login(entry_username, entry_password))
    button_login.pack(pady=10)

    label_result = ctk.CTkLabel(app, text="")
    label_result.pack(pady=10)

# Validate Login using SQL
def validate_login(entry_username, entry_password):
    global label_result, user_id
    username = entry_username.get()
    password = entry_password.get()

    conn = sqlite3.connect("mood_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        user_id = user[0]  # Store user ID for future operations
        submit()
    else:
        label_result.configure(text="Invalid username or password.", text_color="red")

# Removes all widgets
def reset():
    for widget in app.winfo_children():
        widget.destroy()

# Submit button (Main Menu)
def submit():
    reset()
    test3_label = ctk.CTkLabel(app, text="Mood Tracker")
    test3_label.pack(pady=50)

    # Main Menu Buttons
    button_log_mood = ctk.CTkButton(app, text="Log New Mood", command=Log_New_Mood)
    button_log_mood.pack(pady=10)

    button_mood_history = ctk.CTkButton(app, text="Mood History", command=Mood_History)
    button_mood_history.pack(pady=10)

# Log new mood entry
def Log_New_Mood():
    reset()

    label_question1 = ctk.CTkLabel(app, text="1. On a scale from 1-10, how powerful is the emotion you are currently feeling?")
    label_question1.pack(pady=(20, 5))
    entry_question1 = ctk.CTkEntry(app)
    entry_question1.pack(pady=5)

    label_question2 = ctk.CTkLabel(app, text="2. On a scale from 1-10, how good do you feel?")
    label_question2.pack(pady=(20, 5))
    entry_question2 = ctk.CTkEntry(app)
    entry_question2.pack(pady=5)

    button_Q3 = ctk.CTkButton(app, text="Next Question", command=lambda: Question3(entry_question1, entry_question2))
    button_Q3.pack(pady=10)

# Store mood entry in SQL database
def log_mood(user_id, emotion_strength, mood_quality, selected_emotion):
    conn = sqlite3.connect("mood_tracker.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO moods (user_id, emotion_strength, mood_quality, selected_emotion) VALUES (?, ?, ?, ?)", 
                   (user_id, emotion_strength, mood_quality, selected_emotion))
    conn.commit()
    conn.close()

def Question3(Q1, Q2):
    global emotion_strength, mood_quality
    emotion_strength = Q1.get()
    mood_quality = Q2.get()
    
    reset()

    colour_table()
    

# Retrieve mood history from SQL database
def get_mood_history(user_id):
    conn = sqlite3.connect("mood_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT emotion_strength, mood_quality, selected_emotion, timestamp FROM moods WHERE user_id=? ORDER BY timestamp DESC", (user_id,))
    moods = cursor.fetchall()
    conn.close()
    return moods

# Display mood history
def Mood_History():
    reset()

    # Create scrollable frame for the mood history table
    scrollable_frame = ctk.CTkScrollableFrame(app, width=600, height=400)
    scrollable_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Define column headers
    headers = ["Emotion Strength", "Mood Quality", "Final Emotion", "Date"]
    for col, header in enumerate(headers):
        header_label = ctk.CTkLabel(scrollable_frame, text=header, font=("Arial", 16, "bold"))
        header_label.grid(row=0, column=col, padx=10, pady=5)

    # Retrieve mood history data from the database
    history = get_mood_history(user_id)

    # Populate rows with mood data
    for row, entry in enumerate(history, start=1):
        for col, data in enumerate(entry):
            data_label = ctk.CTkLabel(scrollable_frame, text=str(data), font=("Arial", 14))
            data_label.grid(row=row, column=col, padx=10, pady=5)

    # Add a return button to go back to the main menu
    button_back = ctk.CTkButton(app, text="Back to Menu", command=submit)
    button_back.pack(pady=10)

# Create colour table for emotions
def on_cell_click(row, col, cell_number):
    global emotion_strength, mood_quality
    selected_cell = [row, col]
    print(f"Cell {selected_cell} selected")
    selected_emotion = Emotions[cell_number-1]
    print(f"Emotion Selected: {selected_emotion}")
    if user_id is not None:
        log_mood(user_id, emotion_strength, mood_quality, selected_emotion)
    submit()

def colour_table():
    scrollable_frame = ctk.CTkScrollableFrame(app, width=500, height=300)
    scrollable_frame.pack(expand=True, padx=10, pady=10, fill="both")
    cell_number = 0
    for row in range(rows):
        for col in range(cols):
            for i in range(len(colours)):
                if row == i or row == rows - i - 1 or col == i or col == cols - i - 1:
                    cell_colour = colours[i]
                    break        
            cell_number += 1
            btn = ctk.CTkButton(
                scrollable_frame, text=(Emotions[cell_number-1]), text_color="black", font=("Arial", 15, "bold"), width=100, height=100, 
                fg_color=cell_colour, border_color="black", border_width=2,
                command=lambda r=row, c=col, ce=cell_number: on_cell_click(r, c, ce)
            )
            btn.grid(row=row, column=col, padx=2, pady=2)

# Define table size
rows = 8
cols = rows

# Define colours from red to blue
colours = ["#FF0000", "#FF4500", "#FF8C00", "#FFD700", "#32CD32", "#1E90FF", "#0000FF"]

# Define emotions
Emotions = [
            "", "", "", "", "Elated", "Exhilirated", "Inspired", "",
            "", "Enraged", "Irritated", "Agitated", "Bubbly", "Optimistic", "", "",
            "", "Indignant", "Fury", "Annoyed", "Excited", "Joyful", "", "",
            "", "Injustice", "Provoked", "Anger", "Happy", "Focused", "", "",
            "", "Pessimistic", "Failure", "Sad", "Chill", "Appriciative", "Thoughtful", "",
            "Inferior", "Hopeless", "Depressed", "Down", "Tired", "Content", "Grateful", "",
            "", "Despair", "Gloomy", "Lost", "Complacent", "Loving", "Peaceful", "",
            "", "", "Empty", "", "Sleepy", "Fulfilled", "", "Tranquil",
            ] * 64  # Adjusted to match original positioning

# Set up the first page
ctk.set_appearance_mode("light")
app = ctk.CTk()
app.title("Login Page")
app.geometry("1200x800")

login_page()
app.mainloop()