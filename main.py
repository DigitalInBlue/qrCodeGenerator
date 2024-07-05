import tkinter as tk
from tkinter import ttk
from vcard_qr import VCardQRGenerator
from qr_code_parameters import QRCodeParameters

# Function to show the relevant frame based on the selected QR code type
def show_frame(frame):
    frame.tkraise()

# Main window setup
root = tk.Tk()
root.title("QR Code Generator")

grid_options = {"sticky": tk.W, "padx": 5, "pady": 5}
label_options = {"sticky": tk.E, "padx": 5, "pady": 5}

# Container for layout
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

# Left column frame
left_frame = tk.Frame(main_frame)
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

# Right column frame
right_frame = tk.Frame(main_frame)
right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

# Dropdown menu to select QR code type at the top of the left column
qr_type = tk.StringVar()
qr_type_menu = ttk.Combobox(left_frame, textvariable=qr_type)
qr_type_menu['values'] = ('VCard', 'Calendar', 'URL', 'Location', 'Social Media', 'Audio')
qr_type_menu.grid(row=0, column=0, sticky=tk.EW, padx=10, pady=10)
qr_type_menu.current(0)

# Container for different QR code type frames
container = tk.Frame(left_frame)
container.grid(row=1, column=0, padx=10, pady=10)

# Define frames for different QR code types
frames = {}

for F in (VCardQRGenerator,):
    page_name = F.__name__
    frame = F(parent=container, controller=root)
    frames[page_name] = frame
    frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

# QR Code parameters section in the right column
qr_code_parameters = QRCodeParameters(right_frame)
qr_code_parameters.grid(row=0, column=0, padx=5, pady=5)

# Update the frame shown based on dropdown selection
qr_type_menu.bind("<<ComboboxSelected>>", lambda e: show_frame(frames[qr_type.get()]))

# Start with the vCard frame
show_frame(frames["VCardQRGenerator"])

root.mainloop()
