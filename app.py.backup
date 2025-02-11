import tkinter as tk
import subprocess
import os
import sys
def check_for_updates():
    print("test")
    """Updater'ı çalıştırarak güncellemeleri kontrol eder."""
    result = subprocess.run(["python", "updater.py"], capture_output=True, text=True)
    
    if "Güncellenen dosyalar:" in result.stdout:
        message_label.config(text="Güncelleme tamamlandı! Program yeniden başlatılıyor.")
        root.after(2000, restart_program)  # 2 saniye bekleyip programı yeniden başlat
    else:
        message_label.config(text="Uygulama zaten güncel.")

def restart_program():
    """Programı yeniden başlatır."""
    root.destroy()
    os.execl(sys.executable, sys.executable, *sys.argv)

# Ana pencere oluştur
root = tk.Tk()
root.title("Test Auto Update")
root.geometry("300x200")

# Mesaj etiketi
message_label = tk.Label(root, text="Merhaba! Güncellemeleri kontrol edelim.", font=("Arial", 12))
message_label.pack(pady=20)

# Güncellemeleri kontrol et butonu
update_button = tk.Button(root, text="Güncellemeleri Kontrol Et", command=check_for_updates, font=("Arial", 10))
update_button.pack(pady=10)

# Çıkış butonu
exit_button = tk.Button(root, text="Çıkış", command=root.quit, font=("Arial", 10))
exit_button.pack(pady=10)

# Pencereyi çalıştır
root.mainloop()
