#!/usr/bin/env python

import sys, os, random, math, argparse

# Use secure system random number generator
# (uses /dev/urandom on Unix and CryptGenRandom on Windows)
system_random = random.SystemRandom()

__version__ = '1.0'


def copy_to_clipboard(text):
    """Copy text to clipboard"""
    try:
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import QEvent, QTimer
    except ImportError:
        from PyQt4.QtGui import QApplication
        from PyQt4.QtCore import QEvent, QTimer

    app = QApplication(sys.argv)
    clipboard = app.clipboard()
    clipboard.setText(text)
    #event = QEvent(QEvent.Clipboard)
    #QApplication.sendEvent(clipboard, event)
    QTimer.singleShot(500, app.quit)
    app.exec_()


def generate_passphrase(wordlist, length, separator=' ', transform=None):
    """Generate random passphrase from wordlist"""
    words = []
    for i in range(length):
        word = system_random.choice(wordlist)
        words.append(transform(word) if transform else word)
    return separator.join(words)


def main():
    parser = argparse.ArgumentParser(
        prog='pwgen-passphrase',
        description='generate secure random passphrase from wordlist'
    )

    parser.add_argument('-t', '--stats', action='store_true',
                        help='show statistics about generated passphrase')
    parser.add_argument('-c', '--clipboard', action='store_true',
                        help='copy generated passphrase to clipboard (needs PyQt)')
    parser.add_argument('-s', '--separator', default=' ',
                        help='words separator (default is space)')
    parser.add_argument('-n', '--count', type=int, default=1,
                        help='generate multiple passphrases (default is 1)')

    wordlist_group = parser.add_mutually_exclusive_group()
    wordlist_group.add_argument('-w', '--wordlist', choices=['diceware', 'bip0039', 'skey', 'cracklib-small'],
                                default='diceware',
                                help='select wordlist (default is diceware)')
    wordlist_group.add_argument('-f', '--wordlist-file', type=argparse.FileType('r'),
                                help='path to external wordlist file')

    length_group = parser.add_mutually_exclusive_group()
    length_group.add_argument('-l', '--length', type=int, default=6,
                              help='length of generated passphrase (number of words, default is 6)')
    length_group.add_argument('-b', '--bits', type=int,
                              help='minimal passphrase strength (bits of entropy)')

    transform_group = parser.add_mutually_exclusive_group()
    transform_group.add_argument('-L', '--lower', dest='transform', action='store_const', const=str.lower,
                                 help='make words lowercase')
    transform_group.add_argument('-U', '--upper', dest='transform', action='store_const', const=str.upper,
                                 help='make words uppercase')
    transform_group.add_argument('-C', '--capitalize', dest='transform', action='store_const', const=str.capitalize,
                                 help='make words capitalized')

    parser.add_argument('--min', type=int, default=None,
                        help='limit minimum length of word (default is unlimited)')
    parser.add_argument('--max', type=int, default=None,
                        help='limit maximum length of word (default is unlimited)')
    parser.add_argument('--version', action='version',
                        version='%(prog)s {}'.format(__version__))

    args = parser.parse_args()

    if args.wordlist_file:
        wordlist = args.wordlist_file.read().splitlines()
    else:
        wordlist = open('{}/wordlists/{}.txt'.format(
            os.path.dirname(os.path.abspath(__file__)), args.wordlist
        )).read().splitlines()

    if args.min:
        wordlist = [w for w in wordlist if len(w) >= args.min]

    if args.max:
        wordlist = [w for w in wordlist if len(w) <= args.max]

    if args.bits:
        args.length = math.ceil(args.bits / math.log2(len(wordlist)))

    passphrases = []
    for i in range(args.count):
        passphrase = generate_passphrase(wordlist, args.length, args.separator, args.transform)
        passphrases.append(passphrase)
        print(passphrase)

    if args.stats:
        passphrase_strength = math.log2(len(wordlist)) * args.length

        print()
        print('Statistics:')
        print('===========')
        print('Number of words in passphrase: {:d}'.format(args.length))
        print('Wordlist length: {:d} words'.format(len(wordlist)))
        print('Passphrase strength (entropy): {:.1f} bits'.format(passphrase_strength))
        print()
        print('{} length: {:d} chars'.format(
            'Average passphrase' if args.count > 1 else 'Passphrase',
            round(sum(len(p) for p in passphrases) / len(passphrases))
        ))
        print('Length of equivalent case sensitive alphanumeric password: {:d} chars'.format(
            math.ceil(passphrase_strength / math.log2(62))
        ))
        print('Length of equivalent all ASCII printable characters password: {:d} chars'.format(
            math.ceil(passphrase_strength / math.log2(95))
        ))

    if args.clipboard:
        copy_to_clipboard(os.linesep.join(passphrases))


if __name__ == '__main__':
    main()
