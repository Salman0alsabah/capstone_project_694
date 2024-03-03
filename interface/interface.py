import tkinter as tk
from tkinter import messagebox
import sys
sys.path.append('/Users/salmanalsabah/Desktop/capstone_project_694')
from AI import check_and_scan_url

# Function to read user data from a file
def read_user_data_from_file():
    user_data = {}
    try:
        with open('users.txt', 'r') as file:
            for line in file:
                email, password = line.strip().split(':')
                user_data[email] = password
    except FileNotFoundError:
        pass  # It's okay if the file doesn't exist yet
    return user_data

class FraudDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fraud Detection System")
        self.user_data = read_user_data_from_file()  # Load user data from file
        self.current_user = None
        self.api_key = 'ca44cc05-a78a-4a0a-ab83-71d46e971518'  # Replace with your actual API key


        # Welcome Page
        self.welcome_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.welcome_frame.pack(pady=100)

        tk.Label(self.welcome_frame, text="Welcome to AI Fraud Detection", bg="#f0f0f0", fg="#007bff", font=("Helvetica", 36, "bold")).pack(pady=20)
        tk.Button(self.welcome_frame, text="Get Started", command=self.show_login_page, bg="#4CAF50", fg="white", font=("Helvetica", 16, "bold"), padx=20, pady=10).pack()

        # Login Frame
        self.create_login_frame()

        # Signup Frame
        self.create_signup_frame()

        # Dashboard Frame
        self.create_dashboard_frame()

    def create_login_frame(self):
        self.login_frame = tk.Frame(self.root, bg="#f0f0f0")
        tk.Label(self.login_frame, text="Email:", bg="#f0f0f0", fg="black", font=("Helvetica", 18)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.email_entry = tk.Entry(self.login_frame, font=("Helvetica", 18))
        self.email_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.login_frame, text="Password:", bg="#f0f0f0", fg="black", font=("Helvetica", 18)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.password_entry = tk.Entry(self.login_frame, show="*", font=("Helvetica", 18))
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(self.login_frame, text="Login", command=self.login, bg="#007bff", fg="white", font=("Helvetica", 16, "bold"), padx=20, pady=10).grid(row=2, column=0, columnspan=2, pady=20)

        # Signup link
        self.signup_link = tk.Label(self.login_frame, text="Don't have an account? Signup", bg="#f0f0f0", fg="#007bff", cursor="hand2", font=("Helvetica", 14, "underline"))
        self.signup_link.grid(row=3, column=0, columnspan=2, pady=10)
        self.signup_link.bind("<Button-1>", lambda event: self.show_signup_page())

    def create_signup_frame(self):
        self.signup_frame = tk.Frame(self.root, bg="#f0f0f0")
        tk.Label(self.signup_frame, text="Email:", bg="#f0f0f0", fg="black", font=("Helvetica", 18)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.new_email_entry = tk.Entry(self.signup_frame, font=("Helvetica", 18))
        self.new_email_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.signup_frame, text="Password:", bg="#f0f0f0", fg="black", font=("Helvetica", 18)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.new_password_entry = tk.Entry(self.signup_frame, show="*", font=("Helvetica", 18))
        self.new_password_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(self.signup_frame, text="Signup", command=self.signup, bg="#007bff", fg="white", font=("Helvetica", 16, "bold"), padx=20, pady=10).grid(row=2, column=0, columnspan=2, pady=20)

        # Login link
        self.login_link = tk.Label(self.signup_frame, text="Already have an account? Login", bg="#f0f0f0", fg="#007bff", cursor="hand2", font=("Helvetica", 14, "underline"))
        self.login_link.grid(row=3, column=0, columnspan=2, pady=10)
        self.login_link.bind("<Button-1>", lambda event: self.show_login_page())

    def create_dashboard_frame(self):
        self.dashboard_frame = tk.Frame(self.root, bg="#f0f0f0")
        tk.Label(self.dashboard_frame, text="Dashboard", bg="#f0f0f0", fg="black", font=("Helvetica", 24)).pack(pady=20)

        # URL Check Button
        self.check_url_button = tk.Button(self.dashboard_frame, text="Check URL", command=self.check_url, bg="#007bff", fg="white", font=("Helvetica", 16, "bold"), padx=20, pady=10)
        self.check_url_button.pack(pady=20)

    def show_login_page(self):
        self.welcome_frame.pack_forget()
        self.signup_frame.pack_forget()
        self.dashboard_frame.pack_forget()
        self.login_frame.pack(pady=20)

    def show_signup_page(self):
        self.login_frame.pack_forget()
        self.dashboard_frame.pack_forget()
        self.signup_frame.pack(pady=20)

    def show_dashboard(self):
        self.login_frame.pack_forget()
        self.signup_frame.pack_forget()
        self.welcome_frame.pack_forget()
        self.dashboard_frame.pack(pady=20)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if email in self.user_data and self.user_data[email] == password:
            self.current_user = email
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid email or password")

    def signup(self):
        new_email = self.new_email_entry.get()
        new_password = self.new_password_entry.get()

        if new_email in self.user_data:
            messagebox.showerror("Error", "User already exists")
        else:
            self.write_user_data_to_file(new_email, new_password)
            self.user_data[new_email] = new_password
            messagebox.showinfo("Success", "Account created successfully. Please login.")
            self.show_login_page()

    def write_user_data_to_file(self, email, password):
        with open('users.txt', 'a') as file:
            file.write(f'{email}:{password}\n')



    def check_url(self):
        # Try to get URL from clipboard
        try:
            url = self.root.clipboard_get()
        except tk.TclError:
            url = None

        # If no URL is found in the clipboard, prompt the user to enter a URL manually
        if not url:
            url_entry_window = tk.Toplevel(self.root)
            url_entry_window.title("Enter URL")

            tk.Label(url_entry_window, text="Enter URL:", font=("Helvetica", 12)).pack(padx=10, pady=5)

            url_entry = tk.Entry(url_entry_window, font=("Helvetica", 12), width=50)
            url_entry.pack(padx=10, pady=5)
            url_entry.focus_set()

            def submit_url():
                entered_url = url_entry.get()
                if entered_url:
                    # Use the check_and_scan_url function from the AI module with the manually entered URL
                    check_and_scan_url(entered_url, self.api_key)
                    url_entry_window.destroy()
                else:
                    messagebox.showerror("Error", "Please enter a valid URL")

            submit_button = tk.Button(url_entry_window, text="Check URL", command=submit_url, bg="#4CAF50", fg="white", font=("Helvetica", 12))
            submit_button.pack(pady=10)

            url_entry_window.bind('<Return>', lambda event: submit_url())
        else:
            # Use the check_and_scan_url function from the AI module with the URL from the clipboard
            check_and_scan_url(url, self.api_key)


if __name__ == "__main__":
    root = tk.Tk()
    app = FraudDetectionApp(root)
    root.mainloop()
