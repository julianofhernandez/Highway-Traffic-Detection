import os
import io
import uuid
from imageai.Detection import ObjectDetection

from vardata import resnet_model_path, minimum_probibility, custom_objects

os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'

def download_jpg(jpg_url):
    '''Takes a url for a jpg and returns a location for it'''
    file_name = str(uuid.uuid4())
    with open(file_name, 'wb') as jpg_file:
        jpg_file.write(urlopen(jpg_url).read())
    return file_name

def setup_retinanet_detector(model_path):
    detector = ObjectDetection()
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath(model_path)
    detector.loadModel()
    return detector

def process_image(jpg_path):
    detector = setup_retinanet_detector(resetnet_model_path)
    detector.detectCustomObjectsFromImage(
        custom_objects,
        input_image=jpg_path, 
        output_image_path="imagenew.jpg", minimum_percentage_probability=minimum_probibility
    )