import tkinter as tk
from tkinter import filedialog
import qrcode
import vobject
import logging

logger = logging.getLogger('root')

class VCardQRGenerator(tk.Frame):
    def __init__(self, parent, controller, qr_code_parameters):
        tk.Frame.__init__(self, parent)
        self.qr_code_parameters = qr_code_parameters
        self.controller = controller

        grid_options = {"sticky": tk.EW, "padx": 5, "pady": 5}
        label_options = {"sticky": tk.E, "padx": 5, "pady": 5}

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # VCard data entry section
        frame_vcard = tk.LabelFrame(self, text="VCard Data")
        frame_vcard.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        self.fields = {
            "First Name": tk.Entry(frame_vcard),
            "Last Name": tk.Entry(frame_vcard),
            "Telephone": tk.Entry(frame_vcard),
            "Email": tk.Entry(frame_vcard),
            "URL 1": tk.Entry(frame_vcard),
            "URL 2": tk.Entry(frame_vcard),
            "LinkedIn": tk.Entry(frame_vcard),
            "Organization": tk.Entry(frame_vcard),
            "Title": tk.Entry(frame_vcard),
            "Photo URL": tk.Entry(frame_vcard),
            "Note": tk.Entry(frame_vcard),
            "Language": tk.Entry(frame_vcard),
            "Time Zone": tk.Entry(frame_vcard)
        }

        for idx, (label_text, entry) in enumerate(self.fields.items()):
            tk.Label(frame_vcard, text=label_text).grid(row=idx, column=0, **label_options)
            entry.grid(row=idx, column=1, **grid_options)
            entry.bind("<KeyRelease>", self.update_data)

    def update_data(self, event=None):
        vcard_lines = ["BEGIN:VCARD", "VERSION:4.0"]

        fn = self.fields["First Name"].get()
        ln = self.fields["Last Name"].get()
        if fn or ln:
            vcard_lines.append(f"FN:{fn}")
            vcard_lines.append(f"N:{ln};{fn};;;")

        tel = self.fields["Telephone"].get()
        if tel:
            vcard_lines.append(f"TEL;TYPE=WORK,VOICE,pref:{tel}")

        email = self.fields["Email"].get()
        if email:
            vcard_lines.append(f"EMAIL:{email}")

        url = self.fields["URL 1"].get()
        if url:
            vcard_lines.append(f"URL:{url}")

        url2 = self.fields["URL 2"].get()
        if url2:
            vcard_lines.append(f"URL:{url2}")

        linkedin = self.fields["LinkedIn"].get()
        if linkedin:
            vcard_lines.append(f"X-SOCIALPROFILE;type=linkedin:{linkedin}")

        org = self.fields["Organization"].get()
        if org:
            vcard_lines.append(f"ORG:{org}")

        title = self.fields["Title"].get()
        if title:
            vcard_lines.append(f"TITLE:{title}")

        photo = self.fields["Photo URL"].get()
        if photo:
            vcard_lines.append(f"PHOTO;VALUE=uri:{photo}")

        note = self.fields["Note"].get()
        if note:
            vcard_lines.append(f"NOTE:{note}")

        lang = self.fields["Language"].get()
        if lang:
            vcard_lines.append(f"LANG:{lang}")

        tz = self.fields["Time Zone"].get()
        if tz:
            vcard_lines.append(f"TZ:{tz}")

        vcard_lines.append("END:VCARD")
        vcard_data = "\n".join(vcard_lines)

        self.qr_code_parameters.update_data(vcard_data)
