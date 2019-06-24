import paho.mqtt.client as mqtt
from events import Events
import json


class MyEvents(Events):
    __events__ = ("uplink_msg", "downlink_msg", "connection", "disconnection")


class MQTTClient:

    def __init__(self, APPID, APPEUI, PSW):
        self.__client = mqtt.Client()
        self.__APPID = APPID
        self.__APPEUI = APPEUI
        self.__PSW = PSW
        self.__currentMSG = {}
        self.__events = MyEvents()
        self.connectFlag = 1
        self.disconnectFlag = 0
        self.midCounter = 0

    def connect(self, address='eu.thethings.network', port=1883):
        if self.__client.on_connect is None:
            self.__client.on_connect = self._onConnect()
        self.__client.on_publish = self._onPublish()
        self.__client.on_message = self._onMessage()
        if self.__client.on_disconnect is None:
            self.__client.on_disconnect = self._onDisconnect()

        self.__client.username_pw_set(self.__APPID, self.__PSW)
        self.__client.connect(address, port, 120)

    def _onConnect(self):
        def on_connect(client, userdata, flags, rc):
            if(rc == 0):
                print('CONNECTED AND SUBSCRIBED')
                client.subscribe('+/devices/+/up'.format(self.__APPEUI))
                self.connectFlag = 1
            else:
                print('ERROR CONNECTING')
                self.connectFlag = 0
        return on_connect

    def _onDisconnect(self):
        def on_disconnect(client, userdata, rc):
            if rc != 0:
                print('UNEXPECTED DISCONNECTION')
                self.disconnectFlag = 0
            else:
                self.disconnectFlag = 1
                print('DISCONNECTED')
        return on_disconnect

    def _onMessage(self):
        def on_message(client, userdata, msg):
            print('MESSAGE RECEIVED')
            j_msg = json.loads(msg.payload.decode('utf-8'))
            self.__currentMSG = j_msg
            if self.__events.uplink_msg:
                self.__events.uplink_msg(j_msg, client=self)
        return on_message

    def _onPublish(self):
        def on_publish(client, userdata, mid):
            print('MSG PUBLISHED')
            self.midCounter = mid
            if self.__events.downlink_msg:
                self.__events.downlink_msg(mid, client=self)
        return on_publish

    def setUplinkCallback(self, callback):
        self.__events.uplink_msg += callback

    def setDownlinkCallback(self, callback):
        self.__events.downlink_msg += callback

    def setConnectBehavior(self, connect):
        self.__client.on_connect = connect

    def start(self):
        print('LOOP STARTED')
        self.__client.loop_forever()

    def startBackground(self):
        print('LOOP STARTED BACKGROUND')
        self.__client.loop_start()

    def stopBackground(self):
        print('LOOP STOPPED BACKGROUND')
        self.__client.loop_stop()
        self.disconnect()

    def disconnect(self):
        self.__client.disconnect()
        self.connectFlag = 0

    def publish(self, devID, msg):
        result = self.__client.publish(
            self.__APPID+'/devices/'+devID+'/down',
            msg)
        print("Message will be published on the next uplink message")
