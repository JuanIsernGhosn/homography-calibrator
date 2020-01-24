import PIL
from urllib.request import urlopen
from Model.key import _KEY
import os
from io import BytesIO
from Model.observable import Observable
from Model.map import Map
import math

_EARTHPIX = 268435456  # Number of pixels in half the earth's circumference at zoom = 21
_DEGREE_PRECISION = 4  # Number of decimal places for rounding coordinates
_TILESIZE = 640        # Larget tile we can grab without paying
_DEGREE_PRECISION = 4  # Number of decimal places for rounding coordinates
_pixrad = _EARTHPIX / math.pi


def _grab_tile(lat, lon, zoom, maptype, _TILESIZE):
    urlbase = 'https://maps.googleapis.com/maps/api/staticmap?center=%f,%f&zoom=%d&maptype=%s&size=%dx%d&format=jpg'
    urlbase = urlbase + "&key=" + _KEY

    specs = lat, lon, zoom, maptype, _TILESIZE, _TILESIZE
    filename = 'mapscache/' + ('%f_%f_%d_%s_%d_%d' % specs) + '.jpg'

    if os.path.isfile(filename):
        tile = PIL.Image.open(filename)
    else:
        url = urlbase % specs
        result = urlopen(url).read()
        tile = PIL.Image.open(BytesIO(result))
        # Some tiles are in mode `RGBA` and need to be converted
        if tile.mode != 'RGB':
            tile = tile.convert('RGB')
        if not os.path.exists('mapscache'):
            os.mkdir('mapscache')
        tile.save(filename)
    return tile


class BirdViewer:

    def __init__(self):
        self.map = Observable(Map())

    def change_map(self, lat, lon, zoom, map_type):
        map_img = _grab_tile(lat, lon, zoom, map_type, _TILESIZE)
        map = Map(lat, lon, zoom, map_type, map_img)
        self.map.set(map)

    def change_zoom(self, zoom):
        curr_map = self.map.get()
        curr_map.zoom = zoom
        self.update_map(curr_map)

    def change_map_type(self, map_type):
        curr_map = self.map.get()
        curr_map.map_type = map_type
        self.update_map(curr_map)

    def change_map_coords(self, latitude, longitude):
        curr_map = self.map.get()
        curr_map.lat = float(latitude)
        curr_map.lon = float(longitude)
        self.update_map(curr_map)

    def update_map(self, map):
        map_img = _grab_tile(map.lat, map.lon, map.zoom, map.map_type, _TILESIZE)
        map.img = map_img
        self.map.set(map)

    def get_coord_from_px(self, px_point):

        latitude = self.map.get().lat
        longitude = self.map.get().lon

        lonpix = int(_EARTHPIX + longitude * math.radians(_pixrad))

        sinlat = math.sin(math.radians(latitude))
        latpix = int(_EARTHPIX - _pixrad * math.log((1 + sinlat) / (1 - sinlat)) / 2)

        lat_args = latpix+self._pixels_to_degrees(px_point[1]-(_TILESIZE/2))
        lon_args = lonpix+self._pixels_to_degrees(px_point[0]-(_TILESIZE/2))

        print(lat_args)
        print(lon_args)

        lat = self._pix_to_lat(lat_args)
        lon = self._pix_to_lon(lon_args)

        print(lat)
        print(lon)

        print(self._lat_to_pix(lat))
        print(self._lon_to_pix(lon))

        return lat, lon

    def get_px_from_coord(self, coord_point):

        latitude = coord_point[0]
        longitude = coord_point[1]

        latpix = self._pix_to_lat(latitude)
        lonpix = self._pix_to_lon(longitude)

        return (latpix, lonpix)

    def _degrees_to_pixels(self, degrees):
        return degrees / 2 ** (21 - self.map.get().zoom)

    def _lat_to_pix(self, lat):
        hola = (math.tan(math.radians(lat)/2+math.pi))
        return _pixrad * math.exp(-1) * math.log(hola) +_EARTHPIX

    def _lon_to_pix(self, lon):
        return math.radians(lon)*_pixrad+_EARTHPIX

    def _pixels_to_degrees(self, pixels):
        return pixels * 2 ** (21 - self.map.get().zoom)

    def _pix_to_lon(self, lonpix):
        return math.degrees((lonpix - _EARTHPIX) / _pixrad)

    def _pix_to_lat(self, latpix):
        return math.degrees(math.pi / 2 - 2 * math.atan(math.exp((latpix - _EARTHPIX) / _pixrad)))


