import customtkinter as ctk

# Dict of valid usernames and their passwords
VALID_USERS = {
    "alice": "alice123",
    "bob": "bob456",
    "charlie": "charlie789",
    "test": "test"
}

def validate_login():
    username = entry_username.get()
    password = entry_password.get()
    if username in VALID_USERS and password == VALID_USERS[username]:
        submit()
    else:
        label_result.configure(text="Invalid username or password.", text_color="red")

# Set up the main window
ctk.set_appearance_mode("light")
app = ctk.CTk()
app.title("Login Demo")
app.geometry("300x300")

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

# Label Button
label_result = ctk.CTkLabel(app, text="")
label_result.pack(pady=10)


# Login button
button_login = ctk.CTkButton(app, text="Login", command=validate_login)
button_login.pack(pady=10)


# Submit button
def submit():
    # Destroy all widgets in the window
    for widget in app.winfo_children():
        widget.destroy()

    # Prints Test Text
    test3_label = ctk.CTkLabel(app, text=f"W Rizz")
    test3_label.pack(pady=50)

    # Main Menu Buttons
    button_log_mood = ctk.CTkButton(app, text="Log New Mood", command=Log_New_Mood)
    button_log_mood.pack(pady=10)
    button_mood_history = ctk.CTkButton(app, text="Mood History", command=Mood_History)
    button_mood_history.pack(pady=10)

def Log_New_Mood():
    # Destroy all widgets in the window
    for widget in app.winfo_children():
        widget.destroy()

    # Print Test Text
    test1_label = ctk.CTkLabel(app, text=f"Happy Logging")
    test1_label.pack(pady=50)
    
def Mood_History():
    # Destroy all widgets in the window
    for widget in app.winfo_children():
        widget.destroy()

    # Print Test Text
    test2_label = ctk.CTkLabel(app, text=f"Memory Lane")
    test2_label.pack(pady=50)

app.mainloop()