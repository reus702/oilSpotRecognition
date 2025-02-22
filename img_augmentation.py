import cv2, os, sys
from pathlib import Path
import albumentations as A
import matplotlib.pyplot as plt

if len(sys.argv) != 3 :
    print("Usage: python img_augmentation.py <image-folder> <output>")
    sys.exit(1)

images_folder = sys.argv[1]
output_folder = Path(sys.argv[2])


image_filenames = [f for f in os.listdir(images_folder) if f.lower().endswith(('png', 'tiff'))]

# Definisci trasformazioni più forti
transform = A.Compose([
    A.Rotate(limit=90, p=0.5),
    A.RandomBrightnessContrast(brightness_limit=0.3, contrast_limit=0.3, p=0.5),
    A.GaussNoise(var_limit=7, p=0.5),
    A.MotionBlur(blur_limit=7, p=0.5),
    A.RandomGamma(gamma_limit=(20, 100), p=0.5),
    A.HorizontalFlip(p=0.5),
    A.VerticalFlip(p=0.5),
])

# Numero di immagini da generare
num_images = 5

# Crea la cartella "results" se non esiste
output_folder.mkdir(exist_ok=True)  

for img_filename in image_filenames:
    # Carica l'immagine
    img = cv2.resize(cv2.imread(os.path.join(images_folder, img_filename), cv2.IMREAD_GRAYSCALE), (512,512)) # Resized image

    # Genera e salva le immagini trasformate singolarmente
    for i in range(num_images):
        augmented = transform(image=img)["image"]
        # Crea un nuovo nome per ogni immagine generata
        filename_aug = f"{Path(img_filename).stem}_aug_{i}.png"  # Esempio: image_aug_0.png

        # Salva l'immagine usando OpenCV
        cv2.imwrite(os.path.join(output_folder,filename_aug), augmented)