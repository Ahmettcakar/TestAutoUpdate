import tkinter as tk
import subprocess
import os
import sys
import requests
import json

def check_for_updates():
    print("dasadsa")
    """Updater'ı çalıştırarak eksik dosyaları kontrol eder."""
    result = subprocess.run(["python", "updater.py"], capture_output=True, text=True)
    
    if "Güncellenecek dosyalar:" in result.stdout:
        update_list = result.stdout.split("Güncellenecek dosyalar:")[-1].strip()
        message_label.config(text=f"Güncellenecek dosyalar:\n{update_list}")
        update_button.config(state=tk.NORMAL)  # Güncelleme butonunu aktif et
    elif "Uygulama zaten güncel." in result.stdout:
        message_label.config(text="Uygulama zaten güncel.")
        update_button.config(state=tk.DISABLED)
    else:
        message_label.config(text="Güncelleme kontrol edilemedi.")
        update_button.config(state=tk.DISABLED)

def download_updates():
    """Eksik dosyaları indirir ve uygular."""
    result = subprocess.run(["python", "updater.py"], capture_output=True, text=True)

    if "Güncellenecek dosyalar:" in result.stdout:
        update_list = result.stdout.split("Güncellenecek dosyalar:")[1].strip().split(", ")
        update_list = [file.strip() for file in update_list]  # Boşlukları temizle

        updated_versions = {}  # Güncellenen dosyaların versiyonlarını saklayacağız

        for file_name in update_list:
            file_url = f"https://raw.githubusercontent.com/Ahmettcakar/TestAutoUpdate/main/{file_name}"
            
            try:
                print(f"🔄 {file_name} indiriliyor...")  # İndirme işlemi başlıyor
                
                response = requests.get(file_url, stream=True)
                if response.status_code == 200:
                    temp_file = file_name + ".new"
                    
                    # Yeni dosyayı indir
                    with open(temp_file, "w", encoding="utf-8") as f:
                        f.write(response.text)

                    # Dosya gerçekten indirildi mi?
                    if os.path.exists(temp_file):
                        print(f"✅ {file_name} başarıyla indirildi.")

                    # Eğer eski dosyanın yedeği varsa, önce sil
                    backup_file = file_name + ".backup"
                    if os.path.exists(backup_file):
                        os.remove(backup_file)
                        print(f"🗑️ {backup_file} silindi.")

                    # Eski dosyanın yedeğini al
                    if os.path.exists(file_name):
                        os.rename(file_name, backup_file)
                        print(f"🔄 {file_name} yedeklendi -> {backup_file}")

                    # Yeni dosyayı eski dosyanın yerine koy
                    os.rename(temp_file, file_name)
                    print(f"✅ {file_name} başarıyla güncellendi.")

                    # Güncellenen dosyanın yeni versiyonunu al
                    updated_versions[file_name] = get_latest_version(file_name)

                else:
                    print(f"❌ {file_name} indirilemedi. HTTP Hata Kodu: {response.status_code}")
            except Exception as e:
                message_label.config(text=f"Hata: {e}")
                return
        
        # Güncellenmiş `files.json`'u kaydet
        update_local_files_json(updated_versions)

        message_label.config(text="Güncelleme tamamlandı! Program yeniden başlatılıyor.")
        root.after(2000, restart_program)

def get_latest_version(file_name):
    """GitHub'dan en güncel dosya versiyonunu alır."""
    response = requests.get("https://raw.githubusercontent.com/Ahmettcakar/TestAutoUpdate/main/files.json")
    if response.status_code == 200:
        latest_versions = json.loads(response.text)
        return latest_versions.get(file_name, "0.0.0")
    return "0.0.0"

def update_local_files_json(updated_versions):
    """Güncellenmiş `files.json` dosyasını kaydeder."""
    local_files_path = "files.json"

    try:
        # Mevcut `files.json`'u oku
        if os.path.exists(local_files_path):
            with open(local_files_path, "r", encoding="utf-8") as f:
                local_files = json.load(f)
        else:
            local_files = {}

        # Güncellenen dosyaların versiyonlarını kaydet
        local_files.update(updated_versions)

        # Güncellenmiş `files.json` dosyasını tekrar yaz
        with open(local_files_path, "w", encoding="utf-8") as f:
            json.dump(local_files, f, indent=4)

        print("✅ `files.json` başarıyla güncellendi!")

    except Exception as e:
        print(f"❌ `files.json` güncellenirken hata oluştu: {e}")

def restart_program():
    """Programı yeniden başlatır."""
    root.destroy()
    os.execl(sys.executable, sys.executable, *sys.argv)

# Ana pencere oluştur
root = tk.Tk()
root.title("Test Auto Update")
root.geometry("400x250")

# Mesaj etiketi
message_label = tk.Label(root, text="Merhaba! Güncellemeleri kontrol edelim.", font=("Arial", 12))
message_label.pack(pady=10)

# Güncellemeleri kontrol et butonu
check_button = tk.Button(root, text="Güncellemeleri Kontrol Et", command=check_for_updates, font=("Arial", 10))
check_button.pack(pady=5)

# Güncellemeleri yükle butonu (başlangıçta pasif)
update_button = tk.Button(root, text="Güncellemeleri Yükle", command=download_updates, font=("Arial", 10), state=tk.DISABLED)
update_button.pack(pady=5)

# Çıkış butonu
exit_button = tk.Button(root, text="Çıkış", command=root.quit, font=("Arial", 10))
exit_button.pack(pady=5)

# Pencereyi çalıştır
root.mainloop()
