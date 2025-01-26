import DBOperators

def currPriceFormatter(raw_data):
    formatted_data = []
    for item in raw_data:
        formatted_data.append({
            'stock': item[0],
            'price': item[1],
        })
    return formatted_data
def detailsFormatter(raw_data):
    formatted_data = []
    for item in raw_data:
        formatted_data.append({
            'symbol': item[0],
            'buy_price': f"{item[1]}",
            'curr_price': f"{item[2]}",
            'quantity': f"{item[3]}",
            'profit': f"{round(float((item[2]-item[1])*item[3]),2)}",
            'total': f"{round(item[2]*item[3],2)}",
            'ratio': f"{round(((item[2]-item[1])/item[1])*100,2)}"
        })
    return formatted_data
def sembolNameFormatter(raw_data):
    formatted_data = []
    for item in raw_data:
        formatted_data.append({'sembol':item["sembol"]})
    return formatted_data


