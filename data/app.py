from __future__ import print_function
# from flask import Flask
# from flask import request
# from flask.json import jsonify
from flask_cors import CORS
import flask
# import flask.Response
import sys
from urllib.request import urlopen
import json
from flask import render_template
import yfinance as yf
from statsmodels.tsa.ar_model import AR
from datetime import timedelta
import time
import random
from flask import Flask, redirect, url_for, escape, request, render_template, jsonify
import MySQLdb


db = MySQLdb.connect(host="localhost", user="root", passwd="", db="stockdb")    #new
cur = db.cursor()   #new

app = flask.Flask(__name__, template_folder="../views/")
#app=flask.Flask(__name__)
CORS(app)
global user_balance
user_balance = 10000
global portfolio
portfolio = {}
global all_stocks
all_stocks = {}
session={}
client=app.test_client()
def getAllCompanies():
    companies = ["ABT", "ABBV", "ADBE", "ADT", "AAP", "AES", "AFL", "AMG", "A", 
                "APD", "AKAM", "AA", "AGN", "ALXN", "ALLE", "ADS", "ALL", "ALTR", "MO", "AMZN", "AEE",
                "AAL", "AEP", "AXP", "AIG", "AMT", "AMP", "ABC", "AME", "AMGN", "APH", "APC", "ADI", "AON"
                "APA", "AIV", "AMAT", "ADM", "AIZ", "T", "ADSK", "ADP", "AN", "AZO", "AVGO", "AVB", "AVY",
                "BHI", "BLL", "BAC", "BK", "BCR", "BXLT", "BAX", "BBT", "BDX", "BBBY", "BRK-B", "BBY", "BLX",
                "HRB", "BA", "BWA", "BXP", "BSK", "BMY", "BRCM", "BF-B", "CHRW", "CA", "CVC", "COG", "CAM", "CPB",
                "COF", "CAH", "HSIC", "KMX", "CCL", "CAT", "CBG", "CBS", "CELG", "CNP", "CTL", "CERN", "CF", "SCHW", "CHK",
                "CVX", "CMG", "CB", "CI", "XEC", "CINF", "CTAS", "CSCO", "C", "CTXS", "CLX", "CME", "CMS", "COH", "KO", "CCE",
                "CTSH", "CL", "CMCSA", "CMA", "CSC", "CAG", "COP", "CNX", "ED", "STZ", "GLW", "COST", "CCI", "CSX", "CMI", "CVS",
                "DHI", "DHR", "DRI", "DVA", "DE", "DLPH", "DAL", "XRAY", "DVN", "DO", "DTV", "DFS", "DISCA", "DISCK", "DG", "DLTR",
                "D", "DOV", "DOW", "DPS", "DTE", "DD", "DUK", "DNB", "ETFC", "EMN", "ETN", "EBAY", "ECL", "EIX", "EW", "EA",
                "EMC", "EMR", "ENDP", "ESV", "ETR", "EOG", "EQT", "EFX", "EQIX", "EQR", "ESS", "EL", "ES", "EXC", "EXPE",
                "EXPD", "ESRX", "XOM", "FFIV", "FB", "FAST", "FDX", "FIS", "FITB", "FSLR", "FE", "FSIV", "FLIR", "FLS",
                "FLR", "FMC", "FTI", "F", "FOSL", "BEN", "FCX", "FTR", "GME", "GPS", "GRMN", "GD", "GE", "GGP", "GIS",
                "GM", "GPC", "GNW", "GILD", "GS", "GT", "GOOGL", "GOOG", "GWW", "HAL", "HBI", "HOG", "HAR", "HRS", "HIG",
                "HAS", "HCA", "HCP", "HCN", "HP", "HES", "HPQ", "HD", "HON", "HRL", "HSP", "HST", "HCBK", "HUM", "HBAN",
                "ITW", "IR", "INTC", "ICE", "IBM", "IP", "IPG", "IFF", "INTU", "ISRG", "IVZ", "IRM", "JEC", "JBHT", "JNJ",
                "JCI", "JOY", "JPM", "JNPR", "KSU", "K", "KEY", "GMCR", "KMB", "KIM", "KMI", "KLAC", "KSS", "KRFT", "KR", "LB",
                "LLL", "LH", "LRCX", "LM", "LEG", "LEN", "LVLT", "LUK", "LLY", "LNC", "LLTC", "LMT", "L", "LOW", "LYB", "MTB",
                "MAC", "M", "MNK", "MRO", "MPC", "MAR", "MMC", "MLM", "MAS", "MA", "MAT", "MKC", "MCD", "MHFI", "MCK", "MJN",
                "MMV", "MDT", "MRK", "MET", "KORS", "MCHP", "MU", "MSFT", "MHK", "TAP", "MDLZ", "MON", "MNST", "MCO", "MS", "MOS",
                "MSI", "MUR", "MYL", "NDAQ", "NOV", "NAVI", "NTAP", "NFLX", "NWL", "NFX", "NEM", "NWSA", "NEE", "NLSN", "NKE", "NI",
                "NE", "NBL", "JWN", "NSC", "NTRS", "NOC", "NRG", "NUE", "NVDA", "ORLY", "OXY", "OMC", "OKE", "ORCL", "OI", "PCAR",
                "PLL", "PH", "PDCO", "PAYX", "PNR", "PBCT", "POM", "PEP", "PKI", "PRGO", "PFE", "PCG", "PM", "PSX", "PNW", "PXD",
                "PBI", "PCL", "PNC", "RL", "PPG", "PPL", "PX", "PCP", "PCLN", "PFG", "PG", "PGR", "PLD", "PRU", "PEG", "PSA", "PHM",
                "PVH", "QRVO", "PWR", "QCOM", "DGX", "RRC", "RTN", "O", "RHT", "REGN", "RF", "RSG", "RAI", "RHI", "ROK", "COL", "ROP",
                "ROST", "RLC", "R", "CRM", "SNDK", "SCG", "SLB", "SNI", "STX", "SEE", "SRE", "SHW", "SIAL", "SPG", "SWKS", "SLG", "SJM",
                "SNA", "SO", "LUV", "SWN", "SE", "STJ", "SWK", "SPLS", "SBUX", "HOT", "STT", "SRCL", "SYK", "STI", "SYMC", "SYY",
                "TROW", "TGT", "TEL", "TE", "TGNA", "THC", "TDC", "TSO", "TXN", "TXT", "HSY", "TRV", "TMO", "TIF", "TWX", "TWC", "TJK", "TMK", "TSS",
                "TSCO", "RIG", "TRIP", "FOXA", "TSN", "TYC", "UA", "UNP", "UNH", "UPS", "URI", "UTX", "UHS", "UNM", "URBN", "VFC", "VLO", "VAR", "VTR",
                "VRSN", "VZ", "VRTX", "VIAB", "V", "VNO", "VMC", "WMT", "WBA", "DIS", "WM", "WAT", "ANTM", "WFC", "WDC", "WU", "WY", "WHR", "WFM", "WMB",
                "WEC", "WYN", "WYNN", "XEL", "XRX", "XLNX", "XL", "XYL", "YHOO", "YUM", "ZBH", "ZION", "ZTS"]
    return companies


def getSymbols():
    symbols = ["ABT", "ABBV", "ADBE", "ADT", "AAP", "AES", "AFL", "AMG", "A", 
                            "APD"]
    return symbols

@app.route('/api/register', methods=['POST'])
def register():
    json_data = request.get_json()
    username=json_data['username']
    name=json_data['name']
    password=json_data['password']
    amount='10000'
    userid=random.choice(range(100))
    temp = "Select * from user";
    cur.execute(temp)
    userdetails=[dict(
                id=row[0],
                name=row[1],
                uname=row[2],
                pw=row[3],
                amount=row[4],
            ) for row in cur.fetchall()]
    f=1
    while(f==1):
        for i in userdetails:
            if(i['id']==userid):
                f=2
                userid=random.choice(range(100))
                break
        if(f==2):
            f=1
        else:
            f=0
    #temp = "Insert into User(UserID,Name,Username,Password,Amount) values (%s,%s,%s,%s,%s)"(userid,#('"+userid+"','"+name+"','"+username+"','"+pwd+"',10000);"
    cur.execute("""Insert into User(UserID,Name,Username,Password,Amount) values (%s,%s,%s,%s,%s)""",(userid,name,username,password,amount))
    db.commit()
    status = 'success'
    return jsonify({'result': status})

@app.route('/api/login', methods=['POST'])
def login():
    json_data = request.get_json()
    uname=json_data["username"]
    pwd=json_data["pwd"]
    temp = "Select * from user where Username='"+uname+"' and Password='"+pwd+"';"
    cur.execute(temp)
    userdetails=[dict(
                id=row[0],
                name=row[1],
                uname=row[2],
                pw=row[3],
                amount=row[4],
            ) for row in cur.fetchall()]
    if(len(userdetails)==1):
        #cur.execute("""Insert into User(UserID,Name,Username,Password,Amount) values (%s,%s,%s,%s,%s)""",(userid,name,username,password,amount))
        cur.execute("truncate logged")
        cur.execute("""Insert into logged(userid,name,username,password,amount) values (%s,%s,%s,%s,%s)""",(userdetails[0]["id"],userdetails[0]["name"],userdetails[0]["uname"],userdetails[0]["pw"],userdetails[0]["amount"]))
        status = True
    else:
        status = False
    db.commit()
    return jsonify({'result': status})

@app.route('/api/user',methods=['GET'])
def user():
    temp = "Select * from logged;"
    cur.execute(temp)
    userdetails=[dict(
                id=row[0],
                name=row[1],
                uname=row[2],
                pw=row[3],
                amount=row[4],
            ) for row in cur.fetchall()]
    x=dict()
    x["uname"]=""
    x["amount"]=""
    if(userdetails):
        x["uname"]=userdetails[0]["uname"]
        x["amount"]=str(userdetails[0]["amount"])
    return jsonify(x)

@app.route('/api/logout',methods=['GET'])
def logout():
    cur.execute("truncate logged")
    x=dict()
    x["uname"]=""
    x["amount"]=""
    db.commit()
    return jsonify(x)

@app.route('/stocks/all')
def allStocks():
    global all_stocks
    symbolList = getSymbols()
    #query = buildQuery(symbolList)
    #response = json.loads(urlopen(query).read())
    # return jsonify(response["query"])
    response = yf.Tickers(symbolList)
    #TODO: parse safely
    #quotes = response["query"]["results"]["quote"]

    for ticker in symbolList:
        #symbol = quote["Symbol"]
        #price = quote["LastTradePriceOnly"]
        #name = quote["Name"]
        #change = quote["Change"]
        #time = quote["LastTradeTime"]
        name=getattr(response.tickers,ticker).info["longName"]
        symbol=getattr(response.tickers,ticker).info["symbol"]
        price=getattr(response.tickers,ticker).info["regularMarketPrice"]
        change=getattr(response.tickers,ticker).info["SandP52WeekChange"]
        time=getattr(response.tickers,ticker).info["exchangeTimezoneShortName"]
        all_stocks[symbol] = {"name": name, "symbol": symbol, "price": price, "change": change, "time": time}

    #return render_template("index.html",mainController.stocks=flask.jsonify(all_stocks))
    return flask.jsonify(all_stocks)

def buildQuery(symbolList):
    query_prefix = "https://query.yahooapis.com/v1/public/yql?q=select%20Symbol%2CLastTradePriceOnly%2CLastTradeTime%2CLastTradeDate%2CChange%2CName%20from%20yahoo.finance.quotes%20where%20symbol%20in%20("
    query_suffix = ")&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback="
    query_companies = ""

    first_symbol = True
    for symbol in symbolList:
        if first_symbol:
            first_symbol = False
            query_companies = "%22{0}%22".format(symbol)
        else:
            query_companies += "%2C%22{0}%22".format(symbol)

    return query_prefix + query_companies + query_suffix

@app.route('/stocks/buy', methods=['POST'])
def buyStock():
    print('hello')
    global all_stocks
    global portfolio
    global user_balance
    #symbol = flask.request.get_json()#.encode('ascii')
    #symbol = symbol[10:-1]
    x = flask.request.get_json()#.encode('ascii')
    symbol = x["symbol"]
    username=x["username"]
    print(all_stocks.keys())
    print(symbol,type(symbol))
    #quantity = flask.request.form['quantity']
    stock = all_stocks[symbol]
    price = stock["price"]
    transid=random.choice(range(1000))
    temp = "Select * from user where Username='"+username+"';"
    cur.execute(temp)
    userdetails=[dict(
                id=row[0],
                name=row[1],
                uname=row[2],
                pw=row[3],
                amount=row[4],
            ) for row in cur.fetchall()]
    uid=userdetails[0]["id"]
    amount=float(userdetails[0]["amount"])
    temp = "Select * from transactions";
    cur.execute(temp)
    transdetails=[dict(
                tid=row[0],
                uid=row[1],
                c_s=row[2],
                a_p=row[3],
                a_s=row[4],
            ) for row in cur.fetchall()]
    f=1
    while(f==1):
        for i in transdetails:
            if(i['tid']==transid):
                f=2
                transid=random.choice(range(1000))
                break
        if(f==2):
            f=1
        else:
            f=0
    amount-=float(price)
    cur.execute("""Insert into transactions(TID,UID,Company_Symbol,Amount_Purchased,Amount_Sold) values (%s,%s,%s,%s,%s)""",(transid,uid,symbol,price,0))
    cur.execute("""Update user set AMOUNT=%s where UserID=%s""",(amount,uid));
    cur.execute("""Update logged set AMOUNT=%s where userid=%s""",(amount,uid))
    db.commit()
    #    portfolio[symbol] = {"quantity": portfolio[symbol]["quantity"] + 1, "price": all_stocks[symbol]["price"], "name": all_stocks[symbol]["name"], "change": all_stocks[symbol]["change"]}
    #else:
    #    portfolio[symbol] = {"quantity": 1, "price": all_stocks[symbol]["price"], "name": all_stocks[symbol]["name"], "change": all_stocks[symbol]["change"]}

    #user_balance -= float(price)

    print(amount)

    return flask.jsonify(amount)

    '''
    if symbol in portfolio:
        portfolio[symbol] = {"quantity": portfolio[symbol]["quantity"] + 1, "price": all_stocks[symbol]["price"], "name": all_stocks[symbol]["name"], "change": all_stocks[symbol]["change"]}
    else:
        portfolio[symbol] = {"quantity": 1, "price": all_stocks[symbol]["price"], "name": all_stocks[symbol]["name"], "change": all_stocks[symbol]["change"]}

    user_balance -= float(price)

    print(user_balance)

    return flask.jsonify(user_balance)
    '''
@app.route('/stocks/sell', methods=['POST'])
def sellStock():
    '''
    global all_stocks
    global portfolio
    global user_balance
    symbol = flask.request.get_json()#.encode('ascii')
    symbol = symbol[10:-1]
    print(all_stocks.keys())
    print(symbol)
    #quantity = flask.request.form['quantity']
    stock = all_stocks[symbol]
    price = stock["price"]
    '''
    x = flask.request.get_json()#.encode('ascii')
    symbol = x["symbol"]
    username=x["username"]
    print(all_stocks["A"])
    print(symbol,type(symbol))
    '''
    if symbol in portfolio:
        quantity = portfolio[symbol]["quantity"]
        if quantity > 0:
            user_balance += float(price)
            portfolio[symbol] = {"quantity": quantity - 1, "price": all_stocks[symbol]["price"], "name": all_stocks[symbol]["name"], "change": all_stocks[symbol]["change"]}
    '''
    stock = all_stocks[symbol]
    price = stock["price"]
    temp = "Select * from user where Username='"+username+"';"
    cur.execute(temp)
    userdetails=[dict(
                id=row[0],
                name=row[1],
                uname=row[2],
                pw=row[3],
                amount=row[4],
            ) for row in cur.fetchall()]
    uid=userdetails[0]["id"]
    amount=float(userdetails[0]["amount"])
    temp = "Select * from transactions;"
    cur.execute(temp)
    transdetails=[dict(
                tid=row[0],
                uid=row[1],
                c_s=row[2],
                a_p=row[3],
                a_s=row[4],
            ) for row in cur.fetchall()]
    transid=random.choice(range(1000))
    f=1
    while(f==1):
        for i in transdetails:
            if(i['tid']==transid):
                f=2
                transid=random.choice(range(1000))
                break
        if(f==2):
            f=1
        else:
            f=0
    temp = "Select * from transactions where UID='"+uid+"' and company_symbol='"+symbol+"';"
    cur.execute(temp)
    transdetails=[dict(
                tid=row[0],
                uid=row[1],
                c_s=row[2],
                a_p=row[3],
                a_s=row[4],
            ) for row in cur.fetchall()]
    total=0
    for i in transdetails:
        total-=i["a_s"]
        total+=i["a_p"]
    print(total)
    if(total>0):
            amount+=float(price)
            cur.execute("""Insert into transactions(TID,UID,Company_Symbol,Amount_Purchased,Amount_Sold) values (%s,%s,%s,%s,%s)""",(transid,uid,symbol,0,price))
            cur.execute("""Update user set AMOUNT=%s where UserID=%s""",(amount,uid));
            cur.execute("""Update logged set AMOUNT=%s where userid=%s""",(amount,uid))
            db.commit()
            s={"status1":amount}
    else:
        print("Not in Stock")
        s={"status":"Null"}
    return jsonify(s)
    '''
    else:
        print("Not in Stock")
        print(user_balance)

    return flask.jsonify(user_balance)
    '''

def date_unix(dates):
   
    dates=list(map(lambda x:x.to_pydatetime(),dates))
    #d=datetime.strptime('2020-04-10','%Y-%m-%d')
    unixtime = list(map(lambda x:time.mktime(x.timetuple()),dates))
    return unixtime

@app.route('/stocks/detail', methods=['POST'])
def getDetail():
    symbol = flask.request.get_json()#.encode('ascii')
    symbol = symbol[10:-1]
    print(symbol)
    response = yf.Tickers(symbol)
    hist=getattr(response.tickers,symbol).history('3mo')
    open_data=hist.iloc[:,0]

    model = AR(open_data)
    model_fit = model.fit(disp=0)
    print(model_fit.summary())
    predictions = model_fit.predict(start=len(open_data),end=len(open_data)+9,dynamic=False)

    dates=open_data.index.tolist()
    final_date=dates[-1].to_pydatetime()
    dates=date_unix(dates)
    open_data=list(open_data)
   
    l=[]
    for i in range(1,11):
        l.append(final_date+timedelta(days=i))

    predict_dates=list(map(lambda x:time.mktime(x.timetuple()),l))
    predict_open=list(predictions)

    actual=list(zip(dates,open_data))
    predict=list(zip(predict_dates,predict_open))

    data={"actual":actual,"predict":predict}
    return flask.jsonify(data)


@app.route('/user/balance')
def getBalance():
    '''
    global user_balance
    return flask.jsonify(user_balance)
    '''
    temp = "Select * from logged;"
    cur.execute(temp)
    userdetails=[dict(
                id=row[0],
                name=row[1],
                uname=row[2],
                pw=row[3],
                amount=row[4],
            ) for row in cur.fetchall()]
    return flask.jsonify(str(userdetails[0]["amount"]))

@app.route('/user/portfolio', methods=['GET'])
def getPortfolio():
    '''
    global portfolio
    return flask.jsonify(portfolio)
    '''
    temp = "Select * from logged;"
    cur.execute(temp)
    userdetails=[dict(
                id=row[0],
                name=row[1],
                uname=row[2],
                pw=row[3],
                amount=row[4],
            ) for row in cur.fetchall()]
    uid=userdetails[0]["id"]
    uname=userdetails[0]["uname"]
    amount=userdetails[0]["amount"]
    temp = "Select * from transactions where uid='"+uid+"';"
    cur.execute(temp)
    transdetails=[dict(
                tid=row[0],
                uid=row[1],
                c_s=row[2],
                a_p=row[3],
                a_s=row[4],
            ) for row in cur.fetchall()]
    stuff={"transactions":[],"amount":str(amount),"name":uname}
    for i in transdetails:
        if(i["a_p"]):
            key1="a_p"
            string="Amount_Purchased"
        else:
            key1="a_s"
            string="Amount_Sold"
        stuff["transactions"].append({"company_symbol":i["c_s"],string:str(i[key1])})
    return flask.jsonify(stuff)


@app.route('/about/description', methods=['GET'])
def getDescription():
    text = open('description.txt', 'r+')
    content = text.read()
    text.close()
    #response=make_response(content,200)
    #response.mimetype="text/html"
    return content

@app.route('/about/video', methods=['GET'])
def getVideo():
    video=open("y2mate.com - Watch high-speed trading in action_2u007Msq1qo_360p.mp4","rb")
    content=video.read()
    video.close()
    return content, {'Content-Type': 'video/mp4'}

@app.route('/check', methods=['POST'])
def checkCompany():
    term = flask.request.get_json()
    term=term[8:-1]
    #print(type(term))
    res=[]
    final_result={}
    allCompanies=getAllCompanies();
    print(allCompanies)
    for company in allCompanies:
        #print(type(company))
        if(term==company[:len(term)]):
            res.append(company)
    print(res)
    return flask.jsonify(res)
@app.after_request
def apply_caching(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = "GET, PUT, POST, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] =  "Origin, X-Requested-With, Content-Type, Accept"
    return response

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
