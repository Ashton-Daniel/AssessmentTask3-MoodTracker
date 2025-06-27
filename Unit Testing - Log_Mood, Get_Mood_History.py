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

# Creates a test version of the validation function
# This function handles login logic separately from GUI, so we can test it more easily
def check_credentials(username, password, db_path="mood_tracker.db"):
    if len(username) < 3 or len(password) < 3:
        return "Too short"
    elif not username.isalnum() or not password.isalnum():
        return "Not alphanumeric"
    elif len(password) > 20 or len(username) > 20:
        return "Too long"
    elif "'" in username or ";" in username or "'" in password or ";" in password:
        return "SQL injection attempt"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return "Success"
    else:
        return "Invalid"

# Test the check_credentials function
# Run simple tests
def run_tests():
    # Test 1: Successful login
    assert check_credentials("testuser", "testpass", db_path=TEST_DB) == "Success"
    print("✅ Test 1 Passed: Valid login")

    # Test 2: Wrong password
    assert check_credentials("testuser", "wrongpass", db_path=TEST_DB) == "Invalid"
    print("✅ Test 2 Passed: Invalid password")

    # Test 3: Too short
    assert check_credentials("ab", "12", db_path=TEST_DB) == "Too short"
    print("✅ Test 3 Passed: Too short input")

    # Test 4: SQL injection attempt
    assert check_credentials("testuser;", "testpass", db_path=TEST_DB) == "SQL injection attempt"
    print("✅ Test 4 Passed: SQL injection blocked")

    # Test 5: Not alphanumeric
    assert check_credentials("user!", "pass!", db_path=TEST_DB) == "Not alphanumeric"
    print("✅ Test 5 Passed: Non-alphanumeric input rejected")


# Run tests
if __name__ == "__main__":
    test_log_and_retrieve_mood()
    run_tests()