import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtCore import Qt

# Import page classes
from pagina_inicial import PaginaInicial
from elements_app import ElementsApp
from keywords import KeywordsApp

class MainWindow(QMainWindow):
    """
    Main application window that manages different views using QStackedWidget.
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MOPAC Assistant")
        self.setGeometry(100, 100, 1200, 800)
        # --- COLOR CHANGE: Back to pinkish background ---
        self.setStyleSheet("background-color: #fce4ec;") # Soft pink background for the main window

        # Create the QStackedWidget to hold different pages
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create instances of each page
        self.home_page = PaginaInicial()
        self.elements_page = ElementsApp()
        self.keywords_page = KeywordsApp()

        # Add pages to the stacked widget
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.elements_page)
        self.stacked_widget.addWidget(self.keywords_page)

        # Connect signals from pages to slots in the main window
        self.home_page.show_methods_signal.connect(lambda: self.stacked_widget.setCurrentWidget(self.elements_page))
        self.home_page.show_keywords_signal.connect(lambda: self.stacked_widget.setCurrentWidget(self.keywords_page))
        
        self.elements_page.back_signal.connect(lambda: self.stacked_widget.setCurrentWidget(self.home_page))
        self.keywords_page.back_signal.connect(lambda: self.stacked_widget.setCurrentWidget(self.home_page))

        # Set the home page as the initially displayed page
        self.stacked_widget.setCurrentWidget(self.home_page)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())