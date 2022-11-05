import level4_1
import Restart_page

variable = False
while 1:

    if level4_1.run_level(variable, False):
        Restart_page.restart()
        variable = False



