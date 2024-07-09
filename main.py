import tkinter as tk
from tkinter import ttk
from vcard_qr import VCardQRGenerator
from wifi_qr import WiFiQRGenerator
from url_qr import URLQRGenerator
from email_qr import EmailQRGenerator
from sms_qr import SMSQRGenerator
from qr_code_parameters import QRCodeParameters
import logging
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Set up the logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('root')

class QRCodeGeneratorApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")

        self.title("QR Code Generator")

        # Set the application icon
        icon = tk.PhotoImage(file="icon.png")
        self.iconphoto(False, icon)

        grid_options = {"sticky": tk.W, "padx": 5, "pady": 5}
        label_options = {"sticky": tk.E, "padx": 5, "pady": 5}

        # Container for layout
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True)

        # Make the window non-resizable
        self.resizable(False, False)

        # Left column frame
        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        # Right column frame
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        # Dropdown menu to select QR code type at the top of the left column
        self.qr_type = tk.StringVar()
        qr_type_menu = ttk.Combobox(left_frame, textvariable=self.qr_type)
        qr_type_menu['values'] = ('vCard', 'WiFi', 'URL', 'EMail', 'SMS')
        qr_type_menu.grid(row=0, column=0, sticky=tk.EW, padx=10, pady=10)
        qr_type_menu.current(0)
        qr_type_menu.bind("<<ComboboxSelected>>", self.update_qr_parameters)

        # Container for different QR code type frames
        self.container = ttk.Frame(left_frame)
        self.container.grid(row=1, column=0, padx=10, pady=10)

        # QR Code parameters section in the right column
        self.qr_code_parameters = QRCodeParameters(right_frame)
        self.qr_code_parameters.grid(row=0, column=0, padx=5, pady=5)

        # Define frames for different QR code types
        self.frames = {}
        for F in (VCardQRGenerator, WiFiQRGenerator, URLQRGenerator, EmailQRGenerator, SMSQRGenerator):
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
        selected_type = self.qr_type.get()
        if selected_type == 'vCard':
            self.show_frame("VCardQRGenerator")
        elif selected_type == 'WiFi':
            self.show_frame("WiFiQRGenerator")
        elif selected_type == 'URL':
            self.show_frame("URLQRGenerator")
        elif selected_type == 'EMail':
            self.show_frame("EmailQRGenerator")
        elif selected_type == 'SMS':
            self.show_frame("SMSQRGenerator")
        self.qr_code_parameters.update_preview()

if __name__ == "__main__":
    app = QRCodeGeneratorApp()
    app.mainloop()
