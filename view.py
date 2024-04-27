import matplotlib.pyplot as plt
from songtree import Chord, Song
class ChordPlotter():
    """gets chords in tree-form and plots them"""
    def __init__(self, songTree:Song):
        self.songTree = songTree
    
    
    def plot(self):
        for section in self.songTree.sections:
            distances=list(map((lambda chord: chord.fifthsToKey),section.chords))
            plt.plot(distances, marker='o')
            plt.savefig("progression.png")
            plt.close()
            
    
