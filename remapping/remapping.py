import os
import re
import shutil

# 1. Path Sumber (Data asli yang berantakan)
SOURCE_TRAIN = r'C:\Users\crism\Downloads\buah\fruits\versions\84\fruits-360_100x100\fruits-360\Test'

# 2. Path Tujuan (Folder baru yang kamu minta)
DEST_TRAIN = r'C:\Users\crism\Downloads\buah\code\dataset\Test'

def get_clean_label(folder_name):
    """Menghapus spasi dan angka di akhir. Contoh: 'Apple 8' -> 'Apple'"""
    clean_name = re.sub(r'\s+\d+$', '', folder_name)
    return clean_name.strip()

def move_and_merge(src_dir, dst_dir):
    if not os.path.exists(src_dir):
        print(f"❌ Folder sumber tidak ditemukan: {src_dir}")
        return

    # Buat folder tujuan utama jika belum ada
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
        print(f"📁 Membuat folder dataset baru di: {dst_dir}")

    print(f"\n--- Memulai Proses Pemindahan & Penggabungan ---")
    
    # List semua folder di sumber (Apple 8, Apple 9, dst)
    all_folders = [d for d in os.listdir(src_dir) if os.path.isdir(os.path.join(src_dir, d))]
    
    for folder in all_folders:
        original_path = os.path.join(src_dir, folder)
        clean_name = get_clean_label(folder)
        target_path = os.path.join(dst_dir, clean_name)

        # Buat folder kategori (misal: 'Apple') di lokasi baru jika belum ada
        if not os.path.exists(target_path):
            os.makedirs(target_path)
            print(f"📂 Kategori Baru: {clean_name}")

        # Pindahkan semua file gambar
        files = os.listdir(original_path)
        for f in files:
            src_file = os.path.join(original_path, f)
            # Beri nama unik agar file dari 'Apple 8' dan 'Apple 9' tidak tabrakan
            new_file_name = f"{folder}_{f}"
            dst_file = os.path.join(target_path, new_file_name)

            try:
                # Menggunakan move agar data asli pindah ke folder code kamu
                shutil.move(src_file, dst_file)
            except Exception as e:
                print(f"⚠️ Gagal pindah {f}: {e}")

        # Hapus folder asli yang sudah kosong
        try:
            os.rmdir(original_path)
        except:
            pass
            
    print(f"\n✅ Selesai! Cek folder baru kamu di: {dst_dir}")

if __name__ == "__main__":
    confirm = input(f"Pindahkan data dari fruits-360 ke {DEST_TRAIN}? (y/n): ")
    if confirm.lower() == 'y':
        move_and_merge(SOURCE_TRAIN, DEST_TRAIN)
    else:
        print("Dibatalkan.")