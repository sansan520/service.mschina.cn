# coding:utf-8
from flask import Blueprint


api = Blueprint('api', __name__)

from service_api.v1_0 import userbase
from service_api.v1_0 import houseowner
from service_api.v1_0 import housetype
from service_api.v1_0 import guestroom
from service_api.v1_0 import houseresources

# from service_api.v1_0 import test
