from parser import SubtitleFileParser

def main():
    with SubtitleFileParser(r'examples\example_subtitle.srt') as sfp:
        for _ in range(20):
            print(sfp.get_line())

if __name__=="__main__":
    main()