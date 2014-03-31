#!/usr/bin/env python3


def main(source, rawlog, datalog):
    from rgslib import receive
    datalog = open(datalog, 'w')
    rawlog = open(rawlog, 'wb')
    try:
        for result in receive(source, datalog, rawlog):
            print(result)
    except KeyboardInterrupt:
        print('Shutdown...')
    finally:
        source.close()
        datalog.close()
        rawlog.close()


if __name__ == '__main__':
    import serial
    from argparse import ArgumentParser

    optp = ArgumentParser(description='''Open a port, with buadrate to
                                        communicate with arduino radio''')
    optp.add_argument('port', type=str, help='port to open')
    optp.add_argument('baudrate', type=int, help='baudrate to use')
    optp.add_argument('-r', '--rawlog', type=str, help='logfile for raw data',
                        default='./data.raw')
    optp.add_argument('-d', '--datalog', type=str, help='logfile for json data',
                        default='./data.log')

    args = optp.parse_args()
    source = serial.Serial(args.port, args.baudrate)
    main(source, args.rawlog, args.datalog)
