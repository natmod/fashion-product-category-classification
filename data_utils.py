import requests
import os


SOURCE_JSON_URL = "https://raw.githubusercontent.com/chenlh0/product-classification-challenge/master/product_data.json"
IMAGE_WRITE_PATH = "<YOUR_DIRECTORY>/fashion-product-category-classification/images"

def fetch_data(download_images=False):
    product_data = get_json()
    # Only run this once
    if download_images:
        write_images_to_local()
    return product_data

def get_json(url=SOURCE_JSON_URL):
    r = requests.get(SOURCE_JSON_URL)
    return r.json()

def get_image_filename(image_url, image_dir):
    image_suffix = os.path.basename(image_url)
    return os.path.join(image_dir, image_suffix)

def download_image(image_url, output_path=IMAGE_WRITE_PATH):
    r = requests.get(image_url)
    image_file = get_image_filename(image_url, output_path)
    with open(image_file, 'wb') as fp:
        fp.write(r.content)

def write_images_to_local(output_path=IMAGE_WRITE_PATH):
    data = get_json()
    for product_listing in data:
        image_url = product_listing['image_url']
        download_image(image_url, output_path)


    