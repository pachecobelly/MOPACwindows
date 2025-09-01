import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QTextBrowser, QLabel, QSplitter, QPushButton, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal

# --- JSON Data Loading ---
def load_data(filename):
    """Function to load data from a JSON file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file {filename} is not a valid JSON.")
        return None
        
keywords = load_data('dados/keywords.json')

class KeywordsApp(QWidget):
    """
    Widget to display a list of MOPAC keywords and their descriptions.
    """
    back_signal = pyqtSignal() # Signal to go back to the home page

    def __init__(self):
        super().__init__()
        # --- COLOR CHANGE: Restoring original pink theme ---
        self.setStyleSheet("""
            QWidget {
                background-color: #fce4ec; /* Main app pink background */
            }
            QLabel {
                color: #4e342e; /* Dark brown for general text */
            }
            QListWidget {
                background-color: #ffffff;
                color: #4e342e; /* Dark brown list text */
                border: 1px solid #e91e63; /* Pink border */
                border-radius: 8px;
                padding: 5px;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #f8bbd0; /* Lighter pink selection */
                color: #c2185b; /* Darker pink text */
                border-radius: 5px;
            }
            QTextBrowser {
                background-color: #ffffff;
                color: #4e342e; /* Dark brown text */
                border: 1px solid #e91e63; /* Pink border */
                padding: 15px;
                border-radius: 8px;
                font-size: 14px;
                line-height: 1.5;
            }
            QPushButton#backButton {
                background-color: #e91e63; /* Pink for back button */
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 18px;
                font-weight: bold;
                min-width: 120px;
                margin-top: 20px;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            }
            QPushButton#backButton:hover {
                background-color: #d81b60; /* Darker pink on hover */
                box-shadow: 3px 3px 8px rgba(0, 0, 0, 0.3);
            }
            QLabel#titleLabel {
                color: #c2185b; /* Title color */
            }
        """)
        if not keywords:
            print("Error: Keywords data not loaded for KeywordsApp.")
            # Consider adding a specific error message to the UI
        else:
            self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)

        # Title for the Keywords Page
        title_label = QLabel("MOPAC Keywords Reference")
        title_label.setObjectName("titleLabel")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        splitter = QSplitter(Qt.Horizontal)
        
        self.keyword_list = QListWidget()
        self.keyword_list.setFont(QFont("Arial", 12))
        for keyword in sorted(keywords.keys()):
            self.keyword_list.addItem(keyword)
        self.keyword_list.currentItemChanged.connect(self.display_description)
        
        self.description_display = QTextBrowser()
        self.description_display.setFont(QFont("Arial", 12))
        
        splitter.addWidget(self.keyword_list)
        splitter.addWidget(self.description_display)
        splitter.setSizes([200, 700])
        main_layout.addWidget(splitter)
        
        if self.keyword_list.count() > 0:
            self.keyword_list.setCurrentRow(0)

        # --- "Back" button at the bottom ---
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        btn_back = QPushButton("← Back to Home")
        btn_back.setObjectName("backButton")
        btn_back.setFont(QFont("Arial", 12, QFont.Bold))
        btn_back.clicked.connect(self.back_signal.emit)
        bottom_layout.addWidget(btn_back)
        main_layout.addLayout(bottom_layout)

    def display_description(self, current, previous):
        """Displays the description of the selected keyword."""
        if current:
            keyword = current.text()
            description_text = keywords.get(keyword, "Description not found.").replace('\n', '<br>')
            self.description_display.setText(description_text)