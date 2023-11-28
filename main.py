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
        case_name_lower = case_name.lower()
        cost = get_case_price(case_name_lower)

        release_date = case_release_dates.get(case_name_lower, "Unknown")

        if cost is not None:
            prices_text += f"{case_name}: ${cost:.2f}   Released: {release_date}\n"
        else:
            prices_text += f"{case_name}: Case not found\n"

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
    "Revolution Case": "09-02-2023",
    "Recoil Case": "01-07-2022",
    "Dreams & Nightmares Case": "20-01-2022",
    "Operation Riptide Case": "22-09-2021",
    "Snakebite Case": "03-05-2021",
    "Operation Broken Fang Case": "03-12-2020",
    "Fracture Case": "06-08-2020",
    "Prisma 2 Case": "31-03-2020",
    "Shattered Web Case": "18-11-2019",
    "CS20 Case": "18-09-2019",
    "Prisma Case": "13-03-2019",
    "Danger Zone Case": "06-12-2018",
    "Horizon Case": "31-07-2018",
    "Clutch Case": "15-02-2018",
    "Spectrum 2 Case": "13-11-2017",
    "Operation Hydra Case": "23-05-2017",
    "Spectrum Case": "15-03-2017",
    "Glove Case": "28-11-2016",
    "Gamma 2 Case": "17-05-2016",
    "Gamma Case": "04-05-2016",
    "Chroma 3 Case": "17-02-2016",
    "Operation Wildfire Case": "17-02-2016",
    "Revolver Case": "08-12-2015",
    "Shadow Case": "17-09-2015",
    "Falchion Case": "01-07-2015",
    "Chroma 2 Case": "26-05-2015",
    "Chroma Case": "08-01-2015",
    "Operation Vanguard Weapon Case": "11-11-2014",
    "eSports 2014 Summer Case": "11-06-2014",
    "Operation Breakout Weapon Case": "02-07-2014",
    "Huntsman Weapon Case": "01-05-2014",
    "Operation Phoenix Weapon Case": "20-02-2014",
    "CS:GO Weapon Case 3": "14-11-2013",
    "eSports 2013 Winter Case": "14-11-2013",
    "Winter Offensive Weapon Case": "18-12-2013",
    "CS:GO Weapon Case 2": "19-09-2013",
    "Operation Bravo Case": "19-09-2013",
    "eSports 2013 Case": "14-08-2013",
    "CS:GO Weapon Case": "14-08-2013",
}
case_release_dates = {key.lower(): value for key, value in case_release_dates.items()}


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

    # Pack the buttons to the top of the window
    case_entry_label.pack(side=tk.TOP, padx=10, pady=25)
    case_entry.pack(side=tk.TOP, padx=10, pady=20)
    add_case_button.pack(side=tk.TOP, padx=10, pady=10)
    remove_case_button.pack(side=tk.TOP, padx=10, pady=5)
    get_prices_button.pack(side=tk.TOP, padx=10, pady=15)

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


