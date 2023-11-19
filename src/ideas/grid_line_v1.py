from PIL import Image, ImageDraw

def draw_grid(image_path, left_margin, right_margin, top_margin, bottom_margin):
    # Загрузка изображения
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    width, height = img.size

    # Определение границ выделенной области
    left = width * left_margin
    right = width * (1 - right_margin)
    top = height * top_margin
    bottom = height * (1 - bottom_margin)

    # Рисование линий сетки
    step_x = (right - left) / 10
    step_y = (bottom - top) / 10
    for i in range(11):
        # Горизонтальные линии
        y = top + i * step_y
        draw.line([(left, y), (right, y)], fill="red", width=1)

        # Вертикальные линии
        x = left + i * step_x
        draw.line([(x, top), (x, bottom)], fill="red", width=1)

    img.show()

# Использование функции
draw_grid("path_to_your_image.jpg", 0.15, 0.15, 0.2, 0.1)
