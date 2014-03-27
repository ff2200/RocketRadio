if __name__ == '__main__':
    import serial
    from argparse import ArgumentParser

    optp = ArgumentParser(description='Open a port, with buadrate to communicate with arduino radio')
    optp.add_argument('port', type=str, help='port to open')
    optp.add_argument('baudrate', type=int, help='baudrate to use')

    args = optp.parse_args()
    source = serial.Serial(args.port, args.baudrate)

    from rgslib import receive

    for result in receive(source):
        print(result)
