from os import environ
import openai


def smart(question, bank_info):
    openai.api_key = environ.get('OPENAI_API_KEY')
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[
        {"role": "system", "content": """
        You are an AI that can answer questions about bank transactions.
        You are connected to a bank account and can answer questions about the
        current balance and common transactions.
        You must answer succinctly and in plain English the questions asked.
        """},
        {"role": "system", "content": f"""
        Here is the current information about the bank account, with his categories and the amount:
        {bank_info}
        """},
        {"role": "user", "content": question}
    ])
    print(completion.choices[0].message.content)
    return 'I am too dumb to answer that question.'


if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()
    smart('What is the current balance?', 'Current balance: $1000')
