from typing import Any, Iterator
import pytest
import builtins

from condition import Condition


class TestCondition:
    """Tests for the Condition class.

    Attributes:
        condition:
            An instance of the Condition class.

    Methods:
        test_get_avg_condition:
            Tests the 'get_avg_condition' method of the Condition class.
        test_is_valid_indicator:
            Tests the 'is_valid_indicator' method of the Condition class.
        test_get_indicator:
            Tests the 'get_indicator' method of the Condition class.
        new_condition:
            Fixture method that returns a new instance of the Condition class.
        test_set_condition:
            Tests the 'set_condition' method of the Condition class.
    """

    condition: Condition = Condition()

    @pytest.mark.parametrize(
            'r, hr, bl, pd, count, expected',
            [
                (
                    10, 10, 10, 10, 2,
                    {
                        'respiration': 10 / 2,
                        'heart rate': 10 / 2,
                        'blushing level': 10 / 2,
                        'pupillaty dilation': 10 / 2,
                    },
                ),
                (
                    100, 100, 100, 100, 50,
                    {
                        'respiration': 100 / 50,
                        'heart rate': 100 / 50,
                        'blushing level': 100 / 50,
                        'pupillaty dilation': 100 / 50,
                    },
                ),
            ]
    )
    def test_get_avg_condition(
        self,
        r: int,
        hr: int,
        bl: int,
        pd: int,
        count: int,
        expected: dict[str, float]
    ) -> None:
        """Test the 'get_avg_condition' method of the Condition class.

        Args:
            r (int):
                    Respiration value.
            hr (int):
                    Heart rate value.
            bl (int):
                    Blushing level value.
            pd (int):
                    Pupillary dilation value.
            count (int):
                    Count value.
            expected (dict):
                    Expected average values.
        """
        self.condition.respiration = r
        self.condition.heart_rate = hr
        self.condition.blushing_level = bl
        self.condition.pupillary_dilation = pd
        self.condition.count = count
        assert self.condition.get_avg_condition() == expected

    @pytest.mark.parametrize(
        'indicator, min_value, max_value, expected',
        [
            (10, 3, 30, True),
            (20, 3, 13, False),
            ('40', 0, 100, True),
            (44.4, 4, 400, True),
            ('12', 1, 10, False),
        ]
    )
    def test_is_valid_indicator(
        self,
        indicator: Any,
        min_value: int,
        max_value: int,
        expected: bool
    ) -> None:
        """Test the 'is_valid_indicator' method of the Condition class.

        Args:
            indicator (Any):
                Indicator value.
            min_value (int):
                Minimum valid value.
            max_value (int):
                Maximum valid value.
            expected (bool):
                Expected result.
        """
        assert self.condition.is_valid_indicator(
            indicator,
            min_value,
            max_value
        ) == expected

    @pytest.mark.parametrize(
            'min_value, max_value, text, _input, expected',
            [
                (0, 100, 'some text', '1', 1.0),
                (50, 200, 'some text 2', '54.4', 54.4),
            ]
    )
    def test_get_indiccator(
        self,
        min_value: int,
        max_value: int,
        text: str,
        _input: str,
        expected: float,
        monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test the 'get_indicator' method of the Condition class.

        Args:
            min_value (int):
                Minimum valid value.
            max_value (int):
                Maximum valid value.
            text (str):
                Text prompt.
            _input (str):
                Input value.
            expected (float):
                Expected result.
            monkeypatch (pytest.MonkeyPatch):
                Pytest fixture for monkeypatching.
        """
        monkeypatch.setattr(builtins, 'input', lambda _: _input)
        assert self.condition.get_indicator(
            min_value,
            max_value,
            text
        ) == expected

    @pytest.fixture
    def new_condition(self) -> Condition:
        """Fixture method that returns a new instance of the Condition class.

        Returns:
            Condition:
                A new instance of the Condition class.
        """
        return Condition()

    @pytest.mark.parametrize(
        '_input',
        [
            (['10', '10', '5', '2']),
            (['a', '10', 'b', '10', '10', '5', '10', '2']),
        ]
    )
    def test_set_condition(
        self,
        _input: list[str],
        monkeypatch: pytest.MonkeyPatch,
        new_condition: Condition
    ) -> None:
        """Test the 'set_condition' method of the Condition class.

        Args:
            _input (list[str]):
                List of input values.
            monkeypatch (pytest.MonkeyPatch):
                Pytest fixture for monkeypatching.
            new_condition (Condition):
                A new instance of the Condition class.
        """
        responses: Iterator[str] = iter(_input)
        monkeypatch.setattr(builtins, 'input', lambda _: next(responses))
        new_condition.set_condition()
        assert (
            new_condition.respiration == 10
            and new_condition.heart_rate == 10
            and new_condition.blushing_level == 5
            and new_condition.pupillary_dilation == 2
            and new_condition.count == 1
        )
