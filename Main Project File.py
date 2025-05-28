import customtkinter as ctk

# Temporary dict of valid usernames and their passwords
VALID_USERS = {
    "alice": "alice123",
    "bob": "bob456",
    "charlie": "charlie789",
    "test": "test"
}

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
    button_login = ctk.CTkButton(app, text="Login", command=lambda : validate_login(entry_password, entry_password))
    button_login.pack(pady=10)

    label_result = ctk.CTkLabel(app, text="")
    label_result.pack(pady=10)

# Checks username and password
def validate_login(entry_username, entry_password):
    global label_result
    username = entry_username.get()
    password = entry_password.get()
    if username in VALID_USERS and password == VALID_USERS[username]:
        submit()  
    else:
        label_result.configure(text="Invalid username or password.", text_color="red")
   
# Removes all widgets
def reset():
    for widget in app.winfo_children():
        widget.destroy()


# Submit button
def submit():
    # Destroy all widgets in the window
    reset()

    # Prints Test Text
    test3_label = ctk.CTkLabel(app, text=f"Mood Tracker")
    test3_label.pack(pady=50)

    # Main Menu Buttons
    button_log_mood = ctk.CTkButton(app, text="Log New Mood", command=Log_New_Mood)
    button_log_mood.pack(pady=10)
    button_mood_history = ctk.CTkButton(app, text="Mood History", command=Mood_History)
    button_mood_history.pack(pady=10)

def Log_New_Mood():
    # Destroy all widgets in the window
    reset()

    # Create Questions 1 & 2
    label_question1 = ctk.CTkLabel(app, text="1. On a scale from 1-10 how powerful is the emotion you are currently feeling?")
    label_question1.pack(pady=(20, 5))
    label_question2 = ctk.CTkLabel(app, text="2. On a scale from 1-10 how good do you feel?")
    label_question2.pack(pady=(20, 5))

    button_Q3 = ctk.CTkButton(app, text="Next Question", command=lambda : Question3())
    button_Q3.pack(pady=10)
    
def Mood_History():
    # Destroy all widgets in the window
    reset()

    # Print Test Text
    scrollable_frame2 = ctk.CTkScrollableFrame(app, width=500, height=300)
    scrollable_frame2.pack(pady=20, padx=20, fill="both", expand=True)

    for i in range(20):
        ctk.CTkLabel(scrollable_frame2, text=f"Label {i+1}", font=("Arial", 16)).pack(pady=5, padx=10)


def on_cell_click(row, col, cell_number):
    selected_cell = [row, col]
    print(f"Cell {selected_cell} selected")
    print(f"Emotion Selected: {Emotions[cell_number-1]}")


# Create a colour table
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
            cell_number = cell_number + 1
            btn = ctk.CTkButton(
                scrollable_frame, text=(Emotions[cell_number-1]), text_color="black", font = ("Arial", 15, "bold"), width=100, height=100, 
                fg_color=cell_colour, border_color="black", border_width=2,
                command=lambda r=row, c=col, ce=cell_number : on_cell_click(r, c, ce)
            )
            btn.grid(row=row, column=col, padx=2, pady=2)

def Question3():
    reset()
    colour_table()

label_result = None

# Define table size
rows = 8
cols = rows

# Define colours from red to blue
colours = ["#FF0000", "#FF4500", "#FF8C00", "#FFD700", "#32CD32", "#1E90FF", "#0000FF"]

# Define Emotions
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