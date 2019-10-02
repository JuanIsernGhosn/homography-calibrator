import json

def serialize_data(homography):
    json_ser={
        "image_name": homography.image.get().filename,
        "px": homography.px.get().tolist(),
        "coord": homography.coord.tolist(),
        "h_matrix": homography.h.get().tolist()
    }
    return json_ser

def save_json_file(json_data, filename):
    with open(filename, 'w') as json_file:
        json.dump(json_data, json_file)
