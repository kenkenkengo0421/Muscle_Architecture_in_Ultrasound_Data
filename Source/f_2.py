import os
from PIL import Image
from collections import Counter
import matplotlib.pyplot as plt


def check_image_mask_sizes(image_dir, mask_dir):
    """
    全画像について
    image と mask のサイズの組み合わせを確認する
    """

    image_files = sorted([
        f for f in os.listdir(image_dir)
        if f.lower().endswith((".tif", ".tiff", ".png", ".jpg", ".jpeg"))
    ])

    size_counter = Counter()

    for file_name in image_files:
        image = Image.open(os.path.join(image_dir,file_name))
        mask = Image.open(os.path.join(mask_dir,file_name))
        size_counter[(image.size, mask.size)] += 1

    print("files:", len(image_files))
    print("image / mask size patterns:")

    for sizes, count in size_counter.items():
        print(
            "image:",
            sizes[0],
            "mask:",
            sizes[1],
            "count:",
            count
        )

def find_image_by_size_pattern(
    image_dir,
    mask_dir,
    target_image_size,
    target_mask_size
):
    """
    指定した image / mask サイズの組み合わせを持つ
    ファイルを1枚探す
    """

    image_files = sorted([
        f for f in os.listdir(image_dir)
        if f.lower().endswith((".tif", ".tiff", ".png", ".jpg", ".jpeg"))
    ])

    for file_name in image_files:
        image = Image.open(os.path.join(image_dir, file_name))
        mask = Image.open(os.path.join(mask_dir, file_name))

        if image.size == target_image_size and mask.size == target_mask_size:
            return file_name

    return None


def show_image_and_mask(image_dir, mask_dir, file_name):
    """
    image と mask を並べて表示する
    """

    image = Image.open(os.path.join(image_dir, file_name))
    mask = Image.open(os.path.join(mask_dir, file_name))

    print("file:", file_name)
    print("image size:", image.size)
    print("mask size:", mask.size)

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.imshow(image)
    plt.title("image")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(mask)
    plt.title("mask")
    plt.axis("off")

    plt.show()


def image_mask(image_path, mask_path, image_name, mask_name):
    """
    image, mask, image+mask, 3枚描画
    """
    image = Image.open(image_path)
    mask = Image.open(mask_path)

    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(image)
    plt.title(image_name)
    plt.axis("off")
    plt.subplot(1, 2, 2)
    plt.imshow(mask)
    plt.title(mask_name)
    plt.axis("off")

    plt.show()
    print("")

    mask_resized = mask.resize(image.size)

    plt.figure(figsize=(6, 5))
    plt.imshow(image)
    plt.imshow(mask_resized, alpha=0.4)
    plt.title(image_name + mask_name)
    plt.axis("off")
    plt.show()
    print("")