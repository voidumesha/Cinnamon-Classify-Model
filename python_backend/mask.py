import cv2
import os
import numpy as np
from tqdm import tqdm

# Path to the dataset
DATASET_DIR = r'C:/CINNAMON/Cinnamon App/cinnamon_quality/dataset'
MASKS_DIR = r'C:/CINNAMON/Cinnamon App/cinnamon_quality/dataset/masks'

# Quality categories
QUALITY_CLASSES = ['Extra_Special_Quality', 'High_Quality', 'Medium_Quality', 'Low_Quality']

def create_mask(image_path, mask_path):
    print(f"Processing: {image_path}")
    if not os.path.exists(image_path):
        print(f"File not found: {image_path}")
        return

    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to read image: {image_path}")
        return

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur to smooth the image
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Thresholding to isolate the cinnamon trunk
    _, mask = cv2.threshold(blurred, 120, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Morphological operations to remove small noise
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)

    # Save the mask
    cv2.imwrite(mask_path, mask)
    print(f"Mask saved: {mask_path}")

def generate_all_masks():
    for quality in QUALITY_CLASSES:
        image_dir = os.path.join(DATASET_DIR, quality)
        mask_dir = os.path.join(MASKS_DIR, quality)

        # Create mask directories if not exist
        os.makedirs(mask_dir, exist_ok=True)

        # Iterate over images and generate masks
        for img_name in tqdm(os.listdir(image_dir), desc=f"Generating masks for {quality}"):
            if not img_name.lower().endswith(('.jpg', '.png', '.jpeg')):
                print(f"Skipping invalid file: {img_name}")
                continue

            img_path = os.path.join(image_dir, img_name)
            mask_path = os.path.join(mask_dir, img_name.replace('.jpg', '_mask.png'))
            create_mask(img_path, mask_path)

if __name__ == "__main__":
    generate_all_masks()
