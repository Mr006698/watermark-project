import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image, ImageDraw, ImageFont
from system_fonts import SystemFonts

class AutoScrollbar(ttk.Scrollbar):
  def set(self, low, high):
    if float(low) <= 0.0 and float(high) >= 1.0:
      self.grid_remove()
    else:
      self.grid()
      ttk.Scrollbar.set(self, low, high)
    
  
  def pack(self, **kwargs):
    raise tk.TclError('Cannot use pack with this widget')
  

  def place(self, **kwargs):
    raise tk.TclError('Cannot use place with this widget')


class ImageContainer(ttk.Frame):
  _backup_img = None
  _original_img = None
  _tk_image = None
  _scale_image = False
  _scale_factor = 1.0

  def __init__(self, parent: tk.Tk, system_fonts: SystemFonts):
    # Call the parent class constructor
    super().__init__(master=parent)

    # Save reference to the system fonts
    self._system_fonts = system_fonts

    # Vertical and horizontal scrollbars
    vertical_scrollbar = AutoScrollbar(self, orient='vertical')
    vertical_scrollbar.grid(row=0, column=1, sticky='ns')
    horizontal_scrollbar = AutoScrollbar(self, orient='horizontal')
    horizontal_scrollbar.grid(row=1, column=0, sticky='ew')

    # Create the canvas
    self._canvas = tk.Canvas(
      self,
      bg='black',
      highlightthickness=0,
      xscrollcommand=horizontal_scrollbar.set,
      yscrollcommand=vertical_scrollbar.set
    )

    self._canvas.grid(row=0, column=0, sticky='nsew')
    self._canvas.update_idletasks()
    vertical_scrollbar.config(command=self._canvas.yview)
    horizontal_scrollbar.config(command=self._canvas.xview)
    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)

    # Bind the mouse wheel to the canvas
    self._canvas.bind('<MouseWheel>', None)  # with Windows and MacOS, but not Linux
    self._canvas.bind('<Button-5>',   None)  # only with Linux, wheel scroll down
    self._canvas.bind('<Button-4>',   None)  # only with Linux, wheel scroll up


  def load_image(self, filename: str) -> None:
    # Load the image
    self._backup_img = Image.open(filename)
    self._original_img = self._backup_img.copy() #Image.open(filename)
    self._scale_factor = 1.0
    self._show_image()
  

  def rotate_image(self, angle: int) -> None:
    if self._original_img is None:
      return
    
    self._original_img = self._original_img.rotate(angle, expand=True)
    self._show_image()


  def fit_to_window(self) -> None:
    if self._original_img is None:
      return
    
    self._scale_image = True
    self._show_image()


  def actual_size(self) -> None:
    if self._original_img is None:
      return
    
    self._scale_factor = 1.0
    self._show_image()


  def add_watermark(self, text: str, font: str, font_size: int, colour: str) -> None:
    if self._original_img is None:
      return
    
    draw_img = ImageDraw.Draw(self._original_img)
    font_file = self._system_fonts.get_font_path(font)
    font = ImageFont.truetype(font_file, size=font_size)

    text_box = draw_img.textbbox((0, 0), text, font)
    margin = 10
    img_width, img_height = self._original_img.size
    position = (img_width - text_box[2] - margin, img_height - text_box[3] - margin)
    draw_img.text(position, text, font=font, fill=colour)

    self._show_image()


  def reset_image(self) -> None:
    if self._backup_img is None:
      return
    
    self._original_img = self._backup_img.copy()
    self._show_image()


  def _show_image(self) -> None:
    if self._original_img is None:
      return
    
    # Destroy all existing widgets on the canvas
    self._canvas.delete('all')

    img_width, img_height = self._original_img.size

    if self._scale_image:
      # Get the size of the canvas
      canvas_width = self._canvas.winfo_width()
      canvas_height = self._canvas.winfo_height()

      # Only scale if the image is larger than the canvas
      if img_width > canvas_width or img_height > canvas_height:
        # Calculate the scale factor to fit the image within the canvas
        self._scale_factor = min(canvas_width / img_width, canvas_height / img_height)

      else:
        self._scale_factor = min(canvas_width / img_width, canvas_height / img_height)

      # Reset the scale image flag
      self._scale_image = False

    # Scale the image copy to the scale factor
    img_copy = self._original_img.copy()
    if self._scale_factor != 1.0:
      # Resize the image
      new_size = (int(img_width * self._scale_factor), int(img_height * self._scale_factor))
      img_copy = self._original_img.resize(new_size, Image.Resampling.NEAREST)

    # Set the canvas scroll region to the image size
    copy_width, copy_height = img_copy.size
    self._canvas.config(scrollregion=(0, 0, copy_width, copy_height))

    # Display the image on the canvas
    self._tk_img = ImageTk.PhotoImage(img_copy)
    self._canvas.create_image(0, 0, anchor=tk.NW, image=self._tk_img)
    