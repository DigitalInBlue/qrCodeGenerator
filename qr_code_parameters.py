import tkinter as tk
from tkinter import ttk, colorchooser, filedialog
from PIL import Image, ImageTk, ImageColor
import qrcode
import qrcode.image.svg
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer, SquareModuleDrawer, CircleModuleDrawer, VerticalBarsDrawer, HorizontalBarsDrawer, GappedSquareModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask, RadialGradiantColorMask, SquareGradiantColorMask, HorizontalGradiantColorMask, VerticalGradiantColorMask, ImageColorMask
import logging
import time

logger = logging.getLogger('root')

def color_to_rgb(color):
    """
    Convert a color label or hex value to an RGB tuple.

    :param color: A string representing the color label (e.g., "black") or hex value (e.g., "#6dd380").
    :return: A tuple (R, G, B).
    """
    try:
        # Convert the color to RGB using PIL's ImageColor module
        rgb = ImageColor.getrgb(color)
        return rgb
    except ValueError as e:
        print(f"Invalid color: {color}. Error: {e}")
        return None

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
        label = ttk.Label(self.tooltip, text=self.text, background="orange", relief="solid", foreground="black", borderwidth=1, wraplength=200, padding=(5, 2))
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class QRCodeParameters(tk.LabelFrame):
    def __init__(self, parent):
        ttk.LabelFrame.__init__(self, parent, text="QR Code Parameters")

        self.debounce_job = None
        self.debounce_start_time = None

        current_row = 0
        pad_options = {"padx": 5, "pady": 5}
        grid_options = {"sticky": tk.EW, "padx": 5, "pady": 5}
        label_options = {"sticky": tk.E, "padx": 5, "pady": 5}

        self.parent = parent
        self.data = 'https://johnfarrier.com'

        ttk.Label(self, text="Error Correction:").grid(row=current_row, column=0, **label_options)
        self.entry_error_correction = ttk.Combobox(self, values=["L - Low (7%)", "M - Medium (15%)", "Q - Quartile (25%)", "H - High (30%)"])
        self.entry_error_correction.grid(row=current_row, column=1, **grid_options)
        self.entry_error_correction.current(1)
        self.entry_error_correction.bind("<<ComboboxSelected>>", self.update_preview)
        ToolTip(self.entry_error_correction, "Error correction level specifies the amount of data correction (L, M, Q, H).")
        current_row += 1

        ttk.Label(self, text="Box Size (pixels):").grid(row=current_row, column=0, **label_options)
        self.entry_box_size = ttk.Entry(self)
        self.entry_box_size.grid(row=current_row, column=1, **grid_options)
        self.entry_box_size.insert(0, "10")
        self.entry_box_size.bind("<KeyRelease>", self.update_preview)
        ToolTip(self.entry_box_size, "Box size specifies the number of pixels for each box in the QR code.")
        current_row += 1

        ttk.Label(self, text="Border (boxes):").grid(row=current_row, column=0, **label_options)
        self.entry_border = ttk.Entry(self)
        self.entry_border.grid(row=current_row, column=1, **grid_options)
        self.entry_border.insert(0, "1")
        self.entry_border.bind("<KeyRelease>", self.update_preview)
        ToolTip(self.entry_border, "Border specifies the thickness of the border (in boxes).")
        current_row += 1

        ttk.Label(self, text="Module Drawer:").grid(row=current_row, column=0, **label_options)
        self.entry_module_drawer = ttk.Combobox(self, values=["Square", "Gapped Square", "Circle", "Rounded", "Vertical Bars", "Horizontal Bars"])
        self.entry_module_drawer.grid(row=current_row, column=1, **grid_options)
        self.entry_module_drawer.current(0)
        self.entry_module_drawer.bind("<<ComboboxSelected>>", self.update_preview)
        ToolTip(self.entry_module_drawer, "Module drawer specifies the shape of the QR code modules.")
        current_row += 1

        # ttk.Label(self, text="SVG Method:").grid(row=current_row, column=0, **label_options)
        # self.svg_method = ttk.Combobox(self, values=["Basic", "Fragment", "Path Image", "Fill Image", "Path Fill Image"])
        # self.svg_method.grid(row=current_row, column=1, **grid_options)
        # self.svg_method.current(0)
        # self.svg_method.bind("<<ComboboxSelected>>", self.update_preview)
        # ToolTip(self.svg_method, "Controls how the SVG is constructed.")
        # current_row += 1

        ttk.Label(self, text="Color Mask:").grid(row=current_row, column=0, **label_options)
        self.entry_color_mask = ttk.Combobox(self, values=["Solid", "Radial Gradient", "Square Gradient", "Horizontal Gradient", "Vertical Gradient"])
        self.entry_color_mask.grid(row=current_row, column=1, **grid_options)
        self.entry_color_mask.current(0)
        self.entry_color_mask.bind("<<ComboboxSelected>>", self.update_preview)
        ToolTip(self.entry_color_mask, "Color mask specifies the color filling method for the QR code.")
        current_row += 1

        self.background_color = "white"
        self.color_accent_1 = "red"
        self.color_accent_2 = "blue"

        # Color selection
        ttk.Label(self, text="Background Color:").grid(row=current_row, column=0, **label_options)
        self.background_color_button = ttk.Button(self, text="Select", command=self.select_background_color)
        self.background_color_button.grid(row=current_row, column=1, **grid_options)
        self.background_color_swatch = ttk.Label(self, background=self.background_color, width=2)
        self.background_color_swatch.grid(row=current_row, column=2, **grid_options)
        self.background_color_swatch.bind("<KeyRelease>", self.update_preview)
        current_row += 1

        ttk.Label(self, text="Color Accent 1:").grid(row=current_row, column=0, **label_options)
        self.color_accent_1_button = ttk.Button(self, text="Select", command=self.select_color_accent_1)
        self.color_accent_1_button.grid(row=current_row, column=1, **grid_options)
        self.color_accent_1_swatch = ttk.Label(self, background=self.color_accent_1, width=2)
        self.color_accent_1_swatch.grid(row=current_row, column=2, **grid_options)
        self.color_accent_1_swatch.bind("<KeyRelease>", self.update_preview)
        current_row += 1

        ttk.Label(self, text="Color Accent 2:").grid(row=current_row, column=0, **label_options)
        self.color_accent_2_button = ttk.Button(self, text="Select", command=self.select_color_accent_2)
        self.color_accent_2_button.grid(row=current_row, column=1, **grid_options)
        self.color_accent_2_swatch = ttk.Label(self, background=self.color_accent_2, width=2)
        self.color_accent_2_swatch.grid(row=current_row, column=2, **grid_options)
        self.color_accent_2_swatch.bind("<KeyRelease>", self.update_preview)
        current_row += 1

        # QR Code preview
        preview_canvas_width = 256
        preview_canvas_height = 256
        self.preview_canvas = tk.Canvas(self, width=preview_canvas_width, height=preview_canvas_height, bg="white", bd=2)
        self.preview_canvas.grid(row=current_row, column=0, columnspan=3, **pad_options)

        # Busy overlay canvas
        self.busy_canvas = tk.Canvas(self.preview_canvas, width=preview_canvas_width, height=preview_canvas_height, bg="white", bd=0, highlightthickness=0)
        self.busy_text = self.busy_canvas.create_text(preview_canvas_width/2, preview_canvas_height/2, text="Rendering...", fill="black", font=("Helvetica", 16))
        self.busy_canvas.pack_forget()
        current_row += 1

        # Button to save the SVG file
        self.write_svg_button = ttk.Button(self, text="Export QR Code", command=self.write)
        self.write_svg_button.grid(row=current_row, column=2, columnspan=1, **grid_options)
        current_row += 1

    def select_color_accent_1(self):
        self.color_accent_1 = colorchooser.askcolor(title="Choose Color")[1] or self.color_accent_1
        self.color_accent_1_swatch.config(background=self.color_accent_1)
        self.update_preview()

    def select_color_accent_2(self):
        self.color_accent_2 = colorchooser.askcolor(title="Choose Color")[1] or self.color_accent_2
        self.color_accent_2_swatch.config(background=self.color_accent_2)
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

    def select_background_image(self):
        self.background_image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if self.background_image_path:
            self.background_image_label.config(text=self.background_image_path.split("/")[-1])
        else:
            self.background_image_label.config(text="No image selected")
        self.update_preview()

    def generate_qr_code(self):
        qr = qrcode.QRCode(
            version=self.get_minimum_qr_version(self.data),
            error_correction=self.get_error_correction(self.entry_error_correction.get().split()[0]),
            box_size=int(self.entry_box_size.get()),
            border=int(self.entry_border.get()),
        )

        qr.add_data(self.data)
        qr.make(fit=True)

        # Select the module drawer based on user selection
        module_drawer_option = self.entry_module_drawer.get()
        module_drawer = {
            "Square": SquareModuleDrawer(),
            "Gapped Square": GappedSquareModuleDrawer(),
            "Circle": CircleModuleDrawer(),
            "Rounded": RoundedModuleDrawer(),
            "Vertical Bars": VerticalBarsDrawer(),
            "Horizontal Bars": HorizontalBarsDrawer(),
        }.get(module_drawer_option, SquareModuleDrawer())

        # Select color mask
        color_mask_option = self.entry_color_mask.get()
        color_mask = {
            "Solid": SolidFillColorMask(back_color=color_to_rgb(self.background_color)),
            "Radial Gradient": RadialGradiantColorMask(back_color=color_to_rgb(self.background_color), center_color=color_to_rgb(self.color_accent_1), edge_color=color_to_rgb(self.color_accent_2)),
            "Square Gradient": SquareGradiantColorMask(back_color=color_to_rgb(self.background_color), center_color=color_to_rgb(self.color_accent_1), edge_color=color_to_rgb(self.color_accent_2)),
            "Horizontal Gradient": HorizontalGradiantColorMask(back_color=color_to_rgb(self.background_color), left_color=color_to_rgb(self.color_accent_1), right_color=color_to_rgb(self.color_accent_2)),
            "Vertical Gradient": VerticalGradiantColorMask(back_color=color_to_rgb(self.background_color), top_color=color_to_rgb(self.color_accent_1), bottom_color=color_to_rgb(self.color_accent_2)),
        }.get(color_mask_option, None)

        # Create the image
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=module_drawer,
            color_mask=color_mask
        ).convert("RGBA")

        return img

    def update_data(self, new_data):
        self.data = new_data
        #logger.info(f"Data updated: {self.data}")
        self.update_preview()

    def update_preview(self, event=None):
        if self.debounce_job is not None:
            self.after_cancel(self.debounce_job)

        # Show the busy canvas
        current_time = time.time()
        if self.debounce_start_time is None:
            self.debounce_start_time = current_time

        if current_time - self.debounce_start_time > 1.3:
            # Show the busy canvas
            self.busy_canvas.pack()

        self.debounce_job = self.after(300, self._do_update_preview)

    def _do_update_preview(self, event=None):
        canvas_width = self.preview_canvas.winfo_width()
        canvas_height = self.preview_canvas.winfo_height()

        img = self.generate_qr_code()
        img.thumbnail((canvas_width, canvas_height), Image.Resampling.LANCZOS)

        self.qr_preview_image = ImageTk.PhotoImage(img)
        self.preview_canvas.create_image(canvas_width // 2, canvas_height // 2, image=self.qr_preview_image)

        # Hide the busy canvas
        self.busy_canvas.pack_forget()

        self.debounce_job = None
        self.debounce_start_time = None  # Reset the debounce start time

    def write(self):
        img = self.generate_qr_code()

        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            img.save(file_path)

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
                border=1
            )
            try:
                qr.add_data(data)
                qr.make(fit=True)
                return version
            except qrcode.exceptions.DataOverflowError:
                continue
        return None  # If no suitable version is found
