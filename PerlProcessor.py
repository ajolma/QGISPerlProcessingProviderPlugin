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
import subprocess

from qgis.PyQt.QtCore import QSettings
from qgis.core import *
from qgis.utils import iface

from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.parameters import ParameterVector, ParameterRaster, ParameterExtent
from processing.core.outputs import OutputVector, OutputRaster
from processing.tools import dataobjects, vector
from processing.tools.system import userFolder


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
        super().__init__()

    def defineCharacteristics(self):
        print("define characteristics")
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
                                                          [dataobjects.TYPE_RASTER],
                                                          False)) # False = not optional
                    else:
                        self.addOutput(OutputRaster(name,
                                                    self.tr(desc)))
                elif (klass == "Extent"):
                    self.addParameter(ParameterExtent(name,
                                                      self.tr(desc)))
                    
        except Exception as e: print(e)

    def processAlgorithm(self, feedback):
        """Here is where the processing itself takes place."""

        try:
            print("Arguments:")
            for param in self.characteristics['args']:
                klass, name, desc = param[1].split(",")
                if (param[0] == 'Input'):
                    print(name+": "+self.getParameterValue(name))
                else:
                    print(name+": "+self.getOutputValue(name))

            # run the perl program

            command = ['perl', '-w']
            command.append(self.characteristics['filename'])
            for param in self.characteristics['args']:
                klass, name, desc = param[1].split(",")
                if (param[0] == 'Input'):
                    value = self.getParameterValue(name)
                else:
                    value = self.getOutputValue(name)
                if (klass == "Extent"):
                    xmin,xmax,ymin,ymax = value.split(",")
                    value = xmin+','+ymin+','+xmax+','+ymax
                command.append(value)
            command.append('-q')
            print(command)
            proc = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True)
            try:
                out, err = proc.communicate()
            except TimeoutExpired:
                proc.kill()
            out += err
            print(out)

        except Exception as e: print(e)
