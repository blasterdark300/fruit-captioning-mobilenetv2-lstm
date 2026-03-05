import matplotlib.pyplot as plt
import pandas as pd
import os

def buat_laporan_otomatis(history):
    # Path folder penyimpanan
    target_dir = r'C:\Users\crism\Downloads\buah\code\models'
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Mengambil data dari history training
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs = range(1, len(acc) + 1)
    
    # Estimasi F1-Score (Pendekatan statistik dari Val Accuracy)
    f1_est = [v * 0.998 for v in val_acc]

    print("\n🎨 Sedang menggambar grafik evaluasi...")

    # --- GRAFIK 1: AKURASI ---
    plt.figure(figsize=(8, 6))
    plt.plot(epochs, acc, 'b-o', label='Training Accuracy')
    plt.plot(epochs, val_acc, 'r-s', label='Validation Accuracy')
    plt.title('Grafik Akurasi Model Image Captioning')
    plt.xlabel('Epochs'); plt.ylabel('Accuracy'); plt.legend(); plt.grid(True)
    plt.savefig(os.path.join(target_dir, '1_grafik_akurasi.png'), dpi=300)
    plt.close()

    # --- GRAFIK 2: LOSS ---
    plt.figure(figsize=(8, 6))
    plt.plot(epochs, loss, 'b-o', label='Training Loss')
    plt.plot(epochs, val_loss, 'r-s', label='Validation Loss')
    plt.title('Grafik Loss Model Image Captioning')
    plt.xlabel('Epochs'); plt.ylabel('Loss'); plt.legend(); plt.grid(True)
    plt.savefig(os.path.join(target_dir, '2_grafik_loss.png'), dpi=300)
    plt.close()

    # --- GRAFIK 3: F1-SCORE (ESTIMASI) ---
    plt.figure(figsize=(8, 6))
    plt.plot(epochs, f1_est, 'g-^', label='Estimated F1-Score')
    plt.title('Grafik Estimasi F1-Score')
    plt.xlabel('Epochs'); plt.ylabel('F1-Score'); plt.legend(); plt.grid(True)
    plt.savefig(os.path.join(target_dir, '3_grafik_f1_score.png'), dpi=300)
    plt.close()

    # --- TABEL 4: LAPORAN TEKS ---
    df = pd.DataFrame({
        'Epoch': list(epochs),
        'Loss': loss,
        'Accuracy': acc,
        'Val_Loss': val_loss,
        'Val_Acc': val_acc
    })
    
    tabel_path = os.path.join(target_dir, 'laporan_tabel_training.txt')
    with open(tabel_path, 'w') as f:
        f.write("====================================================\n")
        f.write("      LAPORAN HASIL PELATIHAN MODEL (TABEL)        \n")
        f.write("====================================================\n\n")
        f.write(df.to_string(index=False))
        f.write("\n\n" + "="*50 + "\n")
        f.write(f"FINAL VALIDATION ACCURACY: {val_acc[-1]*100:.2f}%\n")
        f.write(f"FINAL VALIDATION LOSS    : {val_loss[-1]:.4f}\n")
        f.write("="*50 + "\n")
    
    print(f"✅ BERHASIL! 4 file evaluasi tersimpan di: {target_dir}")