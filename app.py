import tkinter as tk
import subprocess

def check_for_updates():
    """Updater'ı çalıştırarak güncellemeleri kontrol eder."""
    subprocess.Popen(["python", "updater.py"])

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
