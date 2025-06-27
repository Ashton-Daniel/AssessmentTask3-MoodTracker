import sqlite3
from Main_Project_File import log_mood, get_mood_history

# Create a test user
def create_test_user():
    conn = sqlite3.connect("mood_tracker.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("testuser", "testpass"))
    conn.commit()
    cursor.execute("SELECT id FROM users WHERE username=?", ("testuser",))
    user_id = cursor.fetchone()[0]
    conn.close()
    return user_id

# Test log_mood and get_mood_history functions
def test_log_and_retrieve_mood():
    user_id = create_test_user()

    # Call log_mood with test data
    log_mood(user_id, 6, 8, "Grateful")

    # Call get_mood_history to retrieve the test data
    history = get_mood_history(user_id)

    # Assert that the history contains the logged mood
    assert len(history) > 0, "No mood entries found."
    latest_entry = history[0]
    
    # Check if the latest entry matches the logged mood
    assert latest_entry[0] == 6, "Emotion strength mismatch."
    assert latest_entry[1] == 8, "Mood quality mismatch."
    assert latest_entry[2] == "Grateful", "Emotion label mismatch."
    
    # If all assertions pass, print success message
    print("log_mood and get_mood_history functions passed the test successfully.")


# Run tests
if __name__ == "__main__":
    test_log_and_retrieve_mood()