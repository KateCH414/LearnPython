# --*-- coding:utf-8 --*--
import re

def is_valid_email(addr):
    if re.match(r'[A-Za-z0-9_\-\.]*@[A-Za-z0-9_\-\.]*.com$', addr):
        return True
    else:
        return False


def name_of_email(addr):
    m = re.match(r'(<*[\w]*[\W]*[\w]*>*)([]*)@([A-Za-z0-9_]*).com$', addr)
    if m:
        print(m.group(1))
        print(m.group(2))
        if m.group(1) != "":
            return m.group(1)
        elif m.group(2) != "":
            return m.group(2)
        else:
            return None
    else:
        return None


if __name__ == '__main__':
    # assert name_of_email('tom@voyager.org') == 'tom'
    # assert name_of_email('<Tom Paris> tom@voyager.org') == 'Tom Paris'
    # print('ok')

    str = '010-12345'

    m = re.match(r'^(\d{3})-(\d{3,8})$', str)
    print(m.group(1))
