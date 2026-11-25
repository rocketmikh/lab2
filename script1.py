from pathlib import Path
from datetime import datetime
from PIL import Image, ImageFilter, ImageOps, UnidentifiedImageError
import os

BASE_DIR = Path(__file__).resolve().parent / "Lab2_Media"

INPUT_DIR = BASE_DIR / "data" / "input"
OUTPUT_DIR = BASE_DIR / "data" / "output"
LOG_FILE = BASE_DIR / "logs" / "history.txt"

def write_log(filename, filter_name, status):
    with open(LOG_FILE, "a", encoding="UTF-8") as log:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(
            f"[{current_time}] Файл: {filename} | "
            f"Фильтр: {filter_name} | Статус: {status}\n"
        )

def main():
    print("Фильтр Гаусса + Автоконтраст")

    filename = input("Введите имя изображения: ").strip()
    filter_name = "Фильтр Гаусса + Автоконтраст"
    z = input("Введите радиус для Фильтра Гаусса: ").strip()
    z = int(z)

    if not filename or Path(filename).name != filename:
        print("Ошибка: Некорректное имя файла")
        return

    image_path = INPUT_DIR / filename

    try:
        if not os.access(image_path, os.W_OK):
            raise PermissionError

        with Image.open(image_path) as image:
            image = image.convert("RGB")
            image = image.filter(ImageFilter.GaussianBlur(radius=z))
            image = ImageOps.autocontrast(image)
            output_path = OUTPUT_DIR / "result.jpg"
            image.save(output_path, format="JPEG")

        print(f"Результат сохранён: {output_path}")
        write_log(filename, filter_name, "Успешно")

    except PermissionError:
        print(f"Ошибка: Нет прав на чтение файла {filename}. Обратитесь к администратору")
        write_log(filename, filter_name, "Ошибка доступа")

    except FileNotFoundError:
        print("Ошибка: Файл не найден")
        write_log(filename, filter_name, "Файл не найден")

    except UnidentifiedImageError:
        print("Ошибка: Файл не является изображением")
        write_log(filename, filter_name, "Ошибка формата")

    except OSError as error:
        print(f"Ошибка при обработке изображения: {error}")
        write_log(filename, filter_name, "Ошибка обработки")

main()
