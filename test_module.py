""""
Unit test for the class AudioPipe module

help from: https://www.pythontutorial.net/python-unit-testing/python-test-fixtures/

TODO:

Set up test file system
- Root, ReadDir, WriteDir, path to textdoc. 

Set up fake audios
"""
import unittest

import pyflac  # to make random flacs
import numpy as np  # to make random flacs

import os  # to make tmp directories
import audiopipe as ap


def setUpModule():
    # create test file and random flacs
    #
    pass


def tearDownModule():
    # remove files and random flacs
    pass


class TestAP(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        print("setting up class...")

    @classmethod
    def tearDownClass(cls) -> None:
        print("tearing down class...")

    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_writeAudio(self):
        pass

    def test_sampleAudio1(self):
        pass

    def test_sampleAudioS(self):
        pass

    def test_processAudio(self):
        pass

    def test_sampleAudio(self):
        pass

    def test_savePickle(self):
        pass

    def test_createAudioPathList(self):
        pass

    def test_getIDs(self):
        pass

    def test_getreaddir(self):
        pass

    def test_writedir(self):
        pass
