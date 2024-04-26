from dataclasses import dataclass
from enum import Enum,auto
from typing import List


class ChordRoot(Enum):
    C=auto()
    Db=auto()
    D=auto()
    Eb=auto()
    E=auto()
    F=auto()
    Gb=auto()
    G=auto()
    Ab=auto()
    A=auto()
    Bb=auto()
    B=auto()

class ChordType(Enum):
    Major=auto()
    Minor=auto()
    DominantSeventh=auto()
    MajorSeventh=auto()
    MinorSeventh=auto()
    
class SectionType(Enum):
    Verse=auto()
    Chorus=auto()
    Bridge=auto()
    Tag=auto()

@dataclass
class Chord():
    chordRoot: str
    chordType: str

class Section:
    sectionType:str
    chords:List[Chord]

class Song:
    sections:List[Section]