#coding=utf-8
"""
Copyright (C), 2012-2015, Anything Connected Platform
Author: ACP2013
Version: 1.0
Date: 2012-09-21
Description: test
Others:      无
Key Class&Method List: 无             
History: 
1. Date:2012-09-21
   Author:ACP2013
   Modification:New
"""

paths=[ 
       "./lib/",
    ]

import sys
import os.path

cur_dir = os.path.dirname(__file__)
for p in paths:        
    sys.path.append(os.path.join(cur_dir, p))
