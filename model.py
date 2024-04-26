import re
import chordparser

from songtree import Chord, Section, Song

    

class SongfileParser():
    """gets a file and divides it into songtree objects"""
    def __init__(self, chordFilePath):
        with open(chordFilePath, 'r') as cd:
            self.songtext=cd.read()
        self.ce=chordparser.ChordAnalyser()
            
    def divideIntoSections(self ):
        pattern=re.compile(r"\{comment: [\w ]+\}[\s\S]?\n\n")
        res=pattern.findall(self.songtext)
        self.sections=match.groups()
        
    def _getSectionType(self, typeLine:str):
        match=re.match(r"{comment: (\w+)}",typeLine)
        return match.group(1)
    
    def _getSectionChords(self, sectionText:str):
        match=re.match(r"\[(\w+)\]",sectionText)
        return match.groups()
    
    def _parseChord(self, chord_str:str):
        chord=self.ce.create_chord(chord_str)
        root=chord.root.value
        type=chord.quality.value
        return Chord(root,type)
    
    def parseSection(self,section:str):
        sectionType=self._getSectionType(section)
        chords=self._getSectionChords(section)
        return Section(sectionType, chords)
        
    
    def parseFile(self,format:str):
        if format=='ccli':
            self.divideIntoSections()
            sectionsTree=list(map(self.parseSection,self.sections))
            return Song(sections=sectionsTree)
        

ce=chordparser.ChordAnalyser()
# ch=ce.create_chord("Ab/C")
# print(ch.root.value)
# print(ch.quality.value)
# print(ch.quality.ext)

# def parseChords(data:str,format:str):
    