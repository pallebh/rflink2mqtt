from unittest import TestCase
import ProtocolPacket
import os
import TranslatePacketValues
import json


def translates( keyword , value ):
    k2f = TranslatePacketValues.keyword2function
    units = TranslatePacketValues.UNITS

    func = lambda x: x
    if keyword in k2f :
        func = k2f[ keyword ]

    if not func and keyword in units :
        func = units[keyword]

    return func( value )

class ProcotolPakcetTest(TestCase):
    def test_ProtocolPacket(self):
        print(os.listdir())
        with open( os.path.join( 'protocol.txt' ) , 'rt') as file_:
            for line in file_:
                for pp in ProtocolPacket.ProtocolPacket(line):
                    keyvaluepair = { keyword : translates(keyword, value) for keyword , value in pp.keyvaluepair.items() }
                    header = pp.header
                    print( json.dumps( { **{"header" : header }, **{"labels" : keyvaluepair } } ) )



