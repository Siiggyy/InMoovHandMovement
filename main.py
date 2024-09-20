import time
from pprint import pprint

import cv2
import serial

from HandTrackingDynamic import HandTrackingDynamic
from config import COM_PORT


def loop(arduino_serial_port, capture, debug):
    ret, frame = capture.read()

    detector = HandTrackingDynamic()
    fingers_frame = detector.findFingers(frame)
    lms, bbox = detector.findPosition(fingers_frame)
    if any(lms) is False:
        return  # TODO handle no hand detected

    finger_angles = detector.getFingerAngles()
    finger_angles = [180 - finger_angle for finger_angle in finger_angles]
    finger_angles = [int(finger_angle) + idx * 180 for idx, finger_angle in enumerate(finger_angles)]
    pprint(finger_angles)

    if debug:
        pprint(finger_angles)
        finger_angles = [42, 353, 529, 704, 870]
        finger_angles = [159, 255, 427, 606, 799]

    messages = [f"{angle}\n" for angle in finger_angles]

    if debug:
        pprint(messages)
        pprint(detector.calculateWristAngle())

    for message in messages:
        arduino_serial_port.write(message.encode())
        pass

    return fingers_frame


def main():
    timeout = 0.3
    debug = False
    ptime = 0
    arduino_serial_port = serial.Serial(COM_PORT, 9600,
                                        timeout=1)  # Replace 'COM3' with your port  # Replace 'COM3' with your port
    time.sleep(0.7)

    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    if not capture.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        time.sleep(timeout)

        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime

        fingers_frame = loop(arduino_serial_port, capture, debug)
        if fingers_frame is None:
            continue

        cv2.putText(fingers_frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow('frame', fingers_frame)
        cv2.waitKey(1)

    arduino_serial_port.close()

if __name__ == "__main__":
    main()
