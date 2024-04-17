import tkinter as tk
import subprocess
from datetime import datetime, timezone
import getpass
import socket

def write_to_log():
    # Get current date and time in UTC
    current_utc_time = datetime.now(timezone.utc)

    # Format the date as a string
    formatted_date = current_utc_time.strftime('%Y-%m-%d %H:%M:%S UTC')

    # Get the current username
    current_username = getpass.getuser()

    # Get the hostname of the PC
    hostname = socket.gethostname()

    # File path for log.txt in the current directory
    file_path = 'log.txt'

    # Write the formatted date, username, and hostname to the log file
    with open(file_path, 'a') as file:
        file.write(f"Date: {formatted_date}, Username: {current_username}, Hostname: {hostname}\n")

    print(f"Current UTC date ({formatted_date}), username ({current_username}), and hostname ({hostname}) have been appended to {file_path}")

def countdown(timer_label, explanation_label, close_button, error_label):
    if countdown.remaining <= 0:
        explanation_label.config(text="Din SP session er nu lukket og du kan starte SP igen")
        timer_label.config(text="")
    else:
        timer_label.config(text=f"Vent venligst: {countdown.remaining} sekunder")
        countdown.remaining -= 1
        root.after(1000, countdown, timer_label, explanation_label, close_button, error_label)

def close_sp_session(timer_label, explanation_label, close_button, error_label):
    write_to_log()  # Log when the user presses the button
    if testing:
        # Simulate an error for testing
        error_message = "Testfejl: Dette er en simuleret fejl."
        error_label.config(text=error_message)
    else:
        try:
            subprocess.Popen(["C:\\Program Files (x86)\\Citrix\\ICA Client\\SelfServicePlugin\\SelfService.exe", "-logoffSessions"])
            error_label.config(text="")  # Clear any previous error message
        except Exception as e:
            error_label.config(text=f"Fejl under lukning af SP session: {str(e)}")

    explanation_label.config(text="vent venligst" if not testing else "")
    close_button.pack_forget()  # Hide the button if testing
    if not testing:
        countdown.remaining = 15  # Set countdown starting number
        countdown(timer_label, explanation_label, close_button, error_label)

def main():
    global root, testing  # Make root and testing accessible everywhere within this script
    testing = False  # Set to True to test error message, False for normal operation

    root = tk.Tk()
    root.title("SP Session Lukning")
    root.geometry("400x200")
    root.resizable(False, False)

    explanation_label = tk.Label(root, text="Tryk på knappen for at lukke din SP session ned")
    explanation_label.pack(pady=10)

    timer_label = tk.Label(root, text="", font=("Helvetica", 14))
    timer_label.pack(pady=20)

    error_label = tk.Label(root, text="", fg="red")  # Use red text for errors
    error_label.pack(pady=5)

    close_button = tk.Button(root, text="Luk SP", command=lambda: close_sp_session(timer_label, explanation_label, close_button, error_label))
    close_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
