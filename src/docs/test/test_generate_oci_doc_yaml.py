#!/usr/bin/env python3

import pytest


def test_example_failure():

    assert False, "This is to exemplify the output of a failed unit test"


def test_example_error():

    raise Exception