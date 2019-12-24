# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#

from enum import Enum, unique

@unique
class JobStatus( Enum ):
    ERROR = 0
    NEW = 1

