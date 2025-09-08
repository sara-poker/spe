import os


def rename_files_in_directory():
    # مسیر دایرکتوری فعلی (همونی که فایل پایتون توشه)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    for filename in os.listdir(current_dir):
        old_path = os.path.join(current_dir, filename)

        # فقط روی فایل‌ها کار کنه (نه پوشه‌ها)
        if os.path.isfile(old_path):
            # تغییر نام: کوچک کردن + حذف فاصله
            new_filename = filename.lower().replace(" ", "")
            new_path = os.path.join(current_dir, new_filename)

            # اگر اسم جدید متفاوت بود، تغییر بده
            if old_path != new_path:
                os.rename(old_path, new_path)
                print(f"{filename} → {new_filename}")


if __name__ == "__main__":
    rename_files_in_directory()
