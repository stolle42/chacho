import matplotlib.pyplot as plt
from circleOfFifths import CircleOfFifths
from songtree import Chord, Song
class ChordPlotter():
    """gets chords in tree-form and plots them"""
    def __init__(self, songTree:Song):
        self.songTree = songTree
        self.cof=CircleOfFifths(songTree.key)
        
    def visualizeChord(self, chord:Chord):
        visualization={
            'major':'red',
            'minor':'blue',
            'dominant':'orange',
            'sus4':'green',
        }
        return  visualization[chord.chordType]
    
    def plot(self):
        fig=plt.figure()
        sectionCount=len(self.songTree.sections)
        columns=min(sectionCount,2)
        rows=(sectionCount+1)//2
        for (i,section) in enumerate(self.songTree.sections):
            ax=plt.subplot(rows, columns,i+1)
            distances=list(map((lambda chord: chord.fifthsToKey),section.chords))
            colors=list(map(self.visualizeChord,section.chords))
            minChord,maxChord=min(distances),max(distances)
            sectionChords=self.cof.getScaleSection(minChord,maxChord)
            ax.set_yticks(range(minChord,maxChord+1))
            ax.set_yticklabels(sectionChords)
            ax.set_title(section.sectionType)
            ax.plot(distances, color='red',zorder=1)
            ax.scatter(range(len(distances)),distances,c=colors,zorder=2)
        plt.tight_layout()
        fig.savefig("progression.png")
        # fig.close()
            
    
