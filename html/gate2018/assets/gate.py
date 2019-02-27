te=raw_input()
i=0
while te[0]!='x':
	i=i+1
	if i<=10:
		print('"g%02d": ["%s","huiku"],' % (i,te.strip()))
	else:
		if te[0]=='p':
			start=te[1:].split(':')[0]
			end=te[1:].split(':')[1]
			print('"e%02d": ["%s","prec","%s"],' %(i-10,start,end))
		else:
			print('"e%02d": ["%s","sdf"],' %(i-10,te))
	te=raw_input()
