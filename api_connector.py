import os
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv


class BankUser:
    def __init__(self, num_client):
        load_dotenv()
        self.client_id = num_client
        self.token = os.getenv(f'USER{num_client}_TOKEN')
        self.transactions = []
        self.current_amount = 0
        self.debt = 0
        self.upcoming_transactions = []

    def get_transactions(self):
        url = "https://int.strandscloud.com/fs-api/transactions?recoverHeatLevel=false&page=0&size=50&sort=DATE_DESC&applyToSplits=false"
        headers = {
            "accept": "application/json",
            "x-api-key": "5brZ6as5Qj3AhS2rzeedm8VGxUBTlMSD8YQsyxz3",
            "Authorization": f"bearer {self.token}"
        }
        response = requests.get(url, headers=headers)
        for element in response.json()["transactions"]:
            self.current_amount += element["amount"]["amount"]
            self.transactions.append({"id": element["id"],
                                      "category":element["category"]["id"],
                                      "amount": element["amount"],
                                      "date": element["date"]})
        print(self.client_id)
        print(self.transactions)
        print(self.current_amount)

    def get_upcoming_transactions(self):
        url = "https://int.strandscloud.com/fs-api/upcoming-transactions?recoverHeatLevel=false&page=0&size=50&sort=DUE_DATE_DESC"
        headers = {
            "accept": "application/json",
            "x-api-key": "5brZ6as5Qj3AhS2rzeedm8VGxUBTlMSD8YQsyxz3",
            "Authorization": f"bearer {self.token}"
        }
        response = requests.get(url, headers=headers)
        for transaction in response.json()["upcomingTransactions"]:
            self.upcoming_transactions.append({
                "transaction": transaction["name"],
                "amount": transaction["amount"],
                "dueDate": transaction["dueDate"],
            })
            given_date = datetime.strptime(transaction["dueDate"], '%Y-%m-%dT%H:%M%z')
            today_date = datetime.now(timezone.utc)
            self.debt += transaction["amount"]["amount"] if given_date > today_date else self.debt
        print(self.upcoming_transactions)
        print(self.debt)

    def calculate_alert(self):
        print()

    def calculate_avg(self):
        current_month = datetime.now().month
        month_amount = 0
        ##########
        # MODE 1 #
        #########
        for transaction in self.transactions:
            date_transaction = transaction["date"]
            if int(date_transaction[5:7]) == current_month and transaction["amount"]["amount"] < 0:
                month_amount += transaction["amount"]["amount"]
        print(month_amount / datetime.now().day)

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
if __name__ == '__main__':
    for client in range(5):
        client_bank = BankUser(client)
        client_bank.get_transactions()
        # client_bank.get_upcoming_transactions()
        # client_bank.calculate_alert()
        client_bank.calculate_avg()
