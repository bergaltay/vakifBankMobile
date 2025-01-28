import DBConnector
import yfinance as yf

def fetch_and_store_stock_data():
    try:
        connection = DBConnector.get_db_connection()
        cursor = connection.cursor()

        # Fetch all stocks from the database
        cursor.execute("SELECT stockID, name FROM stocks")
        stocks = cursor.fetchall()

        if not stocks:
            print("No stocks found in the database.")
            return

        for stockID, stock_name in stocks:
            try:
                yfinance_stock_name = f"{stock_name}.IS"
                print(f"Processing stock: {stock_name}, YFinance Name: {yfinance_stock_name}")

                # Fetch stock data
                stock = yf.Ticker(yfinance_stock_name)
                stock_data = stock.history(period="2d", interval="30m")
                stock_data.reset_index(inplace=True)

                if stock_data.empty:
                    print(f"No data fetched for {stock_name} ({yfinance_stock_name})")
                    continue

                print(f"Fetched {len(stock_data)} rows for {stock_name} ({yfinance_stock_name})")

                # Insert data into the database
                sql = """
                INSERT INTO stock_price_history (stockID, time, price, open, high, low, close, volume)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    price = VALUES(price), open = VALUES(open), high = VALUES(high),
                    low = VALUES(low), close = VALUES(close), volume = VALUES(volume);
                """

                for _, row in stock_data.iterrows():
                    print(f"Inserting data for {stock_name} at time {row['Datetime']} with price {row['Close']}")
                    data = (
                        stockID,
                        row['Datetime'].to_pydatetime(),
                        row['Close'],
                        row['Open'],
                        row['High'],
                        row['Low'],
                        row['Close'],
                        row['Volume']
                    )
                    cursor.execute(sql, data)

                connection.commit()
                print(f"Inserted stock price history for {stock_name} ({yfinance_stock_name})")

            except Exception as e:
                print(f"Error processing stock {stock_name}: {e}")
                continue

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection:
            connection.close()

fetch_and_store_stock_data()
