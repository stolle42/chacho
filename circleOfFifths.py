from collections import deque

from songtree import Chord


class CircleOfFifths:
    """creates a dictionary that maps every note based on its distance 
    to the key according to the fifth-metric ('distance' means how many 
    fifth we need to go up or down to reach the key)
    """
    def __init__(self, key:Chord):
        self.key=key
        #basic music theory
        self.fifths=deque(['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#', 'G#', 'D#', 'A#', 'F'])
        self.minorMajorShift=-3
        #shift key to center of the queue
        self.shiftKeyToHead()
        self.shiftHeadToCenter()
        #add minor scale analogous to major scale
        self.minorFifths=self.fifths.copy()
        self.minorFifths.rotate(self.minorMajorShift)
        #assign fifth-distance to every one of the 12 notes
        self.distances=range(-self.centerIdx,self.centerIdx)
        self.majorMap=dict(zip(self.fifths,self.distances))
        self.minorMap=dict(zip(self.minorFifths,self.distances))

    def shiftHeadToCenter(self):
        self.centerIdx=len(self.fifths)//2
        self.fifths.rotate(self.centerIdx)
        
    def shiftKeyToHead(self):
        """The start of our circle of fifth must be the key.
        We defined our circle to start at C, but since not every song
        uses the key C. if not, we need to shift our circle. 
        """
        shiftToC=self.fifths.index(self.key.chordRoot)
        if self.key.chordType=="minor":
            shiftToC+=self.minorMajorShift
        self.fifths.rotate(-shiftToC)
      
    def getScaleSection(self, minChord, maxChord):
        """
        returns all major and minor chords between min and max
        """
        slc=slice(minChord+self.centerIdx,maxChord+self.centerIdx+1)
        majors=list(self.fifths)[slc]
        minors=list(self.minorFifths)[slc]
        return list(map((lambda maj,min: maj+'|'+min+'m'),majors,minors))