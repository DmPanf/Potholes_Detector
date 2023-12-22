import cv2
import numpy as np
import json

# Load actual configuration
def load_skyline():
    with open('config.json', 'r') as file:
        data = json.load(file)
        limit = round(int(data['Skyline']) / 100, 2)
        # print(f'\nSkyline: {limit}')
        return limit
    
def draw_trapezoid_grid(image: np.ndarray, grid_color=(255, 255, 255), circle_color=(250, 250, 250), line_thickness=1, circle_radius=8) -> np.ndarray:
    height, width = image.shape[:2]
    limit = load_skyline()

    # Вычисление точек для оснований трапеции
    Ymin = int(height * limit)  # 28% от верхнего края upper_base_y
    Ymax = int(height * 0.85)  # [0.7] = 30% от нижнего края lower_base_y
    Wmin = int(width * 0.20)  # 20% ширины изображения upper_base_width
    Wmax = width  # lower_base_width

    X0 = width // 2
    halfWmin = Wmin // 2  # half_upper_base = upper_base_width // 2
    halfWmax = Wmax // 2  # half_lower_base = lower_base_width // 2

    num_lines = 10

    for i in range(num_lines + 1):
        step = i / num_lines
        # Horizontal lines
        y = int(Ymin + step * (Ymax - Ymin))  # ⬇️ Increasing y values from Ymin to Ymax from top to bottom
        x_start = int(X0 - halfWmin - 2 * step * (halfWmax - halfWmin))   # ⬅️ Decreasing x values from X0 to halfWmin from right to left
        x_end = int(X0 + halfWmin + 2 * step * (halfWmax - halfWmin))     # ➡️ Increasing x values from X0 to halfWmin from left to right

        cv2.line(image, (x_start, y), (x_end, y), grid_color, thickness=line_thickness)

        # Vertical lines
        x1_min = int(X0 - (step * Wmin / 2))  # [Top] ⬅️ Decreasing x values from X0 to Wmin from right to left 
        x1_max = int(X0 - (step * Wmax))  # [Bottom] ⬅️ Decreasing x values from X0 to Wmax from right to left
        x2_min = int(X0 + (step * Wmin / 2))  # [Top] ➡️ Increasing x values from X0 to Wmin from left to right
        x2_max = int(X0 + (step * Wmax))  # [Bottom] ➡️ Increasing x values from X0 to Wmax from left to right
        y_min = Ymin
        y_max = Ymax

        cv2.line(image, (x1_min, y_min), (x1_max, y_max), grid_color, thickness=line_thickness) # ⬅️⬇️
        cv2.line(image, (x2_min, y_min), (x2_max, y_max), grid_color, thickness=line_thickness) #   ⬇️➡️


    # ========================= Drawing circles in the corners of the trapezoid ======================
    # Coordinates for the trapezoid
    i_circ = [(X0, Ymin), (X0, Ymax), (X0-Wmin, Ymin), (X0-Wmin, Ymax), (X0+Wmin, Ymin), (X0+Wmin, Ymax), 
              (X0-int(Wmin/2), Ymin), (X0-int(Wmin/2), Ymax), (X0+int(Wmin/2), Ymin), (X0-int(Wmin/2), Ymax), (X0+int(Wmin/2), Ymin), (X0+int(Wmin/2), Ymax)]
    radius = int(circle_radius / 2)  # 1/3 of circle_radius

    for x, y in i_circ:  # Draw circle
        # Ensure the coordinates are within the image boundaries
        x = max(0, min(x, width - 1))
        y = max(0, min(y, height - 1))

        cv2.circle(image, (x, y), radius, circle_color, -1)  # -1 fills the circle

        text = f"[{x}, {y}]"  # Add text
        txtY = y + 20 if y == Ymax else y - 20

        cv2.putText(image, text, (x -60, txtY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, grid_color, 1, cv2.LINE_AA)


    # ========================= Drawing circles in the corners ======================
    offsets = (int(width * 0.1), int(height * 0.1))  # 10% offset for both x and y [0.06, 0.05]

    # Coordinates for the circles
    circle_positions = [(offsets[0], offsets[1]), (width - offsets[0], offsets[1]),
                        (offsets[0], height - offsets[1]), (width - offsets[0], height - offsets[1])]

    for x, y in circle_positions:  # Draw circle
        cv2.circle(image, (x, y), circle_radius, circle_color, -1)  # -1 fills the circle

        text = f"[x={x}, y={y}]"  # Add text
        txtY = y + 20 if y == (height - offsets[1]) else y - 20
        cv2.putText(image, text, (x -60, txtY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, grid_color, 1, cv2.LINE_AA)

    # =========================================================================
    return image
