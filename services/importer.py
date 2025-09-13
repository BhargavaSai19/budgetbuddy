import csv
from datetime import datetime
from budgetbuddy.models.transaction import Transaction

def import_transactions(filepath):
    transactions = []
    try:
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            # Assuming the first row is a header, skip it.
            # If your CSV has no header, you can remove this line.
            header = next(reader)
            print(f"Importing transactions with columns: {', '.join(header)}")
            
            for row in reader:
                try:
                    # Unpack the row. Adjust if your CSV has a different number of columns.
                    date_str, merchant, amount_str = row
                    
                    # Convert string to datetime.date object
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                    
                    # Convert string to float
                    amount_float = float(amount_str)
                    
                    # Create the Transaction object
                    transaction = Transaction(
                        date=date_obj,
                        merchant=merchant,
                        amount=amount_float,
                        category='',  # Placeholder for later categorization
                        raw=tuple(row)
                    )
                    transactions.append(transaction)
                    
                except (ValueError, IndexError) as e:
                    print(f"Skipping invalid row: {row}. Error: {e}")
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
    return transactions