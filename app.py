import streamlit as st
import numpy as np
import pickle
import tensorflow as tf
import os
import pandas as pd
from datetime import datetime
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image

# ==========================================
# 1. KONFIGURASI PATH (DINAMIS)
# ==========================================
# BASE_DIR mengarah ke folder tempat file .py ini berada
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, 'models')

# Path file di dalam folder models
PATH_MODEL_CAPTION = os.path.join(MODEL_DIR, 'fruit_caption_model.h5')
PATH_TOKENIZER = os.path.join(MODEL_DIR, 'tokenizer.pkl')
PATH_GRAFIK = os.path.join(MODEL_DIR, '1_grafik_akurasi.png')
PATH_LOG = os.path.join(MODEL_DIR, 'riwayat_penggunaan.csv')

# ==========================================
# 2. TAMPILAN UI UTAMA
# ==========================================
st.set_page_config(page_title="AI Fruit Captioning", page_icon="🥭", layout="wide")

st.title("🍎 Identifikasi Citra Buah Menggunakan Image Captioning")
st.write("Sistem otomatis yang mendeskripsikan jenis buah, kandungan vitamin, dan manfaatnya menggunakan Deep Learning.")

# ==========================================
# 3. FUNGSI LOGIKA SISTEM
# ==========================================

def save_to_log(nama, vitamin, deskripsi):
    """Menyimpan hasil identifikasi ke file CSV internal."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = {
        'Waktu': [now],
        'Nama Buah': [nama],
        'Vitamin': [vitamin],
        'Deskripsi': [deskripsi]
    }
    df_new = pd.DataFrame(new_data)
    
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
        
    if not os.path.isfile(PATH_LOG):
        df_new.to_csv(PATH_LOG, index=False)
    else:
        df_new.to_csv(PATH_LOG, mode='a', header=False, index=False)

@st.cache_resource
def load_assets():
    """Memuat model dan tokenizer sekali saja (caching)."""
    if not os.path.exists(PATH_MODEL_CAPTION) or not os.path.exists(PATH_TOKENIZER):
        raise FileNotFoundError("File model atau tokenizer tidak ditemukan di folder 'models'!")
        
    model = load_model(PATH_MODEL_CAPTION)
    with open(PATH_TOKENIZER, 'rb') as f:
        tokenizer = pickle.load(f)
    
    # Encoder: MobileNetV2
    base_model = MobileNetV2(weights='imagenet')
    fe_model = tf.keras.Model(inputs=base_model.inputs, outputs=base_model.layers[-2].output)
    
    return model, tokenizer, fe_model

def generate_caption(image, model, tokenizer, fe_model):
    """Proses ekstraksi fitur dan pembuatan teks deskripsi."""
    img = image.convert('RGB')
    img = img.resize((224, 224))
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    
    # Ekstraksi Fitur (CNN)
    feature = fe_model.predict(img, verbose=0)
    
    # Generate Teks (LSTM)
    max_length = 21 
    in_text = 'startseq'
    
    for i in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_length)
        yhat = model.predict([feature, sequence], verbose=0)
        idx = np.argmax(yhat)
        word = tokenizer.index_word.get(idx)
        if word is None or word == 'endseq':
            break
        in_text += ' ' + word
    
    return in_text.replace('startseq', '').strip()

# ==========================================
# 4. ALUR PROSES APLIKASI
# ==========================================

# Memuat Aset
try:
    model, tokenizer, fe_model = load_assets()
except Exception as e:
    st.error(f"⚠️ Gagal memuat sistem: {e}")
    st.stop()

# Input Gambar
uploaded_file = st.file_uploader("Unggah foto buah (JPG/PNG/JPEG)", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    img_display = Image.open(uploaded_file).convert('RGB')
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🖼️ Citra Input")
        st.image(img_display, use_container_width=True)
        
    with col2:
        st.subheader("🤖 Hasil Analisis AI")
        with st.spinner('Menganalisis citra...'):
            try:
                caption = generate_caption(img_display, model, tokenizer, fe_model)
                
                # Parsing teks (asumsi output: "buah [nama] deskripsi [teks] mengandung vitamin [vit]")
                if ' deskripsi ' in caption and ' mengandung vitamin ' in caption:
                    parts = caption.split(' deskripsi ')
                    nama_buah = parts[0].replace('buah ', '').title()
                    detail = parts[1].split(' mengandung vitamin ')
                    deskripsi_clean = detail[0].capitalize()
                    vitamin_clean = detail[1]
                    
                    # Tampilan Hasil ke User
                    st.success(f"**Jenis Buah:** {nama_buah}")
                    st.metric(label="Kandungan Utama", value=f"Vitamin {vitamin_clean}")
                    st.info(f"**Keterangan:**\n{deskripsi_clean}")
                    
                    # Simpan ke Log Internal
                    save_to_log(nama_buah, vitamin_clean, deskripsi_clean)
                    st.toast("Data riwayat telah diperbarui!", icon="✅")
                else:
                    st.warning("Model memberikan output yang tidak standar:")
                    st.write(f"_{caption}_")
                    
            except Exception as e:
                st.error(f"Terjadi kesalahan saat klasifikasi: {e}")

# ==========================================
# 5. SIDEBAR (METODOLOGI & DOWNLOAD USER)
# ==========================================
with st.sidebar:
    st.header("📊 Informasi & Riwayat")
    
    # Visualisasi Akurasi (Jika ada)
    if os.path.exists(PATH_GRAFIK):
        st.image(PATH_GRAFIK, caption="Grafik Performa Model", use_container_width=True)
    
    st.markdown("---")
    st.subheader("📥 Download Riwayat")
    st.write("Unduh hasil identifikasi Anda untuk keperluan laporan.")
    
    if os.path.exists(PATH_LOG):
        df_log = pd.read_csv(PATH_LOG)
        
        # Tombol Download untuk User
        csv_data = df_log.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download File CSV",
            data=csv_data,
            file_name=f"riwayat_identifikasi_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        # Tampilkan tabel singkat di sidebar
        st.write("**5 Data Terakhir:**")
        st.dataframe(df_log.tail(5), use_container_width=True)
    else:
        st.info("Belum ada data riwayat.")

    st.markdown("---")
    st.caption("Teknologi: MobileNetV2 (CNN) + Long Short-Term Memory (LSTM)")