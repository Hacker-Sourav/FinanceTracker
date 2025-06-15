import csv
import os

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    transactions = []
    total_income=0
    total_expense=0

    file_path = os.path.join('data', 'transactions.csv')
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            reader=csv.DictReader(file)
            for row in reader:
                transactions.append(row)
                amount = float(row['Amount'])
                if row['Type'] == 'Income':
                    total_income+=amount
                elif row['Type'] == 'Expense':
                    total_expense+=amount
                
    balance = total_income-total_expense

    return render_template('index.html', transactions=transactions, total_income=total_income, total_expense=total_expense, balance=balance)

@app.route('/add', methods=['POST'])
def add_transaction():
    date = request.form['date']
    description=request.form['description']
    category=request.form['category']
    amount=request.form['amount']
    txn_type = request.form['type']

    file_path = os.path.join('data', 'transactions.csv')

    file_exists=os.path.isfile(file_path)

    with open(file_path, 'a', newline='') as file:
        writer=csv.writer(file)
        if not file_exists:
            writer.writerow(['Date', 'Description', 'Category', 'Amount', 'Type'])
        writer.writerow([date, description, category, amount, txn_type])


    return "Transaction saved successfully!"

if __name__ == '__main__':
    app.run(debug=True)
