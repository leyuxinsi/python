import time
import datetime


def get_timestamp():
    return int(time.time())


def current_date():
    return datetime.datetime.now()


def get_year():
    current_time = current_date()
    return current_time.strftime('%Y')


def get_month():
    current_time = current_date()
    return current_time.strftime('%m')


def get_day():
    current_time = current_date()
    return current_time.strftime('%d')

