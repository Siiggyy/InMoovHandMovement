import cv2
import mediapipe as mp
import time
import math as math


class HandTrackingDynamic:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.__mode__ = mode
        self.__maxHands__ = maxHands
        self.__detectionCon__ = detectionCon
        self.__trackCon__ = trackCon
        self.handsMp = mp.solutions.hands
        self.hands = self.handsMp.Hands()
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findFingers(self, frame, draw=True):
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame, handLms, self.handsMp.HAND_CONNECTIONS)

        return frame

    def findPosition(self, frame, handNo=0, draw=True):
        xList = []
        yList = []
        bbox = []
        self.lmsList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for hand in self.results.multi_handedness:
                print(hand.classification[0].label)
                if hand.classification[0].label == "Left":
                    pass
                    #TODO handle detection of only Left hand



            for id, lm in enumerate(myHand.landmark):

                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                self.lmsList.append([id, cx, cy])
                if draw:
                    cv2.circle(frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax
            print("Hands Keypoint")
            print(bbox)
            if draw:
                cv2.rectangle(frame, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20),
                              (0, 255, 0), 2)

        return self.lmsList, bbox

    def findFingerUp(self):
        fingers = []

        if self.lmsList[self.tipIds[0]][1] > self.lmsList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1, 5):
            if self.lmsList[self.tipIds[id]][2] < self.lmsList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    def findDistance(self, p1, p2, frame, draw=True, r=15, t=3):

        x1, y1 = self.lmsList[p1][1:]
        x2, y2 = self.lmsList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(frame, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(frame, (x2, y2), r, (255, 0, 0), cv2.FILLED)
            cv2.circle(frame, (cx, cy), r, (0, 0.255), cv2.FILLED)
        len = math.hypot(x2 - x1, y2 - y1)

        return len, frame, [x1, y1, x2, y2, cx, cy]

    def calculateAngle(self, point1, point2, point3):
        """
        Calculate the angle between three points.
        """
        # Calculate the vectors
        vector1 = [point1[0] - point2[0], point1[1] - point2[1]]
        vector2 = [point3[0] - point2[0], point3[1] - point2[1]]

        # Calculate dot product and magnitudes
        dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
        magnitude1 = math.sqrt(vector1[0] ** 2 + vector1[1] ** 2)
        magnitude2 = math.sqrt(vector2[0] ** 2 + vector2[1] ** 2)

        # Check for zero magnitudes to avoid division by zero
        if magnitude1 == 0 or magnitude2 == 0:
            return 0  # or some default value indicating an invalid angle

        # Clamp the dot product to the valid range [-1, 1] to avoid math domain errors
        dot_product = max(min(dot_product / (magnitude1 * magnitude2), 1), -1)

        # Calculate the angle in radians and convert to degrees
        angle = math.degrees(math.acos(dot_product))
        return angle

    def getFingerAngles(self):
        """
        Get angles for each finger.
        """
        angles = []
        required_landmarks = [
            (2, 3, 4),  # Thumb landmarks
            (5, 6, 8),  # Index finger landmarks
            (9, 10, 12),  # Middle finger landmarks
            (13, 14, 16),  # Ring finger landmarks
            (17, 18, 20)  # Pinky finger landmarks
        ]

        if self.lmsList:
            for lm_ids in required_landmarks:
                # Check if all required landmarks are available
                if all(idx < len(self.lmsList) for idx in lm_ids):
                    point1 = self.lmsList[lm_ids[0]][1:]
                    point2 = self.lmsList[lm_ids[1]][1:]
                    point3 = self.lmsList[lm_ids[2]][1:]
                    angle = self.calculateAngle(point1, point2, point3)
                    angles.append(angle)
                else:
                    # If not enough points are visible, append None or a default value
                    angles.append(None)  # None indicates angle couldn't be calculated

        return angles

    def calculateWristAngle(self):
        """
        Calculate the wrist angle using landmarks 0, 5, and 17.
        """
        if len(self.lmsList) > 17:  # Ensure there are enough landmarks detected
            # Coordinates for wrist and bases of index and pinky fingers
            wrist = self.lmsList[0][1:]
            base_index = self.lmsList[5][1:]
            base_pinky = self.lmsList[17][1:]

            # Calculate the angle between vectors wrist-base_index and wrist-base_pinky
            angle_wrist = self.calculateAngle(base_index, wrist, base_pinky)
            return angle_wrist
        else:
            return None  # Return None if there are not enough points

def main():
    ctime = 0
    ptime = 0
    cap = cv2.VideoCapture(0)
    detector = HandTrackingDynamic()
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        ret, frame = cap.read()

        frame = detector.findFingers(frame)
        lmsList, bbox = detector.findPosition(frame)
        if len(lmsList) != 0:
            angles = detector.getFingerAngles()
            for i, angle in enumerate(angles):
                if angle is None:
                    print(f"Finger {i+1}: Not enough points detected")
                else:
                    print(f"Finger {i+1} angle: {angle:.2f} degrees")

            # Calculate and display wrist angle
            wrist_angle = detector.calculateWristAngle()
            if wrist_angle is not None:
                print(f"Wrist angle: {wrist_angle:.2f} degrees")
            else:
                print("Not enough points to calculate wrist angle")

        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime

        cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow('frame', frame)
        cv2.waitKey(1)





if __name__ == "__main__":
    main()