import os, shutil, sys

def process_images_from_folder(input_folder_path, output_folder_path, folder_index):
    if not os.path.exists(input_folder_path) or not os.path.exists(output_folder_path):
        print("Errore: La cartella specificata non esiste.")
        return
    
    photo_header = "IDR_"+str(folder_index)
    if (folder_index > 6):
        photo_header = "MOT_"+str(folder_index)

    '''input_vergini = os.path.join(input_folder_path, "B5")
    input_pulite = os.path.join(input_folder_path, "D5")
    input_perdite = os.path.join(input_folder_path, "F5")'''
    input_vergini = os.path.join(input_folder_path, "B"+str(folder_index))
    input_pulite = os.path.join(input_folder_path, "D"+str(folder_index))
    input_perdite = os.path.join(input_folder_path, "F"+str(folder_index))

    if not (os.path.exists(input_vergini) or os.path.exists(input_pulite) or os.path.exists(input_perdite)):
        return

    image_files_vergini = sorted([f for f in os.listdir(input_vergini) if f.lower().endswith(('png', 'jpg', 'jpeg', 'webp'))])
    image_files_pulite = sorted([f for f in os.listdir(input_pulite) if f.lower().endswith(('png', 'jpg', 'jpeg', 'webp'))])
    image_files_perdite = sorted([f for f in os.listdir(input_perdite) if f.lower().endswith(('png', 'jpg', 'jpeg', 'webp'))])
    
    for image_file in image_files_vergini:
        index_file = image_files_vergini.index(image_file)
        output_path = os.path.join(output_folder_path,(photo_header + "_" + str(index_file + 1)))
        
        os.makedirs(output_path, exist_ok=True)

        #moving photos
        shutil.copy(os.path.join(input_vergini,image_file), output_path)
        shutil.copy(os.path.join(input_pulite,image_files_pulite[index_file]), output_path)
        shutil.copy(os.path.join(input_perdite, image_files_perdite[index_file]), output_path)

        #renaming photos
        os.rename(os.path.join(output_path, image_file), os.path.join(output_path, photo_header + "_" + str(index_file + 1)+"_VERGINE.png"))
        os.rename(os.path.join(output_path, image_files_pulite[index_file]), os.path.join(output_path, photo_header + "_" + str(index_file + 1)+"_PULITE.png"))
        os.rename(os.path.join(output_path, image_files_perdite[index_file]), os.path.join(output_path, photo_header + "_" +  str(index_file + 1)+"_PERDITE.png"))

def main(): 
    if len(sys.argv) != 3 :
        print("Usage: python split_dataset.py <input-dataset-folder> <output-divided-dataset-folder>")
        sys.exit(1)

    input_folder_path = sys.argv[1]
    output_folder_path = sys.argv[2]

    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    for folder_index in range (1,14):
        process_images_from_folder(input_folder_path, output_folder_path, folder_index)

main()