from data_utils import fetch_data
from infer_utils import predict_product_label
import json

OUTPUT_FILENAME = 'product_categories.json'

def predict_all_product_categories(product_data):
    for product_entry in product_data:
        product_entry['category'] = predict_product_label(product_entry)
        yield product_entry

def write_output_json(product_data, filename=OUTPUT_FILENAME):
    product_data_with_categories = [product_entry for product_entry in predict_all_product_categories(product_data)]
    with open(filename, 'w') as fp:
        fp.write(json.dumps(product_data_with_categories, indent=2))

product_data = fetch_data()
write_output_json(product_data)




