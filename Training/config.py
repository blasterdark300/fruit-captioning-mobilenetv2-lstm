import os
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# --- Path Utama ---
BASE_DIR = r'C:\Users\crism\Downloads\buah\code\dataset'
TRAIN_DIR = os.path.join(BASE_DIR, 'Training')
MODEL_DIR = r'C:\Users\crism\Downloads\buah\code\models'

# --- File Output ---
CAPTION_FILE = os.path.join(MODEL_DIR, 'captions.txt')
FEATURES_FILE = os.path.join(MODEL_DIR, 'features.pkl')
MODEL_PATH = os.path.join(MODEL_DIR, 'fruit_caption_model.h5')
TOKENIZER_PATH = os.path.join(MODEL_DIR, 'tokenizer.pkl')

# --- Hyperparameters (Disesuaikan untuk MobileNetV2 & GTX 1050) ---
IMG_SIZE = (100, 100)        # Sesuai foto kamu
BATCH_SIZE = 64              # Bisa dinaikkan ke 64 karena 100x100 itu kecil
EPOCHS = 10
LEARNING_RATE = 0.0001

if not os.path.exists(MODEL_DIR): 
    os.makedirs(MODEL_DIR)

# --- Inisialisasi Model Encoder (MobileNetV2) ---
def build_encoder():
    # Input 100x100 sesuai fotomu
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(100, 100, 3))
    base_model.trainable = False  
    
    # Ambil output fitur
    return base_model

def check_setup():
    print(f"--- Mengecek Dataset ---")
    if os.path.exists(TRAIN_DIR):
        folders = [d for d in os.listdir(TRAIN_DIR) if os.path.isdir(os.path.join(TRAIN_DIR, d))]
        print(f"✅ Terdeteksi {len(folders)} folder buah.")
        print(f"🚀 Menggunakan MobileNetV2 dengan input {IMG_SIZE}")
    else:
        print(f"❌ Folder tidak ditemukan: {TRAIN_DIR}")

# Jalankan cek
check_setup()