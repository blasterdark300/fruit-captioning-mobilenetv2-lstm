import os
import pickle
import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import Model
from config import TRAIN_DIR, FEATURES_FILE, IMG_SIZE # Pastikan IMG_SIZE di config sudah (100, 100)

def extract_features():
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(100, 100, 3), pooling='avg')
    model = Model(inputs=base_model.input, outputs=base_model.output)
    
    features = {}
    
    print("🚀 Mengekstraksi Fitur Gambar dengan MobileNetV2 (100x100)...")
    
    image_list = []
    for folder in os.listdir(TRAIN_DIR):
        path = os.path.join(TRAIN_DIR, folder)
        if not os.path.isdir(path): continue
        for img_name in os.listdir(path):
            image_list.append((img_name, os.path.join(path, img_name)))

    count = 0
    total = len(image_list)

    for img_name, img_path in image_list:
        try:
            # Load gambar sesuai ukuran asli kamu (100x100)
            img = load_img(img_path, target_size=(100, 100))
            img = img_to_array(img)
            
            # Preprocess khusus MobileNetV2
            img = img.reshape((1, 100, 100, 3))
            img = preprocess_input(img)
            
            # Predict
            feature = model.predict(img, verbose=0)
            
            # Simpan fitur (img_name sebagai kunci)
            features[img_name] = feature
            
            count += 1
            if count % 1000 == 0:
                print(f"📊 Progress: {count}/{total} gambar selesai...")
                
        except Exception as e:
            print(f"❌ Error pada gambar {img_name}: {e}")
            continue
            
    with open(FEATURES_FILE, "wb") as f:
        pickle.dump(features, f)