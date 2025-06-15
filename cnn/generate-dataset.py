import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

characters = ['你', '好', '学', '习', '中', '文', '测', '试', '数', '据']
img_size = 64
num_images_per_char = 100

# Разделение на train / val / test
split_ratios = {'train': 0.8, 'val': 0.1, 'test': 0.1}

random.seed(42)
np.random.seed(42)


try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(script_dir, "NotoSansSC-Regular.ttf")
    font = ImageFont.truetype(font_path, 48)
except IOError:
    print("Не удалось загрузить шрифт. Используется дефолтный.")
    font = ImageFont.load_default()

def add_gaussian_noise(image, mean=0, std=10):
    """Добавляет гауссов шум"""
    arr = np.array(image).astype(np.int16)
    noise = np.random.normal(mean, std, arr.shape)
    noisy_arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy_arr)

for char in characters:
    for split, ratio in split_ratios.items():
        split_dir = os.path.join('dataset_chinese_chars', split, char)
        os.makedirs(split_dir, exist_ok=True)

    for i in range(num_images_per_char):
        img = Image.new('L', (img_size, img_size), color=255)
        draw = ImageDraw.Draw(img)

        x_shift = random.randint(-3, 3)
        y_shift = random.randint(-3, 3)
        mask = font.getmask(char)
        w, h = mask.size
        x = (img_size - w) // 2 + x_shift
        y = (img_size - h) // 2 + y_shift - 4

        draw.text((x, y), char, font=font, fill=0)

        # Рандомный поворот на ±5°
        angle = random.uniform(-5, 5)
        img = img.rotate(angle, resample=Image.BILINEAR, fillcolor=255)

        img = add_gaussian_noise(img)

        # Разделение на train/val/test
        r = random.random()
        if r < split_ratios['train']:
            split = 'train'
        elif r < split_ratios['train'] + split_ratios['val']:
            split = 'val'
        else:
            split = 'test'

        save_dir = os.path.join('dataset_chinese_chars', split, char)
        img.save(os.path.join(save_dir, f'{char}_{i}.png'))

print("✅ Генерация завершена. Файлы сохранены в dataset_chinese_chars/train|val|test/")