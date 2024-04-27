from dataclasses import dataclass
from enum import Enum,auto
from typing import List, Optional


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
    fifthsToKey:Optional[int]

@dataclass
class Section():
    sectionType: str
    chords: List[Chord]

@dataclass
class Song:
    sections:List[Section]
    key: str