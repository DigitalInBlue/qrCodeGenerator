import tkinter as tk
from tkinter import filedialog
import qrcode
import vobject
import logging
#from main import qr_code_parameters  # Import the QRCodeParameters from main

# Set up the logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VCardQRGenerator(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        grid_options = {"sticky": tk.EW, "padx": 5, "pady": 5}
        label_options = {"sticky": tk.E, "padx": 5, "pady": 5}

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # VCard data entry section
        frame_vcard = tk.LabelFrame(self, text="VCard Data")
        frame_vcard.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        tk.Label(frame_vcard, text="First Name:").grid(row=0, column=0, **label_options)
        self.entry_fn = tk.Entry(frame_vcard)
        self.entry_fn.grid(row=0, column=1, **grid_options)

        tk.Label(frame_vcard, text="Last Name:").grid(row=1, column=0, **label_options)
        self.entry_ln = tk.Entry(frame_vcard)
        self.entry_ln.grid(row=1, column=1, **grid_options)

        tk.Label(frame_vcard, text="Telephone:").grid(row=2, column=0, **label_options)
        self.entry_tel = tk.Entry(frame_vcard)
        self.entry_tel.grid(row=2, column=1, **grid_options)

        tk.Label(frame_vcard, text="Email:").grid(row=3, column=0, **label_options)
        self.entry_email = tk.Entry(frame_vcard)
        self.entry_email.grid(row=3, column=1, **grid_options)

        tk.Label(frame_vcard, text="URL 1:").grid(row=4, column=0, **label_options)
        self.entry_url = tk.Entry(frame_vcard)
        self.entry_url.grid(row=4, column=1, **grid_options)

        tk.Label(frame_vcard, text="URL 2:").grid(row=5, column=0, **label_options)
        self.entry_url2 = tk.Entry(frame_vcard)
        self.entry_url2.grid(row=5, column=1, **grid_options)

        tk.Label(frame_vcard, text="LinkedIn:").grid(row=6, column=0, **label_options)
        self.entry_social = tk.Entry(frame_vcard)
        self.entry_social.grid(row=6, column=1, **grid_options)

        tk.Label(frame_vcard, text="Organization:").grid(row=7, column=0, **label_options)
        self.entry_org = tk.Entry(frame_vcard)
        self.entry_org.grid(row=7, column=1, **grid_options)

        tk.Label(frame_vcard, text="Title:").grid(row=8, column=0, **label_options)
        self.entry_title = tk.Entry(frame_vcard)
        self.entry_title.grid(row=8, column=1, **grid_options)

        tk.Label(frame_vcard, text="Photo URL:").grid(row=9, column=0, **label_options)
        self.entry_photo = tk.Entry(frame_vcard)
        self.entry_photo.grid(row=9, column=1, **grid_options)

        tk.Label(frame_vcard, text="Note:").grid(row=10, column=0, **label_options)
        self.entry_note = tk.Entry(frame_vcard)
        self.entry_note.grid(row=10, column=1, **grid_options)

        tk.Label(frame_vcard, text="Language:").grid(row=11, column=0, **label_options)
        self.entry_lang = tk.Entry(frame_vcard)
        self.entry_lang.grid(row=11, column=1, **grid_options)

        tk.Label(frame_vcard, text="Time Zone:").grid(row=12, column=0, **label_options)
        self.entry_tz = tk.Entry(frame_vcard)
        self.entry_tz.grid(row=12, column=1, **grid_options)

        # Save and Generate button
        btn_save = tk.Button(self, text="Save VCard and Generate QR Code", command=self.save_vcard)
        btn_save.grid(row=2, column=0, columnspan=2, **grid_options)

    # Function to generate and save VCard
    def save_vcard(self):
        base_name = self.entry_base_name.get()
        vcard_data = f"""BEGIN:VCARD
VERSION:4.0
FN:{self.entry_fn.get()}
N:{self.entry_ln.get()};{self.entry_fn.get()};;;
TEL;TYPE=WORK,VOICE,pref:{self.entry_tel.get()}
EMAIL:{self.entry_email.get()}
URL:{self.entry_url.get()}
URL:{self.entry_url2.get()}
X-SOCIALPROFILE;type=linkedin:{self.entry_social.get()}
ORG:{self.entry_org.get()}
TITLE:{self.entry_title.get()}
PHOTO;VALUE=uri:{self.entry_photo.get()}
NOTE:{self.entry_note.get()}
LANG:{self.entry_lang.get()}
TZ:{self.entry_tz.get()}
END:VCARD"""

        vcf_file_path = f"{base_name}.vcf"
        with open(vcf_file_path, "w") as vcf_file:
            vcf_file.write(vcard_data)
        logger.info(f"VCard saved to {vcf_file_path}")
        self.generate_qr_code(vcard_data, base_name)

    # Function to generate and save QR code
    def generate_qr_code(self, vcard_data, base_name):
        qr = qrcode.QRCode(
            version=int(qr_code_parameters.entry_version.get().split()[0]),
            error_correction=self.get_error_correction(qr_code_parameters.entry_error_correction.get().split()[0]),
            box_size=int(qr_code_parameters.entry_box_size.get()),
            border=int(qr_code_parameters.entry_border.get()),
        )
        qr.add_data(vcard_data)
        qr.make(fit=True)

        fill_color = qr_code_parameters.fill_color
        back_color = qr_code_parameters.background_color

        qr_image = qr.make_image(
            fill_color=fill_color,
            back_color=back_color
        )

        qr_image_path = f"{base_name}.png"
        qr_image.save(qr_image_path)
        logger.info(f"QR code saved to {qr_image_path}")

    def get_error_correction(self, level):
        error_correction_map = {
            "L": qrcode.constants.ERROR_CORRECT_L,
            "M": qrcode.constants.ERROR_CORRECT_M,
            "Q": qrcode.constants.ERROR_CORRECT_Q,
            "H": qrcode.constants.ERROR_CORRECT_H
        }
        return error_correction_map.get(level, qrcode.constants.ERROR_CORRECT_L)
