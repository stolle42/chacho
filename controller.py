import argparse
import model
import view

parser=argparse.ArgumentParser()
parser.add_argument("chordfile",help="The file containing the chords")
parser.add_argument("--format",default="ccli")
args=parser.parse_args()


if __name__ == "__main__":
    try:
        if args.format=='ccli':
            sp=model.SongfileParser(args.chordfile)
        elif args.format=='chordpro':
            sp=model.ChordproParser(args.chordfile)
        elif args.format=='ultimate':
            sp=model.UltimateGuitarParser(args.chordfile)
        else:
            raise ValueError(f"Format {args.format} is not known!")
        song=sp.parseFile()
        model.makeProgession(song)
    except Exception as e:
        raise e
    
    try:
        view.plotAll(song)
    except Exception as e:
        raise e