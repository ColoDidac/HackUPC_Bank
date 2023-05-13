from os import environ
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv

from api_connector import BankUser

json_exclude = {'_data'}

load_dotenv()
app = FastAPI()
bank = BankUser(environ.get('API_KEY'), environ.get('USER'))


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get('/transactions')
async def transactions():
    return jsonable_encoder(bank.get_transactions(), exclude=json_exclude)

@app.get('/simplified/transaction')
async def simplify_transaction():
    return bank.get_clear_transactions()

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
