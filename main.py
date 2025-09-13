from budgetbuddy.services.importer import import_transactions

def main_menu():
    while True:
        print("\nBudgetBuddy CLI Menu")
        print("1. Import Transactions")
        print("2. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            filepath = './data/sample_transactions.csv'
            transactions = import_transactions(filepath)
            if transactions:
                print(f"Successfully imported {len(transactions)} transactions.")
            # You can add more logic here, like storing the transactions in a ledger
            
        elif choice == '2':
            print("Exiting BudgetBuddy. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()