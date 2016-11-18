import time
from ColorConstants import *
from GUIPageManager import GUIPageManager

manager = GUIPageManager()
page0 = manager.add_page()
page0.add_button("hello", (180,180))
manager.control_enable()

while True:
  time.sleep(1)
  manager.render()
