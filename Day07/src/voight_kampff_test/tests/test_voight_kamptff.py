import builtins
from typing import Iterator
import pytest
import os
import json

from voight_kampff import VoightKampff
from constants.constants import POSITIVE_RESULT, NEGATIVE_RESULT
import condition


PATH = os.path.join(os.path.dirname(__file__), 'test_files/11.json')
with open(PATH, 'r') as file:
    JSON = json.load(file)


class TestVoightKampff:
    """Tests for the VoightKampff class.

    Methods:
        - voight_kampff(self) -> VoightKampff:
            Fixture that returns an instance of VoightKampff using the default
            PATH.

        - get_voight_kampff(self,
                            request: pytest.FixtureRequest) -> VoightKampff:
            Fixture that returns an instance of VoightKampff using
            a parameterized file path.

        - test_get_questions(self, get_voight_kampff: VoightKampff,
                             expected: dict | None) -> None:
            Tests the get_questions method of VoightKampff.

        - test_get_answer(self, _input: list[str], count_answers: int,
                          expected: int, voight_kampff: VoightKampff,
                          monkeypatch: pytest.MonkeyPatch) -> None:
            Tests the get_answer method of VoightKampff.

        - test_ask_question(self, question: dict, voight_kampff: VoightKampff,
                            capsys: pytest.CaptureFixture[str]) -> None:
            Tests the ask_question method of VoightKampff.

        - test_calculate_result(self,
                            avg_condition: dict[str, int], answers: list[int],
                            expected: bool, voight_kampff: VoightKampff,
                            monkeypatch: pytest.MonkeyPatch) -> None:
            Tests the calculate_result method of VoightKampff.

        - test_show_result(self, result: bool, output: str,
                           voight_kampff: VoightKampff,
                           capsys: pytest.CaptureFixture[str]) -> None:
            Tests the show_result method of VoightKampff.
    """

    @pytest.fixture
    def voight_kampff(self) -> VoightKampff:
        """Fixture that returns an instance of VoightKampff using the default
        PATH.

        Returns:
            VoightKampff:
                An instance of the VoightKampff class.
        """
        return VoightKampff(PATH)

    @pytest.fixture
    def get_voight_kampff(
        self,
        request: pytest.FixtureRequest
    ) -> VoightKampff:
        """Fixture that returns an instance of VoightKampff using
        a parameterized file path.

        Args:
            request (pytest.FixtureRequest):
                The fixture request object.

        Returns:
            VoightKampff:
                An instance of the VoightKampff class.
        """
        return VoightKampff(request.param)

    @pytest.mark.parametrize(
        'get_voight_kampff, expected',
        [
            (os.path.join(os.path.dirname(__file__), 'test_files/1.json'),
                None),
            (os.path.join(os.path.dirname(__file__), 'test_files/2.json'),
                None),
            (os.path.join(os.path.dirname(__file__), 'test_files/3.json'),
                None),
            (os.path.join(os.path.dirname(__file__), 'test_files/4.json'),
                None),
            (os.path.join(os.path.dirname(__file__), 'test_files/5.json'),
                None),
            (os.path.join(os.path.dirname(__file__), 'test_files/6.json'),
                None),
            (os.path.join(os.path.dirname(__file__), 'test_files/7.json'),
                None),
            (os.path.join(os.path.dirname(__file__), 'test_files/8.json'),
                None),
            (os.path.join(os.path.dirname(__file__), 'test_files/9.json'),
                None),
            (os.path.join(os.path.dirname(__file__), 'test_files/10.json'),
                None),
            (PATH, JSON),
        ],
        indirect=['get_voight_kampff']
    )
    def test_get_questions(
        self,
        get_voight_kampff: VoightKampff,
        expected: dict | None
    ) -> None:
        """Tests the 'get_questions' method of VoightKampff.

        Args:
            get_voight_kampff (VoightKampff):
                An instance of the VoightKampffclass.
            expected (dict | None):
                The expected result from get_questions.
        """
        assert get_voight_kampff.get_questions() == expected

    @pytest.mark.parametrize(
            '_input, count_answers, expected',
            [
                (['1'], 4, 0),
                (['a', '20', '2'], 3, 1),
                (['skfn', 'slfiore324', 'fo249ejf', '3'], 3, 2),
            ]
    )
    def test_get_answer(
        self,
        _input: list[str],
        count_answers: int,
        expected: int,
        voight_kampff: VoightKampff,
        monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Tests the 'get_answer' method of VoightKampff.

        Args:
            _input (list[str]):
                List of simulated user inputs.
            count_answers (int):
                The count of expected answers.
            expected (int):
                The expected answer.
            voight_kampff (VoightKampff):
                An instance of the VoightKampff class.
            monkeypatch (pytest.MonkeyPatch):
                The monkeypatch fixture.
        """
        response: Iterator[str] = iter(_input)
        monkeypatch.setattr(builtins, 'input', lambda _: next(response))
        voight_kampff.get_answer(count_answers)
        assert voight_kampff.answers[-1] == expected

    @pytest.mark.parametrize(
            'question',
            [
                ({
                    "question":
                        "You find a wallet on the street. What do you do?",
                    "options": [
                        "Return it to the owner.",
                        "Keep it for yourself.",
                        "Leave it where you found it.",
                    ],
                    "correct_answer": 0,
                }),
                ({
                    "question":
                        "You find a wallet on the street. What do you do?",
                    "options": [
                        "Leave it where you found it.",
                        "Return it to the owner.",
                        "Keep it for yourself.",
                        "Leave it where you found it.",
                        "Return it to the owner.",
                    ],
                    "correct_answer": 0,
                }),
                ({
                    "question":
                        "You find a wallet on the street. What do you do?",
                    "options": [],
                    "correct_answer": 0,
                }),
                ({
                    "question": "",
                    "options": [],
                    "correct_answer": 0,
                }),
            ]
    )
    def test_ask_question(
        self,
        question: dict,
        voight_kampff: VoightKampff,
        capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Tests the 'ask_question' method of VoightKampff.

        Args:
            question (dict):
                The question dictionary.
            voight_kampff (VoightKampff):
                An instance of the VoightKampff class.
            capsys (pytest.CaptureFixture[str]):
                The capsys fixture.
        """
        voight_kampff.ask_question(question)
        captured = capsys.readouterr()
        assert question['question'] in captured.out
        for count, option in enumerate(question['options'], start=1):
            assert f'{count}. {option}' in captured.out

    @pytest.mark.parametrize(
            'avg_condition, answers, expected',
            [
                (
                    {
                        'respiration': 13,
                        'heart rate': 96,
                        'blushing level': 3,
                        'pupillaty dilation': 6,
                    },
                    [0, 0, 1, 1, 0, 1],
                    True,
                ),
                (
                    {
                        'respiration': 13,
                        'heart rate': 96,
                        'blushing level': 3,
                        'pupillaty dilation': 6,
                    },
                    [0, 0, 1, 1, 2, 1],
                    False,
                ),
                (
                    {
                        'respiration': 15,
                        'heart rate': 65,
                        'blushing level': 2,
                        'pupillaty dilation': 5,
                    },
                    [1, 0, 1, 0, 1, 1],
                    True,
                ),
                (
                    {
                        'respiration': 34,
                        'heart rate': 55,
                        'blushing level': 2,
                        'pupillaty dilation': 5,
                    },
                    [1, 0, 1, 0, 1, 1],
                    False,
                ),
            ]
    )
    def test_calculate_result(
        self,
        avg_condition: dict[str, int],
        answers: list[int],
        expected: bool,
        voight_kampff: VoightKampff,
        monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Tests the 'calculate_result' method of VoightKampff.

        Args:
            avg_condition (dict[str, int]):
                The average physiologicalcondition dictionary.
            answers (list[int]):
                List of user answers.
            expected (bool):
                The expected result.
            voight_kampff (VoightKampff):
                An instance of the VoightKampff class.
            monkeypatch (pytest.MonkeyPatch):
                The monkeypatch fixture.
        """
        monkeypatch.setattr(
            condition.Condition,
            'get_avg_condition',
            lambda _: avg_condition
        )
        voight_kampff.answers = answers
        assert voight_kampff.calculate_result() == expected

    @pytest.mark.parametrize(
            'result, output',
            [
                (True, POSITIVE_RESULT),
                (False, NEGATIVE_RESULT),
            ]
    )
    def test_show_result(
        self,
        result: bool,
        output: str,
        voight_kampff: VoightKampff,
        capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Tests the 'show_result' method of VoightKampff.

        Args:
            result (bool):
                The result to display.
            output (str):
                The expected output string.
            voight_kampff (VoightKampff):
                An instance of the VoightKampff class.
            capsys (pytest.CaptureFixture[str]):
                The capsys fixture.
        """
        voight_kampff.show_result(result)
        captured = capsys.readouterr()
        assert output in captured.out

    def test_run(self) -> None:
        pass
