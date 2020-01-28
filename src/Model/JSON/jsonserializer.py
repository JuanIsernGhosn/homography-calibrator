import json

def serialize_homo_data(homography):
    json_ser={
        "image_name": homography.image.get().filename,
        "px": homography.px.get().tolist(),
        "coord": homography.coord.get().tolist(),
        "h_matrix": homography.h.get().tolist()
    }
    return json_ser

def save_json_file(json_data, filename):
    with open(filename, 'w') as json_file:
        json.dump(json_data, json_file)

def read_json_file(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
    return data