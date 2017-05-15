from bing_utilities import *
from PIL import Image
import sys,urllib,math
import io,operator
import socket

def generate_url(quad_key):
    #print quad_key
    #key = 'Ar06c1OUpI2J_CqetJaaKjfTaHjaC8ZtnK_cOPDzd6VBkZN2jimQC3Li0_TjmXIq'
    return "http://h0.ortho.tiles.virtualearth.net/tiles/h%s.jpeg?g=131&" % quad_key


def get_tile_from_quadkey(quad_key):
        sock = urllib.urlopen(generate_url(quad_key))
        read_sock = sock.read()
        tile = Image.open(io.BytesIO(read_sock))
        return tile


def check_null(tile):
    res = (tile == Image.open('error.jpeg'))
    return res

def get_reduced_quality(lat1,lon1,lat2,lon2):
    index=1
    for index in xrange(23,0,-1):
        tile1X, tile1Y = convertLocationToTile(lat1, lon1, index)
        tile2X, tile2Y = convertLocationToTile(lat2,lon2,index)
        if tile1X > tile2X:
            tile1X,tile2X = tile2X,tile1X
        if tile1Y > tile2Y:
            tile1Y, tile2Y = tile2Y, tile1Y
        if(tile2X - tile1X <= 1) and (tile2Y - tile1Y <= 1):
            print "Lowest Zoom Level"
            print index
            return index, tile1X, tile1Y
    print "Error"


def main():
    latitude1 = float(sys.argv[1])
    longitude1 = float(sys.argv[2])
    latitude2 = float(sys.argv[3])
    longitude2 = float(sys.argv[4])

    try:
        socket.create_connection(("www.bing.com",80))
    except:
        print "No Internet Connection"
        sys.exit(0)



    initial_size = 2048
    minimum_size = 128

    final_image = Image.new('RGB',(initial_size,initial_size))
    i, tileX, tileY = get_reduced_quality(latitude1,longitude1,latitude2,longitude2)
    tilesize = initial_size/2
    optimal_flag = True
    optimal_image = final_image

    while i<=23 and tilesize >= minimum_size and optimal_flag:
        print "Current Zoom Level is"
        print i

        tileX1,tileY1 = convertLocationToTile(latitude1,longitude1,i)
        tileX2,tileY2 = convertLocationToTile(latitude2,longitude2,i)
        if(tileX1 > tileX2):
            tileX1,tileX2 = tileX2,tileX1
        if(tileY1 > tileY2):
            tileY1,tileY2 = tileY2,tileY1
        for m in xrange(tileX1,tileX2+1):
            if not optimal_flag:
                break
            for n in xrange(tileY1,tileY2+1):
                if not optimal_flag:
                    break
                quad_key = convertTileToQuadKey(m,n,i)

                tile = get_tile_from_quadkey(quad_key)

                if not check_null(tile):
                    tile = tile.resize((tilesize,tilesize))
                    initx = (m-tileX) * tilesize
                    inity = (n-tileY) * tilesize
                    destx = initx + tilesize
                    desty = inity + tilesize
                    final_image.paste(tile,(initx,inity,destx,desty))
                else:
                    optimal_flag = False
                    break
                    print "Bing Conn Prob"
                    continue
        tileX = tileX * 2
        tileY = tileY * 2
        i += 1
        tilesize /= 2
        if optimal_flag:
            optimal_image=final_image

    print("Finished Processing")
    optimal_image.save('Result.jpeg')
    final_image.show()




if __name__ == '__main__':
	main()