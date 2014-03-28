#!/usr/bin/env python3

def main(source):
    from rgslib import receive
    try:
        for result in receive(source):
            print(result)
    except KeyboardInterrupt:
        print('Shutdown...')
    finally:
        source.close()

if __name__ == '__main__':
    import serial
    from argparse import ArgumentParser

    optp = ArgumentParser(description='Open a port, with buadrate to communicate with arduino radio')
    optp.add_argument('port', type=str, help='port to open')
    optp.add_argument('baudrate', type=int, help='baudrate to use')

    args = optp.parse_args()
    source = serial.Serial(args.port, args.baudrate)
    main(source)
