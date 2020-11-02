import cv2

def compareNumber(_compImg, _compRes):
	num = 0
	match = [0,10]
	trun = [0,10]

	while(num < 15):
		ret = 0
		imgt =  "./Cubes/" + str(num) + ".png"
		imgNum = cv2.imread(imgt,0)
		imgNum = cv2.resize(imgNum, (_compRes[1],_compRes[0]))

		contSrc, hier = cv2.findContours(imgNum, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		contCmp, hier = cv2.findContours(_compImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		imgNum = cv2.cvtColor(imgNum, cv2.COLOR_GRAY2BGR)
		
		for this in range(len(contSrc)):
			if(this > len(contCmp)-1):
				break
			perSrc = cv2.arcLength(contSrc[this], True)
			perCmp = cv2.arcLength(contCmp[this], True)
			if(perSrc < 500 and perCmp < 500):
				ret = ret + cv2.matchShapes(contCmp[this], contSrc[this], 3, 0.0)

		if(len(contCmp) != len(contSrc)):
			ret = ret + 0.5



		if(match[1] > ret):
			print(num)
			for cnt in contCmp:
				cv2.drawContours(imgNum, cnt, -1, (255,0,255), 3)
			for cnt in contSrc:
				cv2.drawContours(imgNum, cnt, -1, (0,255,255), 3)
			cv2.imwrite('AA.png', imgNum)
			match[0] = num
			match[1] = ret

		num = num + 1

	return match