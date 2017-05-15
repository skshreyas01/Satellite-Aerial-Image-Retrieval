import math

# EARTH_RADIUS = 6378137
MIN_LATITUDE = -85.05112878
MAX_LATITUDE = 85.05112878
MIN_LONGITUDE = -180
MAX_LONGITUDE = 180

def clipInputs(numOfClips, minValue, maxValue):
	
	return min(max(numOfClips, minValue), maxValue)

def getSizeOfMap(levelOfDetail):
	
	return 256 << levelOfDetail

def GroundResolution(latitude, levelOfDetail):

 	latitude = clipInputs(latitude, MIN_LATITUDE, MAX_LATITUDE)
 	return math.cos(latitude*math.pi / 180) * 2 * math.pi * EARTH_RADIUS / MapSize(levelOfDetail)

def MapScale(latitude, levelOfDetail, screenDpi):
	
 	return GroundResolution(latitude, levelOfDetail) * screenDpi/0.0254 

def convertLocationToPixel(latitude, longitude, levelOfDetail):
	
	latitude = clipInputs(latitude, MIN_LATITUDE, MAX_LATITUDE)
	longitude = clipInputs(longitude, MIN_LONGITUDE, MAX_LONGITUDE)

	x = (longitude + 180) / 360
	sinLatitude = math.sin(latitude * math.pi / 180)
	y = 0.5 - math.log((1 + sinLatitude) / (1 - sinLatitude)) / (4 * math.pi)

	mapSize = getSizeOfMap(levelOfDetail)
	pixelX = int(clipInputs(x * mapSize + 0.5, 0, mapSize - 1))
	pixelY = int(clipInputs(y * mapSize + 0.5, 0, mapSize - 1))

	return pixelX, pixelY

def PixelXYToLatLong(pixelX, pixelY, levelOfDetail):
	
 	mapSize = getSizeOfMap(levelOfDetail)
 	x = (clipInputs(pixelX, 0, mapSize-1) / mapSize) - 0.5
 	y = 0.5 - (clipInputs(pixelY, 0, mapSize - 1) / mapSize)

 	latitude = 90 - 360 * math.atan(math.exp(-y * 2 * math.pi)) / math.pi
 	longitude = 360 * x

 	return latitude, longitude

def convertPixelToTile(pixelX, pixelY):
	
	tileX = int(pixelX / 256)
	tileY = int(pixelY / 256)
	return tileX, tileY

def TileXYToPixelXY(tileX, tileY):
	
 	pixelX = tileX * 256
 	pixelY = tileY * 256

def convertTileToQuadKey(tileX, tileY, levelOfDetail):
	
	quadKey = ""
	for i in range(levelOfDetail, 0, -1):
		digit = '0'
		mask = 1 << (i-1)
		if ((tileX & mask) != 0):
			digit = chr(ord(digit) + 1)
		if ((tileY & mask) != 0):           # "and" is for booleans, "&" is for bits
			digit = chr(ord(digit) + 1)
			digit = chr(ord(digit) + 1)
		quadKey += digit
	return quadKey

def convertLocationToQuadKey(latitude, longitude, levelOfDetail):
 	pixelX, pixelY = convertLocationToPixel(latitude, longitude, levelOfDetail)
	
 	tileX, tileY = convertPixelToTile(pixelX, pixelY)
	
 	quadKey = convertTileToQuadKey(tileX, tileY, levelOfDetail)
	

def convertLocationToTile(latitude, longitude, levelOfDetail):
	pixelX, pixelY = convertLocationToPixel(latitude, longitude, levelOfDetail)
	tileX, tileY = convertPixelToTile(pixelX, pixelY)
	return tileX, tileY