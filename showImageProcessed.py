import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def process_and_display_image(image_path):
    ddepth = cv2.CV_16S
    kernel_size = 3
    
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Load image in grayscale
    blurred = cv2.GaussianBlur(image, (3, 3), 0)  # Apply Gaussian Blur
    laplacian = cv2.Laplacian(blurred, ddepth, ksize=kernel_size)  # Apply Laplacian filter
    abs_laplacian = cv2.convertScaleAbs(laplacian)
    
    # Display images
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].imshow(image, cmap='gray')
    axes[0].set_title("Original")
    axes[0].axis("off")
    
    axes[1].imshow(blurred, cmap='gray')
    axes[1].set_title("Gaussian Blur")
    axes[1].axis("off")
    
    axes[2].imshow(abs_laplacian, cmap='gray')
    axes[2].set_title("Laplacian")
    axes[2].axis("off")
    
    plt.suptitle(os.path.basename(image_path))
    plt.show()
    
    return abs_laplacian

def process_images_from_folder(folder_path):
    if not os.path.exists(folder_path):
        print("Error: Specified folder does not exist.")
        return
    
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('png', 'jpg', 'jpeg', 'webp', 'tiff'))]
    if not image_files:
        print("No images found in the folder.")
        return
    
    histograms_list = []
    
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        processed_image = process_and_display_image(image_path)  # Process and display image
        hist = cv2.calcHist([processed_image], [0], None, [256], [0, 256])
        histograms_list.append((image_file, hist))
    
    distance_matrix = pd.DataFrame(0, index=image_files, columns=image_files, dtype='float64')
    
    # Calculate histogram distances
    for i in range(len(histograms_list)):
        for j in range(i, len(histograms_list)):
            image1, hist1 = histograms_list[i]
            image2, hist2 = histograms_list[j]
            
            total_distance = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)  # Compute distance
            distance_matrix.loc[image1, image2] = total_distance
            distance_matrix.loc[image2, image1] = total_distance
    
    distance_matrix.to_csv(os.path.join(folder_path, "distance_matrix.csv"))

folder_path = "datasetSuddiviso/UV50"
process_images_from_folder(folder_path)
