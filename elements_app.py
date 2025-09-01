import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
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

# Load elements and methods data
methods_data = load_data('dados/methods_data.json')
elements = load_data('dados/elements.json')

# --- COLOR CHANGE: Traditional Periodic Table Group Colors ---
group_colors = {
    "metais-alcalinos": "#ff6666",        # Reddish (Li, Na, K, Rb, Cs, Fr)
    "metais-alcalino-terrosos": "#ffdead", # Orangish (Be, Mg, Ca, Sr, Ba, Ra)
    "metais-de-transicao": "#ffc0c0",     # Light Pink (Sc to Zn, Y to Cd, Hf to Hg, etc.)
    "lantanideos": "#ffbfff",             # Light Purple (La to Lu)
    "actinideos": "#ff99cc",              # Pink (Ac to Lr)
    "outros-metais": "#cccc99",           # Grey-ish (Al, Ga, In, Sn, Tl, Pb, Bi, Po)
    "semimetais": "#c0a060",              # Brownish (B, Si, Ge, As, Sb, Te)
    "nao-metais": "#a0ffa0",              # Greenish (H, C, N, O, P, S, Se)
    "halogenios": "#c0ffc0",              # Lighter Green (F, Cl, Br, I, At)
    "gases-nobres": "#c0ffff",            # Cyan (He, Ne, Ar, Kr, Xe, Rn)
    "unknown": "#e0e0e0"                  # Default for unknown groups
}

class ElementsApp(QWidget):
    """
    Widget to display a periodic table-like interface for supported elements
    and their associated MOPAC methods.
    """
    back_signal = pyqtSignal() # Signal to go back to the home page

    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background-color: #fce4ec; /* Main app pink background */
            }
            QLabel {
                color: #4e342e; /* Dark brown for general text */
            }
            QPushButton {
                background-color: #ffffff; /* White background for element buttons */
                color: #333333;
                border: 1px solid #c0c0c0;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                border: 2px solid #a0a0a0;
            }
            QLabel#outputLabel {
                background-color: #ffffff;
                border: 1px solid #e91e63; /* Pink border for output */
                padding: 15px;
                border-radius: 8px;
                font-size: 14px;
                color: #4e342e; /* Dark brown for output text */
                min-height: 100px;
                margin-top: 20px;
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
        self.buttons = {}
        self.current_highlighted_button = None # To track the currently highlighted button
        
        if not elements or not methods_data:
            print("Error: Elements or methods data not loaded for ElementsApp.")
            # Consider adding a specific error message to the UI
        else:
            self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Title for the Elements Page
        title_label = QLabel("Supported Elements by MOPAC Methods")
        title_label.setObjectName("titleLabel")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(5)
        main_layout.addLayout(grid_layout)

        # Create buttons for each element
        for element in elements:
            button = QPushButton(element["symbol"])
            button.setFixedSize(60, 60)
            button.setFont(QFont("Arial", 12, QFont.Bold))
            
            # Get color from traditional periodic table group_colors
            color = group_colors.get(element["group"], group_colors["unknown"])
            
            # Apply base style for all buttons, specific color will override background
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: #333333;
                    border: 1px solid #a0a0a0;
                    border-radius: 5px;
                }}
                QPushButton:hover {{
                    border: 2px solid #000000;
                }}
            """)
            # Connect to show_element_info for single element selection
            button.clicked.connect(lambda _, e=element, b=button: self.show_element_info(e, b))
            
            self.buttons[element["symbol"]] = button
            grid_layout.addWidget(button, element["row"], element["col"])

        self.output_label = QLabel("Click an element to see its supported methods.")
        self.output_label.setObjectName("outputLabel")
        self.output_label.setFont(QFont("Arial", 14))
        self.output_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.output_label.setWordWrap(True)
        main_layout.addWidget(self.output_label)

        # --- "Back" button at the bottom ---
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch() # Pushes the button to the right
        btn_back = QPushButton("← Back to Home")
        btn_back.setObjectName("backButton")
        btn_back.setFont(QFont("Arial", 12, QFont.Bold))
        btn_back.clicked.connect(self.back_signal.emit)
        bottom_layout.addWidget(btn_back)
        main_layout.addLayout(bottom_layout)

    def show_element_info(self, clicked_element, clicked_button):
        """
        Displays information about the clicked element and its supported methods.
        Highlights only the clicked element.
        """
        self.clear_highlight() # Clear previous highlight
        self.highlight_element(clicked_element, clicked_button) # Highlight the new one
        
        symbol = clicked_element["symbol"]
        methods = [
            method for method, elems in methods_data.items()
            if any(e["symbol"] == symbol for e in elems)
        ]

        if methods:
            method_info = []
            for method in methods:
                # Find the specific element data for this method to get name/atomic_number
                elements_in_method = [e for e in methods_data[method] if e["symbol"] == symbol]
                if elements_in_method:
                    element_data = elements_in_method[0] # Take the first match
                    element_details = f"{element_data['symbol']} ({element_data['name']}, Atomic No: {element_data['atomic_number']})"
                    method_info.append(f"<b>{method}:</b> {element_details}")
            self.output_label.setText("<br>".join(method_info))
        else:
            self.output_label.setText(f"<b>{symbol}</b> is not supported by any listed method.")

    def highlight_element(self, element, button_to_highlight):
        """Highlights a single element button."""
        # Store the currently highlighted button
        self.current_highlighted_button = button_to_highlight

        # Apply highlight style to the clicked button
        color = group_colors.get(element["group"], group_colors["unknown"])
        button_to_highlight.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: #333333;
                border: 3px solid #000000; /* Stronger border for highlight */
                border-radius: 5px;
            }}
            QPushButton:hover {{
                border: 3px solid #000000; /* Keep highlight on hover */
            }}
        """)

    def clear_highlight(self):
        """Clears the highlight from the previously selected element."""
        if self.current_highlighted_button:
            element_symbol = self.current_highlighted_button.text()
            # Find the element data to get its group and original color
            element_data = next((e for e in elements if e["symbol"] == element_symbol), None)
            if element_data:
                color = group_colors.get(element_data["group"], group_colors["unknown"])
                self.current_highlighted_button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {color};
                        color: #333333;
                        border: 1px solid #a0a0a0;
                        border-radius: 5px;
                    }}
                    QPushButton:hover {{
                        border: 2px solid #000000;
                    }}
                """)
            self.current_highlighted_button = None # Reset tracker