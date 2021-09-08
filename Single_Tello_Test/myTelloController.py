import argparse
from datetime import datetime
import re
import time
import sys

from tello import Tello

#
def printUsage():
    print("Supported command list")
    lst_cmd = get_commands()
    for keyin in lst_cmd:
        telloCommand = TCmd[keyin]
        if (re.match(RE_pattern_go, keyin)):
            keyin = "%s N" % (keyin)
        print("%-5s : %s" % (keyin, telloCommand))

    return
#
def get_commands():
    #
    lst_cmd = []
    lst_cmd.append(CMD_command)
    lst_cmd.append(CMD_takeoff)
    lst_cmd.append(CMD_land)
    lst_cmd.append(CMD_go_forward)
    lst_cmd.append(CMD_go_back)
    lst_cmd.append(CMD_go_right)
    lst_cmd.append(CMD_go_left)
    lst_cmd.append(CMD_flip_forward)
    lst_cmd.append(CMD_flip_back)
    lst_cmd.append(CMD_flip_right)
    lst_cmd.append(CMD_flip_left)
    lst_cmd.append(CMD_stream_on)
    lst_cmd.append(CMD_stream_off)
    lst_cmd.append(CMD_end)

    return lst_cmd

#

#
RE_pattern_go = r'^g[fbrl]$'

#
CMD_command      = "command"
CMD_com          = "com"
CMD_cmd          = "cmd"
CMD_takeoff      = "to"
CMD_land         = "ld"
CMD_go_forward   = "gf"
CMD_go_back      = "gb"
CMD_go_right     = "gr"
CMD_go_left      = "gl"
CMD_flip_forward = "ff"
CMD_flip_back    = "fb"
CMD_flip_right   = "fr"
CMD_flip_left    = "fl"
CMD_stream_on    = "son"
CMD_stream_off   = "soff"
CMD_battery      = "b"
CMD_end          = "end"

#
TCmd = {}
TCmd[CMD_command]      = "command"
TCmd[CMD_com]          = "command"
TCmd[CMD_cmd]          = "command"
TCmd[CMD_takeoff]      = "takeoff"
TCmd[CMD_land]         = "land"
TCmd[CMD_go_forward]   = "forward"
TCmd[CMD_go_back]      = "back"
TCmd[CMD_go_right]     = "right"
TCmd[CMD_go_left]      = "left"
TCmd[CMD_flip_forward] = "flip f"
TCmd[CMD_flip_back]    = "flip b"
TCmd[CMD_flip_right]   = "flip r"
TCmd[CMD_flip_left]    = "flip l"
TCmd[CMD_stream_on]    = "streamon"
TCmd[CMD_stream_off]   = "streamoff"
TCmd[CMD_battery]      = "battery?"
TCmd[CMD_end]          = "end"

#
def ctrl_tello(args):
    start_time = str(datetime.now())

    #
    tello = None
    if (not args.d):
        print("[DBG] create Tello()")
        tello = Tello()

        keyin = CMD_command
        tcommand = TCmd[keyin]
        print("[DBG]tcommand=%s" % tcommand)
        tello.send_command(tcommand)

    while (1):

        #
        print("Please input command : ", end='', flush=True)
        keyin = sys.stdin.readline()
        if (keyin != '' and keyin != '\n'):
            keyin.replace('\n', '')
            keyin = keyin.rstrip()

            if (keyin == "h"):
                printUsage()
                continue

            (cc) = keyin.split(" ")
            if (cc[0] in TCmd):
                if (cc[0] == CMD_end):
                    break
                elif (re.match(RE_pattern_go, cc[0])):
                    tcommand = "%s %s" % (TCmd[cc[0]], cc[1])
                else:
                    tcommand = TCmd[cc[0]]
                print("[DBG]tcommand=%s" % tcommand)
                if (tello is not None):
                    tello.send_command(tcommand)
            else:
                tcommand = keyin
                print("[DBG]tcommand=%s" % tcommand)
                if (tello is not None):
                    tello.send_command(tcommand)
                pass

    return

if (__name__ == '__main__'):

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', action='store_true')
    args = parser.parse_args()

    #
    ctrl_tello(args)

    pass

# eof
