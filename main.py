import cv2
import time
import mediapipe as mp
from playsound import playsound
import threading

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)

def play_alarm():
    threading.Thread(target=lambda: playsound('alar.mp3')).start()

# Eye landmark indices from MediaPipe FaceMesh
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def get_aspect_ratio(landmarks, eye_points, image_w, image_h):
    import math
    def euclidean(p1, p2):
        return math.dist(p1, p2)
    
    p = [landmarks[i] for i in eye_points]
    p = [(int(pt.x * image_w), int(pt.y * image_h)) for pt in p]

    A = euclidean(p[1], p[5])
    B = euclidean(p[2], p[4])
    C = euclidean(p[0], p[3])
    ear = (A + B) / (2.0 * C)
    return ear

cap = cv2.VideoCapture(0)
drowsy_time = 0
EAR_THRESHOLD = 0.25
CLOSED_FRAMES = 30

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)
    h, w, _ = frame.shape

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = face_landmarks.landmark
            left_ear = get_aspect_ratio(landmarks, LEFT_EYE, w, h)
            right_ear = get_aspect_ratio(landmarks, RIGHT_EYE, w, h)
            avg_ear = (left_ear + right_ear) / 2.0

            if avg_ear < EAR_THRESHOLD:
                drowsy_time += 1
                if drowsy_time >= CLOSED_FRAMES:
                    cv2.putText(frame, "DROWSINESS DETECTED", (50, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
                    play_alarm()
            else:
                drowsy_time = 0

    cv2.imshow("Driver Drowsiness Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

