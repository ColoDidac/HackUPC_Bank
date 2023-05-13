import furl
import json
import requests
from calendar import monthrange
from datetime import datetime, timezone
from domain import Transaction
from exceptions import UnauthorizedError, NotFoundError, InternalServerError

from utils import calculate_all


class Client:
    BASE_URL = 'https://int.strandscloud.com/fs-api/'

    def __init__(self, api_key, user):
        self.session = requests.Session()
        self.session.headers.update({
            'accept': 'application/json',
            'x-api-key': api_key,
            'Authorization': 'Bearer ' + user})
        self.url = furl.furl(self.BASE_URL)

    API_OK = 200
    API_ERRORS_MAPPING = {
        403: UnauthorizedError,
        401: UnauthorizedError,
        400: NotFoundError,
        500: InternalServerError,
    }

    def request(self, endpoint):
        response = self.session.get(self.BASE_URL + endpoint)
        if response.status_code != self.API_OK:
            exception = self.API_ERRORS_MAPPING.get(
                response.status_code, Exception)
            raise exception
        return json.loads(response.text)

    def transactions(self):
        endpoint = 'transactions'
        data = self.client.request(endpoint)
        return [Transaction(t) for t in data['transactions']]

    def transaction(self, id):
        endpoint = f'transactions/{id}'
        return Transaction(self.client.request(endpoint))


def needs_transactions(func):
    def wrap(*args, **kwargs):
        args[0].get_transactions()
        result = func(*args, **kwargs)
        return result

    return wrap


class BankUser(Client):
    def __init__(self, api_key, user):
        self.client = Client(api_key, user)
        self.transactions = []
        self.simplified_transactions = []
        self.current_amount = 0
        self.debt = 0
        self.spend = 0
        self.salaries = 0
        self.avg_day_cost = 0
        self.upcoming_transactions = []

    def process_transaction(self, transaction):
        transaction = Transaction(transaction)
        self.current_amount += transaction.amount.amount
        return transaction

    def process_upcoming_transaction(self, transaction):
        transaction = Transaction(transaction)
        given_date = datetime.strptime(transaction.due_date, '%Y-%m-%dT%H:%M%z')
        today_date = datetime.now(timezone.utc)
        self.debt += (transaction.amount.amount if
                      given_date > today_date else self.debt)
        return transaction

    def get_transactions(self):
        endpoint = 'transactions'
        data = self.client.request(endpoint)
        self.transactions = [
            self.process_transaction(t) for t in data['transactions']]
        return self.transactions

    def get_clear_transactions(self):
        result = []
        for t in self.get_transactions():
            t = t.to_json()
            result.append(
                {"id": t["id"],
                 "category": t["category"]["id"],
                 "amount": t["amount"]["amount"],
                 "date": t["date"]})
        self.simplified_transactions = result
        return self.simplified_transactions

    def get_transaction(self, id):
        # Todo: If transactions is already filled search in transactions first
        endpoint = f'transactions/{id}'
        return Transaction(self.client.request(endpoint))

    def get_upcoming_transactions(self):
        endpoint = 'upcoming-transactions'
        data = self.client.request(endpoint)
        self.upcoming_transactions = [
            self.process_upcoming_transaction(t) for t in data[
                'upcomingTransactions']]
        return self.upcoming_transactions

    def status_bank_review(self):
        for transaction in self.simplified_transactions:
            self.current_amount += transaction["amount"]
            if transaction["category"] == 81:
                self.salaries += transaction["amount"]
            else:
                self.spend += transaction["amount"]

    @calculate_all
    def calculate_alert(self):
        current_month = datetime.now().month
        current_day = datetime.now().day
        current_year = datetime.now().year
        restant_days = monthrange(current_year, current_month)[1] - current_day
        print(restant_days)
        if self.salaries + self.debt + self.spend < 0:
            return "This Month your bills will be higher than your incomes."
        elif self.salaries + self.avg_day_cost * restant_days < 0:
            return f"You should try to decrease the daily " \
                   f"costs in order to be able to save some money." \
                   f"Currently you have {self.current_amount}"
        elif self.salaries + self.avg_day_cost < self.salaries * 0.3:
            return "You should try to decrease " \
                   "the daily costs in order to be able to " \
                   "save the 30% of your income."
        else:
            return f"Your month is going alright " \
                   f"with {self.salaries + self.spend} remaining, " \
                   f"currently you have still to pay {self.debt}." \
                   f"Your daily avg cost is {-self.avg_day_cost}. " \
                   f"I estimate you will finish this month with " \
                   f"{self.salaries + self.spend + self.debt + (restant_days * self.avg_day_cost)}"

    def calculate_avg(self):
        current_month = datetime.now().month
        month_amount = 0
        ##########
        # MODE 1 #
        #########
        for transaction in self.transactions:
            if int(transaction.date[5:7]
                   ) == current_month and transaction.amount.amount < 0:
                month_amount += transaction.amount.amount
        self.avg_day_cost += month_amount / datetime.now().day
        return self.avg_day_cost

        #################################
        #   MODE 2                     #
        #   DESDE DE QUE ES COBRA (CAT:80-81)    #
        ##############################
        """
        data_inicio_periodo=""
        for transaction in self.transactions:
            if transaction["category"] == 81:
                data_inicio_periodo=transaction["date"]
        """

    @needs_transactions
    def get_transactions_per_month(self):
        transactions_per_month = {"{:02d}".format(i): [] for i in range(1, 13)}
        for transaction in self.transactions:
            transactions_per_month[transaction.date[5:7]].append(transaction)
        return transactions_per_month
