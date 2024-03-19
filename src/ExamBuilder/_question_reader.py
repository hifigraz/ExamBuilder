import logging
import os

from ._question import Question


class QuestionReader:
    def __init__(self, working_directory: str = "."):
        self._questions = []
        self._working_directory = working_directory
        self._abs_path = os.path.abspath(self._working_directory)
        if not os.path.isdir(self._abs_path):
            raise FileNotFoundError(self._abs_path)
        for root, directories, files in os.walk(self._abs_path):
            logging.debug("Ignoring subdirectories %s", directories)
            for question_file_name in sorted(files):
                if question_file_name[-4:].upper() == ".TEX":
                    with open(
                        os.path.join(root, question_file_name), "r"
                    ) as question_file:
                        content = question_file.read()
                        self._questions.append(Question(question_file_name, content))

    def __len__(self):
        return len(self._questions)

    def _get_nr_of_competences(self):
        competences = set(map(lambda x: x.competence, self._questions))
        logging.info(competences)
        return len(competences)

    nr_competences = property(_get_nr_of_competences)
    competences = property(lambda s: set(map(lambda x: x.competence, s._questions)))

    def __str__(self):
        return_value = ""
        for question in self._questions:
            return_value += str(question) + os.linesep + os.linesep
        return return_value.strip()

    def __iter__(self):
        return iter(self._questions)
