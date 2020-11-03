import time
import getopt, sys
from logger import Logger
from veb import VEB
from input_parser import parse_input

argument_list = sys.argv[1:]

# Options
options = "i:o:w:"

# Long options
long_options = ["input=", "output=", "word-size="]


def main():
    input_file = "./input.txt"
    output_file = "./output.txt"
    w = 64
    try:
        arguments, values = getopt.getopt(argument_list, options, long_options)
        for currentArgument, currentValue in arguments:
            if currentArgument in ("-i", "--input"):
                input_file = currentValue
            elif currentArgument in ("-o", "--output"):
                output_file = currentValue
            elif currentArgument in ("-w", "--word-size"):
                w = int(currentValue)
    except getopt.error as err:
        print(str(err))

    inputs = parse_input(input_file)
    logger = Logger()
    veb = VEB(w=w, logger=logger)

    for ipt in inputs:
        cmd, value = ipt
        veb.apply(cmd, value)

    logger.write(output_file)


if __name__ == "__main__":
    main()
