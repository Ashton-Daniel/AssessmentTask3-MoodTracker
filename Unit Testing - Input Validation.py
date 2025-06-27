import sqlite3
import os

# Create a test database path
TEST_DB = "test_login.db"  

# Function to set up a test database
def setup_test_db(db_path):
    # Delete the existing test DB to start fresh
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Connect to the new test DB
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create the users table
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    
    # Insert a test user into the test DB
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("testuser", "testpass"))
    
    # Save and close
    conn.commit()
    conn.close()

# Test functuon to check user credentials similar to the main project file but without the GUI for easier testing
def check_credentials(username, password, db_path="mood_tracker.db"):
    if len(username) < 3 or len(password) < 3:
        return "Too short"
    elif any(char in username for char in ["'", ";", "--"]) or any(char in password for char in ["'", ";", "--"]):
        return "SQL injection attempt"
    elif not username.isalnum() or not password.isalnum():
        return "Not alphanumeric"
    elif len(password) > 20 or len(username) > 20:
        return "Too long"

    # Connect to the test database and query for the user
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()

    # Return success if found, otherwise invalid
    if user:
        return "Success"
    else:
        return "Invalid"

# Function to run unit tests for the login system
def run_tests():
    #  Setup the test database before testing
    setup_test_db(TEST_DB)

    # Test 1: Successful login
    assert check_credentials("testuser", "testpass", db_path=TEST_DB) == "Success"
    print("Test 1 Passed: Valid login")

    # Test 2: Wrong password
    assert check_credentials("testuser", "wrongpass", db_path=TEST_DB) == "Invalid"
    print("Test 2 Passed: Invalid password")

    # Test 3: Too short input
    assert check_credentials("ab", "12", db_path=TEST_DB) == "Too short"
    print("Test 3 Passed: Too short input")

    # Test 4: SQL injection attempt
    assert check_credentials("testuser;", "testpass", db_path=TEST_DB) == "SQL injection attempt"
    print("Test 4 Passed: SQL injection blocked")

    # Test 5: Not alphanumeric input
    assert check_credentials("user!", "pass!", db_path=TEST_DB) == "Not alphanumeric"
    print("Test 5 Passed: Non-alphanumeric input rejected")

# Run tests if this script is executed directly
if __name__ == "__main__":
    run_tests()
