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

from processing.core.AlgorithmProvider import AlgorithmProvider
from processing.core.ProcessingConfig import Setting, ProcessingConfig
from perlprocessing.PerlProcessor import PerlProcessor


class PerlProcessingProvider(AlgorithmProvider):

    MY_DUMMY_SETTING = 'MY_DUMMY_SETTING'

    def __init__(self):
        super().__init__()

        # Deactivate provider by default
        self.activate = False

        # Load algorithms
        self.alglist = [PerlProcessor()]
        for alg in self.alglist:
            alg.provider = self

    def initializeSettings(self):
        """In this method we add settings needed to configure our
        provider.

        Do not forget to call the parent method, since it takes care
        or automatically adding a setting for activating or
        deactivating the algorithms in the provider.
        """
        AlgorithmProvider.initializeSettings(self)
        #ProcessingConfig.addSetting(Setting('Perl processors',
        #                                    PerlAlgorithmProvider.MY_DUMMY_SETTING,
        #                                    'Perl setting', 'Default value'))

    def unload(self):
        """Setting should be removed here, so they do not appear anymore
        when the plugin is unloaded.
        """
        AlgorithmProvider.unload(self)
        #ProcessingConfig.removeSetting(
        #    PerlAlgorithmProvider.MY_DUMMY_SETTING)

    def id(self):
        """
        It is also used to create the command line name of all the
        algorithms from this provider.
        """
        return 'perl'

    def name(self):
        """This is the name that will appear on the toolbox group.
        This is the provired full name.
        """
        return 'Perl processors'

    def icon(self):
        """We return the default icon.
        """
        return AlgorithmProvider.icon(self)

    def _loadAlgorithms(self):
        """Here we fill the list of algorithms in self.algs.

        This method is called whenever the list of algorithms should
        be updated. If the list of algorithms can change (for instance,
        if it contains algorithms from user-defined scripts and a new
        script might have been added), you should create the list again
        here.

        In this case, since the list is always the same, we assign from
        the pre-made list. This assignment has to be done in this method
        even if the list does not change, since the self.algs list is
        cleared before calling this method.
        """
        print("load processors")
        self.algs = self.alglist
