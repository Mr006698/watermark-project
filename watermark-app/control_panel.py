import tkinter as tk
from tkinter import ttk, font, colorchooser
from collections.abc import Callable
from typing import Optional

# COLOUR BUTTON
class ColourButton(ttk.Frame):
  _callback: Optional[Callable[[], str]] = None
  _btn_normal: Optional[str] = None
  _btn_light: Optional[str] = None
  _btn_dark: Optional[str] = None
  _colour_tint: float = 0.25

  def __init__(self, root=None, colour: Optional[str]=None, cursor: str='', size: int=32):
    super().__init__(root, cursor=cursor)

    # Check the value of the colour paramater
    #if not isinstance(colour, str): raise TypeError('colour must be a string')

    # Create the button colours
    self._btn_normal = colour
    self._create_colour_shades(colour, self._colour_tint)

    # Configure the frame
    self.config(border=1, relief='solid', width=size, height=size)

    # Create the canvas
    self._canvas = tk.Canvas(self, width=size, height=size, bg=self._btn_normal, highlightthickness=1)
    self._canvas.pack(fill=tk.BOTH, expand = True)
    self._canvas.bind('<Enter>', self._btn_enter)
    self._canvas.bind('<Leave>', self._btn_leave)
    self._canvas.bind('<ButtonPress-1>', self._btn_press)
    self._canvas.bind('<ButtonRelease-1>', self._btn_release)


  def set_callback(self, callback: Callable[[], str]) -> None:
    if not callable(callback):
      raise TypeError('Callback must be a callable type')
    
    self._callback = callback


  def _btn_enter(self, event) -> None:
    if self._btn_light is not None:
      self._canvas.config(bg=self._btn_light)


  def _btn_leave(self, event) -> None:
    if self._btn_normal is not None:
      self._canvas.config(bg=self._btn_normal)


  def _btn_press(self, event) -> None:
    if self._btn_dark is not None:
      self._canvas.config(bg=self._btn_dark)


  def _btn_release(self, event) -> None:
    new_colour = colorchooser.askcolor(self._btn_normal, title='Select a colour')
    if new_colour[1] is not None:
      self._btn_normal = new_colour[1]
      self._canvas.config(bg=self._btn_normal)
      self._create_colour_shades(new_colour[1], self._colour_tint)

      # Notify any callback functions
      if self._callback is not None:
        self._callback(self._btn_normal)


  def _create_colour_shades(self, colour: str, tint: float) -> str:
    if colour.startswith('#') and len(colour) == 7:
      rgb = self._hex_to_rgb(colour)

    else:
      rgb = self._name_to_rgb(colour)

    dark_rgb = (int(rgb[0] * (1 - tint)), int(rgb[1] * (1 - tint)), int(rgb[2] * (1 - tint)))
    light_rgb = (int(rgb[0] + ((255 - rgb[0]) * tint)), int(rgb[1] + ((255 - rgb[1]) * tint)), int((rgb[2] + ((255 - rgb[2]) * tint))))

    self._btn_dark = self._rgb_to_hex(*dark_rgb)
    self._btn_light = self._rgb_to_hex(*light_rgb)

  
  def _hex_to_rgb(self, h: str) -> tuple:
    if h.startswith('#'): h = h.lstrip('#') #h[1:]
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
  

  def _rgb_to_hex(self, r: int, g: int, b: int) -> str:
    return f'#{r:02X}{g:02X}{b:02X}'
  

  def _name_to_rgb(self, name: str) -> tuple:
    return (tuple(c//256 for c in self.master.winfo_rgb(name)))
  

# WATERMARK CONTROL PANEL
class WatermarkControlPanel(ttk.Frame):
  def __init__(self, root_window: tk.Tk, add_watermark):
    # Call the parent class constructor
    super().__init__(master=root_window, style='Card.TFrame')

    # Create watermark text entry
    self._create_watermark_text_entry()

    # Create the font combobox
    self._create_font_combobox()

    # Create the colour selector
    self._create_colour_button()

    # Create the add watermark button
    self._create_buttons(add_watermark)


  def get_watermark_text(self) -> str:
    return self._watermark_text.get()
  

  def get_watermark_font(self) -> str:
    return self._selected_font.get()
  

  def get_watermark_colour(self) -> str:
    return self._watermark_colour
  

  def _create_watermark_text_entry(self) -> None:
    self._watermark_text = tk.StringVar(self, value='@copyright')
    self._text_entry = ttk.Entry(self, textvariable=self._watermark_text)
    self._text_entry.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=(5, 10), pady=(5, 5))
  

  def _create_font_combobox(self) -> None:
    # Create the font selection combobox
    fonts = list(font.families())
    fonts.sort()
    self._selected_font = tk.StringVar(self, value=font.nametofont('TkDefaultFont').actual()['family']) # Set this to the default font of tkinter
    font_combobox = ttk.Combobox(self, values=fonts, textvariable=self._selected_font, width=30, state='readonly')
    font_combobox.bind('<<ComboboxSelected>>', self._font_changed)
    font_combobox.pack(side=tk.LEFT, expand=False, fill=tk.Y, padx=(0, 5), pady=5)

  
  def _create_colour_button(self) -> None:
    self._colour_btn = ColourButton(self, colour='black', cursor='hand2', size=32)
    self._colour_btn.pack(side=tk.LEFT, expand=False, fill=tk.Y, padx=(5, 5), pady=5)
    self._colour_btn.set_callback(self._colour_changed)
    self._watermark_colour = 'black'


  def _colour_changed(self, colour: str) -> None:
    self._watermark_colour = colour


  def _font_changed(self, event) -> None:
    # Set the font of the watermark text
    font_name = self._selected_font.get()
    self._text_entry.configure(font=(font_name, 9))

  
  def _create_buttons(self, add_watermark) -> None:
    add_btn = ttk.Button(
      self,
      text='Add Watermark',
      style='Accent.TButton',
      width=15,
      command=add_watermark)
    
    add_btn.pack(side=tk.LEFT, padx=5, pady=5)


# IMAGE CONTROL PANEL
class ImageControlPanel(ttk.Frame):
  def __init__(self, root_window: tk.Tk, load_image, save_image, fit_to_window, actual_size, rotate_image) -> None:
    # Call the parent class constructor
    super().__init__(master=root_window, style='Card.TFrame')

    self._create_load_button(load_image)
    self._create_save_button(save_image)
    self._create_fit_window_btn(fit_to_window)
    self._create_actual_size_btn(actual_size)
    self._create_rotate_btns(rotate_image)


  def _create_load_button(self, load_image) -> None:
    # Create the image selection button
    select_btn = ttk.Button(
      self,
      text='Load Image',
      style='Accent.TButton',
      width=15,
      command=load_image)
    
    select_btn.pack(side=tk.TOP, padx=5, pady=5)

  
  def _create_save_button(self, save_image) -> None:
    # Create the save image button
    save_btn = ttk.Button(
      self,
      text='Save Image',
      style='Accent.TButton',
      width=15,
      command=save_image
    )

    save_btn.pack(side=tk.TOP, padx=5, pady=5)


  def _create_fit_window_btn(self, fit_to_window) -> None:
    # Create the fit window button
    fit_btn = ttk.Button(
      self,
      text='Fit Window',
      style='Accent.TButton',
      width=15,
      command=fit_to_window
    )

    fit_btn.pack(side=tk.TOP, padx=5, pady=5)


  def _create_actual_size_btn(self, actual_size) -> None:
    # Create the fit window button
    fit_btn = ttk.Button(
      self,
      text='1:1',
      style='Accent.TButton',
      width=15,
      command=actual_size
    )

    fit_btn.pack(side=tk.TOP, padx=5, pady=5)
  

  def _create_rotate_btns(self, rotate_image) -> None:
    # Create the rotate buttons
    rotate_left_btn = ttk.Button(
      self,
      text='Rotate Left',
      style='Accent.TButton',
      width=15,
      command=lambda: rotate_image(90)
    )

    rotate_left_btn.pack(side=tk.TOP, padx=5, pady=5)

    rotate_right_btn = ttk.Button(
      self,
      text='Rotate Right',
      style='Accent.TButton',
      width=15,
      command=lambda: rotate_image(-90)
    )

    rotate_right_btn.pack(side=tk.TOP, padx=5, pady=5)
