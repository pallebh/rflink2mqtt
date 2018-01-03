import re
import collections

parseresult = collections.namedtuple( 'parseresult' , ' header  keyvaluepair' )

class ProtocolPacket:

    def __init__(self, line):
        self.headerRegex = "(\d{2};[0-9A-Fa-f]+;[\w /]+;)"
        self.keyvaluepairsRegex = "((?:(?:\w+)=(?:[\w =]+?);)+)"
        self.protcolPacketRegex = re.compile(self.headerRegex + self.keyvaluepairsRegex)
        self.headerName = ["node", "id", "name"]
        self.cmds = []
        self.cmdsIter = iter(self.cmds)

        for pp in self.__protocolpacket(line):
            header, keyvaluepairs = pp
            header = collections.OrderedDict( self.__header( header ) )
            keyvaluepairs = collections.OrderedDict( self.__keyvaluepairs( keyvaluepairs ) )
            self.cmds.append( parseresult( header , keyvaluepairs ) )

    def __header(self, header):
        header = header.split(";")[0:-1]
        header = dict(list(zip(self.headerName, header)))
        return header

    def __keyvaluepairs(self, keyvaluepairs):
        return [ tuple( map( str.lower , kvp.split( '=' , 1  ) ) ) for kvp in keyvaluepairs.split(";") ][:-1]

    def __protocolpacket(self, line):
        return [ kvn.groups() for kvn in re.finditer(self.protcolPacketRegex,line) ]

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.cmdsIter)
