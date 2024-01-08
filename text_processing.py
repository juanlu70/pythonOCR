import numpy as np
import pytesseract
import re
from PIL import Image, ImageEnhance, ImageOps
import jellyfish
from operator import itemgetter
import ia_process


ia = ia_process.IAProcess()


class TextProcessing:
    def __init__(self):
        self.verbose = 0
        self.solution_file = ""
        self.solution_text = ""
        self.solutions = []
        self.darkness_numbral = 0.45

        return

    # -- process solutions --
    def process_solutions(self) -> None:
        self.solutions = re.split(r".Q[0-9]..", self.solution_text)

        return

    # -- tesseract ocr function --
    def tesseract_ocr(self, name: str) -> str:
        """
        Function to make an OCR of a captured image or to procecss every new file with tesseract
        :param name: filename or path
        :return: string
        """
        # -- open image and increase contrast to make a better OCR --
        img = Image.open(name)
        image = ImageEnhance.Contrast(img).enhance(6.00)

        # ################### TEST IMAGE DARK or WhITE ################
        # -- detect if an image is mostly dark or white --
        pixels = image.getdata()  # get the pixels as a flattened sequence
        black_thresh = 50
        nblack = 0
        for pixel in pixels:
            for n in pixel:
                if n < black_thresh:
                    nblack += 1
        n = len(pixels) * 3
        print("DARKNESS:")
        print(nblack / float(n))

        if (nblack / float(n)) > self.darkness_numbral:
            # -- image it is mostly dark, invert colors --
            print("*** WARNING! The image captured is detected as a DARK IMAGE, try to capture a lighter image")
            print("for better results ***")
            image = ImageOps.invert(image)
            # image.show()

        img1 = np.array(image)

        # -- process OCR and generate text --
        text = pytesseract.image_to_string(img1, lang='eng')

        return text

    # -- remove all empty and unwanted text --
    def remove_empty_lines(self, text: str) -> str:
        """
        This function removes empty lines and get original full text if text filters fails

        :param text: str
        :return: str
        """
        new_text = ""
        txt = text.split("\n")

        # -- loop to remove empty lines and trash text --
        if self.verbose > 0:
            print("--------- VERBOSE FULL TEXT ----------------")
        for line in txt:
            if len(line) > 1:
                if self.verbose > 0:
                    print(" ---> "+line)
                if len(line.strip()) > 0:
                    new_text += line + "\n"

        if self.verbose > 0:
            print("--------------------------------------------")

        return new_text

    # -- remove wrong lines --
    def remove_trash_lines(self, text: str) -> str:
        """
        This function removes trash text from a list of trash text loaded from a file

        :param text: str
        :return: str
        """
        new_text = ""

        # -- load wrong lines file --
        with open("trash_text.txt") as fp:
            trash_text = fp.read().split("\n")
            fp.close()

        trash_text = trash_text[0:-1]

        # -- loop to remove wrong trash lines --
        for line in text.split("\n"):
            skip = 0
            for wrong in trash_text:
                if wrong in line:
                    skip = 1
                    break
            if skip == 0:
                new_text += line + "\n"

        return new_text

    # -- get question and answers block from text --
    def get_query_block(self, text: str) -> str:
        """
        Get the block with the question and answers

        :param text: str
        :return: str
        """
        capture = 0
        new_text = ""

        txt = text.split("\n")

        line = 0
        while line < len(txt):
            if capture == 1:
                new_text += txt[line] + "\n"
                if len(txt[line]) > 0 and txt[line][-1] == "?":
                    new_text += "\n"

            if txt[line].find("linkedin.com/skill-assessments") >= 0 \
                    or txt[line].find("linkedin.comyskill-assessments") >= 0 \
                    or txt[line].find("linkedin.comiskill-assessments") >= 0:
                capture = 1

            if txt[line].find("Something wrong with this question") >= 0:
                capture = 0
                line = len(txt)

            line += 1

        return new_text

    # -- get question only --
    def get_question_block(self, text: str) -> str:
        """
        Function to isolate question block for search solution in solution file

        :param text: str
        :return: str
        """
        # -- isolate question --
        question_text = ""
        question = 1

        for line in text.split("\n"):
            if question == 1:
                if line[0:2] == "© " or line[0:2] == "O ":
                    question = 0
            if question == 1 and len(line) > 10:
                if line[-1] == "?":
                    question_text += line + "\n\n"
                else:
                    question_text += line + "\n"

        return question_text

    # -- search the solution by the question --
    def search_solution(self, question: str) -> str:
        """
        Function to search solution by testing similar_text on the question isolated text

        :param question: str
        :return: str
        """
        final_solution = ""
        possible_solutions = []
        to_delete = 0
        max_question = len(question)

        for num, solution in enumerate(self.solutions):
            # -- direct match --
            if solution == question:
                final_solution = solution
                to_delete = num
                break
            # -- no direct match, then look for similar text --
            ratio = jellyfish.jaro_similarity(solution[0:max_question], question[0:max_question])
            possible_solutions.append({
                    'solution': solution,
                    'ratio': ratio,
                    'num': num
                })
        # -- sort solutions by most similar text grade found --
        possible_solutions = sorted(possible_solutions, key=itemgetter('ratio'), reverse=True)

        # -- no solution found --
        if len(possible_solutions) > 0 and final_solution == "":
            final_solution = possible_solutions[0]['solution']
            to_delete = possible_solutions[0]['num']

        # -- delete item in solutions list --
        if to_delete != 0:
            self.solutions.pop(to_delete)

        return final_solution

    # -- enumerate answers from the question block --
    def enumerate_answers(self, text: str) -> str:
        new_text = ""
        answer = 1

        for line in text.split("\n"):
            if r"O " in line[0:2] or r"© " in line[0:2] or r"oO " in line[0:3] or r"O© " in line[0:3] \
                    or r"C© " in line[0:3] or r"CO " in line[0:3]:
                newline = line
                # -- enumerate questions --
                newline = newline.replace("O ", "\n"+str(answer)+".- ")
                newline = newline.replace("oO ", "\n"+str(answer)+".- ")
                newline = newline.replace("O© ", "\n"+str(answer)+".- ")
                newline = newline.replace("C© ", "\n"+str(answer)+".- ")
                newline = newline.replace("CO ", "\n"+str(answer)+".- ")
                newline = newline.replace("© ", "\n"+str(answer)+".- ")
                answer += 1
                new_text += newline + "\n\n"
            else:
                new_text += line + "\n"

        return new_text

    # -- Main function to clean text and show the question block with solutions --
    def main(self, text: str) -> str:
        """
        Main function to show question block with the main solution

        :param text: str
        :return: str
        """
        new_text = ""
        question_block = ""

        original_text = "QUESTION:\n"+text

        # -- remove all empty lines and trash, isolate question and enumerate answers --
        text = self.remove_empty_lines(text)
        text = self.remove_trash_lines(text)
        question_block = self.get_query_block(text)
        question = self.get_question_block(question_block)
        question_block = self.enumerate_answers(question_block)
        new_text = "QUESTION:\n"+question_block

        # -- if filtered text fails, show all OCR result text --
        if len(new_text) < 15:
            print("*** WARNING! Processed text is empty, showing raw text instead! ***")
            new_text = original_text
            question_block = original_text

        # -- search the answer and show --
        if self.solution_file != "":
            answer = self.search_solution(question)
            new_text += "SOLUTION:\n"
            if len(answer) == 0:
                new_text += "** NO SOLUTION FOUND! **\n"
            else:
                new_text += answer + "\n"
        else:
            new_text += "** NO SOLUTION FILE PROVIDED! **\n"
            new_text += "===========================================\n\n"

        print(new_text)

        # -- get IA answer --
        ia_answer = ia.query(question_block, "")
        new_text += ia_answer

        return new_text
