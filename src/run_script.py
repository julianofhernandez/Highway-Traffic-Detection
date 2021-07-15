import time, sched, logging
import sys
from functions import *
from vardata import camera_urls, resnet_model_path, minimum_probibility, custom_objects, download_path


def cycles():
    run_every_minute()
    cycles()


def run_every_minute():
    # jpg_path = download_jpg(jpg_list[124])
    jpg_path = download_jpg(jpg_list[44])
    objects = process_image(det, jpg_path)
    write_objects_to_file(objects, time.time())
    logging.warning('Iteration ' + str(id))
    print(objects)
    print()
    time.sleep(60)


if __name__ == "__main__":
    for arg in sys.argv:
        if(arg == "run"):
            det = setup_retinanet_detector(resnet_model_path)
            jpg_list = get_jpg_list()

            os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'
            cycles()
        elif (arg == "print"):
            create_plot('Cars per minute.png')
