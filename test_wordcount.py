import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from wordcount import count_words, main


class CountWordsTest(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(count_words(""), 0)

    def test_whitespace_only(self):
        self.assertEqual(count_words("  \n\t "), 0)

    def test_mixed_whitespace_and_korean(self):
        self.assertEqual(count_words("Hello world\n안녕하세요  반갑습니다\t파이썬\n"), 5)


class MainTest(unittest.TestCase):
    def run_main(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main(["wordcount.py", *args])
        return code, out.getvalue(), err.getvalue()

    def test_counts_file(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "a.txt"
            p.write_text("one two three", encoding="utf-8")
            code, out, err = self.run_main(str(p))
        self.assertEqual(code, 0)
        self.assertRegex(out, r": 3 단어 \(실행: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\)$")
        self.assertEqual(err, "")

    def test_utf8_bom(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "bom.txt"
            p.write_bytes("﻿하나 둘".encode("utf-8"))
            code, out, _ = self.run_main(str(p))
        self.assertEqual(code, 0)
        self.assertIn("2 단어", out)

    def test_missing_file(self):
        code, out, err = self.run_main("does_not_exist.txt")
        self.assertEqual(code, 1)
        self.assertEqual(out, "")
        self.assertIn("찾을 수 없습니다", err)

    def test_no_args(self):
        code, _, err = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("사용법", err)

    def test_directory(self):
        with tempfile.TemporaryDirectory() as d:
            code, _, err = self.run_main(d)
        self.assertEqual(code, 1)
        self.assertIn("파일이 아닙니다", err)

    def test_non_utf8(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "bad.txt"
            p.write_bytes(b"\xff\xfe\xfa")
            code, _, err = self.run_main(str(p))
        self.assertEqual(code, 1)
        self.assertIn("UTF-8", err)


if __name__ == "__main__":
    unittest.main()
