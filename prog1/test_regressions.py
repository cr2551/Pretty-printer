"""Run from prog1 with: python -m unittest -v test_regressions"""
import io
import subprocess
import sys
import unittest
from pathlib import Path
from contextlib import redirect_stdout

from Parse import Parser, Scanner
from Special import Set, Regular
from Tree import Nil, BoolLit

ROOT = Path(__file__).resolve().parent


def parse(source):
    return Parser(Scanner(io.StringIO(source))).parseExp()


def run(source, *args):
    return subprocess.run([sys.executable, '-B', str(ROOT / 'SPP.py'), *args],
                          input=source, text=True, capture_output=True, timeout=5)


def printed(node):
    stream = io.StringIO()
    with redirect_stdout(stream):
        node.print(0)
    return stream.getvalue()


class RegressionTests(unittest.TestCase):
    def test_operators_and_identifiers(self):
        words = ['+', '-', '...', 'Hello', 'a1+-.@', '!$%&*/:<=>?^_~']
        scanner = Scanner(io.StringIO(' '.join(words)))
        self.assertEqual([scanner.getNextToken().getName() for _ in words],
                         [word.lower() for word in words])
        self.assertIsNone(scanner.getNextToken())
        self.assertEqual(printed(parse('(- n 1)')), '(- n 1)\n')

    def test_whitespace_and_comments(self):
        self.assertEqual(parse(' \t\r\f\n; first\n ; second\r\n 42 ; end').intVal, 42)
        self.assertIsNone(parse('; no final newline'))

    def test_strings_round_trip(self):
        for source in [r'"say \"hello\" \\ path"', '""', '"a\nb"', '"; ()"']:
            with self.subTest(source=source):
                self.assertEqual(printed(parse(source)), source + '\n')
                self.assertEqual(parse(printed(parse(source))).strVal, parse(source).strVal)

    def test_singletons(self):
        self.assertIs(parse('()'), Nil.getInstance())
        self.assertIs(parse('#t'), BoolLit.getInstance(True))
        self.assertIs(parse('#f'), BoolLit.getInstance(False))

    def test_dotted_and_quoted_lists(self):
        for source in ['(a . b)', '(a b . c)', "'(if x 1 0)", "'()"]:
            self.assertEqual(printed(parse(source)), source + '\n')
        self.assertEqual(printed(parse('(a . (b c))')), '(a b c)\n')

    def test_strategy_selection(self):
        self.assertIsInstance(parse('(set! x 1)').form, Set)
        self.assertIsInstance(parse('(set x 1)').form, Regular)
        self.assertEqual(printed(parse('(set! x (+ 2 3))')), '(set! x (+ 2 3))\n')

    def test_expression_boundary(self):
        class CountingScanner:
            def __init__(self):
                self.scanner = Scanner(io.StringIO('(a) 42'))
                self.count = 0
            def getNextToken(self):
                self.count += 1
                return self.scanner.getNextToken()
        scanner = CountingScanner()
        parser = Parser(scanner)
        self.assertEqual(printed(parser.parseExp()), '(a)\n')
        self.assertEqual(scanner.count, 3)
        self.assertEqual(parser.parseExp().intVal, 42)
        self.assertIsNone(parser.parseExp())

    def test_long_flat_list(self):
        source = '(' + ' '.join(['x'] * 2000) + ')'
        self.assertEqual(printed(parse(source)), source + '\n')

    def test_errors_do_not_hang_or_crash(self):
        for source in ['(', '(a (b', '(. a)', '(a .)', '(a . b c)', "'", '(a .',
                       '"unfinished', '#', '#x', '#true', '123abc', '@bad', '-2', r'"\q"']:
            with self.subTest(source=source):
                result = run(source)
                self.assertEqual(result.returncode, 1)
                self.assertIn('Error:', result.stderr)
                self.assertNotIn('Traceback', result.stderr)
        result = run('; comment at EOF')
        self.assertEqual((result.returncode, result.stdout, result.stderr), (0, '', ''))

    def test_recovery_and_exit_status(self):
        result = run(') . 42')
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, '42\n')
        self.assertIn('unexpected RPAREN', result.stderr)
        self.assertIn('unexpected DOT', result.stderr)

    def test_debug_and_usage(self):
        result = run('+ - ...', '-d')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, ''.join('TokenType.IDENT, name = ' + x + '\n' for x in ['+', '-', '...']))
        self.assertEqual(run('', '--bad').returncode, 2)

    def test_supplied_inputs_round_trip(self):
        paths = list((ROOT.parent / 'prog1.test').iterdir()) + [ROOT / 'fac.scm']
        for path in paths:
            if path.name == 'runtests':
                continue
            with self.subTest(file=path.name):
                args = ['-d'] if path.name.endswith('.-d') else []
                result = run(path.read_text(), *args)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stderr, '')
                self.assertTrue(result.stdout)
                if not args:
                    again = run(result.stdout)
                    self.assertEqual((again.returncode, again.stdout, again.stderr), (0, result.stdout, ''))
                if path.name == 'fac.scm':
                    self.assertIn('(g g (- n 1) (* n x))', result.stdout)

    def test_special_forms_expected_output(self):
        cases = {
            '(define (fac n) (if (= n 0) 1 (* n (fac (- n 1)))))':
                '(define (fac n)\n  (if (= n 0)\n    1\n    (* n (fac (- n 1)))\n  )\n)\n',
            '(begin (set! x 6) (set! y 7) (* x y))':
                '(begin\n  (set! x 6)\n  (set! y 7)\n  (* x y)\n)\n',
            '(let ((x 2)) x)': '(let\n  ((x 2))\n  x\n)\n',
            '(cond (else 1))': '(cond\n  (else 1)\n)\n',
            '(lambda (x . args) args)': '(lambda (x . args)\n  args\n)\n',
            '(define x 0)': '(define x 0)\n',
        }
        for source, expected in cases.items():
            with self.subTest(source=source):
                self.assertEqual(printed(parse(source)), expected)


if __name__ == '__main__':
    unittest.main()
