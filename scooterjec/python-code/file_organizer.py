import os
import shutil

def organize_dir(path):
    for file in os.listdir(path):
        if os.path.isdir(os.path.join(path, file)):
            continue
        # Extract file extension and format dir name
        filename, file_ext = os.path.splitext(file)
        dir = file_ext[1:].upper()
        if not dir:
            dir = "Other"
            
        new_dir_path = os.path.join(path, dir)
        
        os.makedirs(new_dir_path, exist_ok=True)
        
        # Move file
        shutil.move(src=os.path.join(path, file), dst=os.path.join(new_dir_path, file))
        print(f"Moved {file} --> {new_dir_path}")

def main():
    organize_dir("/DirectorioQueNoExiste")
    
if __name__ == "__main__":
    main()