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

def UserInvestmentDetails(tckn):
    cursor = conn.cursor()
    try:
        query = f"""
        SELECT
            s.name AS stock_name,
            ROUND(SUM(p.buy_price * p.quantity) / SUM(p.quantity), 2) AS wa_buy_price,
            ROUND(c.price, 2) AS current_price,
            SUM(p.quantity) AS total_quantity
        FROM portfolio p
                 INNER JOIN stocks s ON p.stockID = s.stockID
                 INNER JOIN users u ON p.userID = u.userID
                 INNER JOIN stock_price_curr c ON p.stockID = c.stockID
        WHERE u.tckn = {tckn}
        GROUP BY s.name, c.price;
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

def getBuyandCurrTotal(tckn):
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
        formatted_data = []
        result = cursor.fetchall()[0]
        return result[0], result[1], round(result[1]/result[0]*100,2)
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
