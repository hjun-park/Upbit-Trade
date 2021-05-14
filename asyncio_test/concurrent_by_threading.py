import threading
import itertools
import time
import sys


class Signal:  # 1
    go = True


def spin(msg, signal):  # 2
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):  # 3
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        time.sleep(.1)
        if not signal.go:  # 4
            break
    write(' ' * len(status) + '\x08' * len(status))


def slow_function():  # 5
    # pretend waiting a long time for I/O
    time.sleep(3)  # 6
    return 42


def supervisor():  # 7
    signal = Signal()
    spinner = threading.Thread(target=spin,
                               args=('thinking!', signal))
    print('spinner object:', spinner)  # 8
    spinner.start()  # 9
    result = slow_function()  # 10
    signal.go = False  # 11
    spinner.join()  # 12
    return result


def main():
    result = supervisor()  # 13
    print('Answer:', result)


if __name__ == '__main__':
    main()
