import asyncio
import time
from pytesseract import image_to_string
import re
import os
import pandas as pd
import cv2

match_map = {
    'physical_state': ['Physical state'],
    'color': ['Color'],
    'odor': ['Odor'],
    'ph': ['pH'],
    'boiling_point': ['Boiling point', 'Initial boiling point and boiling range'],
    'flash_point': ['Flash point'],
    'viscosity': ['Viscosity'],
}
data = []


def get_sorted_images():
    all_files = os.listdir('sds')  # Replace 'images' with the actual directory name
    images = [file for file in all_files if file.endswith('.png')]

    def extract_number(filename):
        match = re.search(r"-(\d+)\.", filename)  # Extract only the number part between the hyphen and dot
        return int(match.group(1)) if match else 0

    return sorted(images, key=extract_number)


def get_classified_images():
    images = get_sorted_images()

    def extract_name(filename):
        match = re.search(r"([^-]*)-", filename)  # Match everything before the first hyphen
        return match.group(1) if match else filename

    classified_images = {}

    for image in images:
        name = extract_name(image)
        classified_images.setdefault(name, []).append(image)

    return list(classified_images.values())


async def recognize_file(file_name, image_path_list: list):
    try:
        extracted_text = ""

        for image_path in image_path_list:
            # read image
            image = cv2.imread(f"sds/{image_path}")
            extracted_text += image_to_string(image)

        extracted_text_array = extracted_text.split('\n')

        result = {
            'product_name': file_name,
            'physical_state': 'N',
            'color': 'N',
            'odor': 'N',
            'ph': 'N',
            'boiling_point': 'N',
            'flash_point': 'N',
            'viscosity': 'N',
        }

        for content in extracted_text_array:
            for key, matches in match_map.items():
                if any(content.startswith(match) for match in matches):
                    if result[key] == "N":
                        result[key] = get_content_value(key, content)

        # print(extracted_text)
        data.append(result)
    except Exception as e:
        raise e


def get_content_value(key: str, content: str):
    pattern = ""

    match key:
        case 'physical_state':
            pattern = r"physical state|[:.,;|()]"
        case 'color':
            pattern = r"color|[:.,;|()]"
        case 'odor':
            pattern = r"odor|[:.,;|()]"
        case 'ph':
            pattern = r"ph|[:.,;|()]"
        case 'boiling_point':
            pattern = (r"boiling point|initial boiling point and boiling range|(760 mmhg)|"
                       r"boiling point/boiling range|(760 mmg)|[:.,;|()]")
        case 'flash_point':
            pattern = r"flash point|[:.,;|()]"
        case 'viscosity':
            pattern = r"viscosity|[:.,;|()]"

    return re.sub(pattern, "", content.lower()).strip()


async def main():
    start_time = time.time()

    classified_images = get_classified_images()

    for index, images in enumerate(classified_images):
        print(f"----- Processing: {images[0]} {index+1}/{len(classified_images)} -----")
        name_split = images[0].split('-')
        name_split.pop()
        file_name = '-'.join(name_split)

        await recognize_file(file_name, images)

    df = pd.DataFrame(data)
    df.to_excel('output.xlsx', index=False)
    end_time = time.time()

    print(f"Time taken: {end_time - start_time} seconds")


asyncio.run(main())

# def main():
#     classified_images = get_classified_images()
#     for images in classified_images:
#         print(images)
#
#
# main()
