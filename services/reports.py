import csv
from collections import defaultdict
from budgetbuddy.models.transaction import Transaction
from budgetbuddy.models.ledger import TransactionLedger

# ... (Previous aggregation functions from the last step)

def format_currency(amount):
    """Helper function to format a number as currency."""
    return f"${amount:,.2f}"

def format_monthly_summary(summary_data):
    """Formats the monthly summary data into a human-readable string."""
    income = summary_data['income']
    expenses = summary_data['expenses']
    net = summary_data['net_balance']
    
    report_text = "Monthly Summary\n"
    report_text += "------------------\n"
    report_text += f"Total Income:  {format_currency(income):>10}\n"
    report_text += f"Total Expenses:{format_currency(expenses):>10}\n"
    report_text += f"Net Balance:   {format_currency(net):>10}\n"
    return report_text

def format_spend_by_category_report(category_spend, budgets):
    """Formats the spend by category data into a human-readable table."""
    report_text = "Spend by Category\n"
    report_text += "-----------------------------------------\n"
    report_text += f"{'Category':<15}{'Spent':>10}{'Budget':>10}{'Variance':>10}\n"
    report_text += f"{'-'*15:<15}{'-'*10:>10}{'-'*10:>10}{'-'*10:>10}\n"

    for category, spent in category_spend.items():
        budget = budgets.get(category, 0)
        variance = budget - spent
        report_text += f"{category:<15}{format_currency(spent):>10}{format_currency(budget):>10}{format_currency(variance):>10}\n"
    
    return report_text

def format_top_merchants_report(top_merchants_list):
    """Formats the top merchants data into a numbered list."""
    report_text = "Top Merchants\n"
    report_text += "------------------\n"
    for i, (merchant, spent) in enumerate(top_merchants_list, 1):
        report_text += f"{i}. {merchant:<15}{format_currency(spent):>10}\n"
    return report_text

def export_category_csv(category_spend, budgets, filepath):
    """Exports the spend by category report to a CSV file."""
    try:
        with open(filepath, 'w', newline='') as file:
            writer = csv.writer(file)
            # Write the header row
            writer.writerow(['Category', 'Total Spent', 'Budget', 'Variance'])
            
            # Write the data rows
            for category, spent in category_spend.items():
                budget = budgets.get(category, 0)
                variance = budget - spent
                writer.writerow([category, spent, budget, variance])
        print(f"Successfully exported category spend report to {filepath}.")
    except Exception as e:
        print(f"An error occurred while exporting the CSV: {e}")

def spend_by_category(ledger):
    """
    Aggregates total spending for each category in the ledger.
    Returns a dictionary of {category: total_spend}.
    """
    category_spend = defaultdict(float)
    for transaction in ledger:
        if transaction.amount < 0:
            category_spend[transaction.category] += abs(transaction.amount)
    return dict(category_spend)

def top_merchants(ledger, top_n):
    """
    Identifies the top N merchants by total spending.
    Returns a sorted list of (merchant, total_spend) tuples.
    """
    merchant_spend = defaultdict(float)
    for transaction in ledger:
        if transaction.amount < 0:
            merchant_spend[transaction.merchant.lower().strip()] += abs(transaction.amount)

    sorted_merchants = sorted(merchant_spend.items(), key=lambda item: item[1], reverse=True)
    return sorted_merchants[:top_n]

def monthly_summary(ledger):
    """
    Calculates total income, expenses, and net balance for the ledger.
    Returns a dictionary with these values.
    """
    total_income = 0
    total_expenses = 0

    for transaction in ledger:
        if transaction.amount > 0:
            total_income += transaction.amount
        else:
            total_expenses += transaction.amount
    
    net_balance = total_income + total_expenses
    
    return {
        'income': total_income,
        'expenses': abs(total_expenses),  # Stored as a positive number for display
        'net_balance': net_balance
    }