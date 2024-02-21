import tkinter as tk
from tkinter import messagebox

# Dummy user data (replace with database implementation)
user_data = {
    'user1@example.com': 'password123',
    'user2@example.com': 'securepass',
}

class FraudDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fraud Detection System")

        self.current_user = None

        # Styling
        self.root.configure(bg="#f0f0f0")
        self.root.state("zoomed")  # Maximize window
        self.root.resizable(False, False)

        # Welcome Page
        self.welcome_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.welcome_frame.pack(pady=100)

        tk.Label(self.welcome_frame, text="Welcome to AI Fraud Detection", bg="#f0f0f0", fg="#007bff", font=("Helvetica", 36, "bold")).pack(pady=20)

        tk.Button(self.welcome_frame, text="Get Started", command=self.show_login_page, bg="#4CAF50", fg="white", font=("Helvetica", 16, "bold"), padx=20, pady=10).pack()

        # Login Frame
        self.login_frame = tk.Frame(self.root, bg="#f0f0f0")

        tk.Label(self.login_frame, text="Email:", bg="#f0f0f0", fg="black", font=("Helvetica", 18)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.email_entry = tk.Entry(self.login_frame, font=("Helvetica", 18))
        self.email_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.login_frame, text="Password:", bg="#f0f0f0", fg="black", font=("Helvetica", 18)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.password_entry = tk.Entry(self.login_frame, show="*", font=("Helvetica", 18))
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(self.login_frame, text="Login", command=self.login, bg="#007bff", fg="white", font=("Helvetica", 16, "bold"), padx=20, pady=10).grid(row=2, column=0, columnspan=2, pady=20)

        # Don't have an account? Signup link
        self.signup_link = tk.Label(self.login_frame, text="Don't have an account? Signup", bg="#f0f0f0", fg="#007bff", cursor="hand2", font=("Helvetica", 14, "underline"))
        self.signup_link.grid(row=3, column=0, columnspan=2, pady=10)
        self.signup_link.bind("<Button-1>", lambda event: self.show_signup_page())

        # Signup Frame
        self.signup_frame = tk.Frame(self.root, bg="#f0f0f0")

        tk.Label(self.signup_frame, text="Username:", bg="#f0f0f0", fg="black", font=("Helvetica", 18)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.new_username_entry = tk.Entry(self.signup_frame, font=("Helvetica", 18))
        self.new_username_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.signup_frame, text="Email:", bg="#f0f0f0", fg="black", font=("Helvetica", 18)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.new_email_entry = tk.Entry(self.signup_frame, font=("Helvetica", 18))
        self.new_email_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.signup_frame, text="Password:", bg="#f0f0f0", fg="black", font=("Helvetica", 18)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.new_password_entry = tk.Entry(self.signup_frame, show="*", font=("Helvetica", 18))
        self.new_password_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(self.signup_frame, text="Signup", command=self.signup, bg="#007bff", fg="white", font=("Helvetica", 16, "bold"), padx=20, pady=10).grid(row=3, column=0, columnspan=2, pady=20)

        # Already have an account? Login link
        self.login_link = tk.Label(self.signup_frame, text="Already have an account? Login", bg="#f0f0f0", fg="#007bff", cursor="hand2", font=("Helvetica", 14, "underline"))
        self.login_link.grid(row=4, column=0, columnspan=2, pady=10)
        self.login_link.bind("<Button-1>", lambda event: self.show_login_page())

        # Dashboard Frame
        self.dashboard_frame = tk.Frame(self.root, bg="#f0f0f0")

    def show_login_page(self):
        self.welcome_frame.pack_forget()
        self.login_frame.pack(pady=20)

    def show_signup_page(self):
        self.login_frame.pack_forget()
        self.signup_frame.pack(pady=20)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if email in user_data and user_data[email] == password:
            self.current_user = email
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid email or password")

    def signup(self):
        new_username = self.new_username_entry.get()
        new_email = self.new_email_entry.get()
        new_password = self.new_password_entry.get()

        if new_email in user_data:
            messagebox.showerror("Error", "User already exists")
        else:
            user_data[new_email] = new_password
            messagebox.showinfo("Success", "Account created successfully. Please login.")
            self.show_login_page()  # Go back to login page after signup

    def show_dashboard(self):
        self.login_frame.pack_forget()
        self.signup_frame.pack_forget()

        # Placeholder for dashboard display
        self.dashboard_frame.pack(pady=20)
        tk.Label(self.dashboard_frame, text=f"Welcome, {self.current_user}!", bg="#f0f0f0", fg="black", font=("Helvetica", 24)).pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = FraudDetectionApp(root)
    root.mainloop()