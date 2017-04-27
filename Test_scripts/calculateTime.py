import time
import json


class calculateTime:

    def __init__(self, response):

        self.res = response

    def calTime(self):

        send_time = json.loads(str(self.res.text))['sendtime']
        back_time = json.loads(str(self.res.text))['backtime']

        send = send_time.split(" ")
        back = back_time.split(" ")

        timeArray_send = time.strptime(send[0]+" "+send[1], "%Y-%m-%d %H:%M:%S")
        timeArray_back = time.strptime(back[0]+" "+back[1], "%Y-%m-%d %H:%M:%S")

        timeStamp_send = int(time.mktime(timeArray_send) * 1000 + int(send[2]))
        timeStamp_back = int(time.mktime(timeArray_back) * 1000 + int(back[2]))

        if timeStamp_back == timeStamp_send:
            return str('<1')
        else:
            return int(timeStamp_back - timeStamp_send)