from PIL import Image
import os

# گرفتن مسیر دایرکتوری فعلی
current_directory = os.getcwd()

# لیست تمام فایل‌ها در دایرکتوری
files = os.listdir(current_directory)

# فیلتر کردن فایل‌های تصویری (بر اساس پسوندهای متداول)
image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
image_files = [file for file in files if os.path.splitext(file)[1].lower() in image_extensions]

# پردازش تصاویر
for image_file in image_files:
    try:
        # باز کردن تصویر
        image_path = os.path.join(current_directory, image_file)
        with Image.open(image_path) as img:
            # تبدیل به سیاه و سفید
            grayscale_image = img.convert("L")
            # ذخیره تصویر سیاه و سفید به جای فایل اصلی
            grayscale_image.save(image_path)
            print(f"تصویر سیاه و سفید جایگزین شد: {image_file}")
    except Exception as e:
        print(f"خطا در پردازش {image_file}: {e}")

print("تمام تصاویر پردازش شدند.")
