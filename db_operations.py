import datetime

import DBConnector

conn = DBConnector.get_db_connection()

def get_user_stock_info(tckn,interval):
    data = []
    if interval == "all":
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
                    ROUND(a.wa_buy_price, 2) AS wa_buy_price,
                    ROUND(c.price, 2) AS current_price,
                    a.total_quantity AS total_quantity,
                    date(o.oldest_buy_date) AS from_this_date
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
            data = cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
    else:
        cursor = conn.cursor()
        try:
            query = f"""
                WITH test as (
                    select
                        s.name,
                        date(p.buy_date) as buy_date,
                        if(datediff(current_date,date(p.buy_date))<{interval},p.buy_price,sph.close) as t_buy_price,
                        spc.price as curr_price,
                        p.quantity
                    from stock_price_history sph
                             inner join stocks s on sph.stockID = s.stockID
                             inner join vbmobil.stock_price_curr spc on s.stockID = spc.stockID
                             inner join portfolio p on s.stockID = p.stockID
                             inner join users u on p.userID = u.userID
                    where u.tckn = {tckn} and (if(datediff(current_date,date(p.buy_date))<{interval},subdate(current_date,{interval}),date(sph.time)))=subdate(current_date,{interval})
                    group by s.name,if(datediff(current_date,date(p.buy_date))<{interval},"in","out"), date(p.buy_date), if(datediff(current_date,date(p.buy_date))<{interval},p.buy_price,sph.close), spc.price, p.quantity
                ),OldestBuyDate AS (
                    SELECT
                        s.name,
                        MIN(p.buy_date) AS oldest_buy_date
                    FROM portfolio p
                    inner join stocks s on p.stockID = s.stockID
                    GROUP BY p.stockID
                ),
                calculation as (
                    select
                        t.name as stock_name,
                        round(SUM(t.t_buy_price * t.quantity) / SUM(t.quantity),2) AS wa_buy_price,
                        t.curr_price,
                        SUM(t.quantity) AS total_quantity
                    from test t
                    group by t.name, t.curr_price
                )select
                     c.stock_name,
                     c.wa_buy_price,
                     curr_price,
                     c.total_quantity,
                     if(date(o.oldest_buy_date)>subdate(current_date,{interval}),date(o.oldest_buy_date),subdate(current_date,{interval})) as from_this_date
                 from calculation c
                inner join OldestBuyDate o on c.stock_name=o.name
                order by (c.curr_price-c.wa_buy_price)*c.total_quantity desc

            """
            cursor.execute(query)
            data = cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
    formatted_data =[]
    for i in data:
        formatted_data.append({
            "stock_name":       i[0],
            "wa_buy_price":     i[1],
            "curr_price":       i[2],
            "quantity":   i[3],
            "from_this_time":   i[4].strftime("%m/%d/%Y"),
            "total":            float(round(i[2]*i[3],2)),
            "ratio":            round(((i[2]-i[1])/i[1])*100,2),
            "profit":           round((i[2]-i[1])*i[3],2),
            "days_passed":      (datetime.date.today()-i[4]).days
        })
    return formatted_data


def get_stocks_detail(tckn,stock_name):
    cursor = conn.cursor()
    result = []
    try:
        query = f"""
        with AggregatedData AS (
            SELECT
                p.stockID,
                SUM(p.quantity) AS total_quantity,
                ROUND(SUM(p.buy_price * p.quantity) / SUM(p.quantity),2) AS wa_buy_price
            FROM portfolio p
            inner join stock_price_curr spc on p.stockID=spc.stockID
            GROUP BY p.stockID
        )
        select sd.full_name,
               s.name,
               sd.market,
               a.total_quantity,
               p.blocked_quantity,
               spc.price,
               a.wa_buy_price,
               ROUND(a.wa_buy_price*a.total_quantity,2) AS total,
               ROUND(spc.price*a.total_quantity,2) as curr_total
        from stocks s
        inner join AggregatedData a on a.stockID=s.stockID
        inner join stocks_detail sd on s.stockID = sd.stockID
        inner join portfolio p on s.stockID = p.stockID
        inner join stock_price_curr spc on s.stockID = spc.stockID
        inner join users u on p.userID = u.userID
        where u.tckn = {tckn} and s.name = "{stock_name}"
        group by sd.full_name, s.name, sd.market, a.total_quantity, p.blocked_quantity, spc.price, a.wa_buy_price,total,curr_total
        """
        cursor.execute(query)
        result = cursor.fetchall()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
    formatted_data = []
    for i in result:
        formatted_data.append({
            "stock_full_name":      i[0],
            "stock_name":           i[1],
            "market":               i[2],
            "quantity":             i[3],
            "blocked_quantity":     i[4],
            "curr_price":           "{:,.2f}".format(i[5]),
            "wa_buy_price":         "{:,.2f}".format(i[6]),
            "buy_total":            "{:,.2f}".format(float(round(i[3]*i[6],2))),
            "profit":               "{:,.2f}".format(round((i[5]-i[6])*i[3],2)),
            "curr_total":           "{:,.2f}".format(float(round(i[5]*i[3],2))),
            "tracker":              (i[5]-i[6])*i[3]
        })
        return formatted_data[0]

def get_stock_price_details(stock_name):
    cursor = conn.cursor()
    data = []
    try:
        query = f"""
            select spd.adh7, spd.adh30, spd.market_cap, spd.volume, spd.daily_open from stocks_price_details spd
            inner join stocks s on spd.stockID = s.stockID
            where s.name = "{stock_name}"
        """
        cursor.execute(query)
        data = cursor.fetchall()
    except Exception as e:
        print(e)
        return data
    finally:
        cursor.close()
    formatted_data = {
        "adh7": "{:,.2f}".format(data[0][0]),
        "adh30": "{:,.2f}".format(data[0][1]),
        "market_cap": "{:,.2f}".format(data[0][2]),
        "volume":  "{:,.2f}".format(data[0][3]),
        "daily_open": "{:,.2f}".format(data[0][4]),
    }
    return formatted_data






print(get_stock_price_details("THYAO"))
