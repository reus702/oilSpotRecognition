import os, shutil

def process_images_from_folder(input_folder_path, output_folder_path):
    if not os.path.exists(input_folder_path) or not os.path.exists(output_folder_path):
        print("Errore: La cartella specificata non esiste.")
        return
    
    input_vergini = os.path.join(input_folder_path, "B5")
    input_pulite = os.path.join(input_folder_path, "D5")
    input_perdite = os.path.join(input_folder_path, "F5")

    image_files_vergini = sorted([f for f in os.listdir(input_vergini) if f.lower().endswith(('png', 'jpg', 'jpeg', 'webp'))])
    image_files_pulite = sorted([f for f in os.listdir(input_pulite) if f.lower().endswith(('png', 'jpg', 'jpeg', 'webp'))])
    image_files_perdite = sorted([f for f in os.listdir(input_perdite) if f.lower().endswith(('png', 'jpg', 'jpeg', 'webp'))])
    
    for image_file in image_files_vergini:
        index_file = image_files_vergini.index(image_file)
        output_path = os.path.join(output_folder_path,("UVR" + str(index_file + 1)))
        
        os.makedirs(output_path, exist_ok=True)

        #moving photos
        shutil.copy(os.path.join(input_vergini,image_file), output_path)
        shutil.copy(os.path.join(input_pulite,image_files_pulite[index_file]), output_path)
        shutil.copy(os.path.join(input_perdite, image_files_perdite[index_file]), output_path)

        #renaming photos
        os.rename(os.path.join(output_path,image_file),os.path.join(output_path,"UVR" + str(index_file + 1)+"_VERGINE.png"))
        os.rename(os.path.join(output_path,image_files_pulite[index_file]), os.path.join(output_path,"UVR" + str(index_file + 1)+"_PULITE.png"))
        os.rename(os.path.join(output_path,image_files_perdite[index_file]), os.path.join(output_path,"UVR" + str(index_file + 1)+"_PERDITE.png"))

def main(): 
    input_folder_path = "dataset"
    output_folder_path = "datasetSuddivisoUvRed"
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
    process_images_from_folder(input_folder_path, output_folder_path)

main()