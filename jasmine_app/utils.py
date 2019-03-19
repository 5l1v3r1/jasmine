from flask import Response


def not_exist(error):
    return Response(error, status=404)
