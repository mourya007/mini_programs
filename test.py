import unittest
from unittest.mock import patch
import time
import mini
import io
import os
import tempfile


class Test(unittest.TestCase):
    def setUp(self):
        self.f = os.path.join(tempfile.gettempdir(), "tmp-testfile")
        with open(self.f, 'w') as f:
            f.write('test file')
            f.close()

    def test_mini_ls(self):
        owner = 'mourya'
        group = 'tasvob'
        permission = 644
        t = os.stat(self.f).st_mtime
        expected_url = "{} is owned by: {} , group by {} with " \
                       "permission {} and last modified on {}" \
            .format(self.f, owner, group, permission, time.ctime(t))
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            mini.Mini.mini_ls(self, files=(self.f.split()))
            self.assertEqual((fake_out.getvalue().strip()), expected_url)

    def test_mini_grep_with_line_num(self):
        with open(self.f, 'w') as f:
            f.write("test grep")
        pattern = 'grep'
        expected = 'Found a match on line: {} with line number: {} ' \
                   'in file: {}'.format('test grep', 1, self.f)
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            mini.Mini.mini_grep(self, files=(self.f.split()), pattern=pattern, q=False)
            self.assertEqual((fake_out.getvalue().strip()), expected)

    def test_mini_grep_without_line_num(self):
        with open(self.f, 'w') as f:
            f.write("test grep")
        pattern = 'grep'
        expected = 'Found a match on line: {} in file: {}'.format('test grep', self.f)
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            mini.Mini.mini_grep(self, files=(self.f.split()), pattern=pattern, q=True)
            self.assertEqual((fake_out.getvalue().strip()), expected)

    def test_mini_df_with_human_read(self):
        expected = ''
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            mini.Mini.mini_df(self, path='/tmp'.split(), human_read=True)
            self.assertIs((fake_out.getvalue().strip()), expected)
