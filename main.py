from api_connector import BankUser
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from os import environ
from dotenv import load_dotenv
from urllib.parse import unquote
from smart import smart

json_exclude = {'_data'}

load_dotenv()
app = FastAPI()
bank = BankUser(environ.get('API_KEY'), environ.get('USER_KEY'))


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get('/transactions')
async def transactions():
    return jsonable_encoder(bank.get_transactions(), exclude=json_exclude)


@app.get('/simplified/transaction')
async def simplify_transaction():
    transactions = bank.get_clear_transactions()
    traduct_dict={}
    for t in transactions:
        if t["category"] not in traduct_dict.keys():
            traduct_dict[t["category"]]=t["amount"]
        else:
            traduct_dict[t["category"]] += t["amount"]

    result=f'From your revenues of {traduct_dict["Revenues"]}.You have spend a total of'
    for key in traduct_dict.keys():
        if key != 'Revenues':
            result=f'{result} {round(-1*traduct_dict[key])} dolars on {key}.'
    return result


@app.get('/consultai/{question}')
async def simplify_transaction(encoded_question):
    transactions_list = bank.get_clear_transactions()
    decoded_question = encoded_question.encode("utf-8").decode("base64")
    return smart(question, transactions_list)


@app.get('/alerts')
async def alerts():
    return bank.calculate_alert()


@app.get('/transactions/upcoming')
async def upcoming_transactions():
    return jsonable_encoder(bank.get_upcoming_transactions(),
                            exclude=json_exclude)


@app.get('/transactions/avg')
async def avg():
    if not bank.transactions:
        bank.get_transactions()
    return bank.calculate_avg()


@app.get('/transactions/month')
async def transactions_month():
    return jsonable_encoder(bank.get_transactions_per_month(),
                            exclude=json_exclude)


@app.get('/transactions/month/amount')
async def transactions_month_amount():
    monthly_transactions = bank.get_transactions_per_month()
    monthly_totals = {}
    for month in monthly_transactions:
        monthly_totals[month] = sum([
            t.amount.amount for t in monthly_transactions[month]])
    return jsonable_encoder(monthly_totals)


@app.get('/transaction/{id}')
async def transaction(id: str):
    return bank.get_transaction(id).to_json()


@app.get('/transactions/month/current')
async def transaction_month_current():
    month_status = bank.get_month_status()
    text = f"Current month status: {month_status['total_month']}, "
    if month_status['total_month'] > month_status['total_previous_month']:
        text += "which is %s more than last month." % (
                month_status['total_month'] - month_status['total_previous_month'])
    elif month_status['total_month'] < month_status['total_previous_month']:
        text += "which is %s less than last month." % (
                month_status['total_previous_month'] - month_status['total_month'])
    return text
