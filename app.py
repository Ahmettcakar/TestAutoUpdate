import tkinter as tk
import subprocess
import os
import sys
import requests

def check_for_updates():
    print("caliss")
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

        for file_name in update_list:
            file_url = f"https://raw.githubusercontent.com/Ahmettcakar/TestAutoUpdate/main/{file_name}"
            
            try:
                print(f"🔄 {file_name} indiriliyor...")  # İndirme işlemi başlıyor
                
                response = requests.get(file_url, stream=True)
                if response.status_code == 200:
                    with open(file_name + ".new", "w", encoding="utf-8") as f:
                        f.write(response.text)

                    # Dosya gerçekten indirildi mi?
                    if os.path.exists(file_name + ".new"):
                        print(f"✅ {file_name} başarıyla indirildi.")

                    # Eski dosyanın yedeğini al
                    if os.path.exists(file_name):
                        os.rename(file_name, file_name + ".backup")

                    # Yeni dosyayı eski dosyanın yerine koy
                    os.rename(file_name + ".new", file_name)

                else:
                    print(f"❌ {file_name} indirilemedi. HTTP Hata Kodu: {response.status_code}")
            except Exception as e:
                message_label.config(text=f"Hata: {e}")
                return
        
        message_label.config(text="Güncelleme tamamlandı! Program yeniden başlatılıyor.")
        root.after(2000, restart_program)



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
