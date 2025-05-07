from src.synchronizer import Synchronizer
import argparse

def parse_time_tuple(s):
    parts = s.split(":")
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("Time must be in format MM:SS:MS (e.g. 00:52:002)")
    try:
        return tuple(int(p) for p in parts)
    except ValueError:
        raise argparse.ArgumentTypeError("All time parts must be integers")

def main():
    parser = argparse.ArgumentParser(description="Synchronize subtitle timing.")
    parser.add_argument("--start", type=parse_time_tuple, required=True,
                        help="Delay start time in format MM:SS:MS (e.g. 00:20:002)")
    parser.add_argument("--delay", type=parse_time_tuple, required=True,
                        help="Delay duration in format MM:SS:MS (e.g. 00:52:002)")
    parser.add_argument("--mode", choices=["delay", "advance"], default="delay",
                            help="Whether to delay (add) or advance (subtract) subtitle timings")
    parser.add_argument("--input", type=str, required=True,
                        help="Path to input .srt subtitle file")
    parser.add_argument("--output", type=str, default=None,
                        help="Optional path for output file, default output_name=input_name+'_synchronized'")

    args = parser.parse_args()
    
    mode = 1 if args.mode == "delay" else -1
    synchronizer = Synchronizer(
        subtitle_delay_start_t=args.start,
        subtitle_delay=args.delay,
        mode=mode,
        input_file=args.input,
        output_file=args.output
    )    
    synchronizer.process()
if __name__=="__main__":
    main()