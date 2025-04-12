from matplotlib import font_manager
import tkinter as tk
from tkinter import font


class SystemFonts():
  def __init__(self, root: tk.Tk):
    self.root = root

    self._cache_system_fonts()


  def get_tk_fonts(self) -> list[str]:
    return list(self._tk_font_list)
  

  def get_font_path(self, font: str) -> str:
    return self._mp_font_dict.get(font, 'Arial')

  
  def _cache_system_fonts(self) -> None:
    self._mp_font_dict = {font.name: font.fname for font in font_manager.fontManager.ttflist}
    # Don't know why tkinter and matplotlib system fonts don't match just keep the ones that do
    self._tk_font_list = [f for f in font.families() if f in self._mp_font_dict.keys()]
    self._tk_font_list.sort()


if __name__ == '__main__':
  root = tk.Tk()
  system_fonts = SystemFonts(root)
  tk_fonts = system_fonts.get_tk_fonts()

  print(system_fonts.get_font_path(tk_fonts[0]))
