# coding:utf-8
from flask import Blueprint

api = Blueprint('api', __name__)

from service_api.v1_0 import houseowner
from service_api.v1_0 import test