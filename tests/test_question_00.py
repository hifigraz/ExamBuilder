import logging
import os

import ExamBuilder


def test_00():
    """Test Exam Class constructor."""
    TEST_NAME = "g_kompetenz.1_A_80_01.tex"
    TEST_CONTENT = """\
This is a far too long line for this file and it will probably be beyond 80 chars.
This is a short line.
"""
    EXPECTED_STRING = """\
********************************************************************************
* Competence: kompetenz 1                                                      *
********************************************************************************
* Class: G -- Height 80 -- Group A                                             *
********************************************************************************
* This is a far too long line for this file and it will probably be beyond ... *
* This is a short line.                                                        *
********************************************************************************
"""
    question_1 = ExamBuilder.Question(TEST_NAME, TEST_CONTENT)
    logging.info("%s%s", os.linesep, question_1)
    assert str(question_1) == EXPECTED_STRING
    assert question_1.question_class == "G"
    assert question_1.competence == "kompetenz 1"
    assert question_1.group == "A"
    assert question_1.percentage == 80
    assert len(question_1.text) == len(TEST_CONTENT.strip())


def test_01():
    """Test Exam Class constructor."""
    TEST_NAME = "kompetenz.1_A_80_01.tex"
    TEST_CONTENT = """\
This is a far too long line for this file and it will probably be beyond 80 chars.
This is a short line.
"""
    EXPECTED_STRING = """\
********************************************************************************
* Competence: kompetenz 1                                                      *
********************************************************************************
* Class: GV -- Height 80 -- Group A                                            *
********************************************************************************
* This is a far too long line for this file and it will probably be beyond ... *
* This is a short line.                                                        *
********************************************************************************
"""
    question_1 = ExamBuilder.Question(TEST_NAME, TEST_CONTENT)
    logging.info("%s%s", os.linesep, question_1)
    assert str(question_1) == EXPECTED_STRING
    assert question_1.question_class == "GV"
    assert question_1.competence == "kompetenz 1"
    assert question_1.group == "A"
    assert question_1.percentage == 80
    assert len(question_1.text) == len(TEST_CONTENT.strip())


def test_02():
    """Test Exam Class constructor."""
    TEST_NAME = "G_kompetenz.1_40_01.tex"
    TEST_CONTENT = """\
This is a far too long line for this file and it will probably be beyond 80 chars.
This is a short line.
"""
    EXPECTED_STRING = """\
********************************************************************************
* Competence: kompetenz 1                                                      *
********************************************************************************
* Class: G -- Height 40 -- Group AB                                            *
********************************************************************************
* This is a far too long line for this file and it will probably be beyond ... *
* This is a short line.                                                        *
********************************************************************************
"""
    question_1 = ExamBuilder.Question(TEST_NAME, TEST_CONTENT)
    logging.info("%s%s", os.linesep, question_1)
    assert str(question_1) == EXPECTED_STRING
    assert question_1.question_class == "G"
    assert question_1.competence == "kompetenz 1"
    assert question_1.group == "AB"
    assert question_1.percentage == 40
    assert len(question_1.text) == len(TEST_CONTENT.strip())


def test_03():
    """Test Exam Class constructor."""
    TEST_NAME = "G_kompetenz.1_40_01_asdf_fdssa.tex"
    TEST_CONTENT = """\
This is a far too long line for this file and it will probably be beyond 80 chars.
This is a short line.
"""
    EXPECTED_STRING = """\
********************************************************************************
* Competence: kompetenz 1                                                      *
********************************************************************************
* Class: G -- Height 40 -- Group AB                                            *
********************************************************************************
* This is a far too long line for this file and it will probably be beyond ... *
* This is a short line.                                                        *
********************************************************************************
"""
    question_1 = ExamBuilder.Question(TEST_NAME, TEST_CONTENT)
    logging.info("%s%s", os.linesep, question_1)
    assert str(question_1) == EXPECTED_STRING
    assert question_1.question_class == "G"
    assert question_1.competence == "kompetenz 1"
    assert question_1.group == "AB"
    assert question_1.percentage == 40
    assert len(question_1.text) == len(TEST_CONTENT.strip())


def test_04():
    """Test Exam Class constructor."""
    TEST_NAME = "kompetenz.1_B_40.tex"
    TEST_CONTENT = """\
This is a far too long line for this file and it will probably be beyond 80 chars.
This is a short line.
"""
    EXPECTED_STRING = """\
********************************************************************************
* Competence: kompetenz 1                                                      *
********************************************************************************
* Class: GV -- Height 40 -- Group B                                            *
********************************************************************************
* This is a far too long line for this file and it will probably be beyond ... *
* This is a short line.                                                        *
********************************************************************************
"""
    question_1 = ExamBuilder.Question(TEST_NAME, TEST_CONTENT)
    logging.info("%s%s", os.linesep, question_1)
    assert str(question_1) == EXPECTED_STRING
    assert question_1.question_class == "GV"
    assert question_1.competence == "kompetenz 1"
    assert question_1.group == "B"
    assert question_1.percentage == 40
    assert len(question_1.text) == len(TEST_CONTENT.strip())
