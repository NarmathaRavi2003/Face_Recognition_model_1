from flask import Flask, render_template, request, redirect, url_for
import os
import face_recognition
import cv2
import numpy as np

app = Flask(__name__)

# Dictionary to store user details
users = {}

def register_user(username, face_encoding):
    users[username] = {'face_encoding': face_encoding}

def recognize_user(face_encoding):
    for username, user_data in users.items():
        known_encoding = user_data['face_encoding']
        # Compare the input face encoding with the known face encoding
        result = face_recognition.compare_faces([known_encoding], face_encoding)

        if result[0]:
            return username

    return None

# OpenCV setup for webcam
video_capture = cv2.VideoCapture(0)  # Use 0 for the default webcam

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']

        # Capture a frame from the webcam
        _, frame = video_capture.read()

        # Check if the frame is not empty
        if frame is None:
            print("Empty frame. Unable to process.")
            return render_template('signup_failure.html')  # or return an appropriate response

        # Get the face encoding from the captured frame
        face_encoding = face_recognition.face_encodings(frame)[0]

        # Register the user
        register_user(username, face_encoding)

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Capture a frame from the webcam
        _, frame = video_capture.read()

        # Check if the frame is not empty
        if frame is None:
            print("Empty frame. Unable to process.")
            return render_template('login_failure.html')  # or return an appropriate response

        # Get the face encoding from the captured frame
        face_encoding = face_recognition.face_encodings(frame)[0]

        # Recognize the user
        username = recognize_user(face_encoding)

        if username:
            return render_template('login_success.html', username=username)
        else:
            return render_template('login_failure.html')

    return render_template('login.html')

if __name__ == '__main__':
    # Create the uploads folder if it doesn't exist
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)

# Release the webcam when the application is closed
video_capture.release()
cv2.destroyAllWindows()

