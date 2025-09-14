# BudgetBuddy — A CLI Expense Tracker & Budget Analyzer

BudgetBuddy is a command-line application that helps you track your expenses, manage budgets, and generate financial reports.

## Features
- **Transaction Import:** Load bank transactions from CSV files.
- **Auto-Categorization:** Automatically categorize transactions using a set of keyword rules.
- **Budget Management:** Set and track monthly budgets for different categories.
- **Reporting:** Generate textual reports for monthly summaries, spend by category, and top merchants.
- **Data Persistence:** Store budgets and rules in JSON files for easy access.

## Setup

### Prerequisites
- Python 3.7 or higher

### Installation
1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd budgetbuddy
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On macOS/Linux
    source venv/bin/activate
    # On Windows
    venv\Scripts\activate
    ```

## How to Run

Navigate to the project's root directory (the one containing the `budgetbuddy` folder) and run the application as a module.

```bash
python -m budgetbuddy.main