import tkinter as tk
from tkinter import ttk, colorchooser, filedialog
from PIL import Image, ImageTk
import qrcode
import logging

logger = logging.getLogger('root')

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
        self.tooltip = None

    def show_tooltip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text, background="yellow", relief="solid", borderwidth=1, wraplength=200)
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class QRCodeParameters(tk.LabelFrame):
    def __init__(self, parent):
        tk.LabelFrame.__init__(self, parent, text="QR Code Parameters")

        current_row = 0
        grid_options = {"sticky": tk.EW, "padx": 5, "pady": 5}
        label_options = {"sticky": tk.E, "padx": 5, "pady": 5}

        self.parent = parent
        self.data = 'https://johnfarrier.com'

        tk.Label(self, text="Error Correction:").grid(row=current_row, column=0, **label_options)
        self.entry_error_correction = ttk.Combobox(self, values=["L - Low (7%)", "M - Medium (15%)", "Q - Quartile (25%)", "H - High (30%)"])
        self.entry_error_correction.grid(row=current_row, column=1, **grid_options)
        self.entry_error_correction.current(1)
        self.entry_error_correction.bind("<<ComboboxSelected>>", self.update_preview)
        ToolTip(self.entry_error_correction, "Error correction level specifies the amount of data correction (L, M, Q, H).")
        current_row += 1

        tk.Label(self, text="Box Size:").grid(row=current_row, column=0, **label_options)
        self.entry_box_size = tk.Entry(self)
        self.entry_box_size.grid(row=current_row, column=1, **grid_options)
        self.entry_box_size.insert(0, "10")
        self.entry_box_size.bind("<KeyRelease>", self.update_preview)
        ToolTip(self.entry_box_size, "Box size specifies the number of pixels for each box in the QR code.")
        current_row += 1

        tk.Label(self, text="Border:").grid(row=current_row, column=0, **label_options)
        self.entry_border = tk.Entry(self)
        self.entry_border.grid(row=current_row, column=1, **grid_options)
        self.entry_border.insert(0, "4")
        self.entry_border.bind("<KeyRelease>", self.update_preview)
        ToolTip(self.entry_border, "Border specifies the thickness of the border (in boxes).")
        current_row += 1

        tk.Label(self, text="Module Drawer:").grid(row=current_row, column=0, **label_options)
        self.entry_module_drawer = ttk.Combobox(self, values=["Square", "GappedSquare", "Circle"])
        self.entry_module_drawer.grid(row=current_row, column=1, **grid_options)
        self.entry_module_drawer.current(0)
        self.entry_module_drawer.bind("<<ComboboxSelected>>", self.update_preview)
        ToolTip(self.entry_module_drawer, "Module drawer specifies the shape of the QR code modules.")
        current_row += 1

        tk.Label(self, text="Color Mask:").grid(row=current_row, column=0, **label_options)
        self.entry_color_mask = ttk.Combobox(self, values=["Solid", "RadialGradient", "SquareGradient", "HorizontalGradient"])
        self.entry_color_mask.grid(row=current_row, column=1, **grid_options)
        self.entry_color_mask.current(0)
        self.entry_color_mask.bind("<<ComboboxSelected>>", self.update_preview)
        ToolTip(self.entry_color_mask, "Color mask specifies the color filling method for the QR code.")
        current_row += 1

        # Color selection
        tk.Label(self, text="Fill Color:").grid(row=current_row, column=0, **label_options)
        self.fill_color_button = tk.Button(self, text="Select Fill Color", command=self.select_fill_color)
        self.fill_color_button.grid(row=current_row, column=1, **grid_options)
        self.fill_color_swatch = tk.Label(self, background="black", width=2, height=1)
        self.fill_color_swatch.grid(row=current_row, column=2, **grid_options)
        self.fill_color_swatch.bind("<KeyRelease>", self.update_preview)
        current_row += 1

        tk.Label(self, text="Background Color:").grid(row=current_row, column=0, **label_options)
        self.background_color_button = tk.Button(self, text="Select Background Color", command=self.select_background_color)
        self.background_color_button.grid(row=current_row, column=1, **grid_options)
        self.background_color_swatch = tk.Label(self, background="white", width=2, height=1)
        self.background_color_swatch.grid(row=current_row, column=2, **grid_options)
        self.background_color_swatch.bind("<KeyRelease>", self.update_preview)
        current_row += 1

        self.fill_color = "black"
        self.background_color = "white"

        # Logo image selection
        tk.Label(self, text="Logo Image:").grid(row=current_row, column=0, **label_options)
        self.logo_image_button = tk.Button(self, text="Select Logo Image", command=self.select_logo_image)
        self.logo_image_button.grid(row=current_row, column=1, **grid_options)
        self.logo_image_label = tk.Label(self, text="No image selected")
        self.logo_image_label.grid(row=current_row, column=2, **grid_options)
        self.logo_image_label.bind("<KeyRelease>", self.update_preview)
        current_row += 1

        self.logo_image_path = None

        # QR Code preview
        self.preview_label = tk.Label(self, text="QR Code Preview:")
        self.preview_label.grid(row=current_row, sticky=tk.W, column=0, columnspan=3)
        current_row += 1

        self.update_preview_button = tk.Button(self, text="Update Preview", command=self.update_preview)
        self.update_preview_button.grid(row=current_row, column=0, columnspan=1)
        self.preview_canvas = tk.Canvas(self, width=200, height=200, bg="white", bd=2)
        self.preview_canvas.grid(row=current_row, column=1, columnspan=2)
        current_row += 1

        # Base file name entry
        tk.Label(self, text="Base File Name:").grid(row=current_row, column=0, sticky=tk.E)
        self.entry_base_name = tk.Entry(self)
        self.entry_base_name.grid(row=current_row, column=1, **grid_options)
        current_row += 1

    def select_fill_color(self):
        self.fill_color = colorchooser.askcolor(title="Choose Fill Color")[1] or self.fill_color
        self.fill_color_swatch.config(background=self.fill_color)
        self.update_preview()

    def select_background_color(self):
        self.background_color = colorchooser.askcolor(title="Choose Background Color")[1] or self.background_color
        self.background_color_swatch.config(background=self.background_color)
        self.update_preview()

    def select_logo_image(self):
        self.logo_image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if self.logo_image_path:
            self.logo_image_label.config(text=self.logo_image_path.split("/")[-1])
        else:
            self.logo_image_label.config(text="No image selected")
        self.update_preview()

    def update_data(self, new_data):
        self.data = new_data
        logger.info(f'Data: "{self.data}"')
        self.update_preview()

    def update_preview(self, event=None):
        # Get the dimensions of the canvas
        canvas_width = self.preview_canvas.winfo_width()
        canvas_height = self.preview_canvas.winfo_height()

        qr = qrcode.QRCode(
            #version=1,
            error_correction=self.get_error_correction(self.entry_error_correction.get().split()[0]),
            box_size=int(self.entry_box_size.get()),
            border=int(self.entry_border.get()),
        )
        qr.add_data(self.data)
        qr.make(fit=True)

        img = qr.make_image(
            fill_color=self.fill_color,
            back_color=self.background_color
        ).convert("RGBA")

        # Resize the image to fit the canvas while maintaining aspect ratio
        img.thumbnail((canvas_width, canvas_height), Image.Resampling.LANCZOS)

        if self.logo_image_path:
            logo = Image.open(self.logo_image_path)
            logo = logo.resize((50, 50), Image.Resampling.LANCZOS)
            img.paste(logo, (int((img.size[0] - logo.size[0]) / 2), int((img.size[1] - logo.size[1]) / 2)), logo)

        self.qr_preview_image = ImageTk.PhotoImage(img)
        self.preview_canvas.create_image(canvas_width // 2, canvas_height // 2, image=self.qr_preview_image)

    def get_error_correction(self, level):
        error_correction_map = {
            "L": qrcode.constants.ERROR_CORRECT_L,
            "M": qrcode.constants.ERROR_CORRECT_M,
            "Q": qrcode.constants.ERROR_CORRECT_Q,
            "H": qrcode.constants.ERROR_CORRECT_H
        }
        return error_correction_map.get(level, qrcode.constants.ERROR_CORRECT_L)

    def get_minimum_qr_version(self, data):
        for version in range(1, 41):
            qr = qrcode.QRCode(
                version=version,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4
            )
            try:
                qr.add_data(data)
                qr.make(fit=True)
                return version
            except qrcode.exceptions.DataOverflowError:
                continue
        return None  # If no suitable version is found
