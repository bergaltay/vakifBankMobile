import datetime

import jwt
from flask import Flask, render_template, request, jsonify, redirect, make_response
import os

import DBOperators
import graphOperators
import misc

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "your_secret_key")  # Use environment variable for security
def token_required(func):
    def wrapper(*args, **kwargs):
        token = request.cookies.get("token")
        if not token:
            return redirect("/?error=Unauthorized access. Please log in.")
        try:
            jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            return func(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return redirect("/?error=Session expired. Please log in again.")
        except jwt.InvalidTokenError:
            return redirect("/?error=Invalid token. Please log in.")
    return wrapper


def getUserName():
    token = request.cookies.get("token")
    decoded = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    return decoded["username"]

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/login', methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    psw = DBOperators.getUserTCKN(username)
    try:
        if int(password) == int(psw):
            token = jwt.encode(
                {"username": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
                app.config["SECRET_KEY"],
                algorithm="HS256"
            )
            response = make_response(jsonify({"message": "Login successful"}))
            response.set_cookie("token", token, httponly=True, secure=True)
            return response
        return jsonify({"message": "Invalid username or password"}), 401
    except Exception as e:
        print(e)
        return jsonify({"error": "An unexpected error occurred"}), 500


@app.route('/home')
@token_required
def home():
    tckn = getUserName()
    cursor = DBOperators.tickerListOfUser(tckn)
    accNum = 0
    try:
        cursor.fetchall()
        print("a")
        info_data = misc.detailsFormatter(DBOperators.UserInvestmentDetails(tckn).fetchall())
        print(info_data[0])
        accNum = DBOperators.getAccNumber(tckn)
        print("b")
    except Exception as e:
        print(e)
        info_data=[]
    finally:
        cursor.close()
    return render_template('portfolio.html',
                           username=DBOperators.getUserTCKN(tckn),
                           accNum=accNum,
                           currBalance=DBOperators.getUserCurrentBalance(tckn),
                           table_data=info_data,
                           totalValues=DBOperators.getBuyandCurrTotal(tckn),
                           pieChart=graphOperators.getGraphOfPortfolio(info_data)
                           )

if __name__ == '__main__':
    app.run(debug=True)