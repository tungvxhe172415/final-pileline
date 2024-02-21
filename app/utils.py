import json

from flask import jsonify

from app.model import MessageModel
from app.extensions import red

def send_result(data: any = None, message_id: str = '', message: str = "OK", code: int = 200,
                status: str = 'success', show: bool = False, duration: int = 0,
                val_error: dict = None, is_dynamic=False):
    """
    Args:
        data: simple result object like dict, string or list
        message: message send to client, default = OK
        code: code default = 200
        version: version of api
    :param data:
    :param message_id:
    :param message:
    :param code:
    :param status:
    :param show:
    :param duration:
    :param val_error:
    :param is_dynamic:
    :return:
    json rendered sting result
    """
    message_dict = {
        "id": message_id,
        "text": message,
        "status": status,
        "show": show,
        "duration": duration,
        "dynamic": is_dynamic
    }
    MessageString = red.get(f"message:{message_id}")
    if MessageString != None:
        MessageDict = json.loads(MessageString)
    else :
        MessageDict = {}

    message_obj = MessageModel(**MessageDict)
    if message_obj:
        if message_dict['dynamic'] == 0:
            message_dict['text'] = message_obj.message
        else:
            message_dict['text'] = message_obj.message.format(**val_error)
        message_dict['status'] = message_obj.status
        message_dict['show'] = message_obj.show
        message_dict['duration'] = message_obj.duration

    res = {
        "code": code,
        "data": data,
        "message": message_dict
    }

    return jsonify(res), 200


def trim_dict(input_dict: dict) -> dict:
    """

    Args:
        input_dict:

    Returns:

    """
    # trim dict
    new_dict = {}
    for key, value in input_dict.items():
        if isinstance(value, str):
            new_dict[key] = value.strip()
        else:
            new_dict[key] = value
    return new_dict




