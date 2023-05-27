import cv2
import mediapipe as mp
import math
import sim

# Initialize MediaPipe pose detection
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Initialize CoppeliaSim connection
sim.simxFinish(-1)  # Close any existing connections
clientID = sim.simxStart('127.0.0.1', 19999, True, True, 5000, 5)  # Modify the IP and port if necessary

if clientID != -1:
    print('Connected to CoppeliaSim')

    # Check if the Python program is listening
    result, pingTime = sim.simxGetPingTime(clientID)
    if result == sim.simx_return_ok:
        print('Python program is listening')
    else:
        print('Python program is not listening')
        sim.simxFinish(clientID)
        exit()
else:
    print('Failed to connect to CoppeliaSim')
    exit()

# Initialize OpenCV video capture
cap = cv2.VideoCapture(0)

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
            # Rest of the pose detection code...

        # Display frame
         cv2.imshow('Pose Detection', frame)

        # Exit program when 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break

    # Disconnect from CoppeliaSim
    sim.simxFinish(clientID)

# Release video capture and close window
cap.release()
cv2.destroyAllWindows()
