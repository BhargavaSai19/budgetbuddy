import os
import sys
import json
from datetime import datetime

from budgetbuddy.services.importer import import_transactions
from budgetbuddy.services.storage import load_json, save_json
from budgetbuddy.services.categorize import assign_category
from budgetbuddy.services.reports import (
    monthly_summary,
    spend_by_category,
    top_merchants,
    format_monthly_summary,
    format_spend_by_category_report,
    format_top_merchants_report,
    export_category_csv
)
from budgetbuddy.models.ledger import TransactionLedger

def main_menu():
    """Main function to run the BudgetBuddy CLI."""
    ledger = TransactionLedger()
    
    # Load budgets and rules on startup
    budgets = load_json('./data/budgets.json')
    rules = load_json('./data/rules.json')

    while True:
        print("\nBudgetBuddy Main Menu")
        print("--------------------")
        print("1. Load Transactions from CSV")
        print("2. Manage Budgets")
        print("3. Generate Reports")
        print("4. Search Transactions")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            filepath = input("Enter the path to the CSV file (e.g., data/sample_transactions.csv): ")
            if not os.path.exists(filepath):
                print("Error: File not found. Please try again.")
                continue

            transactions = import_transactions(filepath)
            
            # Categorize and add to ledger
            if transactions:
                for transaction in transactions:
                    categorized_transaction = assign_category(transaction, rules)
                    ledger.add_transaction(categorized_transaction)
                print(f"Successfully loaded and categorized {len(transactions)} transactions.")
            else:
                print("No transactions loaded. The file might be empty or in an incorrect format.")

        elif choice == '2':
            # Manage Budgets Submenu
            print("\nManage Budgets")
            print("1. Set/Update a Budget")
            print("2. View Current Budgets")
            budget_choice = input("Enter your choice: ")
            
            if budget_choice == '1':
                month_key = input("Enter month (YYYY-MM): ")
                category = input("Enter category: ")
                try:
                    amount = float(input("Enter budget amount: "))
                    if month_key not in budgets:
                        budgets[month_key] = {}
                    budgets[month_key][category] = amount
                    save_json(budgets, './data/budgets.json')
                except ValueError:
                    print("Invalid amount. Please enter a number.")
            elif budget_choice == '2':
                if budgets:
                    print(json.dumps(budgets, indent=4))
                else:
                    print("No budgets have been set yet.")
            else:
                print("Invalid choice.")
        
        elif choice == '3':
            # Generate Reports Submenu
            print("\nGenerate Reports")
            print("1. Monthly Summary")
            print("2. Spend by Category")
            print("3. Top Merchants")
            report_choice = input("Enter your choice: ")
            
            if not ledger.transactions:
                print("No transactions loaded. Please import a CSV file first.")
                continue

            month_key_str = input("Enter month to report on (YYYY-MM): ")
            try:
                year, month = map(int, month_key_str.split('-'))
            except ValueError:
                print("Invalid month format. Please use YYYY-MM.")
                continue

            filtered_ledger = ledger.filter_by_month(year, month)
            if not filtered_ledger.transactions:
                print("No transactions found for the specified month.")
                continue

            if report_choice == '1':
                summary = monthly_summary(filtered_ledger)
                report = format_monthly_summary(summary)
                print(report)
                
            elif report_choice == '2':
                category_spend_data = spend_by_category(filtered_ledger)
                monthly_budgets = budgets.get(month_key_str, {})
                report = format_spend_by_category_report(category_spend_data, monthly_budgets)
                print(report)
                
                export_choice = input("Export to CSV? (y/n): ").lower()
                if export_choice == 'y':
                    filepath = f"./outputs/reports/category_spend_{month_key_str}.csv"
                    export_category_csv(category_spend_data, monthly_budgets, filepath)

            elif report_choice == '3':
                try:
                    n = int(input("Enter the number of top merchants to display: "))
                    top_merchants_data = top_merchants(filtered_ledger, n)
                    report = format_top_merchants_report(top_merchants_data)
                    print(report)
                except ValueError:
                    print("Invalid input. Please enter a number.")
            
            else:
                print("Invalid report choice.")

        elif choice == '4':
            # Search Transactions
            query = input("Enter search query (text, category): ").lower()
            
            filtered_ledger = TransactionLedger()
            
            # Simple check to see if the query is a date
            try:
                datetime.strptime(query, '%Y-%m-%d')
                year, month, day = map(int, query.split('-'))
                filtered_ledger.transactions = [t for t in ledger.transactions if t.date == datetime(year, month, day).date()]
            except ValueError:
                # If not a date, perform a text or category search
                filtered_ledger = ledger.search_by_text(query)
                if not filtered_ledger.transactions:
                    filtered_ledger = ledger.filter_by_category(query)

            if filtered_ledger.transactions:
                print(f"Found {len(filtered_ledger.transactions)} matching transactions:")
                for t in filtered_ledger.transactions:
                    print(f"Date: {t.date} | Merchant: {t.merchant} | Amount: {t.amount} | Category: {t.category}")
            else:
                print("No matching transactions found.")

        elif choice == '5':
            print("Exiting BudgetBuddy. Goodbye!")
            sys.exit(0) # Use sys.exit() for a clean exit
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    # Ensure the reports directory exists before trying to save files
    os.makedirs("./outputs/reports", exist_ok=True)
    main_menu()