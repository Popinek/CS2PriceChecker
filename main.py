import tkinter as tk
import requests
import json
import os


def get_case_price(case_name):
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
        cost = get_case_price(case_name)
        if cost is not None:
            prices_text += f"{case_name}: ${cost:.2f}\n"
        else:
            prices_text += f"{case_name}: Case not found\n"

    result_label.config(text=prices_text)


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

    # Create an entry widget for the case name
    case_entry_label = tk.Label(window, text="Enter Case Name:")
    case_entry = tk.Entry(window)

    # Create buttons
    get_prices_button = tk.Button(window, text="Get Prices", command=show_case_prices)
    add_case_button = tk.Button(window, text="Add Case", command=add_case)
    remove_case_button = tk.Button(window, text="Remove Case", command=remove_case)

    # Create a listbox to display added cases
    cases_listbox_label = tk.Label(window, text="Added Cases:")
    cases_listbox = tk.Listbox(window, selectmode=tk.SINGLE, height=len(csgo_cases))

    # Set the initial height of the listbox
    cases_listbox.configure(height=len(cases_listbox.get(0, tk.END)))

    # Create a label widget to display the result
    result_label = tk.Label(window, text="")

    # Pack the widgets into the window
    case_entry_label.pack(pady=5)
    case_entry.pack(pady=5)
    add_case_button.pack(pady=5)
    remove_case_button.pack(pady=5)
    cases_listbox_label.pack(pady=5)
    cases_listbox.pack(pady=5)
    get_prices_button.pack(pady=5)

    result_label.pack(pady=5)

    # Right-click functionality
    #cases_listbox.bind("<Button-3>", lambda event: remove_case())
    # Bind the Delete key to remove_case
    window.bind("<Delete>", lambda event: remove_case())

    # Load saved cases on startup
    load_cases()

    # Start the GUI event loop
    window.mainloop()

    # Save added cases before closing
    save_cases()


