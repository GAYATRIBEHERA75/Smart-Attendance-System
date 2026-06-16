import cv2
import csv
import datetime
import os

# Create Attendance.csv if it doesn't exist
if not os.path.exists("Attendance.csv"):
    with open("Attendance.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Date", "Time"])

# Ask for student name
student_name = input("Enter Student Name: ")

# Face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

# Camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

attendance_marked = False

while True:

    ret, frame = cap.read()

    if not ret:
        print("Cannot read frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )

    for (x, y, w, h) in faces:

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        # Mark attendance only once
        if not attendance_marked:

            now = datetime.datetime.now()

            date = now.strftime("%d-%m-%Y")
            time = now.strftime("%H:%M:%S")

            with open("Attendance.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    student_name,
                    date,
                    time
                ])

            print(
                f"Attendance Marked for {student_name}"
            )

            attendance_marked = True

    # Date and Time on screen
    current_time = datetime.datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )

    cv2.putText(
        frame,
        current_time,
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )

    cv2.imshow(
        "Attendance System",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()