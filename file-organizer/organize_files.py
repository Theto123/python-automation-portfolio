import os, shutil

def organize(folder):
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if os.path.isfile(path):
            ext = file.split(".")[-1]
            target = os.path.join(folder, ext.upper())
            os.makedirs(target, exist_ok=True)
            shutil.move(path, target)

if __name__ == "__main__":
    organize("test_folder")