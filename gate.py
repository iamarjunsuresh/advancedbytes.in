te=raw_input()
i=0
while te[0]!='x':
	i=i+1
	if i<=10:
		print('"g%02d": ["%s","huiku"],' % (i,te))
	else:
		if te[0]=='p':
			start=te[1:].split(':')[0]
			end=te[1:].split(':')[1]
			print('"c%02d": ["%s","prec","%s"],' %(i,start,end))
		else:
			print('"c%02d": ["%s","sdf"],' %(i,te))
	te=raw_input()
