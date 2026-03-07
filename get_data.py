import webbrowser
import time
import os
import shutil
import subprocess

while True:
    rok = int(input("Který rok? "))
    if rok in [2008, 2012, 2014, 2019]:
        break

download_folder = "/home/ondrej/Downloads"
destination_folder = f"/media/ondrej/f33d1d42-ade5-41fb-98df-bd6fefb6cf63/dokument/AV/2025 - stratosferické ohřevy/OV/Merra2/m{rok}"
valid_extensions = [".nc", ".nc4"]

opakovat = []

default_timeout = 20
extra_timeout = 60
check_interval = 20
os.makedirs(destination_folder, exist_ok=True)

with open(f"{rok}.txt") as file:
    lines = file.readlines()

for x, url in enumerate(lines):
    if x not in opakovat:
       continue

    url = url.strip()
    #if not url:
    #    continue

    print(f"\n🔗 {x+1}. Otevírám: {url}")
    webbrowser.open(url)

    timeout = extra_timeout if x in opakovat else default_timeout

    newest_file = None
    newest_mtime = 0
    elapsed = 0

    while elapsed < timeout:
        time.sleep(check_interval)
        elapsed += check_interval

        files = [f for f in os.listdir(download_folder)
                 if any(f.endswith(ext) for ext in valid_extensions)
                 and not f.endswith(".part") and not f.endswith(".crdownload")]

        if not files:
            continue

        latest = max(files, key=lambda f: os.path.getmtime(os.path.join(download_folder, f)))
        latest_path = os.path.join(download_folder, latest)
        latest_mtime = os.path.getmtime(latest_path)

        if latest_mtime > newest_mtime:
            newest_file = latest
            newest_mtime = latest_mtime

        if newest_file:
            age = time.time() - newest_mtime
            if age > 5:
                break

    if newest_file:
        old_path = os.path.join(download_folder, newest_file)
        file_extension = os.path.splitext(newest_file)[1]
        new_filename = f"f{x}{file_extension}"
        new_path = os.path.join(destination_folder, new_filename)

        if os.path.exists(new_path):
            os.remove(new_path)

        try:
            shutil.move(old_path, new_path)
            print(f"✅ Soubor '{newest_file}' přejmenován na '{new_filename}' a přesunut do cílové složky.")
        except Exception as e:
            print(f"⚠️ Chyba při přesunu souboru: {e}")
    else:
        print(f"❌ Soubor pro index {x} nebyl nalezen ani po {timeout} sekundách.")
        continue