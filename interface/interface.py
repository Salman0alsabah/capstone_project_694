import sys
sys.path.append('/Users/salmanalsabah/Desktop/capstone_project_694')
from AI import check_and_scan_url
from database import fetch_sorted_links
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QWidget, QMessageBox, QHBoxLayout, QTableWidget,
    QTableWidgetItem,QHeaderView,QSizePolicy,QScrollArea,
    QTextEdit,QGroupBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from chatbot import ChatBot



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



class FraudDetectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fraud Detection System")

        # Set the dark theme globally for the application
        self.setStyleSheet("""
            QWidget {
                color: #b1b1b1;
                background-color: #323232;
                font-family: 'Segoe UI', sans-serif;
            }
            QPushButton {
                background-color: #5e5e5e;
                border: 1px solid #2a2a2a;
                padding: 5px 15px;
                border-radius: 2px;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QPushButton:pressed {
                background-color: #424242;
            }
            QLabel {
                font-size: 15px;
            }
            QLineEdit {
                background-color: #424242;
                border: 1px solid #2a2a2a;
                border-radius: 2px;
                padding: 5px;
            }
        """)

        self.user_data = read_user_data_from_file()
        self.current_user = None
        self.api_key = 'ca44cc05-a78a-4a0a-ab83-71d46e971518'
        self.chat_bot = ChatBot()

        # Set a fixed size for the QMainWindow
        self.setFixedSize(800, 600)  # Adjust the size as needed


        # Initialize UI components
        self.initUI()

    
    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)


        # Welcome Page
        self.setup_welcome_page()

    def read_user_data_from_file(self):
        user_data = {}
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    email, password = line.strip().split(':')
                    user_data[email] = password
        except FileNotFoundError:
            pass  # It's okay if the file doesn't exist yet
        return user_data

    def setup_welcome_page(self):
        self.welcome_label = QLabel("Welcome to AI Fraud Detection")
        self.welcome_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
            color: white;
        """)
        self.main_layout.addWidget(self.welcome_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.get_started_button = QPushButton("Get Started")
        self.get_started_button.setStyleSheet("""
            background-color: #5e5e5e;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 18px;
            border-radius: 5px;
        """)
        self.get_started_button.clicked.connect(self.show_login_page)
        self.main_layout.addWidget(self.get_started_button, alignment=Qt.AlignmentFlag.AlignCenter)

    def show_login_page(self):
        # Clear the layout and setup the login UI
        self.clear_layout()
        self.setup_login_page()

    def setup_login_page(self):
        self.login_label = QLabel("Login")
        self.login_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 10px;
            color: white;
        """)
        self.main_layout.addWidget(self.login_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.email_label = QLabel("Email:")
        self.email_entry = QLineEdit()
        self.main_layout.addWidget(self.email_label)
        self.main_layout.addWidget(self.email_entry)

        self.password_label = QLabel("Password:")
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self.main_layout.addWidget(self.password_label)
        self.main_layout.addWidget(self.password_entry)

        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet("""
            background-color: #5e5e5e;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 18px;
            border-radius: 5px;
        """)
        self.login_button.clicked.connect(self.login)
        self.main_layout.addWidget(self.login_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.signup_link = QLabel("Don't have an account? <a href='#' style='color: white;'>Sign up</a>")
        self.signup_link.setOpenExternalLinks(False)
        self.signup_link.linkActivated.connect(self.show_signup_page)
        self.main_layout.addWidget(self.signup_link, alignment=Qt.AlignmentFlag.AlignCenter)

    def show_signup_page(self):
        # Clear the layout and setup the signup UI
        self.clear_layout()
        self.setup_signup_page()

    def setup_signup_page(self):
        self.signup_label = QLabel("Sign Up")
        self.signup_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 10px;
            color: white;
        """)
        self.main_layout.addWidget(self.signup_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.new_email_label = QLabel("Email:")
        self.new_email_entry = QLineEdit()
        self.main_layout.addWidget(self.new_email_label)
        self.main_layout.addWidget(self.new_email_entry)

        self.new_password_label = QLabel("Password:")
        self.new_password_entry = QLineEdit()
        self.new_password_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self.main_layout.addWidget(self.new_password_label)
        self.main_layout.addWidget(self.new_password_entry)

        self.signup_button = QPushButton("Sign Up")
        self.signup_button.setStyleSheet("""
            background-color: #5e5e5e;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 18px;
            border-radius: 5px;
        """)
        self.signup_button.clicked.connect(self.signup)
        self.main_layout.addWidget(self.signup_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.login_link = QLabel("Already have an account? <a href='#' style='color: white;'>Login </a>")
        self.login_link.setOpenExternalLinks(False)
        self.login_link.linkActivated.connect(self.show_login_page)
        self.main_layout.addWidget(self.login_link, alignment=Qt.AlignmentFlag.AlignCenter)

    def show_dashboard(self):
        # Clear the main layout first
        self.clear_layout()

        # Horizontal layout for sidebar and main content
        self.dashboard_layout = QHBoxLayout()

        # Sidebar setup
        self.sidebar_layout = QVBoxLayout()
        self.sidebar = QWidget()
        self.sidebar.setLayout(self.sidebar_layout)
        self.sidebar.setFixedWidth(60)  # Match width from the example
        self.sidebar.setStyleSheet("background-color: #333; padding: 10px;")

        # Sidebar icon for showing Check URL button
        self.show_check_url_icon = QPushButton()
        self.show_check_url_icon.setIcon(QIcon('cil-check.png'))  # Update the path to your icon
        self.show_check_url_icon.setIconSize(QSize(40, 40))  # Set icon size similar to the example
        self.show_check_url_icon.setStyleSheet("background-color: transparent; border: none;")
        self.show_check_url_icon.clicked.connect(self.show_check_url_button)
        self.sidebar_layout.addWidget(self.show_check_url_icon)
        
        # Database Icon in the Sidebar
        self.database_icon = QPushButton()
        self.database_icon.setIcon(QIcon('cil-clone.png'))  # Update with the path to your database icon
        self.database_icon.setIconSize(QSize(40, 40))  # Set icon size
        self.database_icon.setStyleSheet("background-color: transparent; border: none;")
        self.database_icon.clicked.connect(self.show_database_info)
        self.sidebar_layout.addWidget(self.database_icon)

        # chatbot Icon in the Sidebar
        self.chatbot_icon = QPushButton()
        self.chatbot_icon.setIcon(QIcon('cil-chat-bubble.png'))  # Update with the path to your database icon
        self.chatbot_icon.setIconSize(QSize(40, 40))  # Set icon size
        self.chatbot_icon.setStyleSheet("background-color: transparent; border: none;")
        self.chatbot_icon.clicked.connect(self.show_chat_window)
        self.sidebar_layout.addWidget(self.chatbot_icon)

        # Add stretch to push subsequent widgets to the bottom
        self.sidebar_layout.addStretch()

        # Settings Button in the Sidebar
        self.settings_button = QPushButton()
        self.settings_button.setIcon(QIcon('cil-settings.png'))  # Update the path to your settings icon
        self.settings_button.setIconSize(QSize(40, 40))  # Set icon size similar to the example
        self.settings_button.setStyleSheet("background-color: transparent; border: none;")
        self.settings_button.clicked.connect(self.show_settings)
        self.sidebar_layout.addWidget(self.settings_button)


        # Main content setup
        self.main_content_area = QWidget()
        self.main_content_layout = QVBoxLayout()
        self.main_content_area.setLayout(self.main_content_layout)
        self.main_content_area.setStyleSheet("background-color: #424242; padding: 20px;")

        # Top bar in the main content area
        self.top_bar = QHBoxLayout()
        self.top_bar_label = QLabel()
        self.top_bar.addWidget(self.top_bar_label)
        self.main_content_layout.addLayout(self.top_bar)

        # Placeholder for extra content in the main content area
        self.extra_content_placeholder = QLabel("Extra Content Here")
        self.extra_content_placeholder.setStyleSheet("color: #FFF; font-size: 16px;")
        self.main_content_layout.addWidget(self.extra_content_placeholder)

        # Assemble the dashboard
        self.dashboard_layout.addWidget(self.sidebar)
        self.dashboard_layout.addWidget(self.main_content_area)

        # Add the dashboard layout to the main layout
        self.main_layout.addLayout(self.dashboard_layout)

    
    def show_chat_window(self):
        # Clear the main content layout first
        self.clear_main_content_layout()

        # Create a layout to hold the chat messages
        self.chat_layout = QVBoxLayout()

        # Create a group box to contain the chat messages
        chat_group_box = QGroupBox("Chat Messages")
        chat_group_box.setLayout(self.chat_layout)

        # Create a QTextEdit widget to display chat messages
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)

        # Add the chat display to the layout
        self.chat_layout.addWidget(self.chat_display)

        # Create a QLineEdit widget for entering chat messages
        self.chat_input = QLineEdit()
        self.chat_input.returnPressed.connect(self.send_message)

        # Add the chat input field to the layout
        self.chat_layout.addWidget(self.chat_input)

        # Add the group box to the main content layout
        self.main_content_layout.addWidget(chat_group_box)

    def send_message(self):
        # Get the message from the input field
        message = self.chat_input.text()

        # Clear the input field
        self.chat_input.clear()

        # Add the user message to the chat display
        self.display_message(self.chat_display, f"You: {message} \n ")

        # Call AI chat method to generate response using the chat_bot instance
        self.chat_bot.ai_chat(message)

        # Get the response from the chatbot
        response = self.chat_bot.get_last_response()

        # Add the chatbot response to the chat display
        self.display_message(self.chat_display, f"ChatGPT: {response} \n")

    def display_message(self, chat_display, message):
        # Append the message to the chat display
        chat_display.append(message)


    def show_database_info(self):
        # Clear the main content layout first
        self.clear_main_content_layout()

        # Fetch the sorted links from the database
        sorted_links = fetch_sorted_links()

        # Create a scroll area to contain the items
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Create a widget to hold the items layout
        items_widget = QWidget()
        items_layout = QVBoxLayout(items_widget)

        # Iterate over each link and create a widget to display its info
        for link in sorted_links:
            # Create a widget to hold the labels for this link
            link_widget = QWidget()
            link_layout = QVBoxLayout(link_widget)

            # Create and configure labels for the URL, Status, and Scan Date
            url_label = QLabel(f"URL: {link['url']}")
            status_label = QLabel(f"Status: {link['status']}")
            date_label = QLabel(f"Scan Date: {link['scan_date']}")

            # Add labels to the link layout
            link_layout.addWidget(url_label)
            link_layout.addWidget(status_label)
            link_layout.addWidget(date_label)

            # Optionally, add styling to the link widget (border, padding, etc.)
            link_widget.setStyleSheet("border: 1px solid #ccc; padding: 10px; margin-bottom: 10px;")

            # Add the link widget to the main items layout
            items_layout.addWidget(link_widget)

        # Add the widget holding the items layout to the scroll area
        scroll_area.setWidget(items_widget)

        # Add the scroll area to the main content layout
        self.main_content_layout.addWidget(scroll_area)
   

    
        
    def show_check_url_button(self):
        # Clear the main content layout first
        self.clear_main_content_layout()

        # Create and add the Check URL button to the main content area
        self.check_url_button = QPushButton("Check URL")
        self.check_url_button.setStyleSheet("""
            background-color: #5e5e5e;
            color: white;
            padding: 10px 20px;
            font-size: 18px;
            border-radius: 5px;
        """)
        self.check_url_button.clicked.connect(self.check_url)  # Assuming check_url is your method for handling URL checks
        self.main_content_layout.addWidget(self.check_url_button)

    def show_settings(self):
        # Method to show settings content in the main content area
        self.clear_main_content_layout()  # Assuming you have a method to clear the main content layout

        # Add settings related content here
        self.settings_content = QLabel("Settings Content Here")
        self.settings_content.setStyleSheet("color: #FFF; font-size: 18px;")
        self.main_content_layout.addWidget(self.settings_content)

    def login(self):
        email = self.email_entry.text()
        password = self.password_entry.text()

        if email in self.user_data and self.user_data[email] == password:
            self.current_user = email
            self.show_dashboard()
        else:
            QMessageBox.warning(self, "Error", "Invalid email or password")

    def signup(self):
        new_email = self.new_email_entry.text()
        new_password = self.new_password_entry.text()

        if not new_email or not new_password:
            QMessageBox.warning(self, "Error", "Please fill in both email and password fields.")
            return

        if new_email in self.user_data:
            QMessageBox.warning(self, "Error", "User already exists")
        else:
            self.write_user_data_to_file(new_email, new_password)
            self.user_data[new_email] = new_password
            QMessageBox.information(self, "Success", "Account created successfully. Please login.")
            self.show_login_page()

    def write_user_data_to_file(self, email, password):
        with open('users.txt', 'a') as file:
            file.write(f'{email}:{password}\n')

    def check_url(self):
        # Define a callback function to update the UI with the result of the URL check
        def ui_update_callback(result):
            # Clear the main content layout first
            self.clear_main_content_layout()

            # Display the result in the main content area
            result_label = QLabel(result)
            result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            result_label.setWordWrap(True)  # Enable word wrapping to ensure the entire text is visible
            result_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)  # Make label expandable
            self.main_content_layout.addWidget(result_label)

        # Try to get URL from clipboard
        clipboard = QApplication.clipboard()
        url_text = clipboard.text()

        if url_text:
            # Use the check_and_scan_url function from the AI module with the URL from the clipboard
            check_and_scan_url(url_text, self.api_key, ui_update_callback)
        else:
            QMessageBox.warning(self, "Error", "No URL found in clipboard")



    def clear_main_content_layout(self):
        while self.main_content_layout.count():
            child = self.main_content_layout.takeAt(0)
            if child.widget():
                widget = child.widget()
                widget.deleteLater()

    def clear_layout(self):
        while self.main_layout.count():
            child = self.main_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FraudDetectionApp()
    window.show()
    sys.exit(app.exec())