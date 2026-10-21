import os
import sys
from pathlib import Path
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.uic import loadUi
from cryptography.fernet import Fernet
from manager import Manager
import pyperclip
from tkinter import messagebox
from PyQt6.QtGui import QFont
from pass_generator import RandomPassword
from log import Log
from PyQt6.QtWidgets import QMessageBox

class DialogBox(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Data")
        self.setFixedSize(450, 320)

        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
            }
            QLabel {
                color: #ffffff;
                font-weight: bold;
                min-width: 100px;
            }
            QLineEdit {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 1px solid #3a3a3a;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #5a5a5a;
            }
            QPushButton {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3e3e3e;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
            QPushButton:pressed {
                background-color: #222222;
            }
            #submitBtn {
                color: #a78bfa; 
            }
            #generatePassword {
                margin-left: 25px;
            }
        """)

        # Main vertical layout with clean padding
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(15)

        # Set shared bold font style
        label_font = QFont("Arial", 11)

        # Row 1: Site Name
        row1 = QHBoxLayout()
        self.site_label = QLabel("Site Name:", self)
        self.site_label.setFont(label_font)
        self.site_entry = QLineEdit(self)
        row1.addWidget(self.site_label)
        row1.addWidget(self.site_entry)
        main_layout.addLayout(row1)

        # Row 2: User/Email
        row2 = QHBoxLayout()
        self.user_email_label = QLabel("User/Email:", self)
        self.user_email_label.setFont(label_font)
        self.user_email_entry = QLineEdit(self)
        row2.addWidget(self.user_email_label)
        row2.addWidget(self.user_email_entry)
        main_layout.addLayout(row2)

        # Row 3: Password + Show Button
        row3 = QHBoxLayout()
        self.password_label = QLabel("Password", self)
        self.password_label.setFont(label_font)
        self.password_entry = QLineEdit(self)
        self.password_entry.setEchoMode(QLineEdit.EchoMode.Password)  # Masks text by default

        self.show_btn = QPushButton("Show", self)
        self.show_btn.setFixedWidth(65)
        self.show_btn.clicked.connect(self.toggle_password_visibility)

        row3.addWidget(self.password_label)
        row3.addWidget(self.password_entry)
        row3.addWidget(self.show_btn)
        main_layout.addLayout(row3)

        # Row 4: Action Button Container (Bottom row)
        row4 = QHBoxLayout()
        row4.setContentsMargins(0, 10, 0, 0)

        self.submit_btn = QPushButton("Submit", self)
        self.submit_btn.setObjectName("submitBtn")  # Hooks into the purple style sheet rule
        self.submit_btn.clicked.connect(self.accept)
        self.generate_btn = QPushButton("GeneratePassword", self)
        self.generate_btn.setObjectName("generatePassword")
        self.generate_btn.clicked.connect(self.generate_random_password)
        # Spacer pushes the button to align cleanly underneath
        row4.addWidget(self.submit_btn)
        row4.addWidget(self.generate_btn)
        row4.addStretch()

        main_layout.addLayout(row4)

    def generate_random_password(self):
        password = RandomPassword.generate_random_password()
        self.password_entry.setText(password)

    def toggle_password_visibility(self):
        """Toggles masking your entry password field just like your UI Show button"""
        if self.password_entry.echoMode() == QLineEdit.EchoMode.Password:
            self.password_entry.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_btn.setText("Hide")
        else:
            self.password_entry.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_btn.setText("Show")

    def get_data(self):
        return self.site_entry.text(), self.user_email_entry.text(), self.password_entry.text()

class User(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logger = Log
        self.manager = Manager()
        ui_path = Path(__file__).resolve().parent / "mainwindow.ui"
        loadUi(str(ui_path), self)
        self.password_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self.submit_btn.clicked.connect(self.get_data)
        self.display_pass.clicked.connect(self.display)
        self.copy_btn.clicked.connect(self.copy_password)
        self.delete_btn.clicked.connect(self.delete_data)
        self.edit_btn.clicked.connect(self.edit_data)
        self.show_btn.clicked.connect(self.password_visibility)
        self.generate_btn.clicked.connect(self.generate_random_password)

        self.cypher_suit = None
        appdata = os.getenv("APPDATA")
        dir = os.path.join(appdata, "Key")
        os.makedirs(dir, exist_ok=True)

        fl = os.path.join(dir, "secret.key")

        file_path = Path(fl)
        if not file_path.exists():
            with open (fl, "wb") as file:
                key = Fernet.generate_key()
                file.write(key)
                print("Key Created")
        else:
            print("Key exist")

        with open(fl, "rb") as file:
            self.cypher_suit = Fernet(file.read())


    def password_visibility(self):
        if self.password_entry.echoMode() == QLineEdit.EchoMode.Password:
            self.password_entry.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_btn.setText("Hide")
        else:
            self.password_entry.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_btn.setText("Show")

    def generate_random_password(self):
        random_password = RandomPassword.generate_random_password()
        self.password_entry.setText(random_password)

    def get_data(self):
        """Get data from the user and send to the manager to add into DataBase"""
        site_name = self.site_entry.text()
        user_email = self.user_entry.text()
        password = self.password_entry.text()

        pass_byts = password.encode("utf-8") # First convert data to bytes
        encrypted_password = self.cypher_suit.encrypt(pass_byts) # Then encrypt data

        if site_name and user_email and password:
            self.site_entry.clear()
            self.user_entry.clear()
            self.password_entry.clear()
            self.manager.store_data([site_name, user_email, encrypted_password])
        else:
            messagebox.showerror(title="Fields", message="Please fill all the fields!")
    def display(self):
        user_email = self.user_entry.text()
        sitename = self.site_entry.text()

        if user_email:
            self.user_entry.clear()
            self.display_by_user_email(user_email)
        elif sitename:
            self.site_entry.clear()
            self.display_by_site(sitename)
        else:
            self.display_all()

    def display_all(self):
        """Display all"""
        data = self.manager.fetch_data()
        if data:
            self.listWidget.clear()
            for d in data:
                id_, site, user_email, password = d
                list_data = f"Id: {id_} ---- SiteName: {site} ---- UserName_Email: {user_email}"
                self.listWidget.addItem(list_data)

    def display_by_site(self, sitename):
        """Display data by sitename"""
        data = self.manager.fetch_data_by_sitename(sitename)
        if data:
            self.listWidget.clear()
            for d in data:
                id_, site, user_email, password = d
                list_data = f"Id: {id_} ---- SiteName: {site} ---- UserName_Email: {user_email}"
                self.listWidget.addItem(list_data)

    def display_by_user_email(self, user_email):
        """Display data by UserName or Email"""
        data = self.manager.fetch_by_user_email(user_email)
        if data:
            self.listWidget.clear()
            for d in data:
                id_, site, user_email, password = d
                list_data = f"Id: {id_} ---- SiteName: {site} ---- UserName_Email: {user_email}"
                self.listWidget.addItem(list_data)

    def copy_password(self):
        selected_item = self.listWidget.currentItem()

        if selected_item is None:
            QMessageBox.information(
                self,
                "No Selection",
                "Please select an account first."
            )
            return

        try:
            # Extract the complete ID, even if it has multiple digits.
            id_ = int(selected_item.text().split(" ---- ", 1)[0].replace("Id: ", ""))

            encrypted_password = self.manager.get_password(id_)

            if encrypted_password:
                decrypted_bytes = self.cypher_suit.decrypt(
                    encrypted_password[0]
                )
                decrypted_password = decrypted_bytes.decode("utf-8")

                pyperclip.copy(decrypted_password)

                QMessageBox.information(
                    self,
                    "Password",
                    "Your password has been copied to the clipboard."
                )

        except Exception as e:
            self.logger.log_err(e)
            QMessageBox.warning(
                self,
                "Error",
                "Could not retrieve the password."
            )

    def delete_data(self):
        selected_item = self.listWidget.currentItem()

        if selected_item is None:
            QMessageBox.information(
                self,
                "No Selection",
                "Please select an account to delete."
            )
            return

        id_ = int(
            selected_item.text().split(" ---- ", 1)[0].replace("Id: ", "")
        )
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this account?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            # if the user chose No
            return

        self.manager.delete_data(id_)

        current_row = self.listWidget.currentRow()
        self.listWidget.takeItem(current_row)

    def edit_data(self):
        selected_text = self.listWidget.currentItem()
        if selected_text:
            id_ = int(selected_text.text().split(" ---- ", 1)[0].replace("Id: ", ""))
            data = self.manager.get_by_id(id_)

            dialog = DialogBox(self)
            dialog.site_entry.setText(data[1])
            dialog.user_email_entry.setText(data[2])

            decrypted_password = self.cypher_suit.decrypt(data[3]).decode("utf-8")
            dialog.password_entry.setText(decrypted_password)

            if dialog.exec() == QDialog.DialogCode.Accepted:
                site_name, user_email, password = dialog.get_data()
                if not site_name and not user_email and not password:
                    """If user change their mind and do not want update, then eat five-star and do nothing"""
                    pass
                else:
                    site = site_name if site_name else data[1]
                    u_e = user_email if user_email else data[2]
                    if password:
                        pass_ = self.cypher_suit.encrypt(password.encode("utf-8"))
                    else:
                        pass_ = data[3]
                    self.manager.update_data(site, u_e, pass_, id_)
                    self.display_all()
            else:
                return
        else:
            messagebox.showinfo(title="Current Selection", message="Please select from the Display list you want to Update")



app = QApplication(sys.argv)
window = User()
window.show()
sys.exit(app.exec())
