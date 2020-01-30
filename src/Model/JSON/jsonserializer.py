import json


def serialize_homo_data(homography, bird_calculator):
    json_ser={
        "image_name": homography.image.get().filename,
        "map_coord": (bird_calculator.map.get().lat, bird_calculator.map.get().lon),
        "map_zoom": bird_calculator.map.get().zoom,
        "map_marks_px": homography.px_bird.get().tolist(),
        "camera_marks_px": homography.px.get().tolist(),
        "coord": homography.coord.get().tolist(),
        "h_matrix": homography.h.get().tolist()
    }
    return json_ser


def serialize_per_data(per_manager, bird_calculator):
    json_ser={
        "map_coord": (bird_calculator.map.get().lat, bird_calculator.map.get().lon),
        "map_zoom": bird_calculator.map.get().zoom,
        "perimeters": str(per_manager.perimeters.get()),
        "perimeters_px": str(per_manager.perimeters_px.get())
    }
    return json_ser


def save_json_file(json_data, filename):
    with open(filename, 'w') as json_file:
        json.dump(json_data, json_file)


def read_json_file(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
    return data