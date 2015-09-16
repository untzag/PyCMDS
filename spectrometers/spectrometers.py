### import ####################################################################


import os
import imp

from PyQt4 import QtCore

import project.project_globals as g
main_dir = g.main_dir.read()
app = g.app.read()
import project.widgets as pw
import project.ini_handler as ini
ini = ini.spectrometers
import project.classes as pc

if g.offline.read():
    prefix = 'v_'
else:
    prifix = ''

### address ###################################################################


class Monochromator(pc.Address):

    def dummy(self):
        print 'hello world im a dummy method'


# list module path, module name, class name, initialization arguments, friendly name
hardware_dict = {'MicroHR': [os.path.join(main_dir, 'spectrometers', 'MicroHR', prefix + 'MicroHR.py'), 'MicroHR', 'MicroHR', [], 'wm']}
hardwares = []
for key in hardware_dict.keys():
    if ini.read('hardware', key):
        lis = hardware_dict[key]
        hardware_module = imp.load_source(lis[1], lis[0])
        hardware_class = getattr(hardware_module, lis[2])
        hardware_obj = pc.Hardware(hardware_class, lis[3], Monochromator, key, True, lis[4])
        hardwares.append(hardware_obj)


### gui #######################################################################

gui = pw.HardwareFrontPanel(hardwares, name='Spectrometers')

advanced_gui = pw.HardwareAdvancedPanel(hardwares, gui.advanced_button)

