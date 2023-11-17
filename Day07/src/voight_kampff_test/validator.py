from constants.constants import (
    ERROR_FILE_NOT_EXISTS,
    ERROR_FILE_NOT_IS_JSON,
    ERROR_FILE_NOT_VALID,
)

import json
import os
from typing import Any


class Validator:
    """The Validator class provides methods for validating various aspects of
    files and data used in a question-and-answer application.

    Methods:
        is_file_exist(path: str) -> bool:
            Checks if a file exists at the specified path.
        is_json(path: str) -> bool:
            Checks if a file has a '.json' extension.
        is_valid_answer(answer: Any, len_option: int) -> bool:
            Checks if an answer is valid.
        is_valid_option(option: Any) -> bool:
            Checks if an option is a valid list of strings.
        is_valid_question(question: Any) -> bool:
            Checks if a question has a valid structure.
        is_valid_structure(data: Any) -> bool:
            Checks if data has a valid structure with at least 10 questions.
        is_valid_file(path: str) -> bool:
            Checks if a file is valid, exists, is in JSON format,
            and has a valid structure.
    """

    def is_file_exist(self, path: str) -> bool:
        """Checks if a file exists at the specified path.

        Args:
            path (str):
                The path to the file.

        Returns:
            bool:
                True if the file exists, False otherwise.
        """
        return os.path.isfile(path)

    def is_json(self, path: str) -> bool:
        """Checks if a file has a '.json' extension.

        Args:
            path (str):
                The path to the file.

        Returns:
            bool:
                True if the file has a '.json' extension, False otherwise.
        """
        return path.endswith('.json')

    def is_valid_answer(self, answer: Any, len_option: int) -> bool:
        """Checks if an answer is valid.

        Args:
            answer (Any):
                The answer to be validated.
            len_option (int):
                The length of the options list.

        Returns:
            bool:
                True if the answer is valid, False otherwise.
        """
        if isinstance(answer, str) and answer.isnumeric():
            answer = int(answer)
        return isinstance(answer, int) and 0 < answer <= len_option

    def is_valid_option(self, option: Any) -> bool:
        """Checks if an option is a valid list of strings.

        Args:
            option (Any):
                The option to be validated.

        Returns:
            bool:
                True if the option is valid, False otherwise.
        """
        if not isinstance(option, list) or not 3 <= len(option) <= 4:
            return False
        for op in option:
            if not isinstance(op, str):
                return False
        return True

    def is_valid_question(self, question: Any) -> bool:
        """Checks if a question has a valid structure.

        Args:
            question (Any):
                The question to be validated.

        Returns:
            bool:
                True if the question has a valid structure, False otherwise.
        """
        return (
            isinstance(question, dict)
            and 'question' in question
            and isinstance(question['question'], str)
            and 'options' in question
            and 'correct_answer' in question
            and self.is_valid_option(question['options'])
            and self.is_valid_answer(
                question['correct_answer'],
                len(question['options']) - 1,
            )
        )

    def is_valid_structure(self, data: Any) -> bool:
        """Checks if data has a valid structure with at least 10 questions.

        Args:
            data (Any):
                The data to be validated.

        Returns:
            bool:
                True if the data has a valid structure, False otherwise.
        """
        if (
            not isinstance(data, dict)
            or 'questions' not in data
            or not isinstance(data['questions'], list)
            or len(data['questions']) < 10
        ):
            return False
        for question in data['questions']:
            if not self.is_valid_question(question):
                return False
        return True

    def is_valid_file(self, path: str) -> bool:
        """Checks if a file is valid, exists, is in JSON format,
        and has a valid structure.

        Args:
            path (str):
                The path to the file.

        Returns:
            bool:
                True if the file is valid, False otherwise.
        """
        if not self.is_file_exist(path):
            print(ERROR_FILE_NOT_EXISTS)
            return False
        if not self.is_json(path):
            print(ERROR_FILE_NOT_IS_JSON)
            return False
        with open(path, 'r') as file:
            try:
                data: Any = json.load(file)
                if not self.is_valid_structure(data):
                    print(ERROR_FILE_NOT_VALID)
                    return False
            except json.JSONDecodeError as e:
                print(e)
                return False
        return True
