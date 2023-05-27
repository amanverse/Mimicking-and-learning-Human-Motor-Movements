import cv2
import mediapipe as mp
import math
import serial
import datetime

# Initialize MediaPipe pose detection
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Initialize OpenCV video capture
cap = cv2.VideoCapture(0)

# Initialize serial connection to Arduino
ser = serial.Serial('COM3', 9600)  # Change the port and baud rate as necessary

# Initialize file to save angle values
file_name = f"angle_values_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
file = open(file_name, "w")

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while True:
        # Read frame from webcam
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to RGB and pass it to MediaPipe pose detection
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame.flags.writeable = False
        results = pose.process(frame)
        frame.flags.writeable = True

        # Draw pose landmarks on the frame
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        if results.pose_landmarks:
            # Get landmarks for the left hand
            left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
            left_elbow = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
            left_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
            left_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]

            # Calculate vectors for torso, shoulder to elbow, and elbow to wrist
            torso = (left_hip.x - left_shoulder.x, left_hip.y - left_shoulder.y, left_hip.z - left_shoulder.z)
            se = (left_elbow.x - left_shoulder.x, left_elbow.y - left_shoulder.y, left_elbow.z - left_shoulder.z)
            ew = (left_wrist.x - left_elbow.x, left_wrist.y - left_elbow.y, left_wrist.z - left_elbow.z)

            # Calculate angles
            shoulder_angle = math.degrees(math.acos(
                (torso[0] * se[0] + torso[1] * se[1] + torso[2] * se[2]) /
                (math.sqrt(torso[0] ** 2 + torso[1] ** 2 + torso[2] ** 2) *
                 math.sqrt(se[0] ** 2 + se[1] ** 2 + se[2] ** 2))
            ))
            elbow_angle = math.degrees(math.acos(
                (se[0] * ew[0] + se[1] * ew[1] + se[2] * ew[2]) /
                (math.sqrt(se[0] ** 2 + se[1] ** 2 + se[2] ** 2) *
                 math.sqrt(ew[0] ** 2 + ew[1] ** 2 + ew[2] ** 2))
            ))

            # Write angle values to file
            file.write(f"{shoulder_angle},{elbow_angle}\n")

            # Send angle values to Arduino over serial connection
            ser.write(f"{shoulder_angle},{elbow_angle}\n".encode())

            # Display angles and landmark points on frame
            cv2.putText(frame, f"Left Shoulder Angle: {shoulder_angle:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 0), 2)
            cv2.putText(frame, f"Left Elbow Angle: {elbow_angle:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 0), 2)
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Display frame
        cv2.imshow('Pose Detection', frame)

        # Exit program when 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break

# Release video capture, close window, and close file
cap.release()
cv2.destroyAllWindows()
file.close()
