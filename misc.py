import DBOperators
from datetime import datetime
from math import ceil

def dataFormatter(raw_data):
    for entry in raw_data:
        buy_date = datetime.strptime(entry['buy_date'], "%Y-%m-%d %H:%M:%S")
        current_date = datetime.now()
        # Calculate days passed as a fraction and use ceiling
        days_passed = ceil((current_date - buy_date).total_seconds() / (24 * 3600))  # Total seconds in a day = 24*3600
        entry['days_passed'] = days_passed
        entry['buy_date_user'] = buy_date.strftime("%d/%m/%Y")
        entry['symbol_graph'] = str(entry['symbol'])[:12]
    return raw_data

def investmentSumFormatter(raw_data):
    raw_data = raw_data[0]
    buy_total = float(raw_data['stocks_buy_total']+raw_data['funds_buy_total'])
    curr_total = float(raw_data['stocks_curr_total']+raw_data['funds_curr_total'])
    change_ratio = round(float(((curr_total-buy_total)/buy_total)*100),2)
    formatted_data = {
        'buy_total': buy_total,
        'current_total': curr_total,
        'change_ratio': change_ratio,
    }
    return formatted_data

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
            'buy_price': f"{item[2]}",
            'curr_price': f"{item[3]}",
            'quantity': f"{item[4]}",
            'profit': f"{round(float((item[3]-item[2])*item[4]),2)}",
            'total': f"{round(item[3]*item[4],2)}",
            'ratio': f"{round(((item[3]-item[2])/item[2])*100,2)}",
            'buy_date': f"{item[1]}",
        })
    return formatted_data
def sembolNameFormatter(raw_data):
    formatted_data = []
    for item in raw_data:
        formatted_data.append({'sembol':item["sembol"]})
    return formatted_data


