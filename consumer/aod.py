import json

def main(data):
    for a in data:
        json_data = {
            "price": get_aod_price(a),
            "seller": get_aod_seller(a),
            "ratings": get_aod_ratings(a),
            "sender": get_aod_sender(a)
        }
        print(json.dumps(json_data))

def get_aod_price(data):
    var = data.find_element_by_css_selector("span.a-price").text.split()
    float_var = float(var[0][1::] + "." + var[1])
    fee = data.find_element_by_css_selector("span.a-color-secondary.a-size-base").text.split()
    float_fee = float(fee[1][1::])
    return round(float_var + float_fee, 2)


def get_aod_sender(data):
    var = data.find_element_by_id("aod-offer-shipsFrom").text.split()
    return var[2]

def get_aod_seller(data):
    return data.find_element_by_css_selector("a.a-size-small.a-link-normal").text

def get_aod_ratings(data):
    var = data.find_element_by_id("seller-rating-count-{iter}").text.split()
    return var[0][1::]
