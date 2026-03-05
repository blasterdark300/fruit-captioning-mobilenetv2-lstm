import os
from buah_knowledge import KNOWLEDGE_BASE, VITAMIN_BASE
from config import TRAIN_DIR, CAPTION_FILE

def generate_captions():
    print("📝 Menghubungkan visual dengan database pengetahuan...")
    
    # Menghitung total file dulu untuk monitoring
    total_files = 0
    count = 0
    
    with open(CAPTION_FILE, 'w', encoding='utf-8') as f:
        folders = [d for d in os.listdir(TRAIN_DIR) if os.path.isdir(os.path.join(TRAIN_DIR, d))]
        
        for folder in folders:
            # Mengambil data dari knowledge base kamu
            desc = KNOWLEDGE_BASE.get(folder, f"buah segar varietas {folder}")
            vit = VITAMIN_BASE.get(folder, "C dan Serat")
            
            # Caption format: startseq [kalimat] endseq
            # Penting: Lowercase semua agar vocabulary tidak membengkak
            caption = f"startseq buah {folder.lower()} deskripsi {desc.lower()} mengandung vitamin {vit.lower()} endseq"
            
            folder_path = os.path.join(TRAIN_DIR, folder)
            img_files = [i for i in os.listdir(folder_path) if i.lower().endswith(('.png', '.jpg', '.jpeg'))]
            
            for img in img_files:
                # Format: nama_file.jpg <TAB> caption
                f.write(f"{img}\t{caption}\n")
                count += 1
                
            print(f"📂 Folder {folder}: {len(img_files)} gambar diproses.")

    print(f"\n✅ Selesai! {count} baris caption berhasil disimpan.")
    print(f"📍 Lokasi: {CAPTION_FILE}")

if __name__ == "__main__":
    generate_captions()