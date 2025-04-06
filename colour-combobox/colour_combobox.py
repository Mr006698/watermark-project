import tkinter as tk
from tkinter import ttk, colorchooser
from ctypes import windll
from collections.abc import Callable
from typing import Optional
from pprint import pprint

# Remove blurry text on high DPI screens
windll.shcore.SetProcessDpiAwareness(1)

class ColourButton(ttk.Frame):
  callback: Optional[Callable[[], str]] = None
  _btn_normal: Optional[str] = None
  _btn_light: Optional[str] = None
  _btn_dark: Optional[str] = None
  _colour_tint: float = 0.25

  def __init__(self, root=None, colour: str=None, cursor: str='', size: int=32):
    super().__init__(root, cursor=cursor)

    # Check the value of the colour paramater
    #if not isinstance(colour, str): raise TypeError('colour must be a string')

    # Create the button colours
    self._btn_normal = colour
    self._create_colour_shades(colour, self._colour_tint)

    # Configure the frame
    self.config(border=1, relief='solid', width=size, height=size)

    # Biind click events to the frame
    # self.bind('<Enter>', self._btn_enter)
    # self.bind('<Leave>', self._btn_leave)
    # self.bind('<ButtonPress-1>', self._btn_press)
    # self.bind('<ButtonRelease-1>', self._btn_release)

    # Create the canvas
    self._canvas = tk.Canvas(self, width=size, height=size, bg=self._btn_normal, highlightthickness=1)
    self._canvas.pack(fill=tk.BOTH, expand = True)
    self._canvas.bind('<Enter>', self._btn_enter)
    self._canvas.bind('<Leave>', self._btn_leave)
    self._canvas.bind('<ButtonPress-1>', self._btn_press)
    self._canvas.bind('<ButtonRelease-1>', self._btn_release)


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


  def _create_colour_shades(self, colour: str, tint: float) -> str:
    if colour.startswith('#') and len(colour) == 7:
      rgb = self._hex_to_rgb(colour)

    else:
      print('Name colour')
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


root = tk.Tk()
root.title('Colour Combobox')
root.geometry('640x480')

options = ['Red', 'Green', 'Blue', 'yellow']
btn = ColourButton(root, colour='grey', cursor='hand2', size=28)
btn.pack(padx=10, pady=10)

if __name__ == '__main__':
  root.mainloop()
