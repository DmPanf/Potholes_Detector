# draw_advanced_with_oval

import cv2
import numpy as np
import math
import json

def draw_boxes(img: np.ndarray, results: list) -> np.ndarray:
    with open('config.json', 'r') as file:
        config = json.load(file)
        alarm = config['Alarm_Size']
    print(f'\nAlarm: {alarm}')
    tKey = 2.3       # Threshold Key for the boxes to be drawn (0 to 3)
    oKey = 0.85      # Oval Key for the boxes to be drawn (0 to 1)
    corner_th = 2    # Thickness of the corner
    diag_th = 1      # Thickness of the diagonal
    oval_th = int(diag_th * 1.5)  # Thickness of the oval
    normal_col =  (250, 190, 50)  ## (250, 190, 50)  # Normal Lines Color
    alert_col =  (0, 255, 0)   ## (0, 0, 255)      # Alert Lines Color
    text_col = (0, 0, 255) ## (255, 255, 255)   # Text Color

    for result in results:
        boxes = result.boxes
        for rect, score in zip(boxes.xyxy.tolist(), boxes.conf.tolist()):
            input_box = np.array(rect)
            x, y, x2, y2 = [int(v) for v in input_box]
            w, h = x2 - x, y2 - y

            # Calculate the length of the diagonal
            diagonal_length = math.sqrt(w ** 2 + h ** 2)

            # Set the line color based on the score
            #if score < 0.6:
            #    line_col = normal_col
            #elif score < 0.8:
            #    line_col = alert_col
            #else:
            #    line_col = normal_col

            # Draw the text on the image with the score value rounded to 2 decimal places and the line color set accordingly based on the score value and the threshold key tKey
            identity_text = f"{score:.2f}"
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            font_thickness = 1
            text_size, _ = cv2.getTextSize(identity_text, font, font_scale, font_thickness)
            text_width, text_height = text_size
            if w >= alarm: ## diagonal_length >= tKey * text_width:
                line_col = alert_col
                print(f"Diagonal [W x H]: {diagonal_length:.2f} [{w} x {h}] | Score: {score:.2f} | Alert")
            else:
                line_col = normal_col

            len = int(0.15 * min(w, h))  # Length of the coners and the line to be drawn (15% of the smaller side of the bounding box)

            # Draw the lines
            for (pt1, pt2) in [((x, y), (x + len, y)), ((x, y), (x, y + len)),
                               ((x2, y), (x2 - len, y)), ((x2, y), (x2, y + len)),
                               ((x, y2), (x + len, y2)), ((x, y2), (x, y2 - len)),
                               ((x2, y2), (x2 - len, y2)), ((x2, y2), (x2, y2 - len))]:
                cv2.line(img, pt1, pt2, line_col, corner_th)
            cv2.line(img, (x, y), (x2, y2), line_col, diag_th)
            cv2.line(img, (x, y2), (x2, y), line_col, diag_th)

            # Draw the oval in the center of the bounding box
            oval_w, oval_h = int(oKey * w), int(oKey * h)
            cv2.ellipse(img, ((x + x2) // 2, (y + y2) // 2), (oval_w // 2, oval_h // 2), 0, 0, 360, line_col, oval_th)

            # Draw the text on the image with the score value rounded to 2 decimal places and the line color set accordingly based on the score value and the threshold key tKey
            text_x = x + (x2 - x) // 2 - text_width // 2
            text_y = y + (y2 - y) // 2 + text_height // 2
            cv2.rectangle(img, (text_x - 2, text_y - text_height - 2), (text_x + text_width + 2, text_y + 2), line_col, -1)
            cv2.putText(img, identity_text, (text_x, text_y), font, font_scale, text_col, font_thickness)

    return img
