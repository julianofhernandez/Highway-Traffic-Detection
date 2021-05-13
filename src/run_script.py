import time, sched
from functions import *
from vardata import camera_urls, resnet_model_path, minimum_probibility, custom_objects, download_path

det = setup_retinanet_detector(resnet_model_path)
jpg_list = get_jpg_list()


# jpg_path = download_jpg(jpg_list[124])

def run_every_minute():
    s.enter(60, 1, run_every_minute, ())
    jpg_path = download_jpg(jpg_list[124])
    objects = process_image(det, jpg_path)
    write_objects_to_file("savefile.csv", objects, time.time())
    print(objects)

s = sched.scheduler(time.time, time.sleep)

s.enter(60, 1, run_every_minute, ())
s.run()