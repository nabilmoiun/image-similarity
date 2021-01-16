import requests
from flask import Flask, jsonify, request

app = Flask(__name__)
URL = "https://api.deepai.org/api/image-similarity"
# Pass this api key for auth in the input; can also use your own by signing up to https://deepai.org/
API_KEY = "b19deb19-152c-4c6f-abea-898d6409efa2"


@app.route('/compare-image', methods=['POST'])
def compare():
    """
    Compares two images and returns a value that tells you how visually similar they are. The lower the the score, the more contextually similar the two images are with a score of '0' being identical.
    input format:
    {
    "api-key": "b19deb19-152c-4c6f-abea-898d6409efa2",
    "image_url1": "IMAGE_URL",
    "image_url2": "IMAGE_URL"
    }
    output format:
    {
    "similarity_score": <int:score>
    }
    """

    if 'api-key' not in request.json:
        return jsonify({"success": False, "error": "Api Key is missing"})
    if 'image_url1' not in request.json:
        return jsonify({"success": False, "error": "Please pass two image urls to compare"})
    if 'image_url2' not in request.json:
        return jsonify({"success": False, "error": "Please pass two image urls to compare"})
        
    api_key = request.json['api-key']
    image1 = request.json['image_url1']
    image2 = request.json['image_url2']
    images = {
        "image1": image1,
        "image2": image2
    }
    headers = {'api-key': api_key}
    response = requests.post(URL, data=images, headers=headers).json()
    try:
        score = response['output']['distance']
    except KeyError:
        return jsonify(response)
    return jsonify({"sucess": True, "similarity_score": score})


if __name__ == '__main__':
    app.run(debug=True)