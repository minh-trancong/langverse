import json
import os

# Tạo thư mục clean nếu nó chưa tồn tại
if not os.path.exists('clean'):
    os.makedirs('clean')

# Đọc và xử lý từng file JSON
for id in range(890, 975):
    with open(f'data/data_{id}.json', 'r') as f:
        data = json.load(f)

    # Kiểm tra dữ liệu
    if isinstance(data, dict) and 'list' in data:
        # Phân tách và lưu dữ liệu
        for item in data['list']:
            if isinstance(item, dict):
                product = {
                    'total': data.get('total'),
                    'productId': item.get('productId'),
                    'priceUnit': item.get('priceUnit'),
                    'marketPrice': item.get('marketPrice'),
                    'price': item.get('price'),
                    'productName': item.get('productName'),
                    'productSummary': item.get('productSummary'),
                    'productUrl': 'https://www.anphatpc.com.vn/' + item.get('productUrl'),
                    'image': item.get('imageCollection', [{}])[0].get('image', {}).get('original'),
                }

                # Lưu dữ liệu vào file JSON riêng biệt
                with open(f'clean/data_{id}.json', 'w') as f:
                    json.dump(product, f)
            else:
                print(f'Item is not a dictionary: {item}')
    else:
        print(f'Data is not a dictionary or does not contain "list": {data}')