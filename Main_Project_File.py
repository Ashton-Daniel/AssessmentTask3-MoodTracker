import customtkinter as ctk
import sqlite3
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

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
user_id = None 
emotion_strength = None
mood_quality = None

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

    # Creates empty label for error message
    label_result = ctk.CTkLabel(app, text="")
    label_result.pack(pady=10)


# Validate Login using SQL
def validate_login(entry_username, entry_password):
    global label_result, user_id
    # Extract username and password from entries
    username = entry_username.get()
    password = entry_password.get()
    
    # Validate and sanitize inputs
    if len(username) < 3 or len(password) < 3:
        label_result.configure(text="Username and password must be at least 3 characters long.", text_color="red")
        return 
    elif not username.isalnum() or not password.isalnum():
        label_result.configure(text="Username and password must be alphanumeric.", text_color="red")
        return
    elif len(password) > 20:
        label_result.configure(text="Password must not exceed 20 characters.", text_color="red")
        return
    elif len(username) > 20:
        label_result.configure(text="Username must not exceed 20 characters.", text_color="red")
        return
    # Check if username and password contains SQL injection characters
    elif "'" in username or "'" in password or ";" in username or ";" in password:
        label_result.configure(text="Username and password must not contain SQL injection characters.", text_color="red")
        return
    else:
        label_result.configure(text="", text_color="black")

    # Check if username and password are matched in the database
    conn = sqlite3.connect("mood_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()

    # If user exists, proceed to submit
    if user:
        user_id = user[0]  # Store user ID for future operations
        submit()
    else:
        # If user does not exist, display error message
        label_result.configure(text="Invalid username or password.", text_color="red")

# Function to clear all widgets
def reset():
    for widget in app.winfo_children():
        widget.destroy()

# Submit button (Opens Main Menu)
def submit():
    # Resets all widgets
    reset()

    # Create main menu label
    test3_label = ctk.CTkLabel(app, text="Mood Tracker")
    test3_label.pack(pady=50)

    # Main Menu Buttons
    button_log_mood = ctk.CTkButton(app, text="Log New Mood", command=Log_New_Mood)
    button_log_mood.pack(pady=10)

    button_mood_history = ctk.CTkButton(app, text="Mood History", command=Mood_History)
    button_mood_history.pack(pady=10)

# Log new mood entry
def Log_New_Mood():
    global emotion_strength, mood_quality

    # Resets all widgets
    reset()
    
    # Mood strength input
    label_question1 = ctk.CTkLabel(app, text="1. On a scale from 0-10, how powerful is the emotion you are currently feeling?")
    label_question1.pack(pady=(20, 5))
    entry_question1 = ctk.CTkEntry(app)
    entry_question1.pack(pady=5)

    # Mood quality input
    label_question2 = ctk.CTkLabel(app, text="2. On a scale from 0-10, how good do you feel?")
    label_question2.pack(pady=(20, 5))
    entry_question2 = ctk.CTkEntry(app)
    entry_question2.pack(pady=5)

    # Button to proceed to Question 3
    button_Q3 = ctk.CTkButton(app, text="Next Question", command=lambda: Question3(entry_question1, entry_question2))
    button_Q3.pack(pady=10)

# Function to handle Question 3 input
def Question3(Q1, Q2):
    global emotion_strength, mood_quality

    # Remove previous error labels before creating a new one
    for widget in app.winfo_children():
        if isinstance(widget, ctk.CTkLabel) and "Please enter" in str(widget.cget("text")):
            widget.destroy()

    # Extract values from entries
    emotion_strength = Q1.get()
    mood_quality = Q2.get()
    # Validate inputs
    try:
        # Convert emotion_strength to an integer
        emotion_strength = int(emotion_strength)
        # Check if emotion_strength is within the valid range
        if emotion_strength > 10 or emotion_strength < 0:
            raise ValueError
    except:
        # If conversion fails or value is out of range, show error message and return
        label_error = ctk.CTkLabel(app, text="Please enter a valid number between 0–10 for emotion strength.", text_color="red")
        label_error.pack(pady=10)
        return

    try:
        # Convert mood_quality to an integer
        mood_quality = int(mood_quality)
        # Check if mood_quality is within the valid range
        if mood_quality > 10 or mood_quality < 0:
            raise ValueError
    except:
        # If conversion fails or value is out of range, show error message and return
        label_error = ctk.CTkLabel(app, text="Please enter a valid number between 0–10 for mood quality.", text_color="red")
        label_error.pack(pady=10)
        return

    # If both inputs are valid, proceed to Question 4
    reset()
    colour_table()

# Function to create an interactive colour-based table for emotions
def colour_table():
    # Creates a scrollable frame for the colour table in case the table is too large for the window
    scrollable_frame = ctk.CTkScrollableFrame(app, width=500, height=300)
    scrollable_frame.pack(expand=True, padx=10, pady=10, fill="both")

    # Counter for cell numbers
    cell_number = 0

    # Create a grid of buttons with colours and emotions based on the rows and columns
    # Iterate though rows and columns to create buttons
    for row in range(rows):
        for col in range(cols):
            # Determine the colour for the cell based on its distance from the edges
            for i in range(len(colours)):
                if row == i or row == rows - i - 1 or col == i or col == cols - i - 1:
                    # Assign colour based on the row or column index then stop
                    cell_colour = colours[i]
                    break

            # Move to the next cell number
            cell_number += 1

            # Create a button for each cell with the corresponding colour and emotion
            btn = ctk.CTkButton(
                scrollable_frame, 
                text=(Emotions[cell_number-1]), # Assign emotion from list based on cell number
                text_color="black", 
                font=("Arial", 15, "bold"), 
                width=100, 
                height=100, 
                fg_color=cell_colour, # Assign colour based on specificity of the emotion
                hover_color="lightgrey",
                border_color="black", 
                border_width=2,
                command=lambda r=row, c=col, ce=cell_number: on_cell_click(r, c, ce) # Call on_cell_click with row, column, and cell number
            )
            # Place the button in the grid
            btn.grid(row=row, column=col, padx=2, pady=2)

# Function to handle cell click events
def on_cell_click(row, col, cell_number):
    global emotion_strength, mood_quality
    # Find the selected emotion based on the cell number
    selected_emotion = Emotions[cell_number-1]

    # If the user_id is set, log the mood and submit
    if user_id is not None:
        log_mood(user_id, emotion_strength, mood_quality, selected_emotion)
        submit()
    else:
        # If user_id is not set, show an error message
        label_error = ctk.CTkLabel(app, text="User ID not set. Please log in first.", text_color="red")
        label_error.pack(pady=10)

# Store mood entry in SQL database
def log_mood(user_id, emotion_strength, mood_quality, selected_emotion):
    conn = sqlite3.connect("mood_tracker.db")
    cursor = conn.cursor()
    # Insert mood entry into the database
    cursor.execute("INSERT INTO moods (user_id, emotion_strength, mood_quality, selected_emotion) VALUES (?, ?, ?, ?)", 
                   (user_id, emotion_strength, mood_quality, selected_emotion))
    conn.commit()
    conn.close()

# Display mood history
def Mood_History():
    # Resets all widgets
    reset()

    # Create scrollable frame for the mood history table in case the table is too large for the window
    scrollable_frame = ctk.CTkScrollableFrame(app, width=600, height=400)
    scrollable_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Define column headers
    headers = ["Emotion Strength", "Mood Quality", "Final Emotion", "Date"]
    # Create header labels
    for col, header in enumerate(headers):
        header_label = ctk.CTkLabel(scrollable_frame, text=header, font=("Arial", 16, "bold"))
        header_label.grid(row=0, column=col, padx=10, pady=5)

    # Retrieve mood history data from the database
    history = get_mood_history(user_id)

    # Create table filled with mood data, starting from row 1 due to header row
    for row, entry in enumerate(history, start=1):
        for col, data in enumerate(entry):
            data_label = ctk.CTkLabel(scrollable_frame, text=str(data), font=("Arial", 14))
            data_label.grid(row=row, column=col, padx=10, pady=5)

    # Create a button to view mood chart
    button_charts = ctk.CTkButton(app, text="View Mood Chart", command=show_chart)
    button_charts.pack(pady=10)

    # Add a return button to go back to the main menu
    button_back = ctk.CTkButton(app, text="Back to Menu", command=submit)
    button_back.pack(pady=10)


# Retrieve mood history from SQL database
def get_mood_history(user_id):
    conn = sqlite3.connect("mood_tracker.db")
    cursor = conn.cursor()
    # Fetch mood entries for the given user_id, ordered by timestamp
    cursor.execute("SELECT emotion_strength, mood_quality, selected_emotion, timestamp FROM moods WHERE user_id=? ORDER BY timestamp DESC", (user_id,))
    moods = cursor.fetchall()
    conn.close()
    # Return the mood entries
    return moods


def show_chart():
    # Resets all widgets
    reset()

    # If there are no mood entries, display an error message
    moods = get_mood_history(user_id)
    if not moods:
        ctk.CTkLabel(app, text="No mood data available to display.", text_color="red").pack(pady=20)
        ctk.CTkButton(app, text="Back to Mood History", command=Mood_History).pack(pady=10)
        return

    # Filter and reverse the mood data to ensure it is in the correct numeric format for the chart and in chronological order
    filtered_data = [
    # Mood strength and mood quality, filtered and converted to integers
    (int(entry[0]), int(entry[1]))

    # For each entry in moods, only include those with valid integer values
    for entry in reversed(moods)
    
    # Check if both emotion_strength and mood_quality are integers
    if isinstance(entry[0], int) and isinstance(entry[1], int)
    ]

    if not filtered_data:
        ctk.CTkLabel(app, text="No valid mood data to display.", text_color="red").pack(pady=20)
        return

    emotion_strength = [e[0] for e in filtered_data]
    mood_quality = [e[1] for e in filtered_data]
    record_indices = list(range(1, len(filtered_data) + 1))

    # Create plot
    fig = Figure(figsize=(7, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(record_indices, emotion_strength, label="Emotion Strength", color='red', marker='o')
    ax.plot(record_indices, mood_quality, label="Mood Quality", color='blue', marker='x')
    ax.set_xticks(record_indices)

    ax.set_title("Mood Trends")
    ax.set_xlabel("Entry Number")
    ax.set_ylabel("Mood Scale (0–10)")
    ax.set_ylim(0, 10)
    ax.set_yticks(range(0, 11))
    ax.legend()
    ax.grid(True)

    native_frame = tk.Frame(master=app)
    native_frame.pack(pady=20, fill="both", expand=True)
    chart_canvas = FigureCanvasTkAgg(fig, master=native_frame)
    chart_canvas.draw()
    chart_canvas.get_tk_widget().pack(fill="both", expand=True)

    ctk.CTkButton(app, text="Back to Mood History", command=Mood_History).pack(pady=10)







# Define table size
rows = 8
cols = rows

# Define colours
colours = ["#FF0000", "#FF8C00", "#32CD32", "#1E90FF", "#0000FF"]

# Create a list of emotions
# Need to fill this list with emotions
Emotions = [
            "", "", "", "", "Elated", "Exhilirated", "Inspired", "",
            "", "Enraged", "Irritated", "Agitated", "Bubbly", "Optimistic", "", "",
            "", "Indignant", "Fury", "Annoyed", "Excited", "Joyful", "", "",
            "", "Injustice", "Provoked", "Anger", "Happy", "Focused", "", "",
            "", "Pessimistic", "Failure", "Sad", "Chill", "Appriciative", "Thoughtful", "",
            "Inferior", "Hopeless", "Depressed", "Down", "Tired", "Content", "Grateful", "",
            "", "Despair", "Gloomy", "Lost", "Complacent", "Loving", "Peaceful", "",
            "", "", "Empty", "", "Sleepy", "Fulfilled", "", "Tranquil",
            ]

# Set up the first page
ctk.set_appearance_mode("light")
app = ctk.CTk()
app.title("Login Page")
app.geometry("1200x800")

login_page()
app.mainloop()