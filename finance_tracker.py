import os
import csv
import json
from fpdf import FPDF
from datetime import datetime
import matplotlib.pyplot as plt
import time

DATA_FILE = "transactions.json"

def load_transactions() -> list:
  if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as file:
      return json.load(file)
  return []

def save_transactions(transactions:list):
  with open(DATA_FILE, "w") as file:
    json.dump(transactions, file, indent=4)

def add_transaction(transactions):
  try:
    date = input("Enter date (YYYY-MM-DD): ")
    datetime.strptime(date, "%Y-%m-%d")  # Validate date format
  except ValueError:
    print("Invalid date format. Please use YYYY-MM-DD.")
    return
  
  category = input("Enter category (e.g., Food, Rent, Salary): ").capitalize()
  try:
    amount = float(input("Enter amount (positive for income, negative for expense): "))
  except ValueError:
    print("Invalid amound. Only numbers please.")
    return

  description = input("Enter description: ")
  transactions.append({
    "date": date,
    "category": category,
    "amount": amount,
    "description": description
  })
  save_transactions(transactions)
  print("Transaction added successfully!")

def generate_summary(transactions:list) -> dict:
  monthly_summary = {}
  for transaction in transactions:
    month = transaction["date"][:7]  # Extract YYYY-MM
    if month not in monthly_summary:
      monthly_summary[month] = {"income": 0, "expenses": 0, "balance": 0}
    if transaction["amount"] > 0:
      monthly_summary[month]["income"] += transaction["amount"]
    else:
      monthly_summary[month]["expenses"] += abs(transaction["amount"])
    monthly_summary[month]["balance"] = monthly_summary[month]["income"] - monthly_summary[month]["expenses"]
  return monthly_summary

def display_summary(summary:dict):
  for month, data in summary.items():
    print(f"Month: {month}")
    print(f"  Income: ${data['income']:.2f}")
    print(f"  Expenses: ${data['expenses']:.2f}")
    print(f"  Balance: ${data['balance']:.2f}")

def generate_pdf_report(transactions:list):
  pdf = FPDF()
  pdf.add_page()
  pdf.set_font("Arial", size=12)
  pdf.cell(200, 10, txt="Finance Tracker Report", ln=True, align='C')
  pdf.cell(200, 10, txt="Transactions:", ln=True)
  
  for transaction in transactions:
    pdf.cell(200, 10, txt=f"{transaction['date']} - {transaction['category']} - ${transaction['amount']:.2f} - {transaction['description']}", ln=True)
  
  pdf_file = os.path.join(r"C:\Users\HP\Desktop\Dumb Projects\Python", "transactions_report.pdf")
  pdf.output(pdf_file)
  print(f"PDF report generated: {pdf_file}")

def generate_csv_report(transactions:list):
  csv_file = os.path.join(r"C:\Users\HP\Desktop\Dumb Projects\Python", "transactions_report.csv")
  with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Date", "Category", "Amount", "Description"])
    for transaction in transactions:
      writer.writerow([transaction["date"], transaction["category"], transaction["amount"], transaction["description"]])
  print(f"CSV report generated: {csv_file}")

def generate_pie_chart(transactions: list):
  categories = {}
  for transaction in transactions:
    if transaction["amount"] < 0:
      categories[transaction["category"]] = categories.get(transaction["category"], 0) + abs(transaction["amount"])

  if categories:
    plt.figure(figsize=(9, 7))
    wedges, texts, autotexts = plt.pie(
      categories.values(),
      labels=categories.keys(),
      autopct='%1.1f%%',
      startangle=140,
      pctdistance=0.85,
      colors=plt.cm.Pastel1.colors,
      wedgeprops=dict(width=0.4, edgecolor='w')
    )
    # Draw circle for donut effect
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    plt.gca().add_artist(centre_circle)

    plt.title("Spending per Category", fontsize=16, fontweight='bold')
    plt.legend(wedges, categories.keys(), title="Categories", loc="center left", bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.show()
  else:
    print("No expenses to visualize.")

if __name__ == "__main__":
  transactions = load_transactions()

  while True:
    print("Welcome to the Finance Tracker!")
    print("1. Add Transaction") 
    print("2. Generate Monthly Summary")
    print("3. Generate PDF Report")
    print("4. Generate CSV Report")
    print("5. Generate Pie Chart")
    print("6. Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
      add_transaction(transactions)
    elif choice == "2":
      sum = 0
      for i in range(10000):
        start = time.time_ns()
        summary = generate_summary(transactions)
        end = time.time_ns()
        duration = end - start
        sum += duration
      print(f"Time taken to generate summary: {(sum / 10000) / 1000} ms")
      display_summary(summary)
    elif choice == "3":
      generate_pdf_report(transactions)
    elif choice == "4":
      generate_csv_report(transactions)
    elif choice == "5":
      generate_pie_chart(transactions)
    elif choice == "6":
      print("Exiting the Finance Tracker. Goodbye!")
      break
    else:
      print("Invalid choice. Please try again.")
