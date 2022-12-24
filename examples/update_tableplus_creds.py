#!/usr/bin/env python3

from argparse import ArgumentParser
import sys

from tableplus_macos_update_creds import update_creds


def main():
    parser = ArgumentParser()
    parser.add_argument('--connection', dest='connection')
    parser.add_argument('--username', dest='username')
    parser.add_argument('--password', dest='password')
    args = parser.parse_args(sys.argv[1:])

    update_creds(args.connection, username=args.username, password=args.password)


if __name__ == '__main__':
    main()
