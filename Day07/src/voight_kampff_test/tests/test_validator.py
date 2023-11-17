from typing import Any
import pytest
import os

from validator import Validator


class TestValidator:
    """Tests for the Validator class.

    Attributes:
        validator (Validator):
            An instance of the Validator class used for testing.

    Methods:
        test_is_file_exists:
            Tests the 'is_file_exist' method of the 'Validator' class.
        test_is_json:
            Tests the 'is_json' method of the 'Validator' class.
        test_is_valid_answer:
            Tests the 'is_valid_answer' method of the 'Validator' class.
        test_is_valid_options:
            Tests the 'is_valid_options' method of the 'Validator' class.
        test_is_valid_question:
            Tests the 'is_valid_question' method of the 'Validator' class.
        test_is_valid_structure:
            Tests the 'is_valid_structure' method of the 'Validator' class.
        test_is_valid_file:
            Tests the 'is_valid_file' method of the 'Validator' class.
    """

    validator: Validator = Validator()

    @pytest.mark.parametrize(
            'path, expected',
            [
                (os.path.join(os.path.dirname(__file__), ''),
                    False),
                (os.path.join(os.path.dirname(__file__), 'aaaa'),
                    False),
                (os.path.join(os.path.dirname(__file__), 'test_validator.py'),
                    True),
                (os.path.join(os.path.dirname(__file__), 'test_files/10.json'),
                    True),
                (os.path.join(os.path.dirname(__file__), 'test_files/4.json'),
                    True),
                (os.path.join(os.path.dirname(__file__), 'files/0.json'),
                    False),
                (
                    os.path.join(
                        os.path.dirname(__file__), 'test_files/file.json'
                    ),
                    False
                ),
            ]
    )
    def test_is_file_exists(self, path: str, expected: bool) -> None:
        """Tests the 'is_file_exist' method of the 'Validator' class.

        Args:
            path (str):
                The path to the file.
            expected (bool):
                The expected result of the test.
        """
        assert self.validator.is_file_exist(path) == expected

    @pytest.mark.parametrize(
            'path, expected',
            [
                ('', False),
                ('file.js', False),
                ('./test_validator.py', False),
                ('file/1.json', True),
                ('./file/11.json', True),
            ]
    )
    def test_is_json(self, path: str, expected: bool) -> None:
        """Tests the 'is_json' method of the 'Validator' class.

        Args:
            path (str):
                The path to the file.
            expected (bool):
                The expected result of the test.
        """
        assert self.validator.is_json(path) == expected

    @pytest.mark.parametrize(
            'answer, len_options, expected',
            [
                (1, 3, True),
                (2, 3, True),
                (3, 3, True),
                (4, 4, True),
                ('1', 3, True),
                (10, 5, False),
                ('9', 5, False),
                ([2], 2, False),
                ({4}, 10, False),
                (['2'], 4, False),
                ('5', 5, True),
            ]
    )
    def test_is_valid_answer(
        self,
        answer: Any,
        len_options: int,
        expected: bool
    ) -> None:
        """Tests the 'is_valid_answer' method of the 'Validator' class.

        Args:
            answer (Any):
                The answer to be validated.
            len_options (int):
                The length of the options.
            expected (bool):
                The expected result of the test.
        """
        assert self.validator.is_valid_answer(answer, len_options) == expected

    @pytest.mark.parametrize(
            'option, expected',
            [
                (['a', 'a', 'a', 'a'], True),
                (['a', 'a', 'a'], True),
                ([1, 2, 3, 4], False),
                (['aa', 'aa'], False),
                ([True, True, True], False),
                ({1: 'a', 2: 'b', 3: 'c'}, False),
                (['a', 'b', 'c', 'd', 'f'], False),
                (['a', 'b', 3], False),
                ('a b c', False),
            ]
    )
    def test_is_valid_options(
        self,
        option: list[Any] | dict[int, str] | str,
        expected: bool
    ) -> None:
        """Tests the 'is_valid_options' method of the 'Validator' class.

        Args:
            option (list[Any] | dict[int, str] | str):
                The option to be validated.
            expected (bool):
                The expected result of the test.
        """
        assert self.validator.is_valid_option(option) == expected

    @pytest.mark.parametrize(
            'question, expected',
            [
                (
                    {
                        'question': 'some question',
                        'options': ['first', 'second', 'third'],
                        'correct_answer': 1,
                    },
                    True,
                ),
                (
                    {
                        'options': ['first', 'second', 'third'],
                        'correct_answer': 1,
                    },
                    False,
                ),
                (
                    {
                        'question': 'some question',
                        'options': ['first', 'second', 'third'],
                    },
                    False,
                ),
                (
                    {
                        'question': 'some question',
                        'correct_answer': 1,
                    },
                    False,
                ),
                (
                    {
                        'options': 'some question',
                        'questions': ['first', 'second', 'third'],
                        'correct_answer': 1,
                    },
                    False,
                )
            ]
    )
    def test_is_valid_question(self, question: dict, expected: bool) -> None:
        """Tests the 'is_valid_question' method of the 'Validator' class.

        Args:
            question (dict):
                The question to be validated.
            expected (bool):
                The expected result of the test.
        """
        assert self.validator.is_valid_question(question) == expected

    @pytest.mark.parametrize(
            'data, expected',
            [
                (
                    {
                        'questions': [
                            {
                                'question': 'some question',
                                'options': ['first', 'second', 'third'],
                                'correct_answer': 1,
                            } for _ in range(10)
                        ]
                    },
                    True,
                ),
                (
                    {
                        'questions': [
                            {
                                'question': 'some question',
                                'options': ['first', 'second', 'third'],
                                'correct_answer': 5,
                            } for _ in range(10)
                        ]
                    },
                    False,
                ),
                (
                    {
                        'questions': [
                            {
                                'question': 'some question',
                                'options': ['first', 'second', 'third'],
                                'correct_answer': 1,
                            } for _ in range(8)
                        ]
                    },
                    False,
                ),
                (
                    [{
                        'questions': [
                            {
                                'question': 'some question',
                                'options': ['first', 'second', 'third'],
                                'correct_answer': 1,
                            } for _ in range(10)
                        ]
                    }],
                    False,
                ),
                (
                    {
                        'options': [
                            {
                                'question': 'some question',
                                'options': ['first', 'second', 'third'],
                                'correct_answer': 1,
                            } for _ in range(10)
                        ]
                    },
                    False,
                ),
            ]
    )
    def test_is_valid_stucture(self, data: dict, expected: bool) -> None:
        """Tests the 'is_valid_structure' method of the 'Validator' class.

        Args:
            data (dict):
                The data structure to be validated.
            expected (bool):
                The expected result of the test.
        """
        assert self.validator.is_valid_structure(data) == expected

    @pytest.mark.parametrize(
        'path, expected',
        [
            (os.path.join(os.path.dirname(__file__), 'test_files/1.json'),
                False),
            (os.path.join(os.path.dirname(__file__), 'test_files/2.json'),
                False),
            (os.path.join(os.path.dirname(__file__), 'test_files/3.json'),
                False),
            (os.path.join(os.path.dirname(__file__), 'test_files/4.json'),
                False),
            (os.path.join(os.path.dirname(__file__), 'test_files/5.json'),
                False),
            (os.path.join(os.path.dirname(__file__), 'test_files/6.json'),
                False),
            (os.path.join(os.path.dirname(__file__), 'test_files/7.json'),
                False),
            (os.path.join(os.path.dirname(__file__), 'test_files/8.json'),
                False),
            (os.path.join(os.path.dirname(__file__), 'test_files/9.json'),
                False),
            (os.path.join(os.path.dirname(__file__), 'test_files/10.json'),
                False),
            (os.path.join(os.path.dirname(__file__), 'test_files/11.json'),
                True),
            (os.path.join(os.path.dirname(__file__), 'test_files/12.json'),
                False),
            (os.path.join(os.path.dirname(__file__), 'test_validator.py'),
                False),
        ]
    )
    def test_is_valid_file(self, path: str, expected: bool) -> None:
        """Tests the 'is_valid_file' method of the 'Validator' class.

        Args:
            path (str):
                The path to the file.
            expected (bool):
                The expected result of the test.
        """
        assert self.validator.is_valid_file(path) == expected
