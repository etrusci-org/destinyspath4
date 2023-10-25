#!/usr/bin/env python3

from lib.core import DP4_Core




if __name__ == '__main__':
    DP4 = DP4_Core()

    if DP4.cliargs.play:
        DP4.play()
    elif DP4.cliargs.list_saves:
        DP4.list_saves()
    else:
        DP4.CLIParser.print_help()
