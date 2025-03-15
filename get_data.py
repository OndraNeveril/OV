import webbrowser
import time
import os
import shutil

download_folder = "/home/ondrej/Downloads"
destination_folder = "/media/ondrej/f33d1d42-ade5-41fb-98df-bd6fefb6cf63/dokument/AV/2025 - stratosferické ohřevy/Merra"
file_extension = ".nc"


with open("subset.txt") as file:
    for x, line in enumerate(file):
        url = line.strip()
        if url:
            print(f"🔗 Otevírám: {url}")
            webbrowser.open(url)
            time.sleep(15)
            files = [f for f in os.listdir(download_folder) if f.endswith(file_extension)]
            if files:
                files.sort(key=lambda f: os.path.getmtime(os.path.join(download_folder, f)), reverse=True)
                newest_file = files[0]

                new_filename = f"f{x}{file_extension}"
                new_path = os.path.join(destination_folder, new_filename)
                old_path = os.path.join(download_folder, newest_file)
                shutil.move(old_path, new_path)

                print(f"✅ Soubor {newest_file} přejmenován na {new_filename} a přesunut do {destination_folder}")
            else:
                print("❌ Žádný nový soubor nenalezen!")
