import argparse
import model
import view

parser=argparse.ArgumentParser()
parser.add_argument("chordfile",help="The file containing the chords")
parser.add_argument("--format",default="ccli")
args=parser.parse_args()


if __name__ == "__main__":
    try:
        sp=model.SongfileParser(args.chordfile)
        song=sp.parseFile(args.format)
        model.makeProgession(song)
    except Exception as e:
        raise e
    
    try:
        plotter=view.ChordPlotter(song)
        plotter.plot()
    except Exception as e:
        raise e