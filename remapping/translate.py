import os
import shutil

# Path ke dataset TEST
DATASET_PATH = r'C:\Users\crism\Downloads\buah\code\dataset\Test'

# Kamus Terjemahan Lengkap untuk folder Test
KAMUS_BUAH = {
    # --- Apple ---
    'Apple Braeburn': 'Apel Braeburn',
    'Apple Crimson Snow': 'Apel Crimson Snow',
    'Apple Golden': 'Apel Golden',
    'Apple Granny Smith': 'Apel Granny Smith',
    'Apple Pink Lady': 'Apel Pink Lady',
    'Apple Red Delicious': 'Apel Merah Delicious',
    'Apple Red Yellow': 'Apel Merah Kuning',
    'Apple Red': 'Apel Merah',
    'Apple': 'Apel',
    
    # --- Tomato ---
    'Tomato Heart': 'Tomat Jantung',
    'Tomato Maroon': 'Tomat Marun',
    'Tomato Yellow': 'Tomat Kuning',
    'Tomato Cherry Maroon': 'Tomat Ceri Marun',
    'Tomato Cherry Orange': 'Tomat Ceri Oranye',
    'Tomato Cherry Red': 'Tomat Ceri Merah',
    'Tomato Cherry Yellow': 'Tomat Ceri Kuning',
    'Tomato': 'Tomat',

    # --- Pepper ---
    'Pepper Red': 'Paprika Merah',
    'Pepper Yellow': 'Paprika Kuning',
    'Pepper Green': 'Paprika Hijau',
    'Pepper Orange': 'Paprika Oranye',
    'Pepper': 'Paprika',

    # --- Pear ---
    'Pear Williams': 'Pir Williams',
    'Pear Abate': 'Pir Abate',
    'Pear Forelle': 'Pir Forelle',
    'Pear Kaiser': 'Pir Kaiser',
    'Pear Monster': 'Pir Monster',
    'Pear Red': 'Pir Merah',
    'Pear Stone': 'Pir Batu',
    'Pear': 'Pir',

    # --- Banana & Berry ---
    'Banana Lady Finger': 'Pisang Ambon',
    'Banana Red': 'Pisang Merah',
    'Banana': 'Pisang',
    'Strawberry Wedge': 'Potongan Stroberi',
    'Strawberry': 'Stroberi',
    'Raspberry': 'Rasberi',
    'Blueberry': 'Bluberi',
    'Blackberry': 'Blackberry',
    'Redcurrant': 'Buni Merah',

    # --- Potato & Onion ---
    'Potato White': 'Kentang Putih',
    'Potato Red': 'Kentang Merah',
    'Potato Sweet': 'Ubi Jalar',
    'Onion White': 'Bawang Putih',
    'Onion Red': 'Bawang Merah',
    'Onion': 'Bawang',

    # --- Others ---
    'Almonds': 'Almond',
    'Apricot': 'Aprikot',
    'Avocado Black': 'Alpukat Hitam',
    'Avocado Green': 'Alpukat Hijau',
    'Avocado': 'Alpukat',
    'Bean pod': 'Polong Buncis',
    'Beetroot': 'Bit',
    'Cabbage red': 'Kubis Merah',
    'Cabbage white': 'Kubis Putih',
    'Cactus fruit green': 'Buah Naga Hijau',
    'Cactus fruit red': 'Buah Naga Merah',
    'Cactus fruit': 'Buah Naga',
    'Caju seed': 'Biji Mete',
    'Cantaloupe': 'Blewah',
    'Carambula': 'Belimbing',
    'Carrot': 'Wortel',
    'Cauliflower': 'Kembang Kol',
    'Cherimoya': 'Sirsak Srikaya',
    'Cherry Rainier': 'Ceri Rainier',
    'Cherry Sour': 'Ceri Asam',
    'Cherry Wax Black': 'Ceri Lilin Hitam',
    'Cherry Wax Red': 'Ceri Lilin Merah',
    'Cherry Wax Yellow': 'Ceri Lilin Kuning',
    'Cherry Wax': 'Ceri Lilin',
    'Cherry': 'Ceri',
    'Chestnut': 'Berangan',
    'Clementine': 'Jeruk Clementine',
    'Cocos': 'Kelapa',
    'Corn Husk': 'Jagung Kulit',
    'Corn': 'Jagung',
    'Cucumber': 'Timun',
    'Dates': 'Kurma',
    'Eggplant long': 'Terong Panjang',
    'Eggplant': 'Terong',
    'Fig': 'Buah Ara',
    'Ginger Root': 'Akar Jahe',
    'Ginger': 'Jahe',
    'Gooseberry': 'Kersen',
    'Granadilla': 'Markisa Kuning',
    'Grape Blue': 'Anggur Biru',
    'Grape Pink': 'Anggur Merah Muda',
    'Grape White': 'Anggur Putih',
    'Grape': 'Anggur',
    'Grapefruit Pink': 'Jeruk Sitrus Merah Muda',
    'Grapefruit White': 'Jeruk Sitrus Putih',
    'Guava': 'Jambu Biji',
    'Hazelnut': 'Hazelnut',
    'Huckleberry': 'Huckleberry',
    'Kaki': 'Kesemek',
    'Kiwi': 'Kiwi',
    'Kohlrabi': 'Kol Rabi',
    'Kumquats': 'Jeruk Kumkuat',
    'Lemon Meyer': 'Lemon Meyer',
    'Lemon': 'Lemon',
    'Limes': 'Jeruk Nipis',
    'Lychee': 'Leci',
    'Mandarine': 'Jeruk Mandarin',
    'Mango Red': 'Mangga Merah',
    'Mango': 'Mangga',
    'Mangostan': 'Manggis',
    'Maracuja': 'Markisa',
    'Melon Piel de Sapo': 'Melon Madu',
    'Mulberry': 'Murbei',
    'Nectarine Flat': 'Nektarin Gepeng',
    'Nectarine': 'Nektarin',
    'Nut Forest': 'Kacang Hutan',
    'Nut Pecan': 'Kacang Pekan',
    'Nut': 'Kacang',
    'Orange': 'Jeruk',
    'Papaya': 'Pepaya',
    'Passion Fruit': 'Markisa',
    'Peach Flat': 'Persik Gepeng',
    'Peach': 'Persik',
    'Peanut shell 1x': 'Kacang Kulit',
    'Pepino': 'Melon Pepino',
    'Physalis with Husk': 'Ciplukan Kulit',
    'Physalis': 'Ciplukan',
    'Pineapple Mini': 'Nanas Mini',
    'Pineapple': 'Nanas',
    'Pistachio': 'Pistachio',
    'Pitahaya Red': 'Buah Naga Merah',
    'Plum': 'Plum',
    'Pomegranate': 'Delima',
    'Pomelo Sweetie': 'Jeruk Bali',
    'Quince': 'Buah Quince',
    'Rambutan': 'Rambutan',
    'Salak': 'Salak',
    'Tamarillo': 'Terong Belanda',
    'Tangelo': 'Jeruk Tangelo',
    'Walnut': 'Kenari',
    'Watermelon': 'Semangka',
    'Zucchini dark': 'Zukini Gelap',
    'Zucchini Green': 'Zukini Hijau',
    'Zucchini': 'Zukini'
}

def translate_folders(path):
    if not os.path.exists(path):
        print(f"❌ Path tidak ditemukan: {path}")
        return

    print(f"--- Memproses Terjemahan Folder TEST di: {path} ---")
    
    folders = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    count = 0

    for folder_name in folders:
        nama_indo = KAMUS_BUAH.get(folder_name)
        
        if nama_indo and nama_indo != folder_name:
            old_path = os.path.join(path, folder_name)
            new_path = os.path.join(path, nama_indo)
            
            try:
                if os.path.exists(new_path):
                    for file in os.listdir(old_path):
                        shutil.move(os.path.join(old_path, file), os.path.join(new_path, file))
                    os.rmdir(old_path)
                else:
                    os.rename(old_path, new_path)
                
                print(f"🔄 Berhasil: {folder_name} -> {nama_indo}")
                count += 1
            except Exception as e:
                print(f"⚠️ Gagal pada {folder_name}: {e}")

    print(f"\n✅ Selesai! {count} folder di direktori Test telah diterjemahkan.")

if __name__ == "__main__":
    translate_folders(DATASET_PATH)