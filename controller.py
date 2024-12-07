import argparse
import model
import view

parser=argparse.ArgumentParser()
parser.add_argument("chordfile",help="The file containing the chords")
parser.add_argument("--max",default="8",help="Maximum number of sections\
    to be squeezed into one sheet")
parser.add_argument("-o", "--outdir", default='.', help="relative or absolute path to where you want to\
    save the sheet to")
parser.add_argument("--format",default="ccli")
args=parser.parse_args()


if __name__ == "__main__":
    try:
        song=model.parseChords(args.format,args.chordfile)
    except Exception as e:
        raise e
    
    try:
        view.plotAll(song, int(args.max), args.outdir)
    except Exception as e:
        raise e