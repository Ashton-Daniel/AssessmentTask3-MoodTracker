# Mood Tracker

## Project Overview
Mood Tracker was developed in response to the growing need for accessible digital tools to manage emotional well-being. In our current digital world, we carry mobile technology everywhere, and yet despite this, wellbeing trackers seem to be limited to outdated methods requiring pen, paper, organisation and way too much time and effort. Mood Tracker aims to be a convenient alternative that allows you to record, view and analyse your moods over time, all from the comfort of your digital device.

## Features
The three core features of the Mood Tracker program are the login system, the mood-based questionnaire and the mood table/graph. The login system  significantly improves the security of this program by adding confidentiality to the program. The mood-based questionnaire is the main attraction of the project as it allows the user to log their mood and store it in an SQL database. The mood history table and graph allow the user to see their mood in a more visually appealing and easy-to-understand format, which can enable the user to see trends in the data more effectively.

## How To Use

### How To Run
1. Go to Releases on the https://github.com/Ashton-Daniel/AssessmentTask3-MoodTracker page and open the most recent release
2. Download the Source Code (zip) folder
3. Go to the folder in the file manager and right click it, then click Extract All.
4. Open VSCode and click File in the top right, then click Open Folder, then navigate to the AssessmentTask3-MoodTracker-Version1 folder and select it.
5. Finally, open Main_Project_File.py and run the program

### Login Credentials
There are 3 test users currently in the database; however, you can add new credentials simply by adding them directly to the 'users' table in the mood_tracker.db database.
The current valid credentials are:
Test: Password
user2: user2
testuser: testpass

### Additional Files
There are 2 files for Unit Testing, a test database, 1 File that shows the creation of the colour table before integration and a README.


## Security
The core security feature of Mood Tracker is the user login system. When the program is launched, the user is required to input their login credentials. In line with authentication guidelines, the system verifies the validity of the credentials by searching the SQL database for a matching username and password. If the credentials are valid, the user will be authorised to access the program. This authorisation is restricted to data linked with their unique account, ensuring they can only access their own information. By preventing unauthorised access, the system successfully safeguards and maintains the confidentiality of sensitive data.

In addition to the core security features, Mood Tracker employs input validation and sanitisation to prevent SQL injection. This strongly establishes the security of the database, further reinforcing the confidentiality and integrity of the data. 
