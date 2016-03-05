"""
RAZE Python Libraries
NATO Phonetic Dictionary.

 * CharacterSets - NATO character sets / translation table.

 * PhoneticDictionary - Maps alphanumeric and punctuation characters to their 
                        respective NATO code word.


RAZE - Copyright (c) 2006 James Harris, Erin Houston
$Id: phonetic.py 362 2006-11-29 23:27:53Z james $
"""
__revision__ = "$Revision: 362 $"
__location__ = "$URL: http://dev.icecave.com.au/main/dav/lib/raze/tags/raze-1.2.0/raze/phonetic.py $"
__all__ = [ 'PhoneticDictionary', 'CharacterSets' ]

from re import compile
from container import BidirectionalDictionary, merge_dictionaries


class CharacterSets(object):
    """ Default character sets for PhoneticDictionary. """
    lower_case  = { 'a' : 'alfa', 'b' : 'bravo', 'c' : 'charlie', 'd' : 'delta', 'e' : 'echo', 'f' : 'foxtrot', 'g' : 'golf', 'h' : 'hotel', 'i' : 'india', 'j' : 'juliett', 'k' : 'kilo', 'l' : 'lima', 'm' : 'mike', 'n' : 'november', 'o' : 'oscar', 'p' : 'papa', 'q' : 'quebec', 'r' : 'romeo', 's' : 'sierra', 't' : 'tango', 'u' : 'uniform', 'v' : 'victor', 'w' : 'whiskey', 'x' : 'xray', 'y' : 'yankee', 'z' : 'zulu' }
    upper_case  = dict((k.upper(), v.upper()) for k, v in lower_case.iteritems())
    punctuation = { '!' : 'EXCLAMATION', '\'' : 'SINGLE_QUOTE', '"' : 'DOUBLE_QUOTE', '#' : 'HASH', '$' : 'DOLLAR', '%' : 'PERCENT', '&' : 'AMPERSAND', '(' : 'LEFT_PARENTHESIS', ')' : 'RIGHT_PARENTHESIS', '*' : 'ASTERISK', '+' : 'PLUS', ',' : 'COMMA', '-' : 'MINUS', '.' : 'PERIOD', '/' : 'SLASH', ':' : 'COLON', ';' : 'SEMICOLON', '<' : 'LESS', '=' : 'EQUAL', '>' : 'GREATER', '?' : 'QUESTION', '@' : 'AT', '[' : 'LEFT_BRACKET', ']' : 'RIGHT_BRACKET', '\\' : 'BACKSLASH', '^' : 'HAT', '_' : 'UNDERSCORE', '`' : 'BACKTICK', '{' : 'LEFT_BRACE', '|' : 'PIPE', '}' : 'RIGHT_BRACE', '~' : 'TILDE' }
    digits      = { '0' : 'ZERO', '1' : 'WUN', '2' : 'TOO', '3' : 'TREE', '4' : 'FOWER', '5' : 'FIFE', '6' : 'SIX', '7' : 'SEVEN', '8' : 'AIT', '9' : 'NINER' }

    all = merge_dictionaries(lower_case,
                             upper_case,
                             punctuation,
                             digits)


class PhoneticDictionary(dict):
    """
    NATO Phonetic Dictionary.

    The phonetic dictionary maps alphanumeric and punctuation characters to 
    their respective NATO code word.

        >>> pd = PhoneticDictionary()
        >>> pd['A']
        'ALFA'

    The dictionary can be used to "spell-out" text using the NATO alphabet:

        >>> pd.spell('Phonetic Dictionary!')
        'PAPA-hotel-oscar-november-echo-tango-india-charlie DELTA-india-charlie-tango-india-oscar-november-alfa-romeo-yankee-EXCLAMATION'

        >>> pd.spell('Here are some digits: 1 2 3 4 5')
        'HOTEL-echo-romeo-echo alfa-romeo-echo sierra-oscar-mike-echo delta-india-golf-india-tango-sierra-COLON WUN TOO TREE FOWER FIFE'
    """
    whitespace_pattern = compile('(\s+)')

    def __init__(self, character_set=CharacterSets.all):
        super(PhoneticDictionary, self).__init__(character_set)

    def translate(self, char):
        """
        Translate the given character to it's NATO code word, if there is no 
        associated code word the character is returned unchanged.
        """
        return self.get(char, char)

    def spell(self, text, separator='-'):
        """
        Spell the given text, seperating terms by the given separator. Any 
        character in text that is not in the NATO alphabet is left as-is.
        """
        sequence = self.whitespace_pattern.split(text)
        for index, word in enumerate(sequence):
            if index % 2 == 0:
                sequence[index] = separator.join(self.translate(char) for char in word)
        return str().join(sequence)


def _test():
    """ Test this module. """
    import doctest
    import phonetic
    return doctest.testmod(phonetic)
