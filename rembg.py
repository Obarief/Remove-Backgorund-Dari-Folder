# from rembg import remove
# from PIL import Image

# input_path = 'bg biru.jpg'
# output_path = 'bg biru.png'

# inp = Image.open(input_path)
# output = remove(inp)

# output.save(output_path)
# Image.open("bg biru.png")



import os
from rembg import remove
from PIL import Image
from pathlib import Path
import concurrent.futures
import time

def process_image(input_path, output_folder):
    """
    Memproses satu gambar untuk menghapus background
    
    Args:
        input_path: Path file gambar input
        output_folder: Folder untuk menyimpan hasil
    """
    try:
        # Buat nama file output
        filename = Path(input_path).stem
        output_path = os.path.join(output_folder, f"{filename}_nobg.png")
        
        # Proses gambar
        input_image = Image.open(input_path)
        output_image = remove(input_image)
        
        # Simpan hasil
        output_image.save(output_path)
        print(f"Berhasil memproses: {input_path}")
        
    except Exception as e:
        print(f"Error memproses {input_path}: {str(e)}")

def batch_remove_background(input_folder, output_folder, max_workers=4):
    """
    Menghapus background dari semua gambar dalam folder secara parallel
    
    Args:
        input_folder: Folder berisi gambar-gambar input
        output_folder: Folder untuk menyimpan hasil
        max_workers: Jumlah worker untuk processing parallel
    """
    # Buat output folder jika belum ada
    os.makedirs(output_folder, exist_ok=True)
    
    # List semua file gambar yang didukung
    supported_formats = ('.png', '.jpg', '.jpeg', '.webp', '.bmp')
    image_files = [
        os.path.join(input_folder, f) for f in os.listdir(input_folder)
        if f.lower().endswith(supported_formats)
    ]
    
    if not image_files:
        print("Tidak ada file gambar yang ditemukan di folder input!")
        return
    
    print(f"Ditemukan {len(image_files)} gambar untuk diproses")
    start_time = time.time()
    
    # Proses gambar secara parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(process_image, image_path, output_folder)
            for image_path in image_files
        ]
        concurrent.futures.wait(futures)
    
    end_time = time.time()
    print(f"\nSelesai memproses {len(image_files)} gambar dalam {end_time - start_time:.2f} detik")

# Contoh penggunaan
if __name__ == "__main__":
    INPUT_FOLDER = "Foto"  # Ganti dengan path folder input Anda
    OUTPUT_FOLDER = "Hasil" # Ganti dengan path folder output yang diinginkan
    
    batch_remove_background(INPUT_FOLDER, OUTPUT_FOLDER)