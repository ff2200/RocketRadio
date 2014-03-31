#!/usr/bin/env python3

def main(file, datalog):
    from rgslib import receive
    datalog = open(datalog, 'w')
    try:
        with open(file, 'rb') as source:
            for result in receive(source, filelog_data=datalog):
                print(result)
    except KeyboardInterrupt:
        print("Shutdown...")
    finally:
            datalog.close()


if __name__ == '__main__':

    from argparse import ArgumentParser

    optp = ArgumentParser(description='Open file to extract rocket data')
    optp.add_argument('file', type=str, help='file to open')
    optp.add_argument('-d', '--datalog', type=str, help='logfile for json data',
                        default='./data.log')

    args = optp.parse_args()
    main(args.file, args.datalog)