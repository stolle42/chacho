from enum import Enum
import re

def parse(chord:str):
    pattern=re.compile(r'(?P<base>\w)(?P<semi>[#b]?)(?P<quality>m?)')
    ret=pattern.match(chord)
    d=ret.groupdict()
    pass

class Extension(Enum):
    """enum for all possible suspended or extended chords"""
    SUS2 = "sus2"
    SUS4 = "sus4"
    EXT7 = "7"
    ADD9 = "add9"
    NOEXT = None
    
    

class Note(Enum):
    """all of the 12 base notes"""
    C='C'
    G='G'
    D='D'
    A='A'
    E='E'
    B='B'
    Gb='Gb'
    Db='Db'
    Ab='Ab'
    Eb='Eb'
    Bb='Bb'
    F='F'

class Chord:
    """guitar Chord"""
    def __init__(self, base:Note,major:bool=True,extend:Extension=None):
        self.base:Note = base
        self.major:bool = major
        self.extend:Extension = extend
        
if __name__ == "__main__":
    c=parse('F')
    c=parse('F#')
    c=parse('Gb')
    c=parse('Gm')
    c=parse('C#m')
    c=parse('E7')
    c=parse('C#m7')