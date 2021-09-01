import subprocess
import time
import argparse


def main():

    parser = argparse.ArgumentParser(description="Scan disk usage value")
    parser.add_argument("--output_file",
                        action="store",
                        nargs=1,
                        default='scan_df_output.txt',
                        required=False,
                        help="where to store results",
                        metavar="FILE_NAME")
    parser.add_argument("--dirs",
                        action="append",
                        nargs="+",
                        required=True,
                        help="Where to scan",
                        metavar="DIR_NAME")
    parser.add_argument("--clean_output_file",
                        action="store_true",
                        default=False,
                        required=False,
                        help="clear the output_file beforehand")
    parser.add_argument("-t",
                        "--period",
                        action="store",
                        default=1,
                        type=int,
                        required=False,
                        help="Sampling period",
                        metavar="X")

    args = parser.parse_args()

    idx = 0
    with open(args.output_file[0],
              "w" if args.clean_output_file == True else "a") as file, open(
                  "/dev/null", "r") as null_file:
        while 1:
            for target_dir in args.dirs:
                cmd = ["du", "-h", "-s"] + target_dir
                subprocess.run(cmd, stdout=file, stderr=null_file)
            print("Scanned: ", idx)
            idx = idx + 1
            time.sleep(args.period)


if __name__ == "__main__":
    main()
