import os
import io
import uuid
import csv
import random
import logging
import time
from imageai.Detection import ObjectDetection
from urllib.request import urlopen
import matplotlib.pyplot as plt
import numpy as np
from vardata import camera_urls, resnet_model_path, \
minimum_probibility, custom_objects, download_path, save_file



# logging.basicConfig(filename='tmp\example.log', encoding='utf-8', level=logging.DEBUG)

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
    # remove_image(new_file_path)
    os.remove(jpg_path)
    return detections

def remove_image(jpg_path):
    if (random.uniform(0,100) < 1):
        pass
    else:
        os.remove(jpg_path)

def write_objects_to_file(objects, time):
    filename = save_file
    cars = 0
    trucks = 0
    for object in objects:
        # print(object)
        if (object['name'] == 'car'):
            cars += 1
        if (object['name'] == 'truck'):
            trucks += 1

    if os.path.exists(filename):
        with open(filename, "a", newline='') as f:
            writer = csv.writer(f)
            writer.writerow([time, cars, trucks])
    else:
        with open(filename, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow([time, cars, trucks])

def create_plot(filename):
    times, cars, trucks = [], [], []

    if os.path.exists(filename):
        os.remove(filename)

    print('Making plot')
    if os.path.exists(save_file):
        with open(save_file, 'r', newline='') as f:
            reader = csv.reader(f)
            for line in reader:
                times.append(float(line[0]))
                cars.append(int(line[1]))
                trucks.append(int(line[2]))
        print(times)
        print(cars)
        print(trucks)
    else:
        print('No savefile.csv to plot')

    fig = plt.figure()
    # Setup labels
    plt.title("Cars per minute")
    plt.xlabel(
        "From: " + 
        str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(times[0]))) + 
        "\nTo: " + 
        str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(times[-1]))))
    plt.ylabel("Cars")
    plt.xticks([])
    plt.plot(times, cars, label="Cars per minute")
    fig.savefig(filename)