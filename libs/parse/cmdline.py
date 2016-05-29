#!/usr/bin/env python
# -*-coding:utf-8-*-
#-*-author:scrat-*-

import os
import sys
from optparse import OptionError
from optparse import OptionParser
from optparse import OptionGroup
from optparse import SUPPRESS_HELP

def cmdLineParser():
    """
    This function parses the command line parameters and arguments
    :return:
    """
    _ = os.path.normpath(sys.argv[0])
    usage = "python %s [options]" % ("\"%s\"" % _ if " " in _ else _)

    parser = OptionParser(usage=usage)