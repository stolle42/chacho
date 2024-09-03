from enum import Enum
import re
from songtree import Chord


def parse(chord:str):
    chord=chord.replace("maj","")#maj is removed, as maj7 is incorrectly recognized as minor by the regex
    pattern=re.compile(r'(?P<base>.)(?P<semi>[#b]?)(?P<quality>m?)(?P<extension>[47]?)')
    ret=pattern.match(chord)
    subgroups=ret.groupdict()
    
    note=Note(subgroups['base'], subgroups['semi'])
    isMinor=subgroups['quality']=='m'
    extension=subgroups['extension']
    if note.error:
        return Chord(chordRoot='err',major=True,extend='err',error=True)
    else:
        return Chord(chordRoot=str(note),major=not isMinor,extend=extension)

class Extension(Enum):
    """enum for all possible suspended or extended chords"""
    SUS2 = "sus2"
    SUS4 = "sus4"
    EXT7 = "7"
    ADD9 = "add9"
    NOEXT = None
    
    

class Note:
    """generates a note in a standard format regardless of
    whether it was provided with # or. Its string representation is 
    one of the 12 base self.notes (or empty string in case of failure)

    Args:
        base (str): base without semitone
        semi (str): # or b, depending on down or up shift. If left empty: no shift
    """
    def __init__(self, base:str, semi:str=''):
        self.notes=['C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B']
        self.noteStr=''#this is supposed to be overwritten
        self.error=False
        if base in self.notes:
            self._makeNoteString(base,semi)
        else:
            self._error(f'Note {base} was not recognized!')            
    
    def _makeNoteString(self, base:str, semi:str):
        shifter={'#':1,'':0,'b':-1}
        if semi in shifter:
            newIdx=self.notes.index(base)+shifter[semi]
            self.noteStr=self.notes[newIdx%12]#more than 12 notes is not possible
        else:
            self._error(f'Note parse error - semitone must be # or b or empty, but was "{semi}"')        
    
    def _error(self, message:str):
        """if anything goes wrong, empty string will be saved and
        the error message printed out
        """
        print(message)
        self.error=True
        
    def __str__(self) -> str:
        if self.error:
            return ''
        else:
            return self.noteStr

        
if __name__ == "__main__":
    c=parse('F')
    c=parse('F#')
    c=parse('Gb')
    c=parse('Gm')
    c=parse('C#m')
    c=parse('E7')
    c=parse('C#m7')
    c=parse('-')