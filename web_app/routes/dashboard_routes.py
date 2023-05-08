
import requests
import json
from flask import Blueprint, request, render_template, redirect

from web_app.services.alpha import AlphavantageService, ALPHAVANTAGE_API_KEY


dashboard_routes = Blueprint("dashboard_routes", __name__)

@dashboard_routes.route("/stocks/form")
def stocks_form():
    print("STOCKS FORM...")
    return render_template("stocks_form.html")


@dashboard_routes.route("/stocks/dashboard", methods=["GET", "POST"])
def stocks_dashboard():
    print("STOCKS DASHBOARD...")

    # if the form sends the data via POST request, we'll have request.form
    # otherwise if we specify url params in a GET request, we'll have request.args
    request_data = dict(request.form or request.args)
    print("REQUEST DATA:", request_data)

    symbol = request_data.get("symbol") or "MSFT"
    print("SYMBOL:", symbol)

    try:
        alpha = AlphavantageService()
        df = alpha.fetch_stocks_daily(symbol=symbol)
        if not df.empty:
            data = df.to_dict("records") # convert data to list of dictionaries (JSON stucture)
            return render_template("stocks_dashboard.html", symbol=symbol, data=data)
        else:
            #flash("OOPS", "warning")
            return redirect("/stocks/form")
    except Exception as err:
        print("ERROR", err)
        #flash("OOPS", "warning")
        return redirect("/stocks/form")
    
@dashboard_routes.route("/income/form")
def income_form():
    print("INCOME FORM...")
    return render_template("stocks_form.html")






@dashboard_routes.route("/income/dashboard", methods=["GET", "POST"])
def income_dashboard():
    print("INCOME DASHBOARD...")

    # if the form sends the data via POST request, we'll have request.form
    # otherwise if we specify url params in a GET request, we'll have request.args
    request_data = dict(request.form or request.args)
    print("REQUEST DATA:", request_data)




    try:
        
        symbol = request_data.get("symbol") or "MSFT"
        print("SYMBOL:", symbol)

        # your app can request data like this:
        request_url = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={ALPHAVANTAGE_API_KEY}"
        response = requests.get(request_url)
        data = json.loads(response.text)

        request_url = f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={symbol}&apikey={ALPHAVANTAGE_API_KEY}"
        response = requests.get(request_url)
        bs_data = json.loads(response.text)

        request_url = f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={symbol}&apikey={ALPHAVANTAGE_API_KEY}"
        response = requests.get(request_url)
        cf_data = json.loads(response.text)

        # pass this data to the page:
        #print(data)
        return render_template("income_dashboard.html", symbol=symbol, data=data, bs_data=bs_data, cf_data=cf_data)
        
    except Exception as err:
        print("ERROR", err)
        #flash("OOPS", "warning")
        return redirect("/stocks/form")