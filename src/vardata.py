from imageai.Detection import ObjectDetection

camera_urls = {
    'district3': 'https://cwwp2.dot.ca.gov/data/d3/cctv/cctvStatusD03.csv'
}
resnet_model_path = '../lib/resnet50_coco_best_v2.1.0.h5'
yolo_model_path = '../lib/yolo.h5'
minimum_probibility = 30
custom_objects = ObjectDetection().CustomObjects(
    car = True, bicycle=True, bus=True, train=False, truck=True,
)