from datetime import datetime

try:
    import tkinter as tk
    from tkcalendar import Calendar
    GUI_ENABLED = True  # If tkinter loads successfully, enable GUI mode
except ImportError:
    print("GUI did not load. Using hardcoded date: 2025-01-01")
    GUI_ENABLED = False  # Disable GUI if Tkinter is not available

def get_user_date():
    default_date = "2025-01-01"

    if GUI_ENABLED:
        try:
            # Initialize the selected_date variable outside of set_date function
            selected_date = None

            # Create a pop-up window
            root = tk.Tk()
            root.withdraw()  # Hide main window
            
            # Create a second window for date selection
            date_window = tk.Toplevel(root)
            date_window.title("Select Minimum Article Date")
            date_window.geometry("400x300")

            # Calendar widget
            cal = Calendar(date_window, selectmode="day", year=2025, month=1, day=1)
            cal.pack(pady=20)

            # Function to set selected date and close window
            def set_date():
                nonlocal selected_date  # Ensure the function modifies the outer variable
                selected_date = cal.get_date()  # Format: M/D/YY or MM/DD/YYYY
                date_window.destroy()

            # Button to confirm date selection
            select_btn = tk.Button(date_window, text="Select Date", command=set_date)
            select_btn.pack()

            # Run the GUI and wait for user input
            root.wait_window(date_window)

            # If no date was selected, return default
            if not selected_date:
                print(f"No date selected. Using default: {default_date}")
                return default_date

            # Convert the selected date format dynamically
            try:
                parsed_date = datetime.strptime(selected_date, "%m/%d/%y")  # Handles M/D/YY
            except ValueError:
                parsed_date = datetime.strptime(selected_date, "%m/%d/%Y")  # Handles MM/DD/YYYY

            formatted_date = parsed_date.strftime("%Y-%m-%d")  # Convert to YYYY-MM-DD
            print(f"Using user-selected date: {formatted_date}")
            return formatted_date

        except Exception as e:
            print(f"GUI error: {e}. Using hardcoded date: {default_date}")
            return default_date