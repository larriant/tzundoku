# -*- coding: utf-8 -*-
'''
This is the tzundoku legal package. It contains information required to generate legal notices, such as the terms and conditions.
'''

import re
import os
import codecs

#ENTITY_DESCRIPTION='''{name of organisation}, a company
#registered in England and Wales (No. {company number}), whose registered
#office is at {insert address of registered office here}'''

ENTITY_DESCRIPTION='''Julyan Davey'''

path=os.path.dirname(os.path.abspath(__file__))

privacy=open(os.path.join(path, "privacy.html"), "r").read()

source={}
for key in ["terms", "privacy"]:
    file_name=key + ".html"
    source[key]=codecs.open(os.path.join(path, file_name), "r", encoding='utf-8').read()
terms=source['terms']
terms=re.sub("ENTITYDESCRIPTION", ENTITY_DESCRIPTION, terms)
privacy=source['privacy']
