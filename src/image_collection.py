from urllib.request import urlopen
from vardata import camera_urls
import os
import logging

logging.basicConfig(filename=__name__ + '.log', filemode="a")



def get_m3u8_urls():
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

urls = get_m3u8_urls()
print(get_ts_from_m3u8_urls(urls))