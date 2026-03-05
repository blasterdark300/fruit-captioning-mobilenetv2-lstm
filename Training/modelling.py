import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, LSTM, Embedding, Dropout, Add
from tensorflow.keras.models import Model
from config import LEARNING_RATE

def build_model(vocab_size, max_length):
    # 1. Visual Encoder (Input MobileNetV2)
    inputs1 = Input(shape=(1280,)) 
    fe1 = Dropout(0.5)(inputs1) 
    fe2 = Dense(256, activation='relu')(fe1)

    # 2. Language Decoder (Input Teks)
    inputs2 = Input(shape=(max_length,))
    se1 = Embedding(vocab_size, 256, mask_zero=True)(inputs2)
    se2 = Dropout(0.5)(se1) 
    se3 = LSTM(256)(se2)

    # 3. Merge Layer
    decoder1 = Add()([fe2, se3])
    decoder2 = Dense(256, activation='relu')(decoder1)
    outputs = Dense(vocab_size, activation='softmax')(decoder2)

    model = Model(inputs=[inputs1, inputs2], outputs=outputs)
    
    # Menampilkan Accuracy saat training
    model.compile(
        loss='categorical_crossentropy', 
        optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        metrics=['accuracy']
    )
    
    return model