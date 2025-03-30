import tkinter as tk
from PIL import ImageTk, Image

class WatermarkImage:
  # PIL Image objects used for processing
  _original_img = None
  _watermarked_img = None
  
  # Tkinter Image objects used for displaying the image
  _tk_img = None

  def __init__(self, root_window: tk.Tk, image_file: str):
    self._original_img = Image.open(image_file)
    self._watermarked_img = self._original_img.copy()
    self._tk_img = ImageTk.PhotoImage(self._original_img)
