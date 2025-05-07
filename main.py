from src.synchronizer import Synchronizer

def main():
    s = Synchronizer((0, 20, 2), (0, 52, 2),r'C:\Users\nikolamaksic\Desktop\coding\subtitle-timing-synchronizer\examples\example_subtitle.srt')
    s.process()
if __name__=="__main__":
    main()