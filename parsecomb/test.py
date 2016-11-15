import unittest
from objs import *
from prim import *
from prac import *

class TestParser(unittest.TestCase):
    def test_fail(self):
        result = FailParser( error = "test" )( "" )
        self.assertTrue( result.is_error() )
        self.assertEqual( result.error, "test" )
    def test_void(self):
        result = VoidParser( result = "test" )( "" ).extract()
        self.assertEqual( result, "test" )
    def test_any(self):
        result = AnyParser()( "a" ).extract()
        self.assertEqual( result, "a" )
        result = AnyParser()( "" )
        self.assertTrue( result.is_error() )
    def test_eos(self):
        result = EOSParser()( "" ).extract()
        self.assertIsNone( result )
        result = EOSParser()( "a" )
        self.assertTrue( result.is_error() )
    def test_peek(self):
        peek = PeekParser( AnyParser() )( "a" ).extract()
        pop = AnyParser()( "a" ).extract()
        self.assertEqual( peek, pop )
    def test_try(self):
        tryp = TryParser( CharParser( "b" ) )
        strinput = StrInput( "a" )
        self.assertIsNone( tryp( strinput ).extract() )
        self.assertEqual( CharParser( "a" )( strinput ).extract(), "a" )
    def test_char(self):
        self.assertFalse( CharParser("a")( "a" ).is_error() )
        self.assertTrue( CharParser("b")( "a" ).is_error() )
    def test_first(self):
        parser = FirstParser( CharParser("a"), CharParser("b"), CharParser("c") )
        self.assertEqual( parser( "b" ).extract(), "b" )
    def test_all(self):
        parser = AllParser( CharParser("a"), CharParser("b"), CharParser("c") )
        self.assertEqual( "".join( parser( "abc" ).extract() ), "abc" )
    def test_many(self):
        parser = ManyParser( CharParser( "a" ) )
        self.assertEqual( tuple( parser( "aaa" ).extract() ), ( "a", "a", "a" ) )
        self.assertEqual( tuple( parser( "aba" ).extract() ), ( "a", ) )
        self.assertEqual( tuple( parser( "" ).extract() ), tuple() )
    def test_many_one(self):
        parser = ManyOneParser( CharParser( "a" ) )
        self.assertEqual( tuple( parser( "aaa" ).extract() ), ( "a", "a", "a" ) )
        self.assertEqual( tuple( parser( "aba" ).extract() ), ( "a", ) )
        self.assertTrue( parser( "" ).is_error() )
    def test_many_until(self):
        parser = ManyUntilParser( CharParser( "a" ), AllParser( CharParser( "a" ), CharParser( "b" ) ) )
        result = parser( "aaaab" ).extract()
        self.assertEqual( tuple(result[0]), ( "a", "a", "a" ) )
        self.assertEqual( tuple(result[1]), ( "a", "b" ) )
    def test_many_one_until(self):
        parser = ManyOneUntilParser( CharParser( "a" ), AllParser( CharParser( "a" ), CharParser( "b" ) ) )
        self.assertTrue( parser( "ab" ).is_error() )
    def test_sep_by_one(self):
        parser = SepByOneParser( CharParser( "a" ), CharParser( "b" ) )
        self.assertEqual( tuple( parser( "aba" ).extract() ), ( "a", "a" ) )
        self.assertTrue( parser( "" ).is_error() )
    def test_sep_by(self):
        parser = SepByParser( CharParser( "a" ), CharParser( "b" ) )
        self.assertEqual( len(parser( "" ).extract()), 0 )
    def test_word(self):
        self.assertTrue( WordParser( "yolo" )( "yolox" ).extract(), "yolo" ) 
    def test_charset(self):
        parser = ManyParser( CharSetParser( "abc" ) )
        self.assertEqual( tuple( parser( "aca" ).extract() ), ( "a", "c", "a" ) )
    def test_wordset(self):
        parser = WordSetParser( "abc", "aac", "adc" )
        self.assertEqual( parser( "aac" ).extract(),"aac" )
    def test_whitespace(self):
        self.assertFalse( WhiteSpaceParser()( " " ).is_error() )
    def test_whitespaces(self):
        parser = AllParser( WhiteSpacesParser(), WordParser( "yo" ) ).map( lambda x : x[1] )
        self.assertEqual( parser( "    yo" ).extract(), "yo" ) 
    def test_alpha(self):
        parser = AlphaParser( "_" )
        self.assertTrue( parser("-").is_error() )
        self.assertTrue( parser("9").is_error() )
        self.assertFalse( parser("_").is_error() )
        self.assertFalse( parser("a").is_error() )
    def test_alnum(self):
        parser = AlnumParser( "_" )
        self.assertTrue( parser("-").is_error() )
        self.assertFalse( parser("9").is_error() )
        self.assertFalse( parser("_").is_error() )
        self.assertFalse( parser("a").is_error() )
    def test_digit(self):
        parser = DigitParser()
        self.assertTrue( parser("-").is_error() )
        self.assertFalse( parser("9").is_error() )
        self.assertTrue( parser("_").is_error() )
        self.assertTrue( parser("a").is_error() )
    def test_int(self):
        parser = IntParser()
        self.assertTrue( parser("").is_error() )
        self.assertEqual( parser( "34" ).extract(), 34 )
        self.assertEqual( parser( "+ 434" ).extract(), 434 )
        self.assertEqual( parser( "- 434" ).extract(), -434 )
        self.assertEqual( parser( "0" ).extract(), 0 )
    def test_ident(self):
        parser = AllParser( IdentParser(), EOSParser() ).map( lambda x : x[0] )
        self.assertTrue( parser("5hello").is_error() )
        self.assertTrue( parser("_-5hello").is_error() )
        self.assertEqual( parser("_5hello").extract(), "_5hello" )
    def test_wrap(self):
        parser = WrapParser( WrapParser.thick_parens,
            AllParser( WhiteSpacesParser(), IdentParser(), WhiteSpacesParser() )
        )
        self.assertTrue( parser("( _5hello )").is_error() )
        self.assertEqual( parser("(| _5hello |)").extract()[1], "_5hello" )
    def test_pad(self):
        parser = AllParser( PadParser( IdentParser(), pad = "l" ), EOSParser() )
        self.assertTrue( parser( "yo " ).is_error() )
        self.assertTrue( parser( " yo " ).is_error() )
        self.assertFalse( parser( " yo" ).is_error() )
        self.assertFalse( parser( "yo" ).is_error() )
        parser = AllParser( PadParser( IdentParser() ), EOSParser() ).map( lambda x: x[0] )
        self.assertEqual( parser( " yo " ).extract(), "yo" )



