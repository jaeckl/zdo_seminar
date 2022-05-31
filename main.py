import argparse

from zdo2022 import annotations

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Instrument Tracker')
    parser.add_argument('--video', type=str, default='', help='path to video file')
    parser.add_argument('--verbose', action='store_true', help='verbose mode')
    parser.add_argument('--save_video', action='store_true', help='save video')
    args = parser.parse_args()
    if args.video:
        annotations.annotate_video(args.video, args.verbose, args.save_video)
