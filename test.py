# -*- coding: utf-8 -*-
import re

addressToVerify ='76868687'
match = re.match('^([-_.0-9]+)$', addressToVerify)

if match == None:
	print('Bad Syntax')