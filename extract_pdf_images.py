import fitz
import os
from PIL import Image

INPUT_DIR = "newphotos"           # Папка с PDF
BIG_BASE = "big"                  # Папка для больших изображений
SMALL_BASE = "small"              # Папка для маленьких изображений
DPI_BIG = 300                     # Разрешение для больших изображений
DPI_SMALL = 100                   # Черновое разрешение для малых (до ресайза)
SMALL_QUALITY = 75                # Качество JPEG для маленьких изображений (0-100)
MAX_SMALL_SIDE = 512              # Максимальный размер большей стороны малых изображений (px)


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def save_small_pixmap(pix, path, max_side=MAX_SMALL_SIDE, quality=SMALL_QUALITY):
    mode = "RGB"
    if pix.alpha:
        mode = "RGBA"
    img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
    if mode == "RGBA":
        img = img.convert("RGB")

    w, h = img.size
    if max(w, h) > max_side:
        if w >= h:
            new_w = max_side
            new_h = int(h * max_side / w)
        else:
            new_h = max_side
            new_w = int(w * max_side / h)
        img = img.resize((new_w, new_h), Image.LANCZOS)

    img.save(path, format='JPEG', quality=quality)


def process_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]

    big_dir = os.path.join(BIG_BASE, base_name)
    small_dir = os.path.join(SMALL_BASE, base_name)
    ensure_dir(big_dir)
    ensure_dir(small_dir)

    mat_big = fitz.Matrix(DPI_BIG / 72, DPI_BIG / 72)
    mat_small = fitz.Matrix(DPI_SMALL / 72, DPI_SMALL / 72)

    for i, page in enumerate(doc):
        pix_big = page.get_pixmap(matrix=mat_big)
        big_path = os.path.join(big_dir, f"{i}.jpg")
        pix_big.save(big_path)

        pix_small = page.get_pixmap(matrix=mat_small)
        small_path = os.path.join(small_dir, f"{i}.jpg")
        save_small_pixmap(pix_small, small_path)

    doc.close()


def main():
    ensure_dir(BIG_BASE)
    ensure_dir(SMALL_BASE)

    for fname in os.listdir(INPUT_DIR):
        if fname.lower().endswith('.pdf'):
            pdf_path = os.path.join(INPUT_DIR, fname)
            print(f"Обработка {fname}...")
            process_pdf(pdf_path)

    print("Готово!")


if __name__ == '__main__':
    main()
