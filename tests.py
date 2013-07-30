#/usr/bin/env python3

import unittest
import warnings

import clap


#   enable debugging output which is basically huge number of print() calls
DEBUG = False


class BaseTests(unittest.TestCase):
    def testAddingNewOption(self):
        base = clap.base.Base([])
        base.add(short='f', long='foo', argument=str, required=True, not_with=['-s'], requires=['--bar'], needs=['--baz', '--bax'], conflicts=['--bay'])
        option0 = clap.option.Option(short='f', long='foo',
                                    argument=str, required=True, not_with=['-s'],
                                    requires=['--bar'], needs=['--baz', '--bax'],
                                    conflicts=['--bay'])
        option1 = clap.option.Option(short='b', long='bar',
                                    argument=int,
                                    needs=['--baz', '--bax'])
        self.assertIn(option0, base.options)
        self.assertNotIn(option1, base.options)

    def testRemovingOption(self):
        base = clap.base.Base([])
        base.add(short='f', long='foo', argument=str, required=True, not_with=['-s'], requires=['--bar'], needs=['--baz', '--bax'], conflicts=['--bay'])
        option0 = clap.option.Option(short='f', long='foo',
                                    argument=str, required=True, not_with=['-s'],
                                    requires=['--bar'], needs=['--baz', '--bax'],
                                    conflicts=['--bay'])
        option1 = clap.option.Option(short='b', long='bar',
                                    argument=int,
                                    needs=['--baz', '--bax'])
        base.add(short='b', long='bar', argument=int, needs=['--baz', '--bax'])
        self.assertIn(option0, base.options)
        self.assertIn(option1, base.options)
        base.remove(short='b')
        self.assertIn(option0, base.options)
        self.assertNotIn(option1, base.options)

    def testGettingInput(self):
        argv = ['--foo', '--bar', 'baz', 'bax']
        base = clap.base.Base(argv)
        base.add(long='foo')
        base.add(long='bar', argument=str)
        self.assertEqual(['--foo', '--bar', 'baz'], base._getinput())

    def testOptionRecognition(self):
        tests = [('-a', True),
                 ('--foo', True),
                 ('--foo=bar', True),
                 ('-abc', True),
                 ('a', False),
                 ('foo', False),
                 ('--a', False),
                 ('-a=foo', False),
                 ('--', False),
                 ('-', False),
                 ]
        for opt, result in tests:
            if DEBUG: print(opt, result)
            self.assertEqual(clap.base.lookslikeopt(opt), result)


class FormatterTests(unittest.TestCase):
    def testSplittingEqualSignedOptions(self):
        argv = ['--foo=bar', '--', '--baz=bax']
        f = clap.formater.Formater(argv)
        f._splitequal()
        if DEBUG: print('\'{0}\' -> \'{1}\''.format(' '.join(argv), ' '.join(f.formated)))
        self.assertEqual(f.formated, ['--foo', 'bar', '--', '--baz=bax'])

    def testSplittingConnectedShortOptions(self):
        argv = ['-abc', '--', '-def']
        f = clap.formater.Formater(argv)
        f._splitshorts()
        if DEBUG: print('\'{0}\' -> \'{1}\''.format(' '.join(argv), ' '.join(f.formated)))
        self.assertEqual(f.formated, ['-a', '-b', '-c', '--', '-def'])

    def testGeneralFormating(self):
        argv = ['-abc', 'eggs', '--bar', '--ham', 'good', '--food=spam', '--', '--bax=bay']
        f = clap.formater.Formater(argv)
        f.format()
        if DEBUG: print('\'{0}\' -> \'{1}\''.format(' '.join(argv), ' '.join(f.formated)))
        self.assertEqual(f.formated,
                         ['-a', '-b', '-c', 'eggs', '--bar', '--ham', 'good', '--food', 'spam', '--', '--bax=bay'])


class OptionTests(unittest.TestCase):
    def testOnlyShortName(self):
        o = clap.option.Option(short='f')
        self.assertEqual(o['short'], '-f')
        self.assertEqual(o['long'], '')
        self.assertEqual(str(o), '-f')

    def testOnlyLongName(self):
        o = clap.option.Option(long='foo')
        self.assertEqual(o['short'], '')
        self.assertEqual(o['long'], '--foo')
        self.assertEqual(str(o), '--foo')

    def testInvalidLongName(self):
        tests = ['a', 'A', '0', '-']
        for o in tests:
            if DEBUG: print(o)
            self.assertRaises(TypeError, clap.option.Option, long=o)

    def testBothNames(self):
        o = clap.option.Option(short='f', long='foo')
        self.assertEqual(o['short'], '-f')
        self.assertEqual(o['long'], '--foo')
        self.assertEqual(str(o), '--foo')

    def testNoName(self):
        self.assertRaises(TypeError, clap.option.Option)

    def testTyping(self):
        o = clap.option.Option(short='f', argument=int)
        self.assertEqual(int, o.type())
        p = clap.option.Option(short='f')
        self.assertEqual(None, p.type())

    def testMatching(self):
        o = clap.option.Option(short='f', long='foo')
        self.assertEqual(True, o.match('-f'))
        self.assertEqual(True, o.match('--foo'))

    def testAliases(self):
        o = clap.option.Option(short='f', long='foo')
        self.assertEqual('--foo', o._alias('-f'))
        self.assertEqual('-f', o._alias('--foo'))
        self.assertRaises(NameError, o._alias, '--bar')


class CheckerTests(unittest.TestCase):
    def test(self):
        warnings.warn('not implemented')

    def test(self):
        warnings.warn('not implemented')

    def test(self):
        warnings.warn('not implemented')

    def test(self):
        warnings.warn('not implemented')

    def test(self):
        warnings.warn('not implemented')

    def test(self):
        warnings.warn('not implemented')

    def test(self):
        warnings.warn('not implemented')

    def test(self):
        warnings.warn('not implemented')

    def test(self):
        warnings.warn('not implemented')

    def test(self):
        warnings.warn('not implemented')

    def test(self):
        warnings.warn('not implemented')


class ParserTests(unittest.TestCase):
    def testShortOptionsWithoutArguments(self):
        argv = ['-a', '-b', '-c', 'd', 'e', 'f']
        p = clap.parser.Parser(argv)
        p.add(short='a')
        p.add(short='b')
        p.add(short='c')
        p.parse()
        self.assertEqual({'-a': None, '-b': None, '-c': None}, p.parsed)
        self.assertEqual(['d', 'e', 'f'], p.arguments)

    def testShortOptionsWithArguments(self):
        argv = ['-s', 'eggs', '-i', '42', '-f', '4.2', 'foo']
        p = clap.parser.Parser(argv)
        p.add(short='s', argument=str)
        p.add(short='i', argument=int)
        p.add(short='f', argument=float)
        p.parse()
        self.assertEqual({'-s': 'eggs', '-i': 42, '-f': 4.2}, p.parsed)
        self.assertEqual(['foo'], p.arguments)

    def testLongOptionsWithoutArguments(self):
        argv = ['--foo', '--bar', '--baz', 'bax']
        p = clap.parser.Parser(argv)
        p.add(long='foo')
        p.add(long='bar')
        p.add(long='baz')
        p.parse()
        self.assertEqual(None, p.get('--foo'))
        self.assertEqual(None, p.get('--bar'))
        self.assertEqual(None, p.get('--baz'))
        self.assertEqual(['bax'], p.arguments)

    def testLongOptionsWithArguments(self):
        argv = ['--str', 'eggs', '--int', '42', '--float', '4.2']
        p = clap.parser.Parser(argv)
        p.add(long='str', argument=str)
        p.add(long='int', argument=int)
        p.add(long='float', argument=float)
        p.parse()
        self.assertEqual('eggs', p.get('--str'))
        self.assertEqual(42, p.get('--int'))
        self.assertEqual(4.2, p.get('--float'))

    def testStopingAtBreaker(self):
        argv = ['--foo', '-s', 'eggs', '--int', '42', '--', '-f', '4.2']
        p = clap.parser.Parser(argv)
        p.add(long='foo')
        p.add(long='int', argument=int)
        p.add(short='s', argument=str)
        p.add(short='f', argument=float)
        p.parse()
        self.assertEqual({'--int': 42, '-s': 'eggs', '--foo': None}, p.parsed)
        self.assertEqual(['-f', '4.2'], p.arguments)


if __name__ == '__main__': unittest.main()