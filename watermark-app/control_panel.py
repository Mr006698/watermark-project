import tkinter as tk
from tkinter import ttk, font

class WatermarkControlPanel(ttk.Frame):
  def __init__(self, root_window: tk.Tk, add_watermark):
    # Call the parent class constructor
    super().__init__(master=root_window, style='Card.TFrame')

    # Create watermark text entry
    self._create_watermark_text_entry()

    # Create the font combobox
    self._create_font_combobox()

    # Create the colour combobox
    self._create_colour_combobox()

    # Create the add watermark button
    self._create_buttons(add_watermark)


  def get_watermark_text(self) -> str:
    return self._watermark_text.get()
  

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
    font_combobox.pack(side=tk.LEFT, expand=False, fill= tk.Y, padx=(0, 5), pady=5)

  
  def _create_colour_combobox(self) -> None:
    # Create the colour selection combobox
    colours = ['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'pink', 'black', 'white']
    self._selected_colour = tk.StringVar(self, value='black')
    colour_combobox = ttk.Combobox(self, values=colours, background='blue', textvariable=self._selected_colour, width=3, state='readonly')
    colour_combobox.pack(side=tk.LEFT, expand=False, fill=tk.Y, padx=(5, 5), pady=5)


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
