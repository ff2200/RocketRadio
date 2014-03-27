if __name__ == '__main__':

    from argparse import ArgumentParser

    optp = ArgumentParser(description='Open file to extract rocket data')
    optp.add_argument('file', type=str, help='file to open')

    args = optp.parse_args()

    from rgslib import receive
    with open(args.file, 'rb') as source:
        for result in receive(source):
            print(result)
