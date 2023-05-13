from os import environ
from fastapi import FastAPI
from dotenv import load_dotenv

from api_connector import BankUser

load_dotenv()
app = FastAPI()
bank = BankUser(environ.get('API_KEY'), environ.get('USER'))


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get('/transactions')
async def transactions():
    return [t.to_json() for t in bank.get_transactions()]

@app.get('/simplified/transaction')
async def transactions():
    result=[]
    for t in bank.get_transactions():
        t=t.to_json()
        result.append({"id":t["id"],"category":t["category"]["id"],"amount":t["amount"]["amount"],"date":t["date"]})
    return result

@app.get('/transactions/upcoming')
async def upcoming_transactions():
    return [t.to_json() for t in bank.get_upcoming_transactions()]


@app.get('/transactions/avg')
async def avg():
    if not bank.transactions:
        bank.get_transactions()
    return bank.calculate_avg()


@app.get('/transactions/month')
async def transactions_month():
    return bank.get_transactions_per_month()


@app.get('/transaction/{id}')
async def transaction(id: str):
    return bank.get_transaction(id).to_json()
