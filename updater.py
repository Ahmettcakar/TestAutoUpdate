import requests
import os
import json

# **GitHub API URL’si (Commit ID'yi almak için)**
COMMITS_API_URL = "https://api.github.com/repos/Ahmettcakar/TestAutoUpdate/commits?path=files.json&page=1&per_page=1"
FILES_LIST_URL_TEMPLATE = "https://raw.githubusercontent.com/Ahmettcakar/TestAutoUpdate/{commit_sha}/files.json"

# **Yerel `files.json` dosyanın yolu**
LOCAL_FILES_JSON = "files.json"

def get_latest_commit_sha():
    """GitHub'dan en son commit SHA bilgisini alır."""
    try:
        response = requests.get(COMMITS_API_URL)
        if response.status_code == 200:
            commit_data = response.json()
            return commit_data[0]["sha"]  # En son commit'in SHA'sını al
        else:
            print(f"🚨 GitHub Commit API Hatası: {response.status_code}")
            return None
    except Exception as e:
        print(f"⚠️ Bağlantı hatası: {e}")
        return None

def get_latest_files():
    """GitHub'dan commit SHA'ya göre güncellenmiş `files.json` dosyasını çeker."""
    commit_sha = get_latest_commit_sha()
    if not commit_sha:
        print("🚨 Commit SHA alınamadı, güncelleme kontrol edilemiyor.")
        return None

    files_list_url = FILES_LIST_URL_TEMPLATE.format(commit_sha=commit_sha)

    try:
        response = requests.get(files_list_url)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            print(f"🚨 GitHub RAW Hatası: {response.status_code}")
            return None
    except Exception as e:
        print(f"⚠️ Bağlantı hatası: {e}")
        return None

def get_local_files():
    """Bilgisayardaki mevcut `files.json` dosyasını okur."""
    if not os.path.exists(LOCAL_FILES_JSON):
        print("⚠️ Yerel `files.json` dosyası bulunamadı, tüm dosyalar güncellenecek.")
        return {}

    try:
        with open(LOCAL_FILES_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Yerel `files.json` okunamadı: {e}")
        return {}

def check_for_updates():
    """Mevcut `files.json` ile GitHub'daki `files.json`'ı karşılaştır ve güncellenmesi gereken dosyaları belirle."""
    latest_files = get_latest_files()
    local_files = get_local_files()

    if not latest_files:
        print("🚨 Güncelleme bilgisi alınamadı.")
        return

    update_list = []  # Güncellenmesi gereken dosyaları tutan liste

    for file_name, latest_version in latest_files.items():
        current_version = local_files.get(file_name, "0.0.0")  # Eğer dosya yoksa eski kabul et

        if current_version < latest_version:  # Eğer güncellenecek bir dosya varsa listeye ekle
            update_list.append(file_name)

    if update_list:
        print(f"Güncellenecek dosyalar: {', '.join(update_list)}")
    else:
        print("✅ Uygulama zaten güncel.")

if __name__ == "__main__":
    check_for_updates()
