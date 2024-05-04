import re
from typing import Tuple
import chordparser

from circleOfFifths import CircleOfFifths
from songtree import Chord, Section, Song

   

class SongfileParser():
    """gets a file and divides it into songtree objects"""
    def __init__(self, chordFilePath):
        with open(chordFilePath, 'r') as cd:
            self.songtext=cd.read()
        self.ce=chordparser.ChordEditor()
        self._parseKey()
        self.circleOfFifths=CircleOfFifths(self.key)
        
    def divideIntoSections(self ):
        pattern=re.compile(r"\{comment: ([\w -]+)\}\n(.*?)\n\n",re.DOTALL)
        self.sections=pattern.findall(self.songtext)
    
    def _getSectionChords(self, sectionText:str):
        pattern=re.compile(r"\[(.*?)\]")
        chordStrings=pattern.findall(sectionText)
        return list(map(self._parseChordWithDistance,chordStrings))
    
    def _getKeyDistance(self, chord:Chord):
        if chord.chordType in ["major","sus4","dominant"]:
            return self.circleOfFifths.majorMap[chord.chordRoot]
        elif chord.chordType=="minor":
            return self.circleOfFifths.minorMap[chord.chordRoot]
        else:
            raise ValueError("type must be either major or minor")
            
    def _parseChordWithDistance(self, chordStr:str):
        """adds fifth distance to the already parsed chord
        """
        chord=self._parseChord(chordStr)
        chord.fifthsToKey=self._getKeyDistance(chord)
        return chord
        
        
    
    def _parseChord(self, chordStr:str)->Chord:
        """convert chord string (e.g. A, Em, Bb) to a 
        chord object which can be inserted in the tree
        fifths-distance is not calculated in this method
        """
        chord=self.ce.create_chord(chordStr)
        root=chord.root.value
        type=chord.quality.value
        return Chord(root,type)
    
    def parseSection(self,section:Tuple[str,str]):
        sectionType,sectionText=section
        #remove chords the parser cannot understand
        sectionText=sectionText.replace('[|]','')
        sectionText=re.sub(r'[\(\)]','',sectionText)
        #extract chords from text
        chords=self._getSectionChords(sectionText)
        return Section(sectionType, chords)
    
    def _parseKey(self):
        pattern=re.compile("{key: (\w+)}")
        (key_str,)=pattern.findall(self.songtext)
        self.key=self._parseChord(key_str)
    
    def parseFile(self,format:str):
        if format=='ccli':
            self.divideIntoSections()
            sectionsTree=list(map(self.parseSection,self.sections))
            return Song(sections=sectionsTree, key=self.key)
        
