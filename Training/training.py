import os
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from modelling import build_model
import config
import evaluasi  # Mengimpor file evaluasi.py

def data_generator(mapping, features, tokenizer, max_length, vocab_size, batch_size):
    X1, X2, y = [], [], []
    n = 0
    while True:
        for img_id, caption in mapping.items():
            if img_id not in features: continue
            feature = features[img_id][0]
            seq = tokenizer.texts_to_sequences([caption])[0]
            for i in range(1, len(seq)):
                in_seq, out_seq = seq[:i], seq[i]
                in_seq = pad_sequences([in_seq], maxlen=max_length)[0]
                out_seq = to_categorical([out_seq], num_classes=vocab_size)[0]
                X1.append(feature)
                X2.append(in_seq)
                y.append(out_seq)
            n += 1
            if n == batch_size:
                yield [np.array(X1), np.array(X2)], np.array(y)
                X1, X2, y = [], [], []
                n = 0

def train():
    try:
        print("📂 Memuat data pendukung...")
        
        # Validasi file config
        if not os.path.exists(config.CAPTION_FILE) or not os.path.exists(config.FEATURES_FILE):
            print("❌ File data tidak ditemukan. Periksa config.py!")
            return

        # Load Captions
        with open(config.CAPTION_FILE, 'r', encoding='utf-8') as f:
            lines = [line for line in f.read().split('\n') if len(line) > 2]
        
        mapping = {line.split('\t')[0]: line.split('\t')[1] for line in lines}
        print(f"✅ Berhasil memuat {len(mapping)} caption.")

        # Load Features
        with open(config.FEATURES_FILE, 'rb') as f:
            features = pickle.load(f)
        print(f"✅ Berhasil memuat fitur visual.")

        # Tokenizer
        tokenizer = Tokenizer()
        tokenizer.fit_on_texts(mapping.values())
        vocab_size = len(tokenizer.word_index) + 1
        max_length = max(len(c.split()) for c in mapping.values())
        
        with open(config.TOKENIZER_PATH, 'wb') as f:
            pickle.dump(tokenizer, f)

        # Split Data 90/10
        all_ids = list(mapping.keys())
        np.random.shuffle(all_ids)
        split = int(len(all_ids) * 0.9)
        train_ids = {k: mapping[k] for k in all_ids[:split]}
        val_ids = {k: mapping[k] for k in all_ids[split:]}

        # Build Model
        model = build_model(vocab_size, max_length)
        batch_size = 128
        
        train_gen = data_generator(train_ids, features, tokenizer, max_length, vocab_size, batch_size)
        val_gen = data_generator(val_ids, features, tokenizer, max_length, vocab_size, batch_size)

        checkpoint = tf.keras.callbacks.ModelCheckpoint(
            config.MODEL_PATH, monitor='val_loss', verbose=1, save_best_only=True, mode='min'
        )

        print(f"🚀 Memulai Training di RTX 2060 (Epochs: {config.EPOCHS})...")
        
        # MENGAMBIL HISTORY TRAINING
        history = model.fit(
            train_gen,
            epochs=config.EPOCHS,
            steps_per_epoch=len(train_ids) // batch_size,
            validation_data=val_gen,
            validation_steps=len(val_ids) // batch_size,
            callbacks=[checkpoint],
            verbose=1
        )

        # OTOMATIS MEMBUAT LAPORAN SETELAH SELESAI
        evaluasi.buat_laporan_otomatis(history)

    except Exception as e:
        print(f"💥 Terjadi ERROR: {e}")

if __name__ == "__main__":
    train()