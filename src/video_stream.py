from urllib.request import urlopen


url_district3 = 'https://cwwp2.dot.ca.gov/data/d3/cctv/cctvStatusD03.csv'
model_path = '../lib/resnet50_coco_best_v2.1.0.h5'

def get_jpeg_urls():
    return_list = []
    district3_csv_string = urlopen(url_district3).read().decode('utf-8')
    for row in district3_csv_string.split('\n'):
        items = row.split(',')
        try:
            potential_jpg = return_list.append(items[22])
            if (potential_jpg):

        except:
            pass
    return return_list

from imageai.Detection import ObjectDetection

def process_image(jpg_url):
    with urlopen(jpg_url) as url:
        f = io.BytesIO(url.read())

detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath(model_path)
detector.loadModel()