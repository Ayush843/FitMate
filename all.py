import cv2
import mediapipe as mp
import numpy as np
import pyttsx3
import threading

# Initialize TTS engine
engine = pyttsx3.init()

def speak(text):
    def tts_task():
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"Error in TTS: {e}")
    
    tts_thread = threading.Thread(target=tts_task)
    tts_thread.start()

def calculate_angle(a, b, c):
    a = np.array(a)  # First point
    b = np.array(b)  # Mid point
    c = np.array(c)  # End point
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(np.degrees(radians))
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle 

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Exercise counters
counter_pushup = 0
counter_curl_left = 0
counter_curl_right = 0
counter_squat = 0
counter_yoga = 0

# Stages for each exercise
stage_pushup = None
stage_curl_left = None
stage_curl_right = None
stage_squat = None
yoga_stage = None

# Select exercise type
EXERCISES = ['pushup', 'curl', 'squat', 'yoga']
selected_exercise = None
selected_yoga_pose = None

def select_exercise():
    global selected_exercise
    print("Select the exercise to perform:")
    print("1. Push-up")
    print("2. Bicep Curl")
    print("3. Squat")
    print("4. Yoga")
    choice = int(input("Enter your choice (1-4): "))

    if choice == 1:
        selected_exercise = 'pushup'
    elif choice == 2:
        selected_exercise = 'curl'
    elif choice == 3:
        selected_exercise = 'squat'
    elif choice == 4:
        select_yoga_pose()
    else:
        print("Invalid choice! Defaulting to push-up.")
        selected_exercise = 'pushup'

    speak(f"You selected {selected_exercise}")

def select_yoga_pose():
    global selected_yoga_pose
    print("Select the yoga pose to perform:")
    print("1. Child's Pose")
    print("2. Warrior I Pose")
    print("3. Warrior II Pose")
    print("4. Tree Pose")
    choice = int(input("Enter your choice (1-4): "))

    if choice == 1:
        selected_yoga_pose = 'child_pose'
    elif choice == 2:
        selected_yoga_pose = 'warrior_1'
    elif choice == 3:
        selected_yoga_pose = 'warrior_2'
    elif choice == 4:
        selected_yoga_pose = 'tree_pose'
    else:
        print("Invalid choice! Defaulting to Child's Pose.")
        selected_yoga_pose = 'child_pose'

    speak(f"You selected {selected_yoga_pose}")

def findPosition(image, results, draw=True):
    lmList = []
    if results.pose_landmarks:
        if draw:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = image.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([id, cx, cy])
    return lmList

def detect_child_pose(landmarks):
    try:
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
        right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
        left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
        right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        
        hip_y = (left_hip.y + right_hip.y) / 2
        knee_y = (left_knee.y + right_knee.y) / 2
        ankle_y = (left_ankle.y + right_ankle.y) / 2
        shoulder_y = (left_shoulder.y + right_shoulder.y) / 2
        
        if ankle_y < hip_y < knee_y and shoulder_y < hip_y:
            angle_left_arm = calculate_angle(left_shoulder, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value], left_ankle)
            angle_right_arm = calculate_angle(right_shoulder, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value], right_ankle)
            
            if (angle_left_arm > 170 and angle_left_arm < 190) and (angle_right_arm > 170 and angle_right_arm < 190):
                return True
    except Exception as e:
        print(f"Error in detecting child's pose: {e}")
        return False
    return False

def detect_warrior_1_pose(landmarks):
    try:
        left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
        right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]

        # Check if the right foot is forward and the left leg is back
        if left_knee.y > right_knee.y and left_shoulder.x < right_shoulder.x:
            return True
    except Exception as e:
        print(f"Error in detecting Warrior I pose: {e}")
        return False
    return False

def detect_warrior_2_pose(landmarks):
    try:
        left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
        right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]

        # Check if the arms are extended and the right leg is bent
        if (left_knee.y < right_knee.y) and (left_shoulder.x < right_shoulder.x):
            return True
    except Exception as e:
        print(f"Error in detecting Warrior II pose: {e}")
        return False
    return False
def detect_tree_pose(landmarks):
    try:
        left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
        right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
        left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
        right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]

        # Check if one leg is lifted
        if left_knee.y > left_ankle.y and right_knee.y < right_ankle.y:
            return True
    except Exception as e:
        print(f"Error in detecting Tree pose: {e}")
        return False
    return False

# Start exercise selection
select_exercise()

cap = cv2.VideoCapture(0)

with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue
        
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)
        image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        
        lmList = findPosition(image_bgr, results, draw=True)

        if len(lmList) != 0:
            # Display count based on the selected exercise
            if selected_exercise == 'pushup':
                count_display = f"Push-ups: {counter_pushup}"
            elif selected_exercise == 'curl':
                count_display = f"Left Curls: {counter_curl_left}, Right Curls: {counter_curl_right}"
            elif selected_exercise == 'squat':
                count_display = f"Squats: {counter_squat}"
            elif selected_exercise == 'yoga':
                count_display = f"Yoga Poses: {counter_yoga}"

            # Put text on the image
            cv2.putText(image_bgr, count_display, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

            # ---------------------- PUSH-UP LOGIC ----------------------
            if selected_exercise == 'pushup':
                try:
                    shoulder = lmList[11]
                    elbow = lmList[13]
                    wrist = lmList[15]
                    
                    angle_pushup = calculate_angle(shoulder[1:], elbow[1:], wrist[1:])
                    print(f"Push-up angle: {angle_pushup}, stage: {stage_pushup}")

                    if angle_pushup > 140:
                        stage_pushup = "up"
                    if angle_pushup < 90 and stage_pushup == "up":
                        stage_pushup = "down"
                        counter_pushup += 1
                        print(f"Push-up count: {counter_pushup}")
                        speak(f"Push-up count: {counter_pushup}")
                except IndexError:
                    print("Landmark missing for push-up!")

            # ---------------------- BICEP CURL LOGIC ----------------------
            elif selected_exercise == 'curl':
                try:
                    shoulder_right = lmList[12]
                    elbow_right = lmList[14]
                    wrist_right = lmList[16]
                    shoulder_left = lmList[11]
                    elbow_left = lmList[13]
                    wrist_left = lmList[15]

                    angle_curl_right = calculate_angle(shoulder_right[1:], elbow_right[1:], wrist_right[1:])
                    print(f"Right Bicep Curl angle: {angle_curl_right}, stage: {stage_curl_right}")

                    if angle_curl_right > 160 and stage_curl_right != 'down':
                        stage_curl_right = "down"
                    if angle_curl_right < 30 and stage_curl_right == "down":
                        stage_curl_right = "up"
                        counter_curl_right += 1
                        print(f"Right Bicep Curl count: {counter_curl_right}")
                        speak(f"Right Bicep Curl count: {counter_curl_right}")
                    
                    angle_curl_left = calculate_angle(shoulder_left[1:], elbow_left[1:], wrist_left[1:])
                    print(f"Left Bicep Curl angle: {angle_curl_left}, stage: {stage_curl_left}")

                    if angle_curl_left > 160 and stage_curl_left != 'down':
                        stage_curl_left = "down"
                    if angle_curl_left < 30 and stage_curl_left == "down":
                        stage_curl_left = "up"
                        counter_curl_left += 1
                        print(f"Left Bicep Curl count: {counter_curl_left}")
                        speak(f"Left Bicep Curl count: {counter_curl_left}")
                except IndexError:
                    print("Landmark missing for bicep curl!")

            # ---------------------- SQUAT LOGIC ----------------------
            elif selected_exercise == 'squat':
                try:
                    hip = lmList[24]
                    knee = lmList[26]
                    ankle = lmList[28]
                    
                    angle_squat = calculate_angle(hip[1:], knee[1:], ankle[1:])
                    print(f"Squat angle: {angle_squat}, stage: {stage_squat}")

                    if angle_squat > 160 and stage_squat != 'up':
                        stage_squat = "up"
                    if angle_squat < 90 and stage_squat == "up":
                        stage_squat = "down"
                        counter_squat += 1
                        print(f"Squat count: {counter_squat}")
                        speak(f"Squat count: {counter_squat}")
                except IndexError:
                    print("Landmark missing for squats!")

            # ---------------------- YOGA LOGIC ----------------------
            elif selected_exercise == 'yoga':
                try:
                    if selected_yoga_pose == 'child_pose' and detect_child_pose(lmList):
                        if yoga_stage != "child_pose":
                            yoga_stage = "child_pose"
                            counter_yoga += 1
                            print(f"Yoga Pose Counter: {counter_yoga}")
                            speak(f"Yoga Pose count: {counter_yoga}")

                    elif selected_yoga_pose == 'warrior_1' and detect_warrior_1_pose(lmList):
                        if yoga_stage != "warrior_1":
                            yoga_stage = "warrior_1"
                            counter_yoga += 1
                            print(f"Yoga Pose Counter: {counter_yoga}")
                            speak(f"Yoga Pose count: {counter_yoga}")

                    elif selected_yoga_pose == 'warrior_2' and detect_warrior_2_pose(lmList):
                        if yoga_stage != "warrior_2":
                            yoga_stage = "warrior_2"
                            counter_yoga += 1
                            print(f"Yoga Pose Counter: {counter_yoga}")
                            speak(f"Yoga Pose count: {counter_yoga}")

                    elif selected_yoga_pose == 'tree_pose' and detect_tree_pose(lmList):
                        if yoga_stage != "tree_pose":
                            yoga_stage = "tree_pose"
                            counter_yoga += 1
                            print(f"Yoga Pose Counter: {counter_yoga}")
                            speak(f"Yoga Pose count: {counter_yoga}")

                except Exception as e:
                    print(f"Error in detecting yoga pose: {e}")

        # Display the frame
        cv2.imshow('Exercise Counter', image_bgr)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
