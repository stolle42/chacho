import argparse
import model
import view

parser=argparse.ArgumentParser()
parser.add_argument("chordfile",help="The file containing the chords")
parser.add_argument("--format",default="ccli")
args=parser.parse_args()


if __name__ == "__main__":
    try:
        song=model.parseChords(args.format,args.chordfile)
    except Exception as e:
        raise e
    
    try:
        view.plotAll(song)
    except Exception as e:
        raise e