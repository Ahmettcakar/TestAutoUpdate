import requests
import os
import shutil
import subprocess
import sys
import json

# GitHub'daki en güncel dosya listesinin olduğu URL
FILES_LIST_URL = "https://raw.githubusercontent.com/Ahmettcakar/TestAutoUpdate/main/files.json"

def get_latest_files():
    """GitHub'dan en güncel dosya listesini çeker."""
    try:
        response = requests.get(FILES_LIST_URL)
        if response.status_code == 200:
            return json.loads(response.text)
        return None
    except Exception:
        return None  # Hata durumunda sessiz çalışsın

def get_current_version(file_name):
    """Mevcut dosyanın versiyonunu bulmaya çalışır."""
    if os.path.exists(file_name):
        return "Mevcut"  # Eğer dosya varsa, güncelleme kontrolüne devam et
    return "0.0.0"  # Eğer dosya yoksa, eski sürüm olarak kabul et ve indir

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

def apply_updates():
    """Güncellenmiş dosyaları uygular."""
    latest_files = get_latest_files()
    
    if not latest_files:
        return  # GitHub'dan dosya listesi alınamazsa işlem yapma

    updated_files = []
    
    for file_name, latest_version in latest_files.items():
        current_version = get_current_version(file_name)
        
        if current_version == "Mevcut" or latest_version > current_version:
            if download_file(file_name):
                # Eski dosyanın yedeğini al
                if os.path.exists(file_name):
                    shutil.copy(file_name, f"{file_name}.backup")
                    os.remove(file_name)

                # Yeni dosyayı eski ismiyle kaydet
                shutil.move(file_name + ".new", file_name)
                updated_files.append(file_name)
    
    if updated_files:
        # Güncelleme tamamlandıysa programı yeniden başlat
        subprocess.Popen([sys.executable] + updated_files)
        sys.exit()

def check_for_updates():
    """Güncellemeleri kontrol et."""
    apply_updates()

if __name__ == "__main__":
    check_fo
