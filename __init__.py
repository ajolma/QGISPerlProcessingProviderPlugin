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

from perlprocessing.PerlProcessingProviderPlugin import PerlProcessingProviderPlugin


def classFactory(iface):
    return PerlProcessingProviderPlugin()
