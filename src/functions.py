import os
import io
import uuid
import csv
import random
from imageai.Detection import ObjectDetection
from urllib.request import urlopen
from vardata import camera_urls, resnet_model_path, minimum_probibility, custom_objects, download_path

os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'

def get_m3u8_urls():
    '''Gets a list of the m3u8 urls from the CalTrans district 3 csv'''
    return_list = []
    csv_string = urlopen(camera_urls['district3']).read().decode('utf-8')
    for row in csv_string.split('\n'):
        items = row.split(',')
        try:
            potential_jpg = items[20]
            if (potential_jpg[-5:] == ".m3u8"):
                return_list.append(potential_jpg)
        except Exception as E:
            pass
    return return_list

def get_chunklist_from_m3u8(m3u8_url):
    '''Gets the chunklist from an m3u8'''
    base_path = os.path.split(m3u8_url)[0]
    ts_urls = []
    try:
        m3u8_data = urlopen(m3u8_url).read().decode('utf-8')
        chunklist = []
        for row in m3u8_data.split('\n'):
            try:
                if (row[0] != '#'):
                    chunklist.append(os.path.join(base_path, row))
            except:
                pass
        for chunk in chunklist:
            chunk_data = urlopen(chunk).read().decode('utf-8')
            for row in chunk_data.split('\n'):
                try:
                    if (row[0] != '#'):
                        ts_urls.append(os.path.join(base_path, row))
                except:
                    pass
    except Exception as e:
        logging.error(m3u8_url + repr(e))
        print(e)
    return ts_urls

def get_jpg_list():
    '''Returns a list of all the jpg urls from the district3 CalTrans csv'''
    jpg_list = []
    csv_string = urlopen(camera_urls['district3']).read().decode('utf-8')
    for row in csv_string.split('\n'):
        items = row.split(',')
        try:
            potential_jpg = items[22]
            filename, file_extension = os.path.splitext(potential_jpg)
            if (file_extension == ".jpg"):
                jpg_list.append(potential_jpg)
        except Exception as E:
            pass
    return jpg_list

def download_jpg(jpg_url):
    '''Takes a url for a jpg and returns a location for it'''
    file_name = os.path.join(download_path, str(uuid.uuid4()) + '.jpg')
    with open(file_name, 'wb') as jpg_file:
        jpg_file.write(urlopen(jpg_url).read())
    return file_name

def setup_retinanet_detector(model_path):
    '''Accepts a model path and returns the detector object'''
    detector = ObjectDetection()
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath(model_path)
    detector.loadModel()
    return detector

def process_image(detector, jpg_path):
    '''Accepts a path to a jpg and returns the ImageAI objects recognized in it'''
    detector = setup_retinanet_detector(resnet_model_path)
    filename, file_extension = os.path.splitext(jpg_path)
    new_file_path = filename + '_processed.jpg'
    detections = detector.detectCustomObjectsFromImage(
        custom_objects = custom_objects,
        input_image=jpg_path, 
        output_image_path=new_file_path, minimum_percentage_probability=minimum_probibility
    )
    os.remove(jpg_path)
    remove_image(new_file_path)
    return detections

def remove_image(jpg_path):
    if (random.uniform(0,100) < 1):
        pass
    else:
        os.remove(jpg_path)

def write_objects_to_file(filename, objects, time):
    cars = 0
    trucks = 0
    for object in objects:
        # print(object)
        if (object['name'] == 'car'):
            cars += 1
        if (object['name'] == 'truck'):
            trucks += 1

    with open(filename, "a") as f:
        writer = csv.writer(f)
        writer.writerow([time, cars, trucks])