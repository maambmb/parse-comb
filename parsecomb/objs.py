
class Result():
    def __init__(self,**args):
        self.error = args.get( "error" )
        self.result = args.get( "result" )
    def is_error(self):
        return self.error is not None
    def extract(self):
        if self.is_error():
            raise ValueError( self.error )
        return self.result
    def map(self,fn):
        if self.is_error():
            return self
        return Result( result = fn( self.result ) )
    def check(self,pred,**args):
        if self.is_error() or pred( self.result ):
            return self
        return Result( error = args.get( "error", "predicate failed" ) )

class StrInput():
    def __init__(self,str,**args):
        self.str = str
        self.pos = args.get( "pos", 0 )
    def _is_at_end(self):
        return self.pos == len(self.str)
    def consume_char(self):
        if self._is_at_end():
            return Result( error = "end of data reached" )
        self.pos += 1
        return Result( result = self.str[ self.pos - 1 ] )
    def consume_end(self):
        if self._is_at_end():
            return Result( result = None )
        return Result( error = "end of data not reached" )
    def clone(self):
        return StrInput(self.str,pos = self.pos )
    def mimic(self,other):
        self.str = other.str
        self.pos = other.pos

class Parser(object):
    def __call__(self,strinput):
        if isinstance(strinput,basestring):
            strinput = StrInput(strinput)
        return self.parse(strinput)
    def map(self, fn ):
        return MapParser( self, fn )
    def check(self,fn):
        return CheckParser( self, fn )

class CheckParser(Parser):
    def __init__(self,parser,predicate):
        self.parser = parser
        self.predicate = predicate
    def parse(self,strinput):
        return self.parser.parse( strinput ).check( self.predicate )

class MapParser(Parser):
    def __init__(self,parser,map):
        self.parser = parser
        self.map = map
    def parse(self,strinput):
        return self.parser.parse( strinput ).map( self.map )
