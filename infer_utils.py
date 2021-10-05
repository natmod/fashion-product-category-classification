import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications.xception import Xception, preprocess_input
from tensorflow.keras.preprocessing.image import load_img, ImageDataGenerator

from nltk import word_tokenize

from data_utils import get_image_filename, IMAGE_WRITE_PATH


IMAGE_MODEL = keras.models.load_model('xception_v4_large_08_0.894.h5')
IMAGE_SIZE = (299, 299)
IMAGE_DIR = IMAGE_WRITE_PATH

LABELS = {
    0: 'TOPS',
    1: 'DRESS',
    2: 'PANT',
    3: 'SKIRT',
    4: 'SHORTS',
    5: 'LINGERIE', # No Image Prediction
    6: 'OUTERWEAR',
    7: 'JUMPSUIT', # No Image Prediction
    8: 'JEWELRY', # No Image Prediction
    9: 'BAG', # No Image Prediction
    10: 'SHOE',
    11: 'OTHERS'
}

IMAGE_LABEL_MAP = {
    'dress': 'DRESS',
    'hat': 'OTHERS',
    'longsleeve': 'TOPS',
    'outwear': 'OUTERWEAR',
    'pants': 'PANT',
    'shirt': 'TOPS',
    'shoes': 'SHOE',
    'shorts': 'SHORTS',
    'skirt': 'SKIRT',
    't-shirt': 'TOPS'
}

IMAGE_LABELS = {
    0: 'dress',
    1: 'hat',
    2: 'longsleeve',
    3: 'outwear',
    4: 'pants',
    5: 'shirt',
    6: 'shoes',
    7: 'shorts',
    8: 'skirt',
    9: 't-shirt'
}

TEXT_KEYWORDS = {
    0: {'shirt', 'blouse'},
    1: {'dress'},
    2: {'pants', 'pant', 'sweatpant', 'jeans'},
    3: {'skirt'},
    4: {'shorts'},
    5: {'lingerie'}, # No Image Prediction
    6: {'jacket', 'coat', 'winter', 'trenchcoat'},
    7: {'jumpsuit', 'overalls', 'jumper'}, # No Image Prediction
    8: {'earing', 'necklace', 'bracelet', 'ring', 'jewelry'}, # No Image Prediction
    9: {'bag', 'purse', 'backpack'}, # No Image Prediction
    10: {'shoe', 'heel', 'sandal'},
    11: {'hat'}
}
def predict_product_label(product_entry):
    text_label = predict_text_label(product_entry['description'])
    image_label = predict_image_label(product_entry['image_url'])
    if text_label:
        return text_label
    elif image_label:
        return image_label
    else:
        return 'OTHERS'

def get_preprocessed_image(path, image_size=IMAGE_SIZE):
    img = load_img(path, target_size=(image_size))
    x = np.array(img)
    X = np.array([x])
    return preprocess_input(X)

def predict_image_label(image_url, model=IMAGE_MODEL):
    image_file = get_image_filename(image_url, image_dir=IMAGE_DIR)
    X = get_preprocessed_image(image_file)
    prediction = model.predict(X)
    return get_prediction_label(prediction, is_image=True)

def keyword_count_predict(tokens):
    token_set = set(tokens)
    prediction = np.zeros(len(LABELS))
    for label, kws in TEXT_KEYWORDS.items():
        for kw in kws:
            if kw in token_set:
                prediction[label] += 1
    return prediction

def tokenize(text):
    tokens = word_tokenize(text)
    return [token.lower() for token in tokens]

def predict_text_label(text):
    tokens = tokenize(text)
    prediction = keyword_count_predict(tokens)
    return get_prediction_label(prediction)

def get_prediction_label(prediction, is_image=False):
    if not prediction.any():
        return None
    if is_image:
        return IMAGE_LABEL_MAP[IMAGE_LABELS[prediction.argmax()]]
    return LABELS[prediction.argmax()]
