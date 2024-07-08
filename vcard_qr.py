import tkinter as tk
from tkinter import ttk, filedialog
import qrcode
import vobject
import logging

logger = logging.getLogger('root')

class VCardQRGenerator(ttk.Frame):
    def __init__(self, parent, controller, qr_code_parameters):
        ttk.Frame.__init__(self, parent)
        self.qr_code_parameters = qr_code_parameters
        self.controller = controller

        grid_options = {"sticky": tk.EW, "padx": 5, "pady": 5}
        label_options = {"sticky": tk.E, "padx": 5, "pady": 5}

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # VCard data entry section
        frame_vcard = ttk.LabelFrame(self, text="VCard Data")
        frame_vcard.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        field_options = {"width": 40}

        self.fields = {
            "First Name": ttk.Entry(frame_vcard, **field_options),
            "Last Name": ttk.Entry(frame_vcard, **field_options),
            "Title": ttk.Entry(frame_vcard, **field_options),
            "Organization": ttk.Entry(frame_vcard, **field_options),
            "--------0": None,
            "Telephone (Work)": ttk.Entry(frame_vcard, **field_options),
            "Telephone (Cell)": ttk.Entry(frame_vcard, **field_options),
            "Telephone (Home)": ttk.Entry(frame_vcard, **field_options),
            "--------1": None,
            "Email (Work)": ttk.Entry(frame_vcard, **field_options),
            "Email (Personal)": ttk.Entry(frame_vcard, **field_options),
            "--------2": None,
            "URL 1": ttk.Entry(frame_vcard, **field_options),
            "URL 2": ttk.Entry(frame_vcard, **field_options),
            "LinkedIn URL": ttk.Entry(frame_vcard, **field_options),
            "Twitter URL": ttk.Entry(frame_vcard, **field_options),
            "Facebook URL": ttk.Entry(frame_vcard, **field_options),
            "--------4": None,
            "Address (Work)": ttk.Entry(frame_vcard, **field_options),
            "Address (Home)": ttk.Entry(frame_vcard, **field_options),
            "--------5": None,
            "Photo URL": ttk.Entry(frame_vcard, **field_options),
            "--------6": None,
            "Note": ttk.Entry(frame_vcard, **field_options),
            "--------7": None,
            "Language": ttk.Combobox(frame_vcard, values=["en", "es", "fr", "de", "zh", "ja"], **field_options),
            "Time Zone": ttk.Combobox(frame_vcard, values=["America/New_York", "America/Chicago", "America/Denver", "America/Los_Angeles", "Europe/London", "Europe/Berlin", "Asia/Tokyo"], **field_options),
            "Birthday": ttk.Entry(frame_vcard, **field_options),
            "Gender": ttk.Combobox(frame_vcard, values=["M", "F", "O"], **field_options),
        }

        for idx, (label_text, entry) in enumerate(self.fields.items()):
            if label_text.startswith("--------") == False:
                ttk.Label(frame_vcard, text=label_text).grid(row=idx, column=0, **label_options)
                entry.grid(row=idx, column=1, **grid_options)
                entry.bind("<KeyRelease>", self.update_data)
            else:
                separator = ttk.Frame(frame_vcard, height=2, relief=tk.SUNKEN)
                separator.grid(row=idx, column=0, columnspan=2, pady=10, sticky=tk.EW)

    def update_data(self, event=None):
        vcard_lines = ["BEGIN:VCARD", "VERSION:4.0"]

        fn = self.fields["First Name"].get()
        ln = self.fields["Last Name"].get()
        if fn or ln:
            vcard_lines.append(f"FN:{fn}")
            vcard_lines.append(f"N:{ln};{fn};;;")

        tel_work = self.fields["Telephone (Work)"].get()
        if tel_work:
            vcard_lines.append(f"TEL;TYPE=WORK,VOICE,pref:{tel_work}")

        tel_home = self.fields["Telephone (Home)"].get()
        if tel_home:
            vcard_lines.append(f"TEL;TYPE=HOME,VOICE:{tel_home}")

        tel_cell = self.fields["Telephone (Cell)"].get()
        if tel_cell:
            vcard_lines.append(f"TEL;TYPE=CELL,VOICE:{tel_cell}")

        email_personal = self.fields["Email (Personal)"].get()
        if email_personal:
            vcard_lines.append(f"EMAIL:{email_personal}")

        email_work = self.fields["Email (Work)"].get()
        if email_work:
            vcard_lines.append(f"EMAIL;TYPE=WORK:{email_work}")

        url1 = self.fields["URL 1"].get()
        if url1:
            vcard_lines.append(f"URL:{url1}")

        url2 = self.fields["URL 2"].get()
        if url2:
            vcard_lines.append(f"URL:{url2}")

        linkedin = self.fields["LinkedIn URL"].get()
        if linkedin:
            vcard_lines.append(f"X-SOCIALPROFILE;type=linkedin:{linkedin}")

        twitter = self.fields["Twitter URL"].get()
        if twitter:
            vcard_lines.append(f"X-SOCIALPROFILE;type=twitter:{twitter}")

        facebook = self.fields["Facebook URL"].get()
        if facebook:
            vcard_lines.append(f"X-SOCIALPROFILE;type=facebook:{facebook}")

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

        addr_work = self.fields["Address (Work)"].get()
        if addr_work:
            vcard_lines.append(f"ADR;TYPE=WORK:{addr_work}")

        addr_home = self.fields["Address (Home)"].get()
        if addr_home:
            vcard_lines.append(f"ADR;TYPE=HOME:{addr_home}")

        bday = self.fields["Birthday"].get()
        if bday:
            vcard_lines.append(f"BDAY:{bday}")

        gender = self.fields["Gender"].get()
        if gender:
            vcard_lines.append(f"GENDER:{gender}")

        vcard_lines.append("END:VCARD")
        vcard_data = "\n".join(vcard_lines)

        self.qr_code_parameters.update_data(vcard_data)
