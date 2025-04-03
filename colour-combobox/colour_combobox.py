import tkinter as tk
from tkinter import ttk
from ctypes import windll
from collections.abc import Iterable
from pprint import pprint

# Remove blurry text on high DPI screens
windll.shcore.SetProcessDpiAwareness(1)

class ColourCombobox(ttk.Combobox):
  def __init__(self, master = None, colours: Iterable[str] = None, textvariable: str = None):
    
    super().__init__(master, values=colours, textvariable=textvariable, state='readonly')
    self.config(postcommand=lambda: self.after_idle(self._config_items))
    self.config(style='Colour.TCombobox', foreground='Green')
    self['style'] = 'Colour.TCombobox'


  def _config_items(self) -> None:
    lines = ['set popdown [ttk::combobox::PopdownWindow .!colourcombobox]']
    for i, v in enumerate(self['values']):
      lines.append(f'$popdown.f.l itemconfigure {i} -background {v}')
    
    self.master.tk.eval('\n'.join(lines))


class SimpleColourSelector(ttk.Entry):
  def __init__(self, master = None, colours: Iterable[str] = None):
    super().__init__(master)
    self.config(background='black', width=10)
    self._menu = tk.Listbox(self)
    for index in range(len(colours)):
      self._menu.insert(index, colours[index])
      self._menu.itemconfig(index, background=colours[index], foreground=colours[index])
    self._menu.pack(side=tk.BOTTOM)


root = tk.Tk()
root.title('Colour Combobox')
root.geometry('640x480')

options = ['Red', 'Green', 'Blue', 'yellow']
colour_selecton = tk.StringVar(root, options[0])
colour_combobox = ColourCombobox(master=root, colours=options, textvariable=colour_selecton)
colour_combobox.pack(padx=10, pady=10)

simple_colour_selector = SimpleColourSelector(root, options)
simple_colour_selector.pack(padx=10, pady=10)

c = ttk.Combobox(root, values=options)
c.pack(padx=10, pady=10)

if __name__ == '__main__':
  root.mainloop()
