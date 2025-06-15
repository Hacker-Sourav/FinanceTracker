import csv
import os

from flask import Flask, render_template, request
from flask import redirect, url_for, flash

app = Flask(__name__)

app.secret_key = 'your_secret_key'  # required for flash messages

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

    flash('Transaction added successfully!')
    return redirect('/')



@app.route('/delete', methods=['POST'])
def delete_transaction():
    target={
        'Date': request.form['date'],
        'Description': request.form['description'],
        'Category': request.form['category'],
        'Amount': request.form['amount'],
        'Type': request.form['type']
    }

    file_path = os.path.join('data', 'transactions.csv')
    transactions= []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row != target:
                transactions.append(row)
        
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Date', 'Description', 'Category', 'Amount', 'Type'])
        writer.writeheader()
        writer.writerows(transactions)

    flash('Transaction deleted successfully!')
    return redirect('/')


@app.route('/edit', methods=['GET', 'POST'])
def edit_transaction():
    file_path = os.path.join('data', 'transactions.csv')
    index = int(request.args.get('index'))

    with open(file_path, 'r') as file:
        reader=list(csv.DictReader(file))
        header=reader[0].keys()
        transaction=reader[index]

    return render_template('edit.html', index=index, transaction=transaction, header=header)


@app.route('/update', methods=['POST'])
def update_transaction():
    index=int(request.form['index'])
    file_path=os.path.join('data', 'transactions.csv')

    with open(file_path, 'r') as file:
        reader=list(csv.DictReader(file))
        fieldnames=reader[0].keys()
        data=list(reader)

    for field in fieldnames:
        data[index][field]=request.form[field]

    with open(file_path, 'w', newline='') as file:
        writer=csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    flash("Transaction updated successfully!")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
