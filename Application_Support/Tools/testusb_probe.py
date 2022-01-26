from escpos import *


Generic = printer.Usb(0x456,0x0808,4,0x81,0x03)
Generic.text("Hello, World!")
Generic.cut()
