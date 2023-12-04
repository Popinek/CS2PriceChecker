import tkinter as tk
import requests
import json
import os
from datetime import datetime

price_cache = {}

def get_case_price(case_name):
    # Cache the prices, no need to fetch prices every time
    if case_name in price_cache:
        return price_cache[case_name]

    url = "https://raw.githubusercontent.com/jonese1234/Csgo-Case-Data/master/latest.json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        def find_cost_recursive(data):
            if isinstance(data, dict):
                if "Name" in data and data["Name"].lower() == case_name.lower():
                    cost = data.get("Cost")
                    if cost is not None:
                        print(f"Debug: Found case data for {case_name}. Cost: {cost}")
                        # Cache the price
                        price_cache[case_name] = cost
                        return cost
                    else:
                        print(f"Debug: Found case data for {case_name}, but cost is missing.")
                        return None

                for key, value in data.items():
                    result = find_cost_recursive(value)
                    if result is not None:
                        return result
            elif isinstance(data, list):
                for item in data:
                    result = find_cost_recursive(item)
                    if result is not None:
                        return result

        cost = find_cost_recursive(data)
        if cost is not None:
            return cost

    print(f"Debug: Unable to find case data for {case_name}.")
    return None


def show_case_prices():
    # Load saved cases from the file
    saved_cases = load_saved_cases()

    if not saved_cases:
        result_label.config(text="No saved cases found.")
        return

    prices_text = ""

    for case_name in saved_cases:
        case_name_lower = case_name.lower()
        cost = get_case_price(case_name_lower)
        case_info = case_release_dates.get(case_name_lower, {"case number": "Unknown", "release_date": "Unknown"})

        if isinstance(case_info, dict):
            case_number = case_info.get("case number", "Unknown")
            release_date = case_info.get("release_date", "Unknown")
        else:
            case_number = "Unknown"
            release_date = "Unknown"

        if cost is not None:
            prices_text += f"{case_number} {case_name}:${cost:.2f}   {release_date}\n"
        else:
            prices_text += f"{case_name}: Cost not found\n"

    result_label.config(text=prices_text)
    # Resize result_label based on the current height of csgo_cases
    result_label.config(height=len(saved_cases))


def add_case():
    case_name = case_entry.get()
    if case_name:
        cases_listbox.insert(tk.END, case_name)
        case_entry.delete(0, tk.END)  # Clear the entry field
        save_cases()  # Save the updated list of cases

def remove_case():
    selected_index = cases_listbox.curselection()
    if selected_index:
        cases_listbox.delete(selected_index)
        save_cases()  # Save the updated list of cases

def save_cases():
    cases = cases_listbox.get(0, tk.END)
    with open("saved_cases.json", "w") as file:
        json.dump(list(cases), file)

def load_cases():
    if os.path.exists("saved_cases.json"):
        try:
            with open("saved_cases.json", "r") as file:
                cases = json.load(file)
                for case in cases:
                    cases_listbox.insert(tk.END, case)
        except json.JSONDecodeError:
            pass  # Ignore if the file is not a valid JSON

def load_saved_cases():
    if os.path.exists("saved_cases.json"):
        try:
            with open("saved_cases.json", "r") as file:
                saved_cases = json.load(file)
                return saved_cases
        except json.JSONDecodeError:
            pass  # Ignore if the file is not a valid JSON
    return []

# Dictionary containing case names and their release dates
case_release_dates = {
    "revolution case": {"case number": "39", "release_date": "09-02-2023"},
    "recoil case": {"case number": "38", "release_date": "01-07-2022"},
    "dreams & nightmares case": {"case number": "37", "release_date": "20-01-2022"},
    "operation riptide case": {"case number": "36", "release_date": "22-09-2021"},
    "snakebite case": {"case number": "35", "release_date": "03-05-2021"},
    "operation broken fang case": {"case number": "34", "release_date": "03-12-2020"},
    "fracture case": {"case number": "33", "release_date": "06-08-2020"},
    "prisma 2 case": {"case number": "32", "release_date": "31-03-2020"},
    "shattered web case": {"case number": "31", "release_date": "18-11-2019"},
    "cs20 case": {"case number": "30", "release_date": "18-09-2019"},
    "prisma case": {"case number": "29", "release_date": "13-03-2019"},
    "danger zone case": {"case number": "28", "release_date": "06-12-2018"},
    "horizon case": {"case number": "27", "release_date": "31-07-2018"},
    "clutch case": {"case number": "26", "release_date": "15-02-2018"},
    "spectrum 2 case": {"case number": "25", "release_date": "13-11-2017"},
    "operation hydra case": {"case number": "24", "release_date": "23-05-2017"},
    "spectrum case": {"case number": "23", "release_date": "15-03-2017"},
    "glove case": {"case number": "22", "release_date": "28-11-2016"},
    "gamma 2 case": {"case number": "21", "release_date": "17-05-2016"},
    "gamma case": {"case number": "20", "release_date": "04-05-2016"},
    "chroma 3 case": {"case number": "19", "release_date": "17-02-2016"},
    "operation wildfire case": {"case number": "18", "release_date": "17-02-2016"},
    "revolver case": {"case number": "17", "release_date": "08-12-2015"},
    "shadow case": {"case number": "16", "release_date": "17-09-2015"},
    "falchion case": {"case number": "15", "release_date": "01-07-2015"},
    "chroma 2 case": {"case number": "14", "release_date": "26-05-2015"},
    "chroma case": {"case number": "13", "release_date": "08-01-2015"},
    "operation vanguard weapon case": {"case number": "12", "release_date": "11-11-2014"},
    "esports 2014 summer case": {"case number": "11", "release_date": "11-06-2014"},
    "operation breakout weapon case": {"case number": "10", "release_date": "02-07-2014"},
    "huntsman weapon case": {"case number": "9", "release_date": "01-05-2014"},
    "operation phoenix weapon case": {"case number": "8", "release_date": "20-02-2014"},
    "cs:go weapon case 3": {"case number": "7", "release_date": "14-11-2013"},
    "esports 2013 winter case": {"case number": "6", "release_date": "14-11-2013"},
    "winter offensive weapon case": {"case number": "5", "release_date": "18-12-2013"},
    "cs:go weapon case 2": {"case number": "4", "release_date": "19-09-2013"},
    "operation bravo case": {"case number": "3", "release_date": "19-09-2013"},
    "esports 2013 case": {"case number": "2", "release_date": "14-08-2013"},
    "cs:go weapon case": {"case number": "1", "release_date": "14-08-2013"},
}
case_release_dates = {key.lower(): value for key, value in case_release_dates.items()}

# Define variables for sorting order
price_sort_order = "asc"
date_sort_order = "asc"

def sort_by_price():
    global price_sort_order
    saved_cases = load_saved_cases()

    # Toggle sorting order
    if price_sort_order == "asc":
        price_sort_order = "desc"
    else:
        price_sort_order = "asc"

    # Sort based on the case prices
    saved_cases.sort(key=lambda case: (get_case_price(case.lower()) or float('inf'), case), reverse=(price_sort_order == "desc"))
    display_sorted_cases(saved_cases)

def sort_by_date():
    global date_sort_order
    saved_cases = load_saved_cases()

    # Toggle sorting order
    if date_sort_order == "asc":
        date_sort_order = "desc"
    else:
        date_sort_order = "asc"

    saved_cases.sort(key=lambda case: (datetime.strptime(case_release_dates.get(case.lower(), {}).get("release_date", "9999-99-99"), "%d-%m-%Y") or datetime.max, case), reverse=(date_sort_order == "desc"))
    display_sorted_cases(saved_cases)

def display_sorted_cases(sorted_cases):
    prices_text = ""

    for case_name in sorted_cases:
        case_name_lower = case_name.lower()
        case_info = case_release_dates.get(case_name_lower, {})
        case_number = case_info.get("case number", "Unknown")
        release_date = case_info.get("release_date", "Unknown")

        # Use the cached price if available, otherwise fetch and cache it
        cost = get_case_price(case_name_lower)

        if cost is not None:
            prices_text += f"{case_number} {case_name}: ${cost:.2f}   {release_date}\n"
        else:
            prices_text += f"{case_name}: Case not found\n"

    result_label.config(text=prices_text)
    result_label.config(height=len(sorted_cases))


if __name__ == '__main__':
    # Check if saved_cases.json exists, create it if not
    if not os.path.exists("saved_cases.json"):
        with open("saved_cases.json", "w") as file:
            json.dump([], file)

    # Load the list of cases from a JSON file
    with open("saved_cases.json", "r") as file:
        csgo_cases = json.load(file)

    # Create the main window
    window = tk.Tk()
    window.title("CS:GO Case Prices")
    # Set the size of the main window
    window.geometry("525x900")

    # Create an entry widget for the case name
    case_entry_label = tk.Label(window, text="Enter Case Name:")
    case_entry = tk.Entry(window)

    # Create buttons
    get_prices_button = tk.Button(window, text="Get Prices", command=show_case_prices)
    add_case_button = tk.Button(window, text="Add Case", command=add_case)
    remove_case_button = tk.Button(window, text="Remove Case", command=remove_case)
    price_button = tk.Button(window, text="Price", command=sort_by_price)
    date_button = tk.Button(window, text="Released Date", command=sort_by_date)

    # Pack the buttons to the top of the window
    case_entry_label.pack(side=tk.TOP, padx=10, pady=25)
    case_entry.pack(side=tk.TOP, padx=10, pady=20)
    add_case_button.pack(side=tk.TOP, padx=10, pady=10)
    remove_case_button.pack(side=tk.TOP, padx=10, pady=5)
    get_prices_button.pack(side=tk.TOP, padx=10, pady=15)
    price_button.pack(side=tk.TOP, padx=10, pady=5)
    date_button.pack(side=tk.TOP, padx=10, pady=5)

    # Create a listbox to display added cases
    cases_listbox = tk.Listbox(window, selectmode=tk.SINGLE, height=len(csgo_cases))
    cases_listbox.pack(side=tk.LEFT, padx=10, pady=10, anchor='n')

    # Set the initial height of the listbox
    cases_listbox.configure(width=35, height=len(cases_listbox.get(0, tk.END)))

    # Create a label widget to display the result
    result_label = tk.Label(window, text="", height=len(csgo_cases), pady=5, font=("Helvetica", 10))
    result_label.pack(side=tk.LEFT, padx=10, pady=12, anchor='n')

    # Pack the widgets into the window
    case_entry_label.pack(pady=5)
    case_entry.pack(pady=5)
    add_case_button.pack(pady=5)
    remove_case_button.pack(pady=5)
    get_prices_button.pack(pady=5)
    price_button.pack(pady=5)
    date_button.pack(pady=5)

    # Right-click functionality
    # cases_listbox.bind("<Button-3>", lambda event: remove_case())
    # Bind the Delete key to remove_case
    window.bind("<Delete>", lambda event: remove_case())

    # Load saved cases on startup
    load_cases()

    # Start the GUI event loop
    window.mainloop()

    # Save added cases before closing
    save_cases()
