from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Оновлені тарифи
PRICE_A4 = 70
SMALL_RECTANGLE_PRICE = {3: 5, 5: 7}
SMALL_FIGURE_PRICE = {3: 6.5, 5: 9}
MINIMUM_RECTANGLE_PRICE = 5
MINIMUM_FIGURE_PRICE = 6.5
LARGE_RECTANGLE_RATE = 0.20
LARGE_FIGURE_RATE = 0.26
BULK_DISCOUNT_THRESHOLD = 100
BULK_DISCOUNT = 0.15
PACK_PROCESSING_SURCHARGE = 0.20
FIGURE_SURCHARGE = 0.30

def calculate_price(width, height, is_figure):
    area = width * height
    if (width == 3 and height == 3) or (width == 5 and height == 5):
        if width == 3:
            return SMALL_FIGURE_PRICE[3] if is_figure else SMALL_RECTANGLE_PRICE[3]
        elif width == 5:
            return SMALL_FIGURE_PRICE[5] if is_figure else SMALL_RECTANGLE_PRICE[5]

    rate = LARGE_FIGURE_RATE if is_figure else LARGE_RECTANGLE_RATE
    price = max(area * rate, MINIMUM_FIGURE_PRICE if is_figure else MINIMUM_RECTANGLE_PRICE)
    
    if area > BULK_DISCOUNT_THRESHOLD:
        price *= (1 - BULK_DISCOUNT)
    
    return round(price, 2)

def calculate_pack_price(area, is_figure):
    base_price = (area / (21 * 29.7)) * PRICE_A4
    surcharge = PACK_PROCESSING_SURCHARGE + (FIGURE_SURCHARGE if is_figure else 0)
    return round(base_price * (1 + surcharge), 2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    width = float(data['width'])
    height = float(data['height'])
    is_figure = data['is_figure']
    is_pack = data['is_pack']

    area = width * height
    if is_pack:
        price = calculate_pack_price(area, is_figure)
    else:
        price = calculate_price(width, height, is_figure)
    
    return jsonify({'price': f"{price} грн"})

if __name__ == '__main__':
    app.run(debug=True)
