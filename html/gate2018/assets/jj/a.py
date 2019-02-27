for i in range(1,66):
	if i<11:
		print('curl https://cdn4.digialm.com//per/g01/pub/585/touchstone/TempQPImagesStoreMode1/adcimages/1518336842250/52334652///585_5123346_0_587434_ga_%02d.jpg>%d.jpg' %(i,i))
	else:
		print('curl https://cdn4.digialm.com//per/g01/pub/585/touchstone/TempQPImagesStoreMode1/adcimages/1518336842250/52334652///585_5123346_0_587434_ee_%2d.jpg>%d.jpg' %(i,i))
