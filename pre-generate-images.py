import asyncio
import time
from pdf2image import convert_from_path
import os
import cv2
import numpy as np

path = 'sds'
data = []

os.makedirs('images', exist_ok=True)


async def generate_improved_image(file_name: str):
    try:
        page_images = convert_from_path(f"{path}/{file_name}", dpi=450)

        for index, page_image in enumerate(page_images):
            # 1. Convert to numpy array
            page_image_cv = np.array(page_image)

            # 2. Apply a median filter to remove salt-and-pepper noise
            median_image = cv2.medianBlur(page_image_cv, 3)

            # 3. Convert to grayscale
            gray_image = cv2.cvtColor(median_image, cv2.COLOR_BGR2GRAY)

            # 4. Apply adaptive thresholding
            threshold_image = cv2.adaptiveThreshold(gray_image, 255,
                                                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

            # 5. Save the image to a folder
            cv2.imwrite(f"images/{file_name.split('.')[0]}-{index+1}.png", threshold_image)
    except Exception as e:
        raise e


async def process_image():
    start_time = time.time()

    file_names = list(filter(lambda x: x.endswith('.pdf'), os.listdir(path)))

    for index, file_name in enumerate(file_names):
        await generate_improved_image(file_name)
        print(f"----- Processing: {index+1}/{len(file_names)} -----")

    end_time = time.time()
    print(f"Process Image: {end_time - start_time} seconds")


async def main():
    await process_image()


asyncio.run(main())
