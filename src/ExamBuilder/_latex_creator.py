import datetime
import importlib.resources
import logging
import os
from random import shuffle

from ._directory_reader import DirectoryReader


class LatexBuilderBase:
    def __init__(self, template_path, directory_reader: DirectoryReader, group="A"):
        self._group = group
        self._directory_reader = directory_reader
        package_dir = importlib.resources.files("ExamBuilder")
        template_file = package_dir.joinpath(template_path)
        with template_file.open("r") as template:
            self._text: str = template.read()

    def _replace(self, key, value):
        self._text = self._text.replace(key, value)

    def latex(self):
        return self._text


class LatexBuilder(LatexBuilderBase):
    EXAM_TEMPLATE = "./ressources/exam_template.tex"
    REPLACE_KEY_CONTENT = "\\replaceMeContent"
    PAGE_HEIGHT = 280

    def __init__(self, directory_reader: DirectoryReader, group="A"):
        super().__init__(self.EXAM_TEMPLATE, directory_reader, group)
        latex_header_builder = LatexBuilderHead(self._directory_reader, self._group)
        latex_grading_builder = LatexBuilderGrading(self._directory_reader, self._group)
        latex_questions_builder = LatexBuilderQuestions(
            self._directory_reader,
            self._group,
            self.PAGE_HEIGHT
            - 1
            - latex_header_builder.head_height
            - latex_grading_builder.grading_height,
            self.PAGE_HEIGHT,
        )
        self._replace(
            self.REPLACE_KEY_CONTENT,
            "%s%s%s%s%s%s"
            % (
                os.linesep,
                latex_header_builder.latex(),
                os.linesep,
                latex_grading_builder.latex(),
                os.linesep,
                latex_questions_builder.latex(),
            ),
        )


class LatexBuilderGrading(LatexBuilderBase):
    GRADING_TEMPLATE = "./ressources/exam_grading_template.tex"
    REPLACE_KEY_PAGE_HEIGHT = "\\replaceMePageHeight"
    REPLACE_KEY_BOX_HEIGHT = "\\replaceMeBoxHeight"
    REPLACE_KEY_COMPETENCES = "\\replaceMeCompetences"

    def __init__(self, directory_reader: DirectoryReader, group: str):
        super().__init__(self.GRADING_TEMPLATE, directory_reader, group)

        basic_height = 6
        competence_height = 4.5
        page_height = (
            basic_height + len(self._directory_reader.competences) * competence_height
        )
        self._grading_height = page_height
        box_height = page_height / 10.0

        self._replace(self.REPLACE_KEY_PAGE_HEIGHT, "%dmm" % page_height)
        self._replace(self.REPLACE_KEY_BOX_HEIGHT, "%f" % box_height)
        competences = ""
        for competence in self._directory_reader.competences:
            competences += "%s & & & \\\\%s" % (competence, os.linesep)
            competences += "\\hline%s" % os.linesep
        self._replace(self.REPLACE_KEY_COMPETENCES, competences)

    grading_height = property(lambda s: s._grading_height)


class LatexBuilderHead(LatexBuilderBase):
    EXAM_HEAD_TEMPLATE = "./ressources/exam_head_template.tex"
    REPLACE_KEY_HEIGHT = "\\replaceMeHeight"
    REPLACE_KEY_COURSE = "\\replaceMeCourse"
    REPLACE_KEY_GROUP = "\\replaceMeGroup"
    REPLACE_KEY_DATE = "\\replaceMeDate"
    REPLACE_KEY_CLASS = "\\replaceMeClass"

    def __init__(self, directory_reader: DirectoryReader, group):
        super().__init__(self.EXAM_HEAD_TEMPLATE, directory_reader, group)
        exam_date = datetime.datetime(
            year=int(self._directory_reader.exam_date[:4]),
            month=int(self._directory_reader.exam_date[4:6]),
            day=int(self._directory_reader.exam_date[6:]),
        )
        self._head_height = 15
        logging.debug("Datetime %s", exam_date)
        self._replace(self.REPLACE_KEY_HEIGHT, "%dmm" % self._head_height)
        self._replace(self.REPLACE_KEY_COURSE, self._directory_reader.exam_course)
        self._replace(self.REPLACE_KEY_GROUP, self._group)
        self._replace(self.REPLACE_KEY_DATE, exam_date.strftime("%d.%m.%Y"))
        self._replace(self.REPLACE_KEY_CLASS, self._directory_reader.exam_class)

    head_height = property(lambda s: s._head_height)


class LatexBuilderQuestions(LatexBuilderBase):
    EXAM_QUESTION_TEMPLATE = "./ressources/exam_question_template.tex"
    REPLACE_KEY_HEIGHT = "\\replaceMeHeight"
    REPLACE_KEY_COMPETENCE = "\\replaceMeCompetence"
    REPLACE_KEY_QUESTION_TEXT = "\\replaceMeQuestionText"
    REPLACE_KEY_G_COLOR = "\\replaceMeGColor"
    REPLACE_KEY_V_COLOR = "\\replaceMeVColor"

    def __init__(
        self,
        directory_reader: DirectoryReader,
        group,
        first_page_height,
        other_page_height,
    ):
        super().__init__(self.EXAM_QUESTION_TEMPLATE, directory_reader, group)
        questions = self._directory_reader.questions
        questions = filter(lambda x: self._group in x.group, questions)
        questions = list(questions)

        advanced_questions = list(filter(lambda x: x.question_class == "V", questions))
        general_questions = list(filter(lambda x: x.question_class == "GV", questions))
        basic_questions = list(filter(lambda x: x.question_class == "G", questions))

        logging.debug("advanced_questions %s", advanced_questions)
        logging.debug("general_questions %s", general_questions)
        logging.debug("basic_questions %s", basic_questions)

        if self._group == "B":
            shuffle(basic_questions)
            shuffle(general_questions)
            shuffle(advanced_questions)

        questions = basic_questions + general_questions + advanced_questions

        logging.debug("All Questions %s", questions)

        logging.debug("Question %s", questions)
        template_text = self._text
        self._text = ""
        completed_height = 0
        for question in questions:
            g_color = "white" if "G" in question.question_class else "black"
            v_color = "white" if "V" in question.question_class else "black"
            logging.debug("FPH %d", first_page_height)
            question_height = int(first_page_height * question.percentage / 100)
            if completed_height > first_page_height:
                question_height = int(other_page_height * question.percentage / 100)
            question_height+=1
            completed_height += question_height
            logging.debug("Question height is %d", question_height)
            self._text += os.linesep
            temp_text = template_text
            temp_text = temp_text.replace(self.REPLACE_KEY_G_COLOR, g_color)
            temp_text = temp_text.replace(self.REPLACE_KEY_V_COLOR, v_color)
            temp_text = temp_text.replace(
                self.REPLACE_KEY_HEIGHT, "%dmm" % question_height
            )
            temp_text = temp_text.replace(
                self.REPLACE_KEY_COMPETENCE, question.competence
            )
            temp_text = temp_text.replace(self.REPLACE_KEY_QUESTION_TEXT, question.text)
            self._text += temp_text

        logging.debug("Firstpage height is %d" % first_page_height)
