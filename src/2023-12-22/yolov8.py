import numpy as np
import cv2


def yolo_box(image: np.ndarray, results: list) -> np.ndarray:
    for result in results:
        for box in result.boxes:
            class_id = result.names[box.cls[0].item()]
            conf = round(box.conf[0].item(), 2)
            input_box = np.array(box.xyxy[0].tolist())
            color = class_id_to_color(class_id)
            cv2.rectangle(image, (int(input_box[0]), int(input_box[1])), (int(input_box[2]), int(input_box[3])), color, 3)
            label = f"{class_id}: {conf}"
            cv2.putText(image, label, (int(input_box[0]), int(input_box[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    return image


def class_id_to_color(class_id, brightness=0.9):
    """
    Generate a consistent color for a given class ID.
    
    Args:
    class_id (int): The class ID.
    brightness (float): Adjusts the brightness of the color (0 to 1).

    Returns:
    tuple: A color in RGB format.
    """
    # Ensure brightness stays within bounds
    brightness = max(min(brightness, 1), 0)

    # Use a hash function to get a unique color for each class ID
    hash_code = hash(class_id)  # Generates a unique integer for the class ID

    # Convert hash code to color
    r = (hash_code & 0xFF0000) >> 16
    g = (hash_code & 0x00FF00) >> 8
    b = (hash_code & 0x0000FF)

    # Adjust brightness
    r = int(r * brightness)
    g = int(g * brightness)
    b = int(b * brightness)

    return (r, g, b)
