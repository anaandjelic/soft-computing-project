import sys
import numpy as np
import pyautogui
import win32api, win32con, win32gui
import cv2
import time
import torch
import time

model = torch.hub.load('ultralytics/yolov5', 'custom', path='model/best-640.pt')
class_names = [ 'counter-terrorist', 'terrorist' ]
opponent = 'terrorist'
opponent_color = (255, 0, 0)
ally_color = (0, 128, 255)

def load_frame():
    hwnd = win32gui.FindWindow(None, 'Counter-Strike: Global Offensive - Direct3D 9')
    rect = win32gui.GetWindowRect(hwnd)
    region = rect[0], rect[1] + 27, rect[2] - rect[0], rect[3] - rect[1] - 27

    frame = np.array(pyautogui.screenshot(region=region))
    frame = cv2.resize(frame, (640, 360))
    return frame

def process_frame(frame):
    height, width = frame.shape[:2]
    top_padding = 140 # (640 - height) / 2
    padded_frame = np.zeros((640, 640, 3), dtype=np.uint8)
    padded_frame.fill(255)
    padded_frame[top_padding:top_padding+height, :width] = frame
    return padded_frame

def is_opponent(label):
    return class_names[label] == opponent

def find_closest(detected_boxes):
    min = 99999
    closest_at = 0
    for i, box in enumerate(detected_boxes):
        x1, _, x2, _ = box
        w = int(x1 - x2)

        if w < min:
            closest_at = i

        return closest_at

if __name__ == "__main__":
    opponent = sys.argv[1]
    
    while True:
        frame = load_frame()
        frame = process_frame(frame)
        height, width = frame.shape[:2]
        
        display_frame = cv2.resize(frame, (500, 500))

        # Detection
        start_time = time.time()
        results = model(frame)
        print(time.time() - start_time)
        rl = results.xyxy[0].tolist()

        # Check every detected object
        detected_boxes = []
        color = (0, 0, 0)
        for item in rl:

            x1, y1, x2, y2, confidence, label = item

            if confidence > 0.5:
                if is_opponent(int(label)):
                    detected_boxes.append((x1, y1, x2, y2))
                    color = opponent_color
                else:
                    color = ally_color

                cv2.rectangle(display_frame, (int(x1/640*500), int(y1/640*500)), (int(x2/640*500), int(y2/640*500)), color, 1)

        print("Detected:", len(detected_boxes), "enemies.")
        
        # Check Closest
        if len(detected_boxes) >= 1:

            closest_at = find_closest(detected_boxes)

            x1, y1, x2, y2 = detected_boxes[closest_at]
            x = int((x1 + x2) / 2 - width / 2)
            y = int((y1 + y2) / 2 - height / 2) - (y2 - y1) * 0.43 # For head shot

            scale = 1.7
            x = int(x * scale)
            y = int(y * scale)
            # Move mouse and shoot
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0, 0)
            time.sleep(0.05)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
            time.sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        
        display_frame = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
        cv2.imshow("frame", display_frame)
        cv2.waitKey(1)