import argparse
import logging
import os
import shutil
from subprocess import Popen
from tempfile import mkdtemp

import ExamBuilder

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
logger = logging.getLogger()


def main():
    parser = argparse.ArgumentParser(
        prog="exam_builder",
        description="Generate PDF from well prepared LaTeX snipplets",
        epilog="Questionfile  format [G|V]_competence_[A|B]_percentage[_*].tex",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Be more verbose")
    parser.add_argument(
        "-d",
        "--directory",
        action="store",
        default=".",
        help="Directory to use (format: DATE_COURSE.NAME_EXAM.NAME_CLASS.NAME)",
    )
    parser.add_argument(
        "-l", "--latex", action="store_true", help="Generate latex instead of pdf files"
    )
    args = parser.parse_args()
    if not args.verbose:
        logger.setLevel(logging.INFO)
    logger.debug("Args = %s", args)

    out_dir = os.path.abspath(os.path.curdir)
    exam_dir = os.path.abspath(args.directory)
    temp_dir = mkdtemp()
    exam_name = os.path.basename(exam_dir)

    directory_reader = ExamBuilder.DirectoryReader(exam_dir)

    os.chdir(exam_dir)

    for group in ["A", "B"]:
        latex_name = "%s_%s.tex" % (exam_name, group)
        latex_name = os.path.join(temp_dir, latex_name)
        latex_name = os.path.abspath(latex_name)

        with open(latex_name, "w") as file:
            latex_builder = ExamBuilder.LatexBuilder(directory_reader, group=group)
            file.write(latex_builder.latex())

        if not args.latex:
            error_name = os.path.join(temp_dir, "pdflatex.err")
            output_name = os.path.join(temp_dir, "pdflatex.out")
            error = open(error_name, "w")
            output = open(output_name, "w")
            process = Popen(
                [
                    "pdflatex",
                    "-halt-on-error",
                    "-output-directory=%s" % temp_dir,
                    latex_name,
                ],
                cwd=exam_dir,
                stdout=output,
                stderr=error,
            )
            logging.debug("process %s", process)
            result = process.wait()
            error.close()
            output.close()
            if result == 0:
                shutil.copy2(latex_name.replace(".tex", ".pdf"), out_dir)
            else:
                logging.error("Failed to run pdflatex")
                with open(output_name, "r") as output:
                    for output_line in output.readlines()[-20:]:
                        logging.error(output_line.strip())
        else:
            shutil.copy2(latex_name, out_dir)

    logging.debug("Cleaning %s", temp_dir)

    for root, directories, files in os.walk(temp_dir):
        if directories:
            logging.error("Temp dir contains folders %s", root)
        for del_file in files:
            logging.debug("Deleting %s", del_file)
            os.remove(os.path.join(root, del_file))
        logging.debug("Deleting %s", root)
        os.rmdir(root)
