# coding:utf-8
from . import api


@api.route("/api/v1.0/test", methods=["GET"])
def json_test():
    return "hello world"


