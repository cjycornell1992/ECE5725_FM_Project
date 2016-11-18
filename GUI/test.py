import time
from ColorConstants import *
from GUIPageManager import GUIPageManager

def button0_callback():
  global button0
  global page1
  print "you clicked on " + button0.text  
  button0.page.manager.turn_to_page(page1)

manager = GUIPageManager(debug = True)
page0   = manager.add_page()
button0 = page0.add_button("Turn to Page 1", (180,180), call_back = button0_callback)
button1 = page0.add_button("How are you", (240, 120), 30, RED)
button2 = page0.add_button("Good", (120, 120), 40, GREEN)
page1   = manager.add_page()
button3 = page1.add_button("You are at page 1", (160, 120), 50, MAGENTA)
manager.control_enable()

while True:
  time.sleep(1)
  manager.render()
