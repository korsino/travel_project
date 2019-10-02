import re

addressToVerify ='infoemailhippocom'
match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)

if match == None:
	print('Bad Syntax')