import cv2
import numpy as np
import os

# Input and output directories
input_dir = 'C:\CINNAMON\Cinnamon App\dataset\extra_quality\images'
output_dir = 'C:\CINNAMON\Cinnamon App\dataset\extra_quality\masks'

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Iterate through all images in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(('.jpeg', '.jpg', '.png')):
        # Read the input image
        image_path = os.path.join(input_dir, filename)
        image = cv2.imread(image_path)

        # Resize image for faster processing
        resized_image = cv2.resize(image, (512, 512))

        # Step 1: Convert to HSV color space
        hsv = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)

        # Dynamically calculate brightness range based on the V channel
        v_mean = np.mean(hsv[:, :, 2])  # Mean brightness
        lower_v = max(40, v_mean - 60)
        upper_v = min(255, v_mean + 60)

        # Define color range for cinnamon trunk
        lower_range = np.array([5, 50, lower_v])  # Hue, Saturation, Value
        upper_range = np.array([30, 255, upper_v])

        # Initial mask using HSV thresholds
        hsv_mask = cv2.inRange(hsv, lower_range, upper_range)

        # Step 2: Apply k-means clustering for color-based segmentation
        reshaped_image = resized_image.reshape((-1, 3))
        reshaped_image = np.float32(reshaped_image)

        # Define criteria and apply k-means
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
        k = 3  # Number of clusters
        _, labels, centers = cv2.kmeans(reshaped_image, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        clustered_image = centers[labels.flatten()].reshape(resized_image.shape)
        clustered_image = np.uint8(clustered_image)

        # Convert clustered image to grayscale and threshold
        gray_clustered = cv2.cvtColor(clustered_image, cv2.COLOR_BGR2GRAY)
        _, clustered_mask = cv2.threshold(gray_clustered, 128, 255, cv2.THRESH_BINARY)

        # Step 3: Combine HSV mask and k-means mask
        combined_mask = cv2.bitwise_and(hsv_mask, clustered_mask)

        # Step 4: Apply GrabCut for final refinement
        mask_grabcut = np.zeros_like(combined_mask, dtype=np.uint8)
        bgd_model = np.zeros((1, 65), np.float64)
        fgd_model = np.zeros((1, 65), np.float64)

        # Define a rectangle that covers most of the image
        rect = (10, 10, resized_image.shape[1] - 20, resized_image.shape[0] - 20)
        cv2.grabCut(resized_image, mask_grabcut, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)

        # Convert GrabCut mask to binary
        mask_grabcut = np.where((mask_grabcut == 2) | (mask_grabcut == 0), 0, 255).astype("uint8")

        # Step 5: Use gradient filtering for edge refinement
        gradient_x = cv2.Sobel(mask_grabcut, cv2.CV_64F, 1, 0, ksize=5)
        gradient_y = cv2.Sobel(mask_grabcut, cv2.CV_64F, 0, 1, ksize=5)
        gradient = cv2.sqrt(cv2.addWeighted(cv2.pow(gradient_x, 2), 0.5, cv2.pow(gradient_y, 2), 0.5, 0))
        gradient = np.uint8(gradient)

        # Step 6: Find contours for shape-based filtering
        contours, _ = cv2.findContours(gradient, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        final_mask = np.zeros_like(mask_grabcut)

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1000:  # Minimum area threshold
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = h / w
                if aspect_ratio > 2.5:  # Likely a tree trunk
                    cv2.drawContours(final_mask, [contour], -1, (255), thickness=cv2.FILLED)

        # Optional: Remove masks with low overall coverage
        if cv2.countNonZero(final_mask) < 5000:  # Low-quality trunk threshold
            final_mask[:] = 0

        # Debugging: Visualize the final mask on the original image
        debug_output = cv2.bitwise_and(resized_image, resized_image, mask=final_mask)

        # Save the mask and debug output
        mask_path = os.path.join(output_dir, filename.replace('.jpeg', '_mask.jpg'))
        debug_output_path = os.path.join(output_dir, filename.replace('.jpeg', '_debug.jpg'))

        cv2.imwrite(mask_path, final_mask)
        cv2.imwrite(debug_output_path, debug_output)

        print(f"Processed {filename}: Mask saved to {mask_path}")

print("Cinnamon tree trunk masks created successfully!")
