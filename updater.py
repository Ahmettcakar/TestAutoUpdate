import requests
import os
import shutil
import json
import sys
import subprocess

# GitHub'daki en güncel dosya listesinin olduğu URL
FILES_LIST_URL = "https://raw.githubusercontent.com/Ahmettcakar/TestAutoUpdate/main/files.json"

# Bilgisayardaki yerel dosyaların sürüm bilgilerini saklayacağımız dosya
LOCAL_FILES_LIST = "local_files.json"

def get_latest_files():
    """GitHub'dan en güncel dosya listesini çeker."""
    try:
        response = requests.get(FILES_LIST_URL)
        if response.status_code == 200:
            return json.loads(response.text)
        return None
    except Exception:
        return None  # Hata durumunda sessiz çalışsın

def get_local_files():
    """Yereldeki dosyaların sürüm listesini yükler."""
    if os.path.exists(LOCAL_FILES_LIST):
        with open(LOCAL_FILES_LIST, "r") as f:
            return json.load(f)
    return {}

def download_file(file_name):
    """Belirtilen dosyayı GitHub'dan indirir."""
    try:
        file_url = f"https://raw.githubusercontent.com/Ahmettcakar/TestAutoUpdate/main/{file_name}"
        response = requests.get(file_url, stream=True)
        
        if response.status_code == 200:
            with open(file_name + ".new", "w", encoding="utf-8") as f:
                f.write(response.text)
            return True
        else:
            return False
    except Exception:
        return False  # Hata durumunda sessiz devam et

def apply_updates(latest_files):
    """Güncellenmiş dosyaları uygular."""
    local_files = get_local_files()
    
    updated_files = []
    
    for file_name, latest_version in latest_files.items():
        local_version = local_files.get(file_name, "0.0.0")
        
        if latest_version != local_version:
            if download_file(file_name):
                # Eski dosyanın yedeğini al
                if os.path.exists(file_name):
                    shutil.copy(file_name, f"{file_name}.backup")
                    os.remove(file_name)

                # Yeni dosyayı eski ismiyle kaydet
                shutil.move(file_name + ".new", file_name)
                updated_files.append(file_name)
                
                # Sürüm bilgilerini güncelle
                local_files[file_name] = latest_version
    
    if updated_files:
        with open(LOCAL_FILES_LIST, "w") as f:
            json.dump(local_files, f, indent=4)
        
        # Güncellenen dosyalar varsa programı yeniden başlat
        subprocess.Popen([sys.executable] + updated_files)
        sys.exit()

def check_for_updates():
    """Güncellemeleri kontrol et."""
    latest_files = get_latest_files()
    if latest_files:
        apply_updates(latest_files)

if __name__ == "__main__":
    check_for_updates()
