import sys
import argparse
import os

from pwd import getpwuid
from grp import getgrgid
import time


class Mini:

    def __init__(self, args):
        self.f = args.file
        self.grep = args.grep
        self.list = args.list
        self.df = args.disk
        self.p = args.path
        self.human = args.human
        self.pattern = args.pattern
        self.q = args.q

    def mini_grep(self, files, pattern, q=False):
        try:
            for i in files:
                line_number = 0
                with open(i, 'r') as f:
                    for line in f:
                        line_number += 1
                        if pattern in line:
                            if q:
                                print('Found a match on line: {} in file: {}'.format(line, i))
                                print("\n")
                            else:
                                print('Found a match on line: {} with line number: {} '
                                      'in file: {}'.format(line, line_number, i))
                                print("\n")
        except FileNotFoundError as e:
            print(str(e))

    def mini_ls(self, files):
        """
        mini_ls function will display list command output with options
        :return:
        """
        try:
            for i in files:
                owner = getpwuid(os.stat(i).st_uid).pw_name
                group = getgrgid(os.stat(i).st_gid).gr_name
                per = oct(os.stat(i).st_mode)[-3:]
                t = os.stat(i).st_mtime
                print("{} is owned by: {} , group by {} with "
                      "permission {} and last modified on {}"
                      .format(i, owner, group, per, time.ctime(t)))
        except FileNotFoundError as e:
            print(str(e))

    def mini_df(self, path, human_read=False):
        """
        mini_df function will display disk_usage
        :return:
        """
        if human_read:
            for i in path:
                print(str(os.system(('df -h %s' % i)))[0:-1])
        else:
            for i in path:
                print(str(os.system(('df %s' % i)))[0:-1])


# Main()
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mini-programs')
    parser.add_argument('-ls', '--list', action='store_true', help='List the directories')
    parser.add_argument('-df', '--disk', action='store_true', help='Disk usage in the directory or file')
    parser.add_argument('-s', '--grep', action='store_true', help='Grep pattern in the file')
    parser.add_argument('-p', '--path', type=str, help='Path for disk usage check', nargs='+')
    parser.add_argument('-H', '--human', default=False, action='store_true',
                        help='Human Readable format for disk usage')
    parser.add_argument('-q', '--q', default=False, action='store_true',
                        help=' Omit line number form the searched lines')
    parser.add_argument('-e', '--pattern', type=str, help='PATTERN regex for grep')
    parser.add_argument('-f', '--file', type=str, help='Files to pass in the list function(ls)', nargs='+')

    m = Mini(parser.parse_args(sys.argv[1:]))
    if m.list:
        if m.f:
            file = m.f
            m.mini_ls(file)
        else:
            for _, _, file in os.walk(os.getcwd()):
                m.mini_ls(file)
        exit()
    if m.df:
        if m.p:
            paths = m.p
            m.mini_df(paths, m.human)
        else:
            current_path = '.'
            m.mini_df(current_path, m.human)
        exit()
    if m.grep:
        if m.f:
            file = m.f
            m.mini_grep(file, m.pattern, m.q)
        else:
            file = []
            print("Enter the file name, provide 'q' to finish input")
            for st in sys.stdin:
                if 'q' == st.rstrip():
                    break
                file.append(st.strip('\n'))
            m.mini_grep(file, m.pattern, m.q)
