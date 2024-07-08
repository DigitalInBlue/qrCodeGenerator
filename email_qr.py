import tkinter as tk
from tkinter import ttk
import qrcode
import logging

logger = logging.getLogger('root')

class EmailQRGenerator(ttk.Frame):
    def __init__(self, parent, controller, qr_code_parameters):
        ttk.Frame.__init__(self, parent)
        self.qr_code_parameters = qr_code_parameters
        self.controller = controller

        grid_options = {"sticky": tk.EW, "padx": 5, "pady": 5}
        label_options = {"sticky": tk.E, "padx": 5, "pady": 5}

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Email data entry section
        frame_email = ttk.LabelFrame(self, text="Email Configuration")
        frame_email.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        field_options = {"width": 40}

        self.fields = {
            "To": ttk.Entry(frame_email, **field_options),
            "Subject": ttk.Entry(frame_email, **field_options),
            "Body": ttk.Entry(frame_email, **field_options),
        }

        for idx, (label_text, entry) in enumerate(self.fields.items()):
            ttk.Label(frame_email, text=label_text).grid(row=idx, column=0, **label_options)
            entry.grid(row=idx, column=1, **grid_options)
            entry.bind("<KeyRelease>", self.update_data)

    def update_data(self, event=None):
        to = self.fields["To"].get()
        subject = self.fields["Subject"].get()
        body = self.fields["Body"].get()

        email_data = f"mailto:{to}?subject={subject}&body={body}"

        self.qr_code_parameters.update_data(email_data)
