from pathlib import Path
import matplotlib.pyplot as plt
from circleOfFifths import CircleOfFifths
from songtree import Chord, Song
from itertools import batched


def plotAll(songTree:Song, maxSections:int=8, outputDir='.'):
    if len(songTree.sections)>maxSections+2:
        for i, sectionSlice in enumerate(batched(songTree.sections, maxSections)):
            song=Song(sectionSlice,songTree.key,f'{songTree.title}({i+1})')
            ChordPlotter(song,outputDir).plot()
    else: 
        ChordPlotter(songTree,outputDir).plot()
        


class ChordPlotter():
    """gets chords in tree-form and plots them"""
    def __init__(self, songTree:Song, outputDir):
        self.songTree:Song = songTree
        self.cof=CircleOfFifths(songTree.key)
        self.outputDir=Path(outputDir)
        assert self.outputDir.exists(),f"Folder {self.outputDir} not found!"
        
    def _visualizeChord(self, chord:Chord):
        if chord.major:
            if chord.extend:
                return 'orange'
            else:
                return 'red'
        else:
            if chord.extend:
                return 'purple'
            else:
                return 'blue'
    
    def plot(self):
        fig=plt.figure()
        sectionCount=len(self.songTree.sections)
        columns=1+(sectionCount>2)
        rows=(sectionCount+1)//2+(sectionCount==2)
        plotColor='red' if self.songTree.key.major else 'blue'
        for (i,section) in enumerate(self.songTree.sections):
            ax=plt.subplot(rows, columns,i+1)
            distances=list(map((lambda chord: chord.fifthsToKey),section.chords))
            colors=list(map(self._visualizeChord,section.chords))
            minChord,maxChord=min(distances),max(distances)
            sectionChords=self.cof.getScaleSection(minChord,maxChord)
            ax.set_yticks(range(minChord,maxChord+1))
            ax.set_yticklabels(sectionChords)
            ax.set_title(section.sectionType)
            ax.plot(distances, color=plotColor,zorder=1)
            ax.scatter(range(len(distances)),distances,c=colors,zorder=2)
        plt.tight_layout()
        fig.savefig(self.outputDir/self.songTree.title)