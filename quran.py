import requests
import os
import json

# Folder dasar
base_folder = "quran/surah"
os.makedirs(base_folder, exist_ok=True)
MAX_REQUEST_EVERY_ACTION = 10

# Step 1: Ambil daftar edisi
edition_url = "http://api.alquran.cloud/v1/edition"
res = requests.get(edition_url)
editions = res.json()['data']

# Simpan daftar edisi ke file editions.json
edition_file_path = os.path.join(base_folder, "editions.json")
with open(edition_file_path, 'w', encoding='utf-8') as f:
    json.dump(editions, f, ensure_ascii=False, indent=2)

# Step 2: Untuk setiap edisi, ambil surah 1 sampai 114
i = 0
for edition in editions:
    identifier = edition['identifier']
    edition_folder = os.path.join(base_folder, identifier)
    os.makedirs(edition_folder, exist_ok=True)

    for surah_num in range(1, 115):
        if i >= MAX_REQUEST_EVERY_ACTION:
            print("Reached max request limit. Stopping.")
            break  # keluar dari loop surah
        surah_filename = f"{surah_num:03}.json"
        surah_path = os.path.join(edition_folder, surah_filename)

        if os.path.exists(surah_path):
            continue

        quran_url = f"https://api.alquran.cloud/v1/surah/{surah_num}/{identifier}"
        print(f"Downloading ({i+1}): {quran_url}")
        try:
            quran_res = requests.get(quran_url)
            quran_data = quran_res.json()
            i += 1

            with open(surah_path, 'w', encoding='utf-8') as f:
                json.dump(quran_data, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f"Failed to download {quran_url}: {e}")

    if i >= MAX_REQUEST_EVERY_ACTION:
        break  # keluar dari loop edisi juga
