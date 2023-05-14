from os import environ
import openai


def smart(question, bank_info, upcoming_transactions):
    # Drop key "id" from all transactions

    for transaction in bank_info:
        transaction.pop("id", None)

    for transaction in upcoming_transactions:
        transaction.pop("id", None)

    # The date is in format: 2023-05-08T00: 00Z
    # Format it to: 2023-05-08

    for transaction in bank_info:
        transaction["date"] = transaction["date"].split("T")[0]

    for transaction in upcoming_transactions:
        if "date" in transaction:
            transaction["date"] = transaction["date"].split("T")[0]

    balance_month = {}
    total_balance = 0
    income = 0
    for transaction in bank_info:
        total_balance += transaction["amount"]
        income = max(income, transaction["amount"])
    
    balance_month["Total Balance"] = total_balance
    balance_month["Income"] = income
    openai.api_key = environ.get('OPENAI_API_KEY')
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[
        {"role": "system", "content": """
        You are an AI that can answer questions about bank transactions.
        You are connected to a bank account and can answer questions about the
        current balance and common transactions.
        You must answer succinctly and in plain English the questions asked.
        When the user asks about income, assume that the user is asking about his received revenue transactons of the month.
        The monthly income is the sum of all revenue transactions.
        If the user asks about his monthly income, you must answer the sum of all revenue transactions.
        Always make a guess, even if you are not sure about the answer.
        Try to be as helpful as possible, avoid saying "I don't know" or "I don't understand".
        Prefer to say "The most likely answer is X, but I'm not sure".
        Do not report negative numbers, only positive numbers.
        All values are in dollars.
        """},
        {"role": "system", "content": f"""
        Here is the current information about the bank account, in JSON format:
        {bank_info}\n\n
        Here is the current information about the upcoming transactions, in JSON format:
        {upcoming_transactions}\n\n

        And here is the current balance in JSON: {balance_month}.
        """},
        {"role": "user", "content": question}
    ])
    print(bank_info)
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content


if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()
    smart('What is the current balance?', 'Current balance: $1000')
