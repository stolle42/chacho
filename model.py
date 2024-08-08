import re
from typing import Tuple
import chachoParser as cc

from circleOfFifths import CircleOfFifths
from songtree import Chord, Section, Song

   

class SongfileParser():
    """gets a file and divides it into songtree objects"""
    def __init__(self, chordFilePath):
        with open(chordFilePath, 'r') as cd:
            self.songtext=cd.read()
        self._parseKey()
        self._parseTitle()
        self.circleOfFifths=CircleOfFifths(self.key)
        self.maxSections=8
        
    def divideIntoSections(self ):
        pattern=re.compile(r"\{comment: ([\w &-]+)\}\n(.*?)\n\n",re.DOTALL)
        self.sections=pattern.findall(self.songtext)
    
    def _getSectionChords(self, sectionText:str):
        pattern=re.compile(r"\[(.*?)\]")
        chordStrings=pattern.findall(sectionText)
        return map(self._parseChordWithDistance,chordStrings)
    
    def _getKeyDistance(self, chord:Chord):
        if chord.major:
            return self.circleOfFifths.majorMap[chord.chordRoot]
        else:
            return self.circleOfFifths.minorMap[chord.chordRoot]
            
    def _parseChordWithDistance(self, chordStr:str):
        """adds fifth distance to the already parsed chord
        """
        chord=cc.parse(chordStr)
        if not chord.error:
            chord.fifthsToKey=self._getKeyDistance(chord)
        return chord
        
        
    
    # def _parseChord(self, chordStr:str)->Chord:
    #     """convert chord string (e.g. A, Em, Bb) to a 
    #     chord object which can be inserted in the tree
    #     fifths-distance is not calculated in this method
    #     """
    #     chord=cc.parse(chordStr)
    #     return Chord(str(chord.root),chord.major, chord.extend)
    
    def parseSection(self,section:Tuple[str,str]):
        sectionType,sectionText=section
        #remove chords the parser cannot understand TODO: remove
        sectionText=re.sub(r'[\(\)\|\.]','',sectionText)
        sectionText=sectionText.replace('[]','')
        #extract chords from text
        chords=self._getSectionChords(sectionText)
        chords=list(filter(lambda c:not c.error, chords))
        return Section(sectionType, chords)
    
    def _parseKey(self):
        pattern=re.compile(r"{key: (\w+)}")
        (self.key_str,)=pattern.findall(self.songtext)
        self.key=cc.parse(self.key_str)
    
    def _parseTitle(self):
        pattern=re.compile(r"{title: (.+)?}")
        (self.title,)=pattern.findall(self.songtext)
        
    
    
    def parseFile(self,format:str):
        if format=='ccli':
            self.divideIntoSections()
            sectionsTree=list(map(self.parseSection,self.sections[:self.maxSections]))
            return Song(sections=sectionsTree, key=self.key, title=self.title+'-'+self.key_str)
        
