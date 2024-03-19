import os
from typing import Iterator

from ._question import Question
from ._question_reader import QuestionReader


class DirectoryReader:
    def __init__(self, working_directory: str = "."):
        self._working_directory = working_directory
        self._abs_path = os.path.abspath(self._working_directory)
        if not os.path.isdir(self._abs_path):
            raise FileNotFoundError(self._abs_path)
        dir_name = os.path.basename(self._abs_path)
        exam_date, exam_course, exam_name, exam_class = dir_name.split("_")
        self._exam_name = exam_name.replace(".", " ")
        self._exam_course = exam_course.replace(".", " ")
        self._exam_date = exam_date
        self._exam_class = exam_class.replace(".", " ")
        self._questions = QuestionReader(working_directory)

    def _get_questions(self) -> Iterator[Question]:
        return self._questions.__iter__()

    abs_path = property(lambda s: s._abs_path)
    exam_course = property(lambda s: s._exam_course)
    exam_date = property(lambda s: s._exam_date)
    exam_name = property(lambda s: s._exam_name)
    questions = property(_get_questions)
    exam_class = property(lambda s: s._exam_class)
    competences = property(lambda s: s._questions.competences)

    def __str__(self):
        return_value = 80 * "*" + os.linesep
        return_value += "* %-76s *" % (" Course: %s" % self._exam_course) + os.linesep
        return_value += "* %-76s *" % ("   Name: %s" % self._exam_name) + os.linesep
        return_value += "* %-76s *" % ("   Date: %s" % self._exam_date) + os.linesep
        return_value += "* %-76s *" % (" Competences:") + os.linesep
        for competence in self._questions.competences:
            return_value += "* %-76s *" % ("     - %s" % competence) + os.linesep
        return_value += 80 * "*" + os.linesep + os.linesep
        return_value += str(self._questions)
        return return_value
