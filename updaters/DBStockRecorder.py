import yfinance as yf
import datetime
import DBConnector

conn = DBConnector.get_db_connection()


def getStockNames():
    cursor = conn.cursor()
    try:
        query="""select stockID, name from stocks"""
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()





def test():
    list = getStockNames()
    cursor = conn.cursor()
    price = 0.0
    stock_name =""
    for symbol in list:
        try:
            # Fetch stock data
            stock_name = symbol[1]
            stock = yf.Ticker(stock_name+".IS")
            stock_data = stock.history(period="1d")

            if not stock_data.empty:
                price = round(stock_data["Close"].iloc[-1],2)
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                query = f"""
                UPDATE stock_price_curr c
                inner join stocks s on c.stockID = s.stockID
                set c.price = {price} where s.stockID={symbol[0]}
                """
                cursor.execute(query)
                conn.commit()
                print(f"Recorded {symbol} - Price: {price} at {timestamp}")
            else:
                print(f"No data available for {symbol}")
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
    conn.close()

test()

def fetch_and_record_prices(stock_symbols):
    cursor = conn.cursor()

    for symbol in stock_symbols:
        try:
            # Fetch stock data
            stock = yf.Ticker(symbol)
            stock_data = stock.history(period="1d")

            if not stock_data.empty:
                # Get the latest closing price
                price = stock_data["Close"].iloc[-1]
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Insert the stock price into the database
                cursor.execute("""
                    INSERT INTO stock_price_curr (stock_symbol, stock_price, timestamp)
                    VALUES (?, ?, ?)
                """, (symbol, price, timestamp))

                print(f"Recorded {symbol} - Price: {price} at {timestamp}")
            else:
                print(f"No data available for {symbol}")
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")

    conn.commit()
    conn.close()