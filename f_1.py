from PIL import Image
import matplotlib.pyplot as plt
import os
import numpy as np
from collections import Counter


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


def check_mask(mask_dir, file_name, mask_name):
    """
    マスク画像のshape、dtype、unique値を確認
    """
    mask_array = np.array(
        Image.open(
            os.path.join(
                mask_dir,
                file_name
            )
        )
    )

    print(mask_name)
    print("shape:", mask_array.shape)
    print("dtype:", mask_array.dtype)
    print("unique:", np.unique(mask_array))
    print("")


def check_mask_palette(mask_dir, file_name, mask_name):
    """
    マスク画像のmode、画素数、paletteを確認する
    """

    mask = Image.open(
        os.path.join(
            mask_dir,
            file_name
        )
    )

    mask_array = np.array(mask)

    print(mask_name)
    print("mode:", mask.mode)
    print("0 pixels:", np.sum(mask_array == 0))
    print("255 pixels:", np.sum(mask_array == 255))

    palette = mask.getpalette()

    if palette is not None:
        print("palette[0]:", palette[0:3])
        print("palette[255]:", palette[255 * 3:255 * 3 + 3])
    else:
        print("palette: None")

    print("")


def check_mask_ratio(mask_dir, file_name, mask_name):
    """
    マスク画像の対象画素(255)の割合を確認する
    """
    mask_array = np.array(
        Image.open(
            os.path.join(
                mask_dir,
                file_name
            )
        )
    )

    total_pixels = mask_array.size
    target_pixels = np.sum(mask_array == 255)
    target_ratio = target_pixels / total_pixels * 100

    print(mask_name)
    print("total pixels:", total_pixels)
    print("target pixels:", target_pixels)
    print("target ratio:", target_ratio, "%")
    print("")


def check_all_masks(mask_dir, mask_name):
    """
    全マスク画像のmode、unique値、paletteを確認する
    """

    image_files = sorted([
        f for f in os.listdir(mask_dir)
        if f.lower().endswith((".tif", ".tiff", ".png", ".jpg", ".jpeg"))
    ])

    modes = set()
    unique_values = set()
    palettes = set()

    for file_name in image_files:

        mask = Image.open(
            os.path.join(
                mask_dir,
                file_name
            )
        )

        mask_array = np.array(mask)

        modes.add(mask.mode)

        unique_values.add(
            tuple(np.unique(mask_array))
        )

        palette = mask.getpalette()

        if palette is not None:
            palettes.add(
                (
                    tuple(palette[0:3]),
                    tuple(palette[255 * 3:255 * 3 + 3])
                )
            )
        else:
            palettes.add(None)

    print(mask_name)
    print("files:", len(image_files))
    print("modes:", modes)
    print("unique values:", unique_values)
    print("palettes:", palettes)
    print("")


def inspect_mask_patterns(mask_dir, mask_name):
    """
    マスクのmodeとunique値のパターン数を集計する
    """

    image_files = sorted([
        f for f in os.listdir(mask_dir)
        if f.lower().endswith((".tif", ".tiff", ".png", ".jpg", ".jpeg"))
    ])

    mode_counter = Counter()
    unique_counter = Counter()

    for file_name in image_files:

        mask = Image.open(
            os.path.join(
                mask_dir,
                file_name
            )
        )

        mask_array = np.array(mask)
        unique_values = tuple(np.unique(mask_array))

        mode_counter[mask.mode] += 1
        unique_counter[unique_values] += 1

    print(mask_name)
    print("files:", len(image_files))
    print("mode counts:", dict(mode_counter))
    print("unique counts:", dict(unique_counter))
    print("")


def find_mask_by_mode(mask_dir, target_mode):
    """
    指定したmodeのマスク画像を1枚探す
    """
    image_files = sorted([
        f for f in os.listdir(mask_dir)
        if f.lower().endswith((".tif", ".tiff", ".png", ".jpg", ".jpeg"))
    ])

    for file_name in image_files:
        mask = Image.open(
            os.path.join(
                mask_dir,
                file_name
            )
        )

        if mask.mode == target_mode:
            return file_name

    return None


def show_mask_values(mask_dir, file_name, mask_name):
    """
    マスク画像と、0/255の画素数を確認する
    """
    mask = Image.open(
        os.path.join(
            mask_dir,
            file_name
        )
    )

    mask_array = np.array(mask)

    print(mask_name)
    print("file:", file_name)
    print("mode:", mask.mode)
    print("unique:", np.unique(mask_array))
    print("0 pixels:", np.sum(mask_array == 0))
    print("255 pixels:", np.sum(mask_array == 255))
    print("")

    plt.figure(figsize=(6, 5))
    plt.imshow(mask, cmap="gray")
    plt.title(f"{mask_name} - {file_name}")
    plt.axis("off")
    plt.show()


def load_apo_binary_mask(mask_dir, file_name):
    """
    apo mask を
    背景=0
    aponeurosis=1
    の二値配列に変換する
    """

    mask = Image.open(
        os.path.join(
            mask_dir,
            file_name
        )
    )

    mask_array = np.array(mask)

    if mask.mode == "P":
        binary_mask = (mask_array == 0).astype(np.uint8)

    elif mask.mode == "L":
        binary_mask = (mask_array == 255).astype(np.uint8)

    else:
        raise ValueError(f"未対応のmodeです: {mask.mode}")

    return binary_mask


def load_fasc_binary_mask(mask_dir, file_name):
    """
    fasc mask を
    背景=0
    fascicle=1
    の二値配列に変換する
    """

    mask = Image.open(
        os.path.join(
            mask_dir,
            file_name
        )
    )

    mask_array = np.array(mask)

    if mask.mode == "L":
        binary_mask = (mask_array == 255).astype(np.uint8)

    else:
        raise ValueError(f"未対応のmodeです: {mask.mode}")

    return binary_mask


def compare_original_binary(mask_dir, file_name, binary_mask, mask_name):
    """
    変換前maskと二値化後maskを並べて確認する
    """

    original_mask = Image.open(
        os.path.join(
            mask_dir,
            file_name
        )
    )

    original_array = np.array(original_mask)

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.imshow(original_mask, cmap="gray")
    plt.title(mask_name + " original")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(binary_mask, cmap="gray")
    plt.title(mask_name + " binary")
    plt.axis("off")

    plt.show()

    print("original unique:", np.unique(original_array))
    print("binary unique:", np.unique(binary_mask))
    print("")