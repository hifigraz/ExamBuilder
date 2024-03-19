import logging
import os

import ExamBuilder

EXAMPLE_DIR = "test_data/20231031_example.course_example.name_example.class"


def test_question_reader_00():
    assert ExamBuilder.QuestionReader
    try:
        ExamBuilder.QuestionReader("does_not_exists")
        assert "This should have raised" == ""
    except FileNotFoundError as e:
        assert str(e) == os.path.abspath(os.path.join(".", "does_not_exists"))
    except Exception as e:
        logging.error("Error occured %s", e)
        raise


def test_question_reader_01():
    """Test if reading questions give the right amount of Questions."""
    question_reader = ExamBuilder.QuestionReader(EXAMPLE_DIR)
    assert question_reader
    assert len(question_reader) == 4
    assert question_reader.nr_competences == 3
    assert set(question_reader.competences) == set(
        ["kompetenz", "kompetenzA", "kompetenzB"]
    )
    assert len(str(question_reader)) == 2435
