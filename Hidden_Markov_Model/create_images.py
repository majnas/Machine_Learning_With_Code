import os
import random
from PIL import Image, ImageDraw
import yaml
import argparse
from rich import print
from typing import Dict
import tqdm


def create_square(config: Dict, part: str):
    square_dir = os.path.join(config["dataset_dir"], part, "square")
    os.makedirs(square_dir, exist_ok=True)

    for i in tqdm.tqdm(range(config[f"n_{part}_samples_per_class"]), desc=f"Create square {part} part:"):
        # Create a new blank image for each iteration
        img = Image.new('RGB', (config["imgsz"], config["imgsz"]), color='white')

        # Define random non-ideal square coordinates with random 10% shift in width and height for each corner
        x1 = random.randint(0, config["imgsz"] // 3)
        y1 = random.randint(0, config["imgsz"] // 3)
        x3 = random.randint(config["imgsz"] - config["imgsz"] // 3, config["imgsz"])
        y3 = random.randint(config["imgsz"] - config["imgsz"] // 3, config["imgsz"])
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
            if x > config["imgsz"]: x = config["imgsz"] - 10
            if y < 0: y = 10
            if y > config["imgsz"]: y = config["imgsz"] - 10
            square_coords_valid.append((x, y))

        # Define random color for both outline and fill
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        # Draw the square onto the image, with the same color for outline and fill
        draw = ImageDraw.Draw(img)
        draw.polygon(square_coords, outline=color, fill=color)

        # Save the image with a unique filename
        img.save(os.path.join(square_dir, f"non_ideal_square_{i}.png"))



def create_cirlce(config: Dict, part: str):
    circle_dir = os.path.join(config["dataset_dir"], part, "circle")
    os.makedirs(circle_dir, exist_ok=True)

    for i in tqdm.tqdm(range(config[f"n_{part}_samples_per_class"]), desc=f"Create circle {part} part:"):
        # Create a new blank image for each iteration
        img = Image.new('RGB', (config["imgsz"], config["imgsz"]), color='white')

        # Define random non-ideal circle coordinates with random 10% shift in radius for each corner
        start_margin = config["imgsz"] // 8
        end_margin = config["imgsz"] - config["imgsz"] // 8
        x = random.randint(start_margin, end_margin)
        y = random.randint(start_margin, end_margin)
        minxy = min([x, y, config["imgsz"]-x, config["imgsz"]-y])
        # print("minxy", minxy)
        r = random.randint(minxy // 10, minxy - minxy // 10)
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



def main(args):
    with open(args.cfg, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    print(config)

    os.makedirs(config["dataset_dir"], exist_ok=True)
    os.makedirs(os.path.join(config["dataset_dir"], "train"), exist_ok=True)
    os.makedirs(os.path.join(config["dataset_dir"], "test"), exist_ok=True)

    # Create square images
    create_square(config=config, part="train")
    create_square(config=config, part="test")

    # Create circle images
    create_cirlce(config=config, part="train")
    create_cirlce(config=config, part="test")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg', type=str, default='config.yaml', help='config.yaml path')
    args = parser.parse_args()
    main(args)
