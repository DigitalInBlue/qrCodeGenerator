import tkinter as tk
from tkinter import ttk
import qrcode
import logging

logger = logging.getLogger('root')

class WiFiQRGenerator(ttk.Frame):
    def __init__(self, parent, controller, qr_code_parameters):
        ttk.Frame.__init__(self, parent)
        self.qr_code_parameters = qr_code_parameters
        self.controller = controller

        grid_options = {"sticky": tk.EW, "padx": 5, "pady": 5}
        label_options = {"sticky": tk.E, "padx": 5, "pady": 5}

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Wi-Fi data entry section
        frame_wifi = ttk.LabelFrame(self, text="Wi-Fi Configuration")
        frame_wifi.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        field_options = {"width": 40}

        self.fields = {
            "SSID": ttk.Entry(frame_wifi, **field_options),
            "Password": ttk.Entry(frame_wifi, show='*', **field_options),
            "Hidden": ttk.Combobox(frame_wifi, values=["False", "True"], **field_options),
            "Authentication": ttk.Combobox(frame_wifi, values=["WPA", "WEP", "nopass"], **field_options),
        }

        # Set default values
        self.fields["Hidden"].set("False")
        self.fields["Authentication"].set("WPA")

        for idx, (label_text, entry) in enumerate(self.fields.items()):
            ttk.Label(frame_wifi, text=label_text).grid(row=idx, column=0, **label_options)
            entry.grid(row=idx, column=1, **grid_options)
            entry.bind("<KeyRelease>", self.update_data)
            if isinstance(entry, ttk.Combobox):
                entry.bind("<<ComboboxSelected>>", self.update_data)

    def update_data(self, event=None):
        ssid = self.fields["SSID"].get()
        password = self.fields["Password"].get()
        hidden = self.fields["Hidden"].get()
        auth = self.fields["Authentication"].get()

        if hidden == "True":
            hidden = "true"
        else:
            hidden = "false"

        wifi_data = f"WIFI:T:{auth};S:{ssid};P:{password};H:{hidden};"

        self.qr_code_parameters.update_data(wifi_data)
