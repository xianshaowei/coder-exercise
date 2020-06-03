# -*- coding: utf-8 -*-


def main():
    import re

    ret = re.match(r"<([a-zA-Z0-9]*)>.*</\1>", "<html>helloworld</html>")
    print(ret.group())

    ret2 = re.match("<([a-zA-Z0-9]*)>.*</\\1>", "<html>helloworld</html>")
    print(ret2.group())

if __name__ == '__main__':
    main()
