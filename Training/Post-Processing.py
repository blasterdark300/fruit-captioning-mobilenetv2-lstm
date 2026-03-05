import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences

def generate_output(model, tokenizer, feature, max_length):
    in_text = 'startseq'
    
    # Proses pembentukan kata demi kata
    for _ in range(max_length):
        # 1. Ubah teks yang sudah ada jadi angka
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_length)
        
        # 2. Prediksi kata berikutnya
        # Model menerima dua input: Fitur Gambar (MobileNetV2) dan Urutan Kata (LSTM)
        yhat = model.predict([feature, sequence], verbose=0)
        
        # 3. Ambil kata dengan probabilitas tertinggi
        idx = np.argmax(yhat)
        word = tokenizer.index_word.get(idx)
        
        # Jika kata tidak ketemu atau sudah sampai akhir kalimat
        if word is None or word == 'endseq': 
            break
            
        in_text += ' ' + word
    
    # --- PROSES CLEANING OUTPUT ---
    # Menghapus token startseq
    res = in_text.replace('startseq', '').strip()
    
    try:
        # Memisahkan kalimat berdasarkan keyword yang kita buat di generate_captions
        if ' deskripsi ' in res and ' mengandung vitamin ' in res:
            parts = res.split(' deskripsi ')
            nama_buah = parts[0].replace('buah ', '').title()
            
            detail = parts[1].split(' mengandung vitamin ')
            deskripsi = detail[0]
            vitamin = detail[1]
            
            print("-" * 30)
            print(f"🍎 Hasil Analisis Gambar:")
            print("-" * 30)
            print(f"Jenis Buah : {nama_buah}")
            print(f"Deskripsi  : {deskripsi.capitalize()}")
            print(f"Kandungan  : Vitamin {vitamin}")
            print("-" * 30)
        else:
            print(f"\n💡 Hasil AI: {res}")
            
    except Exception as e:
        # Jika AI membuat kalimat yang strukturnya berantakan
        print(f"\n💡 Hasil AI (Raw): {res}")

    return res