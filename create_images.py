import os
import random
from PIL import Image, ImageDraw


# Define image size and number of images to generate
imgsz = 480
num_images = 100
DATASET_DIR = "./dataset"
square_dir = os.path.join(DATASET_DIR, "square")
os.makedirs(DATASET_DIR, exist_ok=True)
os.makedirs(square_dir, exist_ok=True)

for i in range(num_images):
    # Create a new blank image for each iteration
    img = Image.new('RGB', (imgsz, imgsz), color='white')

    # Define random non-ideal square coordinates with random 10% shift in width and height for each corner
    x1 = random.randint(0, imgsz // 3)
    y1 = random.randint(0, imgsz // 3)
    x3 = random.randint(imgsz - imgsz // 3, imgsz)
    y3 = random.randint(imgsz - imgsz // 3, imgsz)
    x2 = x3
    y2 = y1
    x4 = x1
    y4 = y3

    width_shift = int(0.1 * (x2 - x1))
    height_shift = int(0.1 * (y2 - y1))

    square_coords = [
        (x1 + random.randint(-width_shift, width_shift), y1 + random.randint(-height_shift, height_shift)),
        (x2 + random.randint(-width_shift, width_shift), y2 + random.randint(-height_shift, height_shift)),
        (x3 + random.randint(-width_shift, width_shift), y3 + random.randint(-height_shift, height_shift)),
        (x4 + random.randint(-width_shift, width_shift), y4 + random.randint(-height_shift, height_shift))
    ]

    square_coords_valid = []
    for (x, y) in square_coords:
        if x < 0: x = 10
        if x > imgsz: x = imgsz - 10
        if y < 0: y = 10
        if y > imgsz: y = imgsz - 10
        square_coords_valid.append((x, y))

    # Define random color for both outline and fill
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # Draw the square onto the image, with the same color for outline and fill
    draw = ImageDraw.Draw(img)
    draw.polygon(square_coords, outline=color, fill=color)

    # Save the image with a unique filename
    img.save(os.path.join(square_dir, f"non_ideal_square_{i}.png"))






circle_dir = os.path.join(DATASET_DIR, "circle")
os.makedirs(circle_dir, exist_ok=True)

for i in range(num_images):
    # Create a new blank image for each iteration
    img = Image.new('RGB', (imgsz, imgsz), color='white')

    # Define random non-ideal circle coordinates with random 10% shift in radius for each corner
    x = random.randint(0, imgsz)
    y = random.randint(0, imgsz)
    r = random.randint(imgsz // 8, imgsz // 4)
    r_shift = int(0.1 * r)

    circle_coords = (x, y, r + random.randint(-r_shift, r_shift))

    # Define random color for both outline and fill
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # Draw the circle onto the image, with the same color for outline and fill
    draw = ImageDraw.Draw(img)
    draw.ellipse((circle_coords[0] - circle_coords[2], circle_coords[1] - circle_coords[2],
                  circle_coords[0] + circle_coords[2], circle_coords[1] + circle_coords[2]),
                 outline=color, fill=color)

    # Save the image with a unique filename
    img.save(os.path.join(circle_dir, f"non_ideal_circle_{i}.png"))
