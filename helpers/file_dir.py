import uuid
from helpers import date
import os


def get_file_path(file_path):

    if file_path.find("?") >-1:
        file_path = file_path[:file_path.find("?")]
    elif file_path.find("!") > -1:
        file_path = file_path[:file_path.find("!")]
    upload_dir = get_upload_dir()

    file_name = str(uuid.uuid1())
    #extension = os.path.splitext(file_path)[1]
    return ['upload/'+upload_dir + file_name.replace('-', '') +'.jpg' , date_dir()+file_name.replace('-', '') +'.jpg']


def get_upload_dir():
    return date_dir()


def date_dir():
    return date.get_year()+""+date.get_month()+"/"+date.get_day()+"/"


def get_file_name():
    uuid_str = str(uuid.uuid1())
    return uuid_str.replace('-', '') + '.png'