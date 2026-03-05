import sys
import os

# Memastikan script bisa membaca file di folder yang sama
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import config
import datapre
import dataload

def main():
    print("="*40)
    print("🍎 FRUIT CAPTIONING SYSTEM - MAIN GENERATOR")
    print("="*40)

    # 1. Cek Folder dan Setup Awal
    config.check_setup()
    
    # 2. Generate Caption (Menghubungkan Nama File ke Pengetahuan Buah)
    print("\n[1/3] Menyiapkan data teks...")
    datapre.generate_captions()
    
    # 3. Ekstraksi Fitur Visual (Bagian paling berat untuk GTX 1050)
    print("\n[2/3] Mengecek Fitur Visual...")
    if not os.path.exists(config.FEATURES_FILE):
        print("🔍 File fitur tidak ditemukan. Memulai proses ekstraksi...")
        print("💡 Estimasi untuk 171k foto: Harap bersabar, ini memakan waktu.")
        dataload.extract_features()
    else:
        print(f"✅ Fitur visual sudah ada di: {config.FEATURES_FILE}")
        print("⏩ Melewati tahap ekstraksi.")

    # 4. Finalisasi
    print("\n[3/3] Finalisasi Data...")
    if os.path.exists(config.CAPTION_FILE) and os.path.exists(config.FEATURES_FILE):
        print("\n" + "="*40)
        print("🚀 STATUS: SIAP UNTUK TRAINING!")
        print("="*40)
        print(f"Total Foto     : 171,000 (Target)")
        print(f"Arsitektur     : MobileNetV2 (Optimized for RTX 2060)")
        print(f"Input Size     : 100x100")
        print("\n👉 Silakan jalankan: python training_final.py")
    else:
        print("\n❌ Terjadi kesalahan: File data belum lengkap.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Proses dihentikan oleh pengguna.")
    except Exception as e:
        print(f"\n\n💥 Terjadi Error Kritis: {e}")