import customtkinter as ctk
import tkinter as tk

# Initialize main application window
app = ctk.CTk()
app.geometry("500x500")
app.title("Custom Table with Buttons")

# Function to handle button click
def on_cell_click(row, col, cell_number):
    selected_cell = [row, col]
    print(f"Cell {selected_cell} selected")
    print(f"Emotion Selected: {Emotions[cell_number-1]}")

# Define table size
rows = 8
cols = rows

# Create a frame for the table
frame = ctk.CTkFrame(app, border_width=2, border_color="black")
frame.pack(expand=True, padx=10, pady=10)

# Define colours from red to blue
colours = ["#FF0000", "#FF4500", "#FF8C00", "#FFD700", "#32CD32", "#1E90FF", "#0000FF"]

# Define Emotions
Emotions = [
            "", "", "", "", "Elated", "Exhilirated", "", "",
            "", "Enraged", "Irritated", "Agitated", "Bubbly", "Optimistic", "", "",
            "", "Indignant", "Fury", "Annoyed", "Excited", "Joyful", "", "",
            "", "Injustice", "Provoked", "Anger", "Happy", "Focused", "", "",
            "", "Pessimistic", "Failure", "Sad", "Chill", "Appriciative", "Thoughtful", "",
            "", "Hopeless", "Depressed", "Down", "Tired", "Content", "", "",
            "", "Despair", "", "Lost", "Complacent", "Loving", "Peaceful", "",
            "", "", "", "", "Sleepy", "Fulfilled", "", "Tranquil",
            ]




# Create a colour table
def colour_table():
    cell_number = 0
    for row in range(rows):
        for col in range(cols):
            for i in range(len(colours)):
                if row == i or row == rows - i - 1 or col == i or col == cols - i - 1:
                    cell_colour = colours[i]
                    break        
            cell_number = cell_number + 1
            btn = ctk.CTkButton(
                frame, text=(Emotions[cell_number-1]), text_color="black", font = ("Arial", 15, "bold"), width=100, height=100, 
                fg_color=cell_colour, border_color="black", border_width=2,
                command=lambda r=row, c=col, ce=cell_number : on_cell_click(r, c, ce)
            )
            btn.grid(row=row, column=col, padx=2, pady=2)

# Run colour table
colour_table()

# Run the application
app.mainloop()