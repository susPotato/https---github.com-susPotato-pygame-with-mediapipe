import cv2
import mediapipe as mp
from queue import Queue
import threading

mp_drawing_utils = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh

class MediaPipe:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.hand_queue = Queue()
        self.nose_queue = Queue()
        self.pose = 0
        self.hand_thread = threading.Thread(target=self.hand_tracking)
        self.face_thread = threading.Thread(target=self.face_mesh_tracking)
        self.hand_thread.start()
        self.face_thread.start()

    def hand_tracking(self):
        with mp_hands.Hands(
            min_detection_confidence=0.8,
            min_tracking_confidence=0.5,
            max_num_hands=1
        ) as hands:
            while self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    break

                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = cv2.flip(image, 1)
                image.flags.writeable = False
                results_hand = hands.process(image)
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                hand_labels = []
                if results_hand.multi_hand_landmarks:
                    for num, hand_landmarks in enumerate(results_hand.multi_hand_landmarks):
                        handtip_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
                        handMCP_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y
                        handtip1_y = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y
                        handMCP1_y = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y

                        self.hand_queue.put((handtip_y, handMCP_y, handtip1_y, handMCP1_y))
    
    def face_mesh_tracking(self):
        with mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        ) as face_mesh:
            while self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    break

                image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results_face = face_mesh.process(image_rgb)

                if results_face.multi_face_landmarks:
                    for face_landmarks in results_face.multi_face_landmarks:
                        nose_tip_landmark = face_landmarks.landmark[4]
                        nose_x = (1 - nose_tip_landmark.x)
                        nose_y = nose_tip_landmark.y
                        self.nose_queue.put((nose_x,nose_y))

   # def update_hand_pose(self):
   #     if not self.hand_queue.empty():
   #         y1, y2, y3, y4 = self.hand_queue.get()
   #         if y1 - y2 < 0 and y3 - y4 < 0:  # punch
   #             self.pose = 1
   #         elif y1 - y2 < 0 and y3 - y4 > 0:  # gun
   #             self.pose = 2
   #         elif y1 - y2 > 0 and y3 - y4 > 0:  # axe
   #             self.pose = 3
   #         else:
   #             self.pose = 4
