import requests
import os
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
        return None  

def get_current_version(file_name, latest_files):
    """Yereldeki dosyanın versiyonunu `files.json`'a göre döndürür."""
    if not os.path.exists(file_name):
        return "0.0.0"  # Dosya yoksa eski sürüm kabul edilir

    return latest_files.get(file_name, "0.0.0")  # Eğer `files.json`'da varsa o versiyonu al

def check_for_updates():
    """Güncellemeleri kontrol et ve eksik/güncellenmesi gereken dosyaları döndür."""
    latest_files = get_latest_files()
    
    if not latest_files:
        print("ERROR: Güncelleme bilgisi alınamadı.")
        return

    update_list = []  # Güncellenmesi gereken dosyaları tutan liste
    
    for file_name, latest_version in latest_files.items():
        current_version = get_current_version(file_name, latest_files)

        if current_version < latest_version:  # Eğer güncellenecek bir dosya varsa listeye ekle
            update_list.append(file_name)

    if update_list:
        print(f"Güncellenecek dosyalar: {', '.join(update_list)}")
    else:
        print("Uygulama zaten güncel.")

if __name__ == "__main__":
    check_for_updates()
