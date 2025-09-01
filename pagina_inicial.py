from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal

class PaginaInicial(QWidget):
    """
    Home page widget with options to navigate to Keywords or Methods.
    """
    show_methods_signal = pyqtSignal()
    show_keywords_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        # --- CHANGE: Updated stylesheet for a more beautiful look ---
        self.setStyleSheet("""
            QWidget {
                background-color: #fce4ec; /* Light pink background */
            }
            QLabel#titleLabel {
                color: #c2185b; /* Darker pink/red for title */
                margin-bottom: 20px;
            }
            QPushButton {
                color: white;
                /* A beautiful linear gradient for the background */
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #f06292, stop: 1 #e91e63);
                border: 1px solid #d81b60; /* A subtle darker border */
                border-radius: 15px; /* A clean, modern radius */
                padding: 10px; /* Padding that allows text to fit */
                font-weight: bold;
                text-align: center;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            }
            QPushButton:hover {
                /* A darker gradient on hover for a nice effect */
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #e91e63, stop: 1 #c2185b);
                border: 1px solid #ad1457;
                box-shadow: 3px 3px 8px rgba(0, 0, 0, 0.3);
            }
        """)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

        # Main Title
        title = QLabel("MOPAC Assistant", self)
        title.setObjectName("titleLabel")
        title.setFont(QFont("Arial", 36, QFont.Bold))
        layout.addWidget(title, 0, Qt.AlignCenter)

        # Subtitle or Welcome Message
        subtitle = QLabel("Your Guide to Computational Chemistry Keywords and Elements", self)
        subtitle.setFont(QFont("Arial", 16))
        subtitle.setStyleSheet("color: #4e342e;")
        layout.addWidget(subtitle, 0, Qt.AlignCenter)

        layout.addSpacing(50)

        # Keywords Button
        btn_keys = QPushButton("Explore Keywords", self)
        # --- CHANGE: Adjusted size and font for better visibility ---
        btn_keys.setFixedSize(350, 60)
        btn_keys.setFont(QFont("Arial", 14)) # Slightly smaller font to guarantee fit
        btn_keys.clicked.connect(self.show_keywords_signal.emit)
        layout.addWidget(btn_keys, 0, Qt.AlignCenter)

        layout.addSpacing(20)

        # Methods Button
        btn_methods = QPushButton("View Supported Elements", self)
        # --- CHANGE: Adjusted size and font for better visibility ---
        btn_methods.setFixedSize(350, 60)
        btn_methods.setFont(QFont("Arial", 14)) # Slightly smaller font to guarantee fit
        btn_methods.clicked.connect(self.show_methods_signal.emit)
        layout.addWidget(btn_methods, 0, Qt.AlignCenter)

        layout.addStretch()