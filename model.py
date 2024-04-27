from collections import deque
import re
from typing import Tuple
import chordparser

from songtree import Chord, Section, Song

   

class SongfileParser():
    """gets a file and divides it into songtree objects"""
    def __init__(self, chordFilePath):
        with open(chordFilePath, 'r') as cd:
            self.songtext=cd.read()
        self.ce=chordparser.ChordEditor()
        self._parseKey()
        self.circleOfFifth=CircleOfFifth(self.key)
        
    def divideIntoSections(self ):
        pattern=re.compile(r"\{comment: ([\w ]+)\}\n(.*?)\n\n",re.DOTALL)
        self.sections=pattern.findall(self.songtext)
    
    def _getSectionChords(self, sectionText:str):
        pattern=re.compile(r"\[(.*?)\]")
        chordStrings=pattern.findall(sectionText)
        return list(map(self._parseChord,chordStrings))
    
    def _getKeyDistance(self, note, type):
        if type in ["major","sus4"]:
            return self.circleOfFifth.majorMap[note]
        elif type=="minor":
            return self.circleOfFifth.minorMap[note]
        else:
            raise ValueError("type must be either major or minor")
            
        
    
    def _parseChord(self, chordStr:str):
        chordStr=re.sub(r'[\(\)]','',chordStr)#chord parser does not understand chords with brackets, so we remove them
        chord=self.ce.create_chord(chordStr)
        root=chord.root.value
        type=chord.quality.value
        relative=self._getKeyDistance(root,type)
        return Chord(root,type, relative)
    
    def parseSection(self,section:Tuple[str,str]):
        sectionType,sectionText=section
        sectionText=sectionText.replace('[|]','')
        chords=self._getSectionChords(sectionText)
        return Section(sectionType, chords)
    
    def _parseKey(self):
        pattern=re.compile("{key: (\w+)}")
        (self.key,)=pattern.findall(self.songtext)
        
    
    def parseFile(self,format:str):
        if format=='ccli':
            self.divideIntoSections()
            sectionsTree=list(map(self.parseSection,self.sections))
            return Song(sections=sectionsTree, key=self.key)
        
class CircleOfFifth:
    """creates a dictionary that maps every note based on its distance 
    to the key according to the fifth-metric ('distance' means how many 
    fifth we need to go up or down to reach the key)
    """
    def __init__(self, key):
        #basic music theory
        baseCircleOfFifth=deque(['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#', 'G#', 'D#', 'A#', 'F'])
        majorMinorShift=-3
        #shift key to beginning of queue (no change if key is C)
        shiftToC=baseCircleOfFifth.index(key)
        baseCircleOfFifth.rotate(shiftToC)
        #shift key to center of the queue
        self.centerIdx=len(baseCircleOfFifth)//2
        baseCircleOfFifth.rotate(self.centerIdx)
        #assign fifth-distance to every one of the 12 notes
        self.majorMap=self.getMap(baseCircleOfFifth,0)
        self.minorMap=self.getMap(baseCircleOfFifth,majorMinorShift)
    def getMap(self, base:deque, scaleShift):
        base.rotate(scaleShift)
        #we need a map with 0 in the center because we rotated the key to the center
        return dict(zip(base,range(-self.centerIdx,self.centerIdx)))
    