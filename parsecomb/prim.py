from objs import *

class FailParser(Parser):
    def __init__(self,**args):
        self.error = args.get( "error", "something went wrong" )
    def parse(self,strinput):
        return Result( error = self.error )

class VoidParser(Parser):
    def __init__(self,**args):
        self.result = args.get( "result", None )
    def parse(self,strinput):
        return Result( result = self.result )

class AnyParser(Parser):
    def parse(self,strinput):
        return strinput.consume_char()

class EOSParser(Parser):
    def parse(self,strinput):
        return strinput.consume_end()

class PeekParser(Parser):
    def __init__(self,parser):
        self.parser = parser
    def parse(self,strinput):
        clone = strinput.clone()
        return self.parser(clone)
        
class CharParser(AnyParser):
    def __init__(self,char):
        self.char = char
    def parse(self,strinput):
        result = super(CharParser,self).parse(strinput)
        return result.check( lambda x : x == self.char )

class FirstParser(Parser):
    def __init__(self,*parsers):
        self.parsers = parsers
    def parse(self,strinput):
        errors = list()
        cloned = strinput.clone()
        for parser in self.parsers:
            strinput.mimic( cloned )
            result = parser(strinput)
            if not result.is_error():
                return result
            errors.append( result.error )
        return Result( error = ",".join( errors ) )

class TryParser(FirstParser):
    def __init__(self,parser,**args):
        super(TryParser,self).__init__( parser, VoidParser( result = args.get( "default" ) ) )

class AllParser(Parser):
    def __init__(self,*parsers):
        self.parsers = parsers
    def parse(self,strinput):
        results = list()
        for parser in self.parsers:
            result = parser(strinput)
            if result.is_error():
                return result
            results.append( result.result )
        return Result( result = results )

class ManyParser(Parser):
    def __init__(self,parser):
        self.parser = parser
    def parse(self,strinput):
        results = list()
        while True:
            cloned = strinput.clone()
            result = self.parser(cloned)
            if result.is_error():
                return Result( result = results )
            strinput.mimic( cloned )
            results.append( result.result )

class ManyOneParser(AllParser):
    def __init__(self,parser):
        super(ManyOneParser,self).__init__( parser, ManyParser( parser ) )
    def parse(self,strinput):
        result = super(ManyOneParser,self).parse(strinput)
        return result.map( lambda res: [ res[0] ] + res[1] )
    
class ManyUntilParser(Parser):
    def __init__(self,many_parser,until_parser):
        self.many_parser = many_parser
        self.until_parser = until_parser
    def parse(self,strinput):
        results = list()
        while True:
            cloned = strinput.clone()
            until_res = self.until_parser( strinput )
            if not until_res.is_error():
                return Result( result = ( results, until_res.result ) )
            strinput.mimic( cloned )
            many_res = self.many_parser( strinput )
            if many_res.is_error():
                return many_res
            results.append( many_res.result )

class ManyOneUntilParser(AllParser):
    def __init__(self,many,until):
        super(ManyOneUntilParser,self).__init__( many, ManyUntilParser( many, until ) )
    def parse(self,strinput):
        result = super(ManyOneUntilParser,self).parse(strinput)
        return result.map( lambda res: ( [ res[0] ] + res[1][0], res[1][1] ) )

class SepByOneParser(AllParser):
    def __init__(self,parser,seperator):
        super(SepByOneParser,self).__init__( parser, ManyParser( AllParser( seperator, parser ) ) )
    def parse(self,strinput):
        result = super(SepByOneParser,self).parse(strinput)
        return result.map( lambda res: [ res[0] ] + [ y[1] for y in res[1] ]  )

class SepByParser(FirstParser):
    def __init__(self,parser,seperator):
        super(SepByParser,self).__init__( SepByOneParser( parser, seperator ), VoidParser( result = list() ) )
