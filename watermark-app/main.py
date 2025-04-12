import tkinter as tk
from tkinter import ttk, filedialog
from ctypes import windll

from control_panel import WatermarkControlPanel, ImageControlPanel
from image_container import ImageContainer
from system_fonts import SystemFonts


class WatermarkApp:
  def __init__(self):
    # Create the root window
    windll.shcore.SetProcessDpiAwareness(1) # Remove blurry text on high DPI screens
    self._root_window = tk.Tk()
    self._root_window.title('Image Watermarker')
    self._root_window.geometry('1280x800')
    self._root_window.minsize(640, 400)

    # Cache the system fonts
    self._system_fonts = SystemFonts(self._root_window)

    # Hide the root window untill all
    # widgets are created and positioned
    self._root_window.withdraw()

    # Load the theme
    self._load_theme()

    # Create the control panel
    self._watermark_control_panel = WatermarkControlPanel(self._root_window, self._system_fonts.get_tk_fonts(), self._add_watermark)
    self._watermark_control_panel.pack(side=tk.TOP, expand=False, fill=tk.X, padx=5, pady=5)

    # Create the image control panel
    self._image_control_panel = ImageControlPanel(
      self._root_window,
      self._load_image,
      self._save_image,
      self._fit_to_window,
      self._actual_size,
      self._rotate_image,
      self._reset_image)
    
    self._image_control_panel.pack(side=tk.LEFT, expand=False, fill=tk.Y, padx=5, pady=5)

    # Create the image container
    self._image_container = ImageContainer(self._root_window, self._system_fonts)
    self._image_container.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    # Center the root window
    self._center_window(self._root_window)

    # Show the root window
    self._root_window.deiconify()


  def run(self):
    self._root_window.mainloop()

  
  def _load_image(self) -> None:
    filename = filedialog.askopenfilename(
      title='Select an image',
      filetypes=[('Image files', '*.png *.jpg *.jpeg')]
    )

    if filename:
      # Load the image
      self._image_container.load_image(filename)

  
  def _save_image(self) -> None:
    print(f'{self.__class__.__name__}: _save_image() called.')


  def _actual_size(self) -> None:
    self._image_container.actual_size()

  
  def _rotate_image(self, angle: int) -> None:
    self._image_container.rotate_image(angle)


  def _fit_to_window(self) -> None:
    self._image_container.fit_to_window()


  def _add_watermark(self) -> None:
    self._image_container.add_watermark(
      self._watermark_control_panel.get_watermark_text(),
      self._watermark_control_panel.get_watermark_font(),
      self._watermark_control_panel.get_watermark_font_size(),
      self._watermark_control_panel.get_watermark_colour())
    

  def _reset_image(self) -> None:
    self._image_container.reset_image()


  def _load_theme(self) -> None:
    # Load the Azure-ttk theme
    #self._root_window.tk.call('source', 'static/Azure-ttk/azure.tcl')
    #self._root_window.tk.call('set_theme', 'dark')

    #Load the Forest-ttk theme
    # self._root_window.call('source', 'static/Forest-ttk/forest-dark.tcl')
    # ttk.Style().theme_use('forest-dark')
    styles = ttk.Style()
    styles.theme_use('clam')

    # TScrollbar config options
    #
    # -arrowcolor color
    # -arrowsize amount
    # -background color
    # -bordercolor color
    # -darkcolor color (color of the dark part of the 3D relief)
    # -foreground color
    # -gripcount count (number of lines on the thumb)
    # -lightcolor color (color of the light part of the 3D relief)
    # -troughcolor color
    styles.configure('Vertical.TScrollbar', background='lightgrey', arrowsize=16)
    styles.configure('Horizontal.TScrollbar', background='lightgrey', arrowsize=16)
    #styles.configure('Accent.TButton', background='lightgrey')


  def _center_window(self, window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


if __name__ == '__main__':
  app = WatermarkApp()
  app.run()
