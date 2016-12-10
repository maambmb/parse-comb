Parse Comb
==========

A barebones parser combinator library for python

## Usage

The best way to explain usage is through an example:

```python
import parsecomb

str_to_parse = "foobar( 1, 2, 3, 18, pos_arg = 5, another_pos_arg = 17 )"
input_to_parse = parsecomb.StrInput( str_to_parse )

# this one shouldn't work...
err_input = parsecomb.StrInput( "foobar[]" )

parser = parsecomb.AllParser(
    # parse a padded identifier
    parsecomb.PadParser( parsecomb.IdentParser() ),
    # parse some amount of whitespace
    parsecomb.WhiteSpacesParser(),
    # parse a parser that is wrapped by a parens set ( )
    parsecomb.WrapParser(
        parsecomb.WrapParser.parens, 
        # repeatedly parse something that is seperated by a comma
        parsecomb.SepByParser(
            # parse a padded argument
            parsecomb.PadParser(
                # an argument is either an integer or a named argument
                parsecomb.FirstParser(
                    parsecomb.IntParser(),
                    # a named argument is formed by an identifier, a padded equals and then an integer
                    parsecomb.AllParser(
                        parsecomb.IdentParser(),
                        parsecomb.PadParser( parsecomb.WordParser( "=" ) ),
                        parsecomb.IntParser()
                    ).map( lambda x : dict( arg = x[0], val = x[2] ) )
                )
            ), 
            parsecomb.WordParser( "," )
        )
    )
).map( lambda x : dict( fn_name = x[0], args = x[2] ) )

result = parser( input_to_parse )
print result.extract()
# should print:
# {
#   fn_name = "foobar",
#   args = [
#     1,
#     2,
#     3,
#     18,
#     { 
#       val = 5, 
#       arg_name = "pos_arg"
#     },
#     { 
#       val = 17, 
#       arg_name = "another_pos_arg"
#     },
#   ]
# }

result = parser( err_input )
# this will throw because there is no result
print result.extract()
```
