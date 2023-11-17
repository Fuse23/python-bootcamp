from condition import Condition
from validator import Validator
from constants.constants import (
    POSITIVE_RESULT,
    NEGATIVE_RESULT,
    ANSWER_TEXT,
    INCORRECT_ANSWER,
)

import json


class VoightKampff:
    """Voight-Kampff test implementation for assessing empathy levels.

    This class represents a simplified version of the Voight-Kampff test,
    a fictional test from the Blade Runner universe used to distinguish between
    humans and replicants based on emotional responses.

    Args:
        path_to_file (str):
            The path to the JSON file containing the test questions
            and options.

    Attributes:
        file (str):
            The path to the JSON file.
        validator (Validator):
            An instance of the Validator class for input validation.
        condition (Condition):
            An instance of the Condition class for tracking test conditions.
        answers (list[int]):
            A list to store user answers to the test questions.

    Methods:
        get_questions() -> dict | None:
            Load and return the questions and options from the JSON file.

        get_answer(count_answers: int) -> None:
            Get and validate user input for a single test question.

        ask_question(question: dict) -> None:
            Display the question and options to the user.

        calculate_result() -> bool:
            Calculate the test result based on user answers and test
            conditions.

        show_result(result: bool) -> None:
            Display the test result.

        run() -> None:
            Execute the Voight-Kampff test by interacting with the user,
            collecting answers, and displaying the final result.
    """

    def __init__(self, path_to_file: str) -> None:
        """Initialize the VoightKampff instance.

        Args:
            path_to_file (str):
                The path to the JSON file containing the test questions
                and options.
        """
        self.file: str = path_to_file
        self.validator: Validator = Validator()
        self.condition: Condition = Condition()
        self.answers: list[int] = []

    def get_questions(self) -> dict | None:
        """Load and return the questions and options from the JSON file.

        Returns:
            dict | None:
                A dictionary containing test questions and options or None
                if the file is invalid.
        """
        if not self.validator.is_valid_file(self.file):
            return None
        with open(self.file, 'r') as file:
            return json.load(file)

    def get_answer(self, count_answers: int) -> None:
        """Get and validate user input for a single test question.

        Args:
            count_answers (int):
                The number of options for the current question.
        """
        answer: str = input(ANSWER_TEXT + f'1 to {count_answers}: ')
        while not self.validator.is_valid_answer(answer, count_answers):
            answer = input(INCORRECT_ANSWER + f'1 to {count_answers}: ')
        self.answers.append(int(answer) - 1)

    def ask_question(self, question: dict) -> None:
        """Display the question and options to the user.

        Args:
            question (dict):
                A dictionary containing the current test question and options.
        """
        print(question['question'])
        for count, option in enumerate(question['options'], start=1):
            print(f'{count}. {option}')

    def calculate_result(self) -> bool:
        """Calculate the test result based on user answers and test conditions.

        Returns:
            bool:
                True if the test result is positive, False otherwise.
        """
        avg_condition: dict[str, float] = self.condition.get_avg_condition()
        if (
            0 <= sum(self.answers) <= 4
            and 12 < avg_condition['respiration'] < 16
            and 60 < avg_condition['heart rate'] < 100
            and avg_condition['blushing level'] < 4
            and avg_condition['pupillaty dilation'] > 4
        ):
            return True
        return False

    def show_result(self, result: bool) -> None:
        """Display the test result.

        Args:
            result (bool):
                The test result to be displayed.
        """
        print(POSITIVE_RESULT) if result else print(NEGATIVE_RESULT)

    def run(self) -> None:
        """Execute the Voight-Kampff test.

        Interact with the user, collect answers, calculate the result,
        and display the final result.
        """
        questions: dict | None = self.get_questions()
        if not questions:
            return
        for question in questions['questions']:
            self.ask_question(question)
            self.get_answer(len(question['options']))
            self.condition.set_condition()
        self.show_result(self.calculate_result())
