# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!

try:
	import sim
except:
	print ('--------------------------------------------------------------')
	print ('"sim.py" could not be imported. This means very probably that')
	print ('either "sim.py" or the remoteApi library could not be found.')
	print ('Make sure both are in the same folder as this file,')
	print ('or appropriately adjust the file "sim.py"')
	print ('--------------------------------------------------------------')
	print ('')

import time
import numpy as np
import cv2
import compareFaces
import pytesseract as pytes


def getImage(_camera):
	errol = 1

	while(errol != sim.simx_return_ok):
		errol, res, image = sim.simxGetVisionSensorImage(clientID, _camera, 0, sim.simx_opmode_buffer)
		time.sleep(0.005)
	nres = [res[0]-4*int(res[0]/30),res[1]]
	img = np.array(image, dtype=np.uint8)		# Como é recebido uma string, precisa reformatar
	img = np.reshape(img, (res[0], res[1], 3))	# Pro CV2, (y, x, [B,R,G])
	img = np.flip(img, 0)						# Por algum motivo vem de ponta cabeça
	img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)	# Transforma o RGB recebido em BGR pro CV2
	img = img[(int(res[0]/5)):res[0]-(int(res[0]/10)), 0:res[1]]
	img = cv2.copyMakeBorder(img, int(res[0]*5/30), 0, 0, 0, cv2.BORDER_CONSTANT)

	cv2.imwrite('0src.png', img)
	return img, nres

def basicFilter(_src, _op):
	"Processamento basico para isolar o topo dos cubos"
	#Isolar a cor branca procurada usando HSV:
	hsv = cv2.cvtColor(_src, cv2.COLOR_BGR2HSV)
	if(_op == 0):
		hsv_lower = np.array([0,1,180])
		hsv_upper = np.array([179,255,255])
		mask = cv2.inRange(hsv, hsv_lower, hsv_upper)
		hsv_lower = np.array([0,0,35])
		hsv_upper = np.array([179,255,100])
		mask2 = cv2.inRange(hsv, hsv_lower, hsv_upper)
	elif(_op == 1):
		hsv_lower = np.array([0,0,145])
		hsv_upper = np.array([10,100,160])
		mask = cv2.inRange(hsv, hsv_lower, hsv_upper)


	#Copiar a mascara para a imagem inicial:
	_src2 = _src.copy()
	img = cv2.bitwise_and(_src, _src, mask=mask)	

	#Transformar para cinza:
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	cv2.imwrite('1gray.png', img)
		
	# Media:
	img = cv2.medianBlur(img, 3)
	cv2.imwrite('4median.png', img)
	

	
	if(_op == 0):
		img2 = cv2.bitwise_and(_src2, _src2, mask=mask2)
		img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
		cv2.imwrite('1gray2.png', img2)
		img2 = cv2.medianBlur(img2, 3)
		cv2.imwrite('4median2.png', img2)
		nimg = cv2.bitwise_or(img, img2)
		cv2.imwrite('4median3.png', nimg)
	else:
		nimg = img.copy()

	return nimg

def compareCenters(_cx, _cy, _centers):
	"Compara os valores [cy,cx] com o vetor 2d conhecido"
	if(len(_centers) == 0):
		return 1
	for coord in _centers:
		if(abs(coord[0] - _cy) > 10 or abs(coord[1] - _cx) > 10):
			pass
		else:
			return 0
	return 1

def findUseful(_src, _img, _factor):
	"Acha os contornos uteis da imagem"
	#Pega todas as bordas por Canny:
	edges = cv2.Canny(_img, 100, 200)
	cv2.imwrite('5edges.png', edges)
	foundCenters = np.empty(shape=[0,2])
	foundShapes = np.empty(shape=[0,5,2])
	foundColors = np.empty(shape=[0,3])
	shapeArea = np.empty(shape=[0])
	

	#Aproxima os possiveis contornos:
	contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	for cnt in contours:
		#Simplifica os contornos em vertices por tamanho de lado:
		perimeter = cv2.arcLength(cnt, True)
		approx = cv2.approxPolyDP(cnt, _factor * perimeter, True)
		#Grava os centros:
		m = cv2.moments(cnt)
		if (m['m00'] == 0):
			m['m00'] = 1
		cx = int(m['m10']/m['m00'])
		cy = int(m['m01']/m['m00'])

		if(compareCenters(cx, cy, foundCenters) == 1):		
			if(len(approx) == 4 and (cv2.contourArea(cnt) > 50) and (cv2.contourArea(cnt) < 1000)):
				k = np.array([[[cx,cy]]])
				for padd in range(5-(len(approx))):
					approx = np.append(approx, [[[0,0]]], axis=0)
				approx = np.reshape(approx, (1,5,2))
				foundShapes = np.append(foundShapes, approx, axis=0)
				foundCenters = np.append(foundCenters, [[cy,cx]], axis=0)
				foundColors = np.append(foundColors, [_src[cy][cx]], axis=0)
				cv2.drawContours(_src, k, -1, (255,0,255), 3)

	cv2.imwrite('8centers.png', _src)
	print(foundCenters)
	print(foundColors)
	return foundShapes, foundColors, foundCenters

def rgbToLetter(_colors):
	newColors = np.empty(shape=(0))
	for color in _colors:
		if(color[0] > 100 and color[1] > 100):
			newColors = np.append(newColors, ['W'], axis=0)
		elif(color[0] > 100):
			newColors = np.append(newColors, ['B'], axis=0)
		elif(color[1] > 100 and color[2] > 100):
			newColors = np.append(newColors, ['Y'], axis=0)
		elif(color[1] > 100):
			newColors = np.append(newColors, ['G'], axis=0)
		elif(color[2] < 100):
			newColors = np.append(newColors, ['K'], axis=0)
		else:
			newColors = np.append(newColors, ['R'], axis=0)
	return newColors

def createArray(_foundCenters, _foundColors, _rangeY, _rangeX):
	squares = np.empty(shape=[0,3])
	_rangeY=_rangeY-int(0.078*_rangeY)
	adder = 0
	if(sigValue == 1):
		adder = 4
	j=0
	for center in _foundCenters:
		subQuadranteX = center[1]/_rangeX
		subQuadranteY = center[0]/_rangeY

		if(center[1] < _rangeX/2 and center[0] > _rangeY/2):
			# Quadrante superior direito (com as prateleiras na parte de cima da arena)
			if(subQuadranteX < 0.27):
				subQuadrante = 3
			else:
				subQuadrante = 2
			if(subQuadranteY > 0.72):
				subQuadrante = subQuadrante-2
			squares = np.append(squares, [[_foundColors[j], 1+adder, subQuadrante]], axis=0)
		elif(center[1] < _rangeX/2):
			# Quadrante inferior direito (com as prateleiras na parte de cima da arena)
			if(subQuadranteX < 0.34):
				subQuadrante = 3
			else:
				subQuadrante = 2
			if(subQuadranteY > 0.32):
				subQuadrante = subQuadrante-2
			squares = np.append(squares, [[_foundColors[j], 3+adder, subQuadrante]], axis=0)
		elif(center[0] > _rangeY/2):
			# Quadrante superior esquerdo (com as prateleiras na parte de cima da arena)
			if(subQuadranteX < 0.72):
				subQuadrante = 3
			else:
				subQuadrante = 2
			if(subQuadranteY > 0.72):
				subQuadrante = subQuadrante-2
			squares = np.append(squares, [[_foundColors[j], 0+adder, subQuadrante]], axis=0)
		else:
			# Quadrante inferior esquerdo (com as prateleiras na parte de cima da arena)
			if(subQuadranteX < 0.63):
				subQuadrante = 3
			else:
				subQuadrante = 2
			if(subQuadranteY > 0.32):
				subQuadrante = subQuadrante-2
			squares = np.append(squares, [[_foundColors[j], 2+adder, subQuadrante]], axis=0)
		j+=1
	return squares

def isolateFace(_img, _res):
	img = _img.copy()
	img = img[int(_res[0]/2):_res[0], 0:int(_res[1]*0.7)]

	edges = cv2.Canny(img, 100, 200)
	cnts, hier = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	thres, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

	cv2.imwrite('5face.png', img)
	


	approx = np.zeros((2,2,1,2))
	for cnt in cnts:
		perimeter = cv2.arcLength(cnt, True)
		if(perimeter > 500):
			print("S")
			approx = cv2.approxPolyDP(cnt, 0.2 * perimeter, True)

	print(approx)

	height = int(min(approx[0][0][1], approx[1][0][1]))
	width = int(min(approx[0][0][0], approx[1][0][0]))
	maxWid = int(max(approx[0][0][0], approx[1][0][0]))
	maxHei = int(max(approx[0][0][1], approx[1][0][1]))
	#print(height, " ", width, " " ,maxWid, " ", approx[1][0][0][1])

	img = img[height:maxHei, width:maxWid]

	return img, [maxHei-height,maxWid-width], 0

def nothing(x):
	pass

def test(camera):

	image, resol = getImage(camera)

	# Create a window
	cv2.namedWindow('image')
	cv2.namedWindow('track')

	boundaries = [
		([17, 15, 100], [50, 56, 200]),
		([86, 31, 4], [220, 88, 50]),
		([25, 146, 190], [62, 174, 250]),
		([103, 86, 65], [145, 133, 128])
	]

	# create trackbars for color change
	cv2.createTrackbar('HMin','track',0,179,nothing) # Hue is from 0-179 for Opencv
	cv2.createTrackbar('SMin','track',0,255,nothing)
	cv2.createTrackbar('VMin','track',0,255,nothing)
	cv2.createTrackbar('HMax','track',0,179,nothing)
	cv2.createTrackbar('SMax','track',0,255,nothing)
	cv2.createTrackbar('VMax','track',0,255,nothing)

	# Set default value for MAX HSV trackbars.
	cv2.setTrackbarPos('HMax', 'track', 179)
	cv2.setTrackbarPos('SMax', 'track', 255)
	cv2.setTrackbarPos('VMax', 'track', 255)

	# Initialize to check if HSV min/max value changes
	hMin = sMin = vMin = hMax = sMax = vMax = 0
	phMin = psMin = pvMin = phMax = psMax = pvMax = 0

	output = image
	wait_time = 33

	#for (lower, upper) in boundaries:
	#	# create NumPy arrays from the boundaries
	#	lower = np.array(lower, dtype = "uint8")
	#	upper = np.array(upper, dtype = "uint8")
	#	# find the colors within the specified boundaries and apply
	#	# the mask
	#	mask = cv2.inRange(image, lower, upper)
	#	output = cv2.bitwise_and(image, image, mask = mask)
	#	# show the images
	#	cv2.imshow("images", np.hstack([image, output]))
	#	cv2.waitKey(0)

	while(1):
		frame, resol = getImage(camera)
		# get current positions of all trackbars
		hMin = cv2.getTrackbarPos('HMin','track')
		sMin = cv2.getTrackbarPos('SMin','track')
		vMin = cv2.getTrackbarPos('VMin','track')

		hMax = cv2.getTrackbarPos('HMax','track')
		sMax = cv2.getTrackbarPos('SMax','track')
		vMax = cv2.getTrackbarPos('VMax','track')

		# Set minimum and max HSV values to display
		lower = np.array([hMin, sMin, vMin])
		upper = np.array([hMax, sMax, vMax])

		# Create HSV Image and threshold into a range.
		hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(hsv, lower, upper)
		output = cv2.bitwise_and(image,image, mask= mask)

		# Print if there is a change in HSV value
		if( (phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (phMax != hMax) | (psMax != sMax) | (pvMax != vMax) ):
			print("(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (hMin , sMin , vMin, hMax, sMax , vMax))
			phMin = hMin
			psMin = sMin
			pvMin = vMin
			phMax = hMax
			psMax = sMax
			pvMax = vMax

		# Display output image
		cv2.imshow('image',output)

		# Wait longer to prevent freeze for videos.
		if cv2.waitKey(wait_time) & 0xFF == ord('q'):
			break

	cv2.destroyAllWindows()


def resolveVision(_clientID, _sigValue):
	global clientID
	global sigValue
	sigValue = _sigValue
	clientID = _clientID

	# Get the camera handle:
	erro, camera = sim.simxGetObjectHandle(clientID, 'Vision_s', sim.simx_opmode_oneshot_wait)
	# Start the Stream
	erro, res, image = sim.simxGetVisionSensorImage(clientID, camera, 0, sim.simx_opmode_streaming)
	frame, resol = getImage(camera)
	
	src = frame.copy()
	img = basicFilter(src, 0)
	foundShape, foundColors, foundCenters = findUseful(src, img, 0.07)
	foundColors = rgbToLetter(foundColors)
	foundCubes = createArray(foundCenters, foundColors, resol[0], resol[1])

	j=0
	for shapes in foundShape:
		shp = np.reshape(shapes,(5,1,2))
		cv2.drawContours(frame, shp.astype(int), -1, (255,0,255), 3)
		j+=1

	cv2.imwrite('7Final.png', frame)
	return foundCubes



def getNumber(_clientID):
	global clientID
	clientID = _clientID

	# Get the camera handle:
	erro, camera = sim.simxGetObjectHandle(clientID, 'Vis_Num', sim.simx_opmode_oneshot_wait)
	# Start the Stream
	erro, res, image = sim.simxGetVisionSensorImage(clientID, camera, 0, sim.simx_opmode_streaming)
	frame, resol = getImage(camera)

	src = frame.copy()
	img = basicFilter(src, 1)
	isolImg, nres, points = isolateFace(img, resol)


	cv2.imwrite('7new.png', isolImg)
	text = pytes.image_to_string(isolImg, config='--oem 2 --psm 7 -c tessedit_char_whitelist=0123456789')
	op2 = compareFaces.compareNumber(isolImg, nres)
	print(text, op2)

	return