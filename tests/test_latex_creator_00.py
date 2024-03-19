import logging
import os

import ExamBuilder


def test_latex_creator_00():
    exam = ExamBuilder.DirectoryReader(
        os.path.join(
            ".", "test_data/20231031_example.course_example.name_example.class"
        )
    )
    latex_creator = ExamBuilder.LatexBuilder(exam)
    latex_text = latex_creator.latex()
    logging.error(latex_text)
    assert len(latex_text) == 3643
