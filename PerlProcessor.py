# -*- coding: utf-8 -*-

"""
***************************************************************************
    __init__.py
    ---------------------
    Date                 : March 2017
    Copyright            : (C) 2017 by Ari Jolma
    Email                : ari.jolma at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Ari Jolma'
__date__ = 'March 2017'
__copyright__ = '(C) 2017, Ari Jolma'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import re
from subprocess import Popen, PIPE, STDOUT

from qgis.PyQt.QtCore import QSettings
from qgis.core import *
from qgis.utils import iface

from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.parameters import *
from processing.core.outputs import *
from processing.tools import dataobjects, vector
from processing.tools.system import userFolder
from processing.core.ProcessingConfig import ProcessingConfig


class PerlProcessor(GeoAlgorithm):

    """This is an perl algorithm that takes a vector layer and
    creates a new one just with just those features of the input
    layer that are selected.

    It is meant to be used as an perl of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the GeoAlgorithm class.
    """

    def __init__(self, characteristics):
        self.characteristics = characteristics
        GeoAlgorithm.__init__(self)

    def defineCharacteristics(self):
        """Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
        try:
            # The name that the user will see in the toolbox
            self.name, self.i18n_name = self.trAlgorithm(self.characteristics['name'])

            # The branch of the toolbox under which the algorithm will appear
            self.group, self.i18n_group = self.trAlgorithm(self.characteristics['group'])

            for param in self.characteristics['args']:
                klass, name, desc = param[1].split(",")
                if (klass == "Raster"):
                    if (param[0] == 'Input'):
                        self.addParameter(ParameterRaster(name,
                                                          self.tr(desc),
                                                          False)) # False = not optional
                    else:
                        self.addOutput(OutputRaster(name,
                                                    self.tr(desc)))
                elif (klass == "Extent"):
                    self.addParameter(ParameterExtent(name,
                                                      self.tr(desc)))
                elif (klass == "Number"):
                    if (param[0] == 'Input'):
                        pass # todo
                    else:
                        print("add "+name+" to "+self.name)
                        self.addOutput(OutputNumber(name,
                                                    self.tr(desc)))
            self.addParameter(ParameterBoolean('KeepLogOpen', 'Keep the log open after processing'))
                    
        except Exception as e: print(e)

    def processAlgorithm(self, feedback):
        try:
            command = ['perl', '-w']
            command.append(self.characteristics['filename'])
            command.append('-l')
            for param in self.characteristics['args']:
                klass, name, desc = param[1].split(",")
                if (param[0] == 'Input'):
                    value = self.getParameterValue(name)
                    if (klass == "Extent"):
                        xmin,xmax,ymin,ymax = value.split(",")
                        value = xmin+','+ymin+','+xmax+','+ymax
                else:
                    value = self.getOutputValue(name)
                    # some things don't make sense to put into the cmdline
                    if (klass == "Extent"):
                        continue
                    elif (klass == "Number"):
                        continue
                command.append(value)
            proc = Popen(command, stdout=PIPE, stderr=STDOUT, bufsize=1, universal_newlines=True)
            output = []
            while True:
                line = proc.stdout.readline()
                if line == '' and proc.poll() is not None:
                    break
                if line:
                    match = re.match(r'^(\d+)/(\d+)$', line)
                    if (match and int(float(match.group(2))) == 100):
                        feedback.setPercentage(int(float(match.group(1))))
                    else:
                        line = line.rstrip()
                        output.append(line)
                        feedback.setInfo(line)
            ProcessingConfig.setSettingValue(ProcessingConfig.KEEP_DIALOG_OPEN, True)
            if (proc.returncode == 0):
                # ok, arrange output for downstream to use
                ProcessingConfig.setSettingValue(ProcessingConfig.KEEP_DIALOG_OPEN, self.getParameterValue('KeepLogOpen'))
                for param in self.characteristics['args']:
                    klass, name, desc = param[1].split(",")
                    if (param[0] == 'Output'):
                        print("output is "+output[0])
                        if (klass == "Extent"):
                            xmin,ymin,xmax,ymax = output[0].split(",")
                            value = [float(xmin),float(xmax),float(ymin),float(ymax)]
                            self.setOutputValue(name, value)
                        elif (klass == "Number"):
                            value = float(output[0])
                            self.setOutputValue(name, value)
            elif (proc.returncode == 126):
                feedback.setInfo("Permission problem or command is not an executable")
            elif (proc.returncode == 127):
                feedback.setInfo("Command not found")
            else:
                # print(type(feedback).__name__) = 'AlgorithmDialog'
                feedback.setInfo("Error in the Perl program.")
                feedback.setInfo("Hopefully error messages above clarify it.")
        except Exception as e:
            print("error in PerlProcessor.processAlgorithm()")
            print(e)
