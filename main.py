import tkinter as tk
from tkinter import ttk
from vcard_qr import VCardQRGenerator
from qr_code_parameters import QRCodeParameters
import logging

# Set up the logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('root')

class QRCodeGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("QR Code Generator")

        grid_options = {"sticky": tk.W, "padx": 5, "pady": 5}
        label_options = {"sticky": tk.E, "padx": 5, "pady": 5}

        # Container for layout
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True)

        # Left column frame
        left_frame = tk.Frame(main_frame)
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        # Right column frame
        right_frame = tk.Frame(main_frame)
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        # Dropdown menu to select QR code type at the top of the left column
        self.qr_type = tk.StringVar()
        qr_type_menu = ttk.Combobox(left_frame, textvariable=self.qr_type)
        qr_type_menu['values'] = ('vCard', 'URL', 'Location')
        qr_type_menu.grid(row=0, column=0, sticky=tk.EW, padx=10, pady=10)
        qr_type_menu.current(0)
        qr_type_menu.bind("<<ComboboxSelected>>", self.update_qr_parameters)

        # Container for different QR code type frames
        self.container = tk.Frame(left_frame)
        self.container.grid(row=1, column=0, padx=10, pady=10)

        # QR Code parameters section in the right column
        self.qr_code_parameters = QRCodeParameters(right_frame)
        self.qr_code_parameters.grid(row=0, column=0, padx=5, pady=5)

        # Define frames for different QR code types
        self.frames = {}
        for F in (VCardQRGenerator,):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self, qr_code_parameters=self.qr_code_parameters)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Start with the vCard frame
        self.show_frame("VCardQRGenerator")
        self.update_qr_parameters()

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def update_qr_parameters(self, event=None):
        self.qr_code_parameters.update_preview()

if __name__ == "__main__":
    app = QRCodeGeneratorApp()
    app.mainloop()
