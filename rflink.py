from RflinkInterface import RflinkInterface
from ProtocolPacket import ProtocolPacket
from mqttclient import MqttClient
import TranslatePacketValues
import json
import logger


logger = createLogger.logger()mt = MqttClient()


def convertered2json(line):
    
    func = TranslatePacketValues.translates
    try:
        for pp in ProtocolPacket(line):
            yield json.dumps({k: func(k, v) for k, v in pp.keyvaluepair.items()})
    except KeyError:
        logger.error(line)


def main():
    rflinkInterface = RflinkInterface()
    while True:
        for line in rflinkInterface:
            for json_ in convertered2json(line):
                logger.info(json_)
                mt.publish("433mhz/incomming", json_)


if __name__ == "__main__":
    main()
