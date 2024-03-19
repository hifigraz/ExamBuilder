import logging
import os

import ExamBuilder


def test_00():
    assert True


def test_import_00():
    import ExamBuilder

    assert ExamBuilder


def test_import_01():
    """Check if DirectoryReader exists."""
    assert ExamBuilder.DirectoryReader


def test_directory_reader_test_name_00():
    try:
        ExamBuilder.DirectoryReader("this/path/does/not/exist")
        assert "This should have raised" == ""
    except FileNotFoundError as e:
        logging.info("Expected error thrown %s.", e)
    except Exception as e:
        logging.error("Unexpected error thrown %s.", e)
        raise


def test_directory_reader_test_name_01():
    """Check if DirectoryReader does recognize exam_name correctly."""
    TEST_PATH = "test_data/20231031_example.course_example.name_example.class"
    directory_reader = ExamBuilder.DirectoryReader(os.path.join(os.curdir, TEST_PATH))
    assert directory_reader.exam_name == "example name"
    assert directory_reader.exam_course == "example course"
    assert directory_reader.exam_date == "20231031"
    assert directory_reader.abs_path == os.path.abspath(TEST_PATH)
    assert directory_reader.competences == set(
        ["kompetenz", "kompetenzA", "kompetenzB"]
    )
    assert directory_reader.exam_class == "example class"

    logging.info("%s%s", os.linesep, directory_reader)
    assert len(str(directory_reader)) == 3165
