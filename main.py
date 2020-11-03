import time
import getopt, sys
from logger import Logger
from veb import VEB
from input_parser import parse_input


def main():
    input_file = "./input.txt"
    output_file = "./output.txt"
    inputs = parse_input(input_file)
    logger = Logger()
    veb = VEB(w=64, logger=logger)

    for ipt in inputs:
        cmd, value = ipt
        veb.apply(cmd, value)

    logger.write(output_file)


if __name__ == "__main__":
    main()
