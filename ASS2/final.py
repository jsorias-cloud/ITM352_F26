# Had an error regarding pandas, so I used Copilot to check my download for pandas and it suggested the following code. I also added a try/except block to catch the error and provide a helpful message to the user.
try:
    import pandas as pd
except ModuleNotFoundError as error:
    if error.name != "pandas":
        raise
    raise SystemExit(
        "Missing dependency: pandas. From the project folder, run "
        "'python -m pip install -r requirements.txt'."
    ) from error

import ssl
import time
 
# Name: Jorryn Skye Orias
# Assignment 2: Sales Data Dashboard
# Individual requirements: #7 (date range before each analysis) and #10 (store and show results)
 
#Temporary fix
ssl._create_default_https_context = ssl._create_unverified_context

# Requirement 10: every pivot table that is produced is stored here (name -> pivot table).
# The name has a running number, the task and the date range, so running the same task for two date ranges keeps both results.

analytics_history = {}
 
# Fields offered by the custom pivot table. Only the ones in the data file are shown.
group_fields = ["employee_name", "job_title", "sales_region", "order_type",
                "customer_type", "customer_state", "product_category", "produce_name"]
value_fields = ["quantity", "unit_price", "sales"]
 
# Load the file while measuring load time, prints # of rows, list of columns, replaces missing values with 0
def load_csv(filepath):
    print(f"Loading CSV file from: {filepath}")
    print("Please wait, loading...")
    start_time = time.time()
 
    try:
        # on_bad_lines='skip' drops malformed lines instead of failing
        df = pd.read_csv(filepath, on_bad_lines='skip')
    except Exception as e:
        print("Error reading the CSV file:", e)
        return None
 
    if df.empty:
        print("Error: the file was read but it contains no rows of data.")
        return None
 
    end_time = time.time()
    load_time = end_time - start_time
    print(f"CSV file loaded successfully in {load_time:.2f} seconds.")
    print(f"Number of rows: {len(df)}")
    print(f"List of columns: {list(df.columns)}")
 
    df, replaced = replace_missing_with_zeros(df)
    if replaced:
        print(f"{replaced} missing values were replaced with zeros.")
 
    # fields the analytics need
    required_fields = [
        "sales_region", "order_type", "unit_price", "quantity",
        "customer_type", "employee_id", "product_category",
        "order_date", "customer_state"
    ]
    missing_fields = [field for field in required_fields if field not in df.columns]
    if len(missing_fields) == len(required_fields):
        print("Error: none of the expected sales fields were found, so this is not the sales data.")
        return None
    if missing_fields:
        print(f"Warning: Missing fields {missing_fields}. Some analytics may not work.")
    else:
        print("All required fields are present.")
 
    return prepare_data(df)
 
 
# Text columns get "0" because a number cannot be stored in a text column
def replace_missing_with_zeros(df):
    df = df.copy()
    replaced = int(df.isna().sum().sum())
    number_columns = df.select_dtypes(include="number").columns
    other_columns = df.select_dtypes(exclude="number").columns
    df[number_columns] = df[number_columns].fillna(0)
    df[other_columns] = df[other_columns].fillna("0")
    return df, replaced
 
 
# Prepares the data for the analytical tasks:
# Converts quantity and unit_price into numeric values.
# Converts order_date into a date format for date filtering.
# Calculates total sales using quantity * unit_price.

def prepare_data(df):
    df = df.copy()
 
    for column in ["quantity", "unit_price"]:
        if column in df.columns:
            numbers = pd.to_numeric(df[column], errors="coerce")
            bad = int(numbers.isna().sum())
            if bad:
                print(f"Warning: {bad} unreadable values in '{column}' were set to 0.")
            df[column] = numbers.fillna(0)
 
    if "quantity" in df.columns and "unit_price" in df.columns:
        df["sales"] = df["quantity"] * df["unit_price"]
 
    if "order_date" in df.columns:
        dates = pd.to_datetime(df["order_date"], format="mixed", dayfirst=True, errors="coerce")
        bad = int(dates.isna().sum())
        if bad:
            print(f"Warning: {bad} rows have an unreadable 'order_date'. "
                  "They are only used when no date range is chosen.")
        df["order_date"] = dates
 
    return df
 
 
# Stops a task with a message if the data does not have the columns it needs
def has_columns(data, needed):
    missing = [column for column in needed if column not in data.columns]
    if missing:
        print(f"\nCannot run this task. Missing columns: {', '.join(missing)}")
        return False
    return True
 
 
# Prints a pivot table so wide or long tables are not cut off
def print_pivot(pivot):
    with pd.option_context("display.width", 200, "display.max_columns", None,
                           "display.max_rows", None,
                           "display.float_format", "{:,.2f}".format):
        print(pivot)
 
 
# Requirement 10: prints a result and stores it in analytics_history

def show_and_save_result(name, pivot, date_label):
    assert isinstance(pivot, pd.DataFrame)
    key = f"{len(analytics_history) + 1}. {name} [{date_label}]"
    analytics_history[key] = pivot
 
    print(f"\n=== {name} ===")
    print(f"Date range: {date_label}")
    print_pivot(pivot)
    print(f"\n(Saved as result #{len(analytics_history)})")
 
 
# Requirement 7: asks for one date (YYYY-MM-DD). Enter returns None.
def prompt_for_date(prompt):
    while True:
        text = input(prompt).strip()
        if text == "":
            return None
        try:
            return pd.to_datetime(text, format="%Y-%m-%d")
        except ValueError:
            print(f"Invalid date '{text}'. Please use the format YYYY-MM-DD, for example 2026-09-11.")
 
 
# Requirement 7: asks which dates to analyze and returns (rows in that range, text for the range).
# Enter at both prompts uses every row. A blank start means "from the earliest order" and a blank end means "to the latest order". The end date is included.

def choose_date_range(data):
    assert isinstance(data, pd.DataFrame)
    if "order_date" not in data.columns or data["order_date"].isna().all():
        print("There are no usable order dates, so all rows will be used.")
        return data, "all dates"
 
    earliest = data["order_date"].min()
    latest = data["order_date"].max()
    print(f"\nOrders are available from {earliest:%Y-%m-%d} to {latest:%Y-%m-%d}.")
    print("Enter the dates to analyze (YYYY-MM-DD). Press Enter to skip a date.")
 
    while True:
        start = prompt_for_date("Start date (Enter = earliest): ")
        end = prompt_for_date("End date (Enter = latest): ")
        if start is None and end is None:
            return data, "all dates"
        if start is None:
            start = earliest
        if end is None:
            end = latest
        if start > end:
            print("The start date cannot be after the end date. Please try again.")
            continue
        break
    
    # Used claude to help me with this part of the code (lines 180-184). I was having trouble coding with the date range.
 
    label = f"{start:%Y-%m-%d} to {end:%Y-%m-%d}"
    in_range = data[(data["order_date"] >= start) & (data["order_date"] <= end)]
    if in_range.empty:
        print(f"\nThere are no sales in the date range {label}. Nothing to analyze.")
    return in_range, label
 
 
# Analytical task #1
def display_initial_rows(data):
    total_rows = len(data)
    print("\nEnter rows to display:")
    print(f"- Enter a number 1 to {total_rows}")
    print("- To see all rows, enter 'all'")
    print("- To skip preview, press Enter")
 
    while True:
        response = input("Your choice: ").strip().lower()
 
        if response == "":
            print("Skipping initial rows display.")
            return
 
        if response == "all":
            num_rows = total_rows
        else:
            try:
                num_rows = int(response)
            except ValueError:
                print(f"Invalid input '{response}'. Please enter a whole number, 'all', or press Enter to skip.")
                continue
            if num_rows < 1 or num_rows > total_rows:
                print(f"Please enter a number from 1 to {total_rows}.")
                continue
 
        with pd.option_context("display.width", 250, "display.max_columns", None,
                               "display.max_rows", None):
            print(data.head(num_rows))
        return
 
 
# Analytical task #2
def total_sales_by_region_order_type(data):
    if not has_columns(data, ["sales_region", "order_type", "sales"]):
        return
    data, date_label = choose_date_range(data)
    if data.empty:
        return
    pivot = pd.pivot_table(data, index="sales_region", columns="order_type",
                           values="sales", aggfunc="sum", fill_value=0,
                           margins=True, margins_name="Total")
    show_and_save_result("Total sales by region and order type", pivot, date_label)
 
 
# Analytical task #3
def average_sales_by_region(data):
    if not has_columns(data, ["sales_region", "customer_state", "order_type", "sales"]):
        return
    data, date_label = choose_date_range(data)
    if data.empty:
        return
    pivot = pd.pivot_table(data, index="sales_region",
                           columns=["customer_state", "order_type"],
                           values="sales", aggfunc="mean", fill_value=0)
    show_and_save_result("Average sales by region, by state and sale type", pivot, date_label)
 
 
# Analytical task #4
def sales_by_customer_type(data):
    if not has_columns(data, ["customer_state", "customer_type", "order_type", "sales"]):
        return
    data, date_label = choose_date_range(data)
    if data.empty:
        return
    pivot = pd.pivot_table(data, index=["customer_state", "customer_type", "order_type"],
                           values="sales", aggfunc="sum", fill_value=0)
    show_and_save_result("Sales by customer type and order type by state", pivot, date_label)
 
 
# Analytical task #5
# "Product" is the product_category column (3 values) because the 67 individual products
# would make the table too long to read.

def total_sales_quantity_price_by_region_product(data):
    if not has_columns(data, ["sales_region", "product_category", "quantity", "sales"]):
        return
    data, date_label = choose_date_range(data)
    if data.empty:
        return
    pivot = pd.pivot_table(data, index=["sales_region", "product_category"],
                           values=["quantity", "sales"], aggfunc="sum", fill_value=0)
    show_and_save_result("Total sales quantity and price by region and product", pivot, date_label)
 
 
# Analytical task #6
def total_sales_quantity_price_customer_type(data):
    if not has_columns(data, ["order_type", "customer_type", "quantity", "sales"]):
        return
    data, date_label = choose_date_range(data)
    if data.empty:
        return
    pivot = pd.pivot_table(data, index=["order_type", "customer_type"],
                           values=["quantity", "sales"], aggfunc="sum", fill_value=0)
    show_and_save_result("Total sales quantity and price by customer type", pivot, date_label)
 
 
# Analytical task #7
# "Sales price" can mean the price of one unit or the amount of one sale, so both are shown:
# unit_price and sales (quantity * unit_price).

def max_min_sales_price_by_category(data):
    if not has_columns(data, ["product_category", "unit_price", "sales"]):
        return
    data, date_label = choose_date_range(data)
    if data.empty:
        return
    pivot = pd.pivot_table(data, index="product_category", values=["unit_price", "sales"],
                           aggfunc=["max", "min"], fill_value=0)
    show_and_save_result("Max and min sales price of sales by category", pivot, date_label)
 
 
# Analytical task #8
# Employees are counted by employee_id so two people with the same name are not merged.
def unique_employees_by_region(data):
    if not has_columns(data, ["sales_region", "employee_id"]):
        return
    data, date_label = choose_date_range(data)
    if data.empty:
        return
    pivot = pd.pivot_table(data, index="sales_region", values="employee_id",
                           aggfunc="nunique", fill_value=0)
    pivot = pivot.rename(columns={"employee_id": "unique_employees"})
    show_and_save_result("Number of unique employees by region", pivot, date_label)
 
 
def get_user_selection(options, prompt, required=False, single=False):
    assert len(options) > 0, "get_user_selection needs at least one option"
    while True:
        print(prompt)
        for i, option in enumerate(options):
            print(f"{i+1}. {option}")
 
        choice = input("Enter the number(s) of your choice(s), separated by commas: ").strip()
        if not choice:
            if required:
                print("A selection is required.")
                continue
            return []
 
        try:
            indexes = [int(i) for i in choice.split(',')]
        except ValueError:
            print("Invalid input. Please enter numbers separated by commas.")
            continue
 
        if any(i < 1 or i > len(options) for i in indexes):
            print(f"Each number must be between 1 and {len(options)}.")
            continue
 
        selected = list(dict.fromkeys(options[i - 1] for i in indexes))
        if single and len(selected) != 1:
            print("Please select exactly one option.")
            continue
        return selected
 
 
# Analytical task #9
# The choices are made first and the date range second, so the saved name can describe
# exactly what was built (this is how custom pivot tables are saved for requirement 10).

def generate_custom_pivot_table(data):
    """Interactively build and display a pivot table."""
    row_options = [field for field in group_fields if field in data.columns]
    value_options = [field for field in value_fields if field in data.columns]
    if not row_options or not value_options:
        print("\nThe data does not have the fields needed for a custom pivot table.")
        return
 
    rows = get_user_selection(row_options, "\nSelect rows (required):", required=True)
 
    col_options = [col for col in row_options if col not in rows]
    if col_options:
        cols = get_user_selection(col_options, "\nSelect columns (optional, Enter to skip):")
    else:
        cols = []
 
    values = get_user_selection(value_options, "\nSelect values:", required=True)
 
    agg_options = ['sum', 'mean', 'count']
    agg_func = get_user_selection(agg_options, "\nSelect aggregation function:", required=True, single=True)[0]
 
    data, date_label = choose_date_range(data)
    if data.empty:
        return
 
    try:
        pivot_table = pd.pivot_table(
            data,
            index=rows,
            columns=cols if cols else None,
            values=values,
            aggfunc=agg_func,
            fill_value=0
        )
    except Exception as e:
        print("Could not create the pivot table:", e)
        return
 
    name = f"Custom pivot: {agg_func} of {', '.join(values)} by {', '.join(rows)}"
    if cols:
        name += f" across {', '.join(cols)}"
    show_and_save_result(name, pivot_table, date_label)
 
 
# Requirement 10: shows every stored result
def show_saved_results(data=None):
    if not analytics_history:
        print("\nNo saved results available.")
        return
    for name, result in analytics_history.items():
        print(f"\n=== {name} ===")
        print_pivot(result)
 
 
def exit_program(data=None):
    print("Exiting the program. Goodbye!")
    raise SystemExit(0)
 
 
# Add, remove or reorder menu items by editing this tuple
menu_options = (
    ("Show the first n rows of sales data", display_initial_rows),
    ("Total sales by region and order type", total_sales_by_region_order_type),
    ("Average sales by region with average sales by state and sale type", average_sales_by_region),
    ("Sales by customer type and order type by state", sales_by_customer_type),
    ("Total sales quantity and price by region and product", total_sales_quantity_price_by_region_product),
    ("Total sales quantity and price by customer type", total_sales_quantity_price_customer_type),
    ("Max and min sales price of sales by category", max_min_sales_price_by_category),
    ("Number of unique employees by region", unique_employees_by_region),
    ("Create a custom pivot table", generate_custom_pivot_table),
    ("Show saved results", show_saved_results),
    ("Exit the program", exit_program)
)
 
 
# Requirement 10: the saved results are listed above the menu
def display_menu():
    """Show the saved results and the menu, and return a valid selection as an index into menu_options."""
    while True:
        if analytics_history:
            print(f"\nAnalytics completed so far ({len(analytics_history)}):")
            for name in analytics_history:
                print(f"  {name}")
        else:
            print("\nNo analytics have been run yet.")
 
        print("\n--- Sales Data Dashboard ---")
        for number, (description, _) in enumerate(menu_options, start=1):
            print(f"{number}. {description}")
 
        choice = input(f"Select an option (1-{len(menu_options)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(menu_options):
            return int(choice) - 1
        print(f"Invalid selection '{choice}'. Please enter a number from 1 to {len(menu_options)}.")
 
 
def main(csv_file='https://drive.google.com/uc?id=1ujY0WCcePdotG2xdbLyeECFW9lCJ4t-K&export=download'):
    # csv_file = "sales_data.csv"  # local copy of the same data
    # csv_file = "junk.csv"  # Intentionally incorrect path to test error handling
    sales_data = load_csv(csv_file)
 
    if sales_data is None:
        raise SystemExit("Could not load the sales data, so the dashboard cannot start.")
 
    try:
        while True:
            selection = display_menu()
            _, action = menu_options[selection]
            action(sales_data)
    except (KeyboardInterrupt, EOFError):
        print("\nExiting.")
 
 
if __name__ == "__main__":
    main()