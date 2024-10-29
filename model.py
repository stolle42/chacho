import re
from typing import Tuple
import chachoParser as cc
import numpy as np
from pathlib import Path
from circleOfFifths import CircleOfFifths
from songtree import Chord, Section, Song

'''
TODO: chordproParser und ultimateParser die von songfileParser erben. alles spezifische auslagern.
evtl. key nicht ablesen sondern chord durchschnitt berechnen (achtung bei 6/-6 ist natürlich nciht 0). Moll key?
für ultimate parser evtl zeilen nur akzeptieren wenn er jedes wort parsen kann?
'''   


class SongfileParser():
    """gets a file and divides it into songtree objects"""
    def __init__(self, chordFilePath):
        with open(chordFilePath, 'r') as cd:
            self.songtext=cd.read()
        
    def _divideIntoSections(self ):
        self.songtext=re.sub(r"\n\n([^{])",r"\n\g<1>",self.songtext)#remove double enter that do not indicate end of section
        pattern=re.compile(r"\{comment: ([\w &-]+)\}\n(.*?)\n\n",re.DOTALL)
        self.sections=pattern.findall(self.songtext)
    
    def _getSectionChords(self, sectionText:str):
        pattern=re.compile(r"\[(.*?)\]")
        chordStrings=pattern.findall(sectionText)
        return map(cc.parse,chordStrings)
        
    def _parseSection(self,section:Tuple[str,str]):
        sectionType,sectionText=section
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
        
    
    
    def parseFile(self):
        self._divideIntoSections()
        self.sectionsTree=map(self._parseSection,self.sections)
        #get rid of sections with no chords
        self.sectionsTree=list(filter(lambda section: section.chords,self.sectionsTree))
        self._parseKey()
        self._parseTitle()
        return Song(sections=self.sectionsTree, key=self.key, title=self.title+'-'+self.key_str)\
    
def makeProgession(song:Song):
    """adds the fifthToKey-property to all chords in Song"""
    circleOfFifths=CircleOfFifths(song.key)
    for section in song.sections:
        for chord in section.chords:
            chord.fifthsToKey=circleOfFifths.getChordDistance(chord)


class ChordproParser(SongfileParser):
    """input is file in chordpro format that was converted from ultimate
    guitar by website"""
    def __init__(self, chordFilePath):
        super(ChordproParser, self).__init__(chordFilePath)
        self.chordFilePath = chordFilePath
    
    def _divideIntoSections(self ):
        pattern=re.compile(r"\{start_of_([\w &-]+)\}\n(.*?)\n\n",re.DOTALL)
        self.sections=pattern.findall(self.songtext)
    def _parseKey(self):
        self.key=self.sectionsTree[0].chords[0]#questionable approach
        self.key_str=''#even more questionable
    
    def _parseTitle(self):
        self.title='songtitle'

class UltimateGuitarParser(SongfileParser):
    """parses ultimate guitar format"""
    def __init__(self, chordFilePath):
        super(UltimateGuitarParser, self).__init__(chordFilePath)
        self.chordFilePath = chordFilePath

    def _divideIntoSections(self):
        sections=re.split(r"\[(.*?)\]",self.songtext)
        sections.pop(0)#discard everyting before first section
        self.sections=np.reshape(sections,(-1,2))
        pass
    
    def _getSectionChords(self, sectionText: str):
        lines=re.split('\n',sectionText)
        pass
        
    def _parseKey(self):
        self.key=self.sectionsTree[0].chords[0]#questionable approach
        self.key_str=''#even more questionable
    
    def _parseTitle(self):
        self.title='songtitle'
       
def parseChords(format:str,chordFileStr:str):
    chordFile=Path(chordFileStr)
    if not chordFile.exists():
        raise FileNotFoundError(f"file {chordFileStr} does not exist!")
    if format=='ccli':
        sp=SongfileParser(chordFile)
    elif format=='chordpro':
        sp=ChordproParser(chordFile)
    elif format=='ultimate':
        sp=UltimateGuitarParser(chordFile)
    else:
        raise ValueError(f"Format {format} is not known!")
    song=sp.parseFile()
    makeProgession(song)
    return song