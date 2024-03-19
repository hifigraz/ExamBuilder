import logging
import os


class Question:
    def __init__(self, file_name: str, content: str):
        """generates a question object."""
        self._filename: str = file_name
        self._question_class: str = ""
        self._competence: str = ""
        self._group: str = ""
        self._percentage: int = 0
        self._text: str = content.strip()

        self._filename = os.path.basename(file_name).replace(".tex", "")

        for component in self._filename.split("_"):
            if not self._question_class:
                if component.upper() in ["G", "V"]:
                    self._question_class = component.upper()
                    continue
                else:
                    self._question_class = "GV"
            if not self._competence:
                self._competence = component.replace(".", " ")
                continue
            if not self._group:
                if component.upper() in ["A", "B"]:
                    self._group = component.upper()
                    continue
                else:
                    self._group = "AB"
            if not self._percentage:
                self._percentage = int(component)
                continue
            logging.debug("Ignoring filename component (%s)" % component)

    def __str__(self):
        representation: str = (
            "********************************************************************************"
            + os.linesep
        )
        representation += (
            "* %-76s *" % ("Competence: %s" % self._competence) + os.linesep
        )
        representation += (
            "********************************************************************************"
            + os.linesep
        )
        representation += (
            "* %-76s *"
            % (
                "Class: %s -- Height %d -- Group %s"
                % (self._question_class, self._percentage, self._group)
            )
            + os.linesep
        )
        representation += (
            "********************************************************************************"
            + os.linesep
        )
        for question_line in self._text.split(os.linesep):
            if len(question_line) > 76:
                question_line = question_line[:72] + " ..."
            representation += "* %-76s *%s" % (question_line, os.linesep)
        representation += (
            "********************************************************************************"
            + os.linesep
        )
        return representation

    question_class = property(lambda x: x._question_class)
    competence = property(lambda x: x._competence)
    group = property(lambda x: x._group)
    percentage = property(lambda x: x._percentage)
    text = property(lambda x: x._text)
