import argparse
import model
import view

parser=argparse.ArgumentParser()
parser.add_argument("chordfile",help="The file containing the chords")
parser.add_argument("--format",default="ccli")
args=parser.parse_args()


if __name__ == "__main__":
    sp=model.SongfileParser(args.chordfile)
    sp.parseFile(args.format)
    if not song.error:
        view.plotSong(song)
    else:
        print(song.error)