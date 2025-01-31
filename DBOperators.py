import DBConnector


conn = DBConnector.get_db_connection()


def getUserTCKN(tckn):
    try:
        tckn = int(tckn)
        cursor = conn.cursor()
        query = f"""
        select password from users
        where tckn = {tckn}
        LIMIT 1;
        """
        cursor.execute(query)
        result = cursor.fetchone()[0]
    except Exception as e:
        print(e)
        result = None
    finally:
        cursor.close()
    return int(result)

def getUserName(tckn):
    try:
        tckn = int(tckn)
        cursor = conn.cursor()
        query = f"""
            select username from users
            where tckn = {tckn}
            LIMIT 1;
            """
        cursor.execute(query)
        result = cursor.fetchone()[0]
    except Exception as e:
        print(e)
        result = None
    finally:
        cursor.close()
    return str(result)

def getAccNumber(tckn):
    try:
        cursor = conn.cursor()
        tckn = int(tckn)
        query = f"""
            select account_number from accounts a
                inner join users u on a.userID = u.userID
            where u.tckn = {tckn}
            limit 1;
            """
        cursor.execute(query)
        result = cursor.fetchone()[0]
    except Exception as e:
        print(e)
        result = None
    finally:
        cursor.close()
    return int(result)

def tickerListOfUser(tckn):
    try:
        cursor = conn.cursor(dictionary=True)
        query = f"""SELECT
                        tl.name AS sembol
                    FROM
                        users u
                            INNER JOIN
                        portfolio p ON u.userID = p.userID
                            INNER JOIN
                        stocks tl ON tl.stockID = p.stockID
                    WHERE
                        u.tckn = {tckn};
                        """
        cursor.execute(query)
        return cursor
    except Exception as e:
        print(e)
        return None

def getTickerListOfUser(tckn):
    result =[]
    try:
        result = tickerListOfUser(tckn)
        formatted_results = {[
            row['sembol']
            for row in result
        ]}
        return formatted_results
    except Exception as e:
        print(e)
        return result

def UserStockPortfolioDetails(tckn):
    cursor = conn.cursor()
    try:
        query = f"""
        WITH OldestBuyDate AS (
            SELECT
                p.stockID,
                MIN(p.buy_date) AS oldest_buy_date
            FROM portfolio p
            GROUP BY p.stockID
        ),
             AggregatedData AS (
                 SELECT
                     p.stockID,
                     SUM(p.quantity) AS total_quantity,
                     SUM(p.buy_price * p.quantity) / SUM(p.quantity) AS wa_buy_price
                 FROM portfolio p
                 GROUP BY p.stockID
             )
        SELECT
            s.name AS stock_name,
            o.oldest_buy_date AS buy_date,
            ROUND(a.wa_buy_price, 2) AS wa_buy_price,
            ROUND(c.price, 2) AS current_price,
            a.total_quantity AS total_quantity
        FROM OldestBuyDate o
                 INNER JOIN stocks s ON o.stockID = s.stockID
                 INNER JOIN stock_price_curr c ON o.stockID = c.stockID
                 INNER JOIN AggregatedData a ON o.stockID = a.stockID
                 INNER JOIN portfolio p ON o.stockID = p.stockID
                 INNER JOIN users u ON p.userID = u.userID
        WHERE u.tckn = {tckn}
        GROUP BY s.name, o.oldest_buy_date, c.price, a.total_quantity, a.wa_buy_price
        ORDER BY  (c.price*a.total_quantity) desc ;
        """
        cursor.execute(query)
        return cursor
    except Exception as e:
        print(e)
        return cursor
def UserFundPortfolioDetails(tckn):
    cursor = conn.cursor()
    try:
        query = f"""
        WITH OldestBuyDate AS (
            SELECT
                fp.fundID,
                MIN(fp.buy_date) AS oldest_buy_date
            FROM fund_portfolio fp
            GROUP BY fp.fundID
        ),
             AggregatedData AS (
                 SELECT
                     fp.fundID,
                     SUM(fp.quantity) AS total_quantity,
                     SUM(fp.buy_price * fp.quantity) / SUM(fp.quantity) AS wa_buy_price
                 FROM fund_portfolio fp
                 GROUP BY fp.fundID
             )
        SELECT
            f.fund_name AS fund_name,
            o.oldest_buy_date AS buy_date,
            ROUND(a.wa_buy_price, 2) AS wa_buy_price,
            ROUND(cf.price, 2) AS current_price,
            a.total_quantity AS total_quantity
        FROM OldestBuyDate o
                 INNER JOIN funds f ON o.fundID = f.fundID
                 INNER JOIN fund_price_curr cf ON o.fundID = cf.fundID
                 INNER JOIN AggregatedData a ON o.fundID = a.fundID
                 INNER JOIN fund_portfolio fp ON o.fundID = fp.fundID
                 INNER JOIN users u ON fp.userID = u.userID
        WHERE u.tckn = {tckn}
        GROUP BY f.fund_name, o.oldest_buy_date, cf.price, a.total_quantity, a.wa_buy_price;
        """
        cursor.execute(query)
        return cursor
    except Exception as e:
        print(e)
        return cursor
def updateCurrBalanceOfUser(balance,tckn):
    cursor = conn.cursor()
    try:
        query = f"""
        update accounts as a
        join users as u on a.userID = u.userID
        set a.current_balance = {balance}
        where u.tckn = {tckn}
        """
        cursor.execute(query)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        cursor.close()

def getUserCurrentBalance(tckn):
    cursor = conn.cursor()
    try:
        query = f"""
        select a.current_balance from accounts a
            inner join users u on a.userID = u.userID
        where account_type='2' and u.tckn = {tckn}
        """
        cursor.execute(query)
        result = cursor.fetchone()[0]
        return float(result)
    except Exception as e:
        print(e)
        return 0.00
    finally:
        cursor.close()


def getCurrPriceOfStocks():
    cursor = conn.cursor()
    try:
        query="""
        select s.name, c.price from stock_price_curr c
        inner join stocks s on c.stockID = s.stockID
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        return None

def getStocksTotalBuyandCurr(tckn):
    cursor = conn.cursor()
    try:
        query = f"""
        select sum(p.buy_price*p.quantity) as buy_total,
               sum(c.price*p.quantity) as curr_total
        from portfolio p
        inner join stock_price_curr c on p.stockID = c.stockID
        inner join users u on p.userID = u.userID
        where u.tckn = {tckn}
        """
        cursor.execute(query)
        result = cursor.fetchall()[0]
        return result[0], result[1], round(((result[1]-result[0])/result[0])*100,2)
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()



def getFundsTotalBuyandCurr(tckn):
    cursor = conn.cursor()
    try:
        query = f"""
        SELECT 
            SUM(fp.buy_price * fp.quantity) AS buy_total,
            SUM(cf.price * fp.quantity) AS curr_total
        FROM fund_portfolio fp
        INNER JOIN fund_price_curr cf ON fp.fundID = cf.fundID
        INNER JOIN users u ON fp.userID = u.userID
        WHERE u.tckn = {tckn};"""
        cursor.execute(query)
        result = cursor.fetchall()[0]
        return result[0], result[1], round(((result[1]-result[0])/result[0])*100,2)
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()

def getInvestmentSums(tckn):
    cursor = conn.cursor()
    try:
        query = f"""
        WITH StockValues AS (
    SELECT 
        ROUND(SUM(p.buy_price * p.quantity), 2) AS buy_total,
        ROUND(SUM(c.price * p.quantity), 2) AS curr_total
    FROM portfolio p
    INNER JOIN stock_price_curr c ON p.stockID = c.stockID
    INNER JOIN users u ON p.userID = u.userID
    WHERE u.tckn = {tckn}
),
FundValues AS (
    SELECT 
        ROUND(SUM(fp.buy_price * fp.quantity), 2) AS buy_total,
        ROUND(SUM(cf.price * fp.quantity), 2) AS curr_total
    FROM fund_portfolio fp
    INNER JOIN fund_price_curr cf ON fp.fundID = cf.fundID
    INNER JOIN users u ON fp.userID = u.userID
    WHERE u.tckn = {tckn}
)
SELECT 
    'stocks' AS asset_type, 
    StockValues.buy_total AS total_buy_value, 
    StockValues.curr_total AS total_current_value
FROM StockValues
UNION ALL
SELECT 
    'funds' AS asset_type, 
    FundValues.buy_total AS total_buy_value, 
    FundValues.curr_total AS total_current_value
FROM FundValues;
"""
        cursor.execute(query)
        result = cursor.fetchall()
        formatted_data = [{
            'stocks_buy_total': result[0][1],
            'stocks_curr_total': result[0][2],
            'funds_buy_total': result[1][1],
            'funds_curr_total': result[1][2],
        }]
        return formatted_data
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()


def getXdayHistoryOfSymbol(symbol,day):
    cursor = conn.cursor()
    try:
        query=f"""
        select sp.open, sp.high, sp.low, sp.close,sp.time from stock_price_history as sp
                  inner join stocks as s on sp.stockID = s.stockID
        where s.name = '{symbol}' and datediff(current_timestamp,sp.time)<{day};
        """
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()



