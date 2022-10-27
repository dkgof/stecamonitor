from lxml import etree

import logging
import requests
import asyncio
import sys

_LOGGER = logging.getLogger(__name__)

class StecaAPI():
    #Steca Grid API definition
    
    def __init__(self, hass, ip):
        self._hass = hass
        self._ip = ip
        self._data = {'acpower': -1, 'acvoltage': -1, 'accurrent': -1, 'derating': -1, 'dcvoltage': -1, 'dccurrent': -1, 'serial': "1234567890NA"}

    def poll(self):
        try:
            r = requests.get("http://"+self._ip+"/measurements.xml")

            if(r.status_code  == 200):
                #Strip <xml> definition
                xml = r.text[38:]

                root = etree.fromstring(xml)

                acpowerList = root.xpath("Device/Measurements/Measurement[@Type='AC_Power']/@Value")
                acvoltageList = root.xpath("Device/Measurements/Measurement[@Type='AC_Voltage']/@Value")
                accurrentList = root.xpath("Device/Measurements/Measurement[@Type='AC_Current']/@Value")
                dcvoltageList = root.xpath("Device/Measurements/Measurement[@Type='DC_Voltage']/@Value")
                dccurrentList = root.xpath("Device/Measurements/Measurement[@Type='DC_Current']/@Value")
                deratingList = root.xpath("Device/Measurements/Measurement[@Type='Derating']/@Value")

                serial = root.xpath("Device/@Serial")[0]

                acpower = 0
                acvoltage = 0
                accurrent = 0
                derating = 0
                dcvoltage = 0
                dccurrent = 0

                if(len(acpowerList)):
                    acpower = acpowerList[0]

                if(len(acvoltageList)):
                    acvoltage = acvoltageList[0]

                if(len(accurrentList)):
                    accurrent = accurrentList[0]

                if(len(deratingList)):
                    derating = deratingList[0]

                if(len(dcvoltageList)):
                    dcvoltage = dcvoltageList[0]

                if(len(dccurrentList)):
                    dccurrent = dccurrentList[0]

                self._data = {'acpower': acpower, 'acvoltage': acvoltage, 'accurrent': accurrent, 'derating': derating, 'dcvoltage': dcvoltage, 'dccurrent': dccurrent, 'serial': serial}
        except:
            _LOGGER.error("Error during poll: %s", sys.exc_info())

        return self._data

    def getData(self):
        return self._data

    def getSerial(self):
        return self._data["serial"]

    def getIp(self):
        return self._ip
