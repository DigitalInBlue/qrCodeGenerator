import tkinter as tk
from tkinter import ttk
import qrcode
import logging

logger = logging.getLogger('root')

class SMSQRGenerator(ttk.Frame):
    def __init__(self, parent, controller, qr_code_parameters):
        ttk.Frame.__init__(self, parent)
        self.qr_code_parameters = qr_code_parameters
        self.controller = controller

        grid_options = {"sticky": tk.EW, "padx": 5, "pady": 5}
        label_options = {"sticky": tk.E, "padx": 5, "pady": 5}

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # SMS data entry section
        frame_sms = ttk.LabelFrame(self, text="SMS Configuration")
        frame_sms.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        field_options = {"width": 40}

        self.fields = {
            "Phone Number": ttk.Entry(frame_sms, **field_options),
            "Message": ttk.Entry(frame_sms, **field_options),
        }

        for idx, (label_text, entry) in enumerate(self.fields.items()):
            ttk.Label(frame_sms, text=label_text).grid(row=idx, column=0, **label_options)
            entry.grid(row=idx, column=1, **grid_options)
            entry.bind("<KeyRelease>", self.update_data)

    def update_data(self, event=None):
        phone_number = self.fields["Phone Number"].get()
        message = self.fields["Message"].get()

        sms_data = f"SMSTO:{phone_number}:{message}"

        self.qr_code_parameters.update_data(sms_data)
