import PIL
from urllib.request import urlopen
from Model.key import _KEY
import os
from io import BytesIO
from Model.observable import Observable
from Model.map import Map

_EARTHPIX = 268435456  # Number of pixels in half the earth's circumference at zoom = 21
_DEGREE_PRECISION = 4  # Number of decimal places for rounding coordinates
_TILESIZE = 640        # Larget tile we can grab without paying


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

    def get_coord_from_px(self, x, y):
        # [TODO: Transform map px to coordinates]
        return x, y
