from constants.constants import (
    RESPIRATION_MIN,
    RESPIRATION_MAX,
    RESPIRATION_TEXT,
    HEART_RATE_MIN,
    HEART_RATE_MAX,
    HEART_RATE_TEXT,
    BLUSHING_LEVEL_MIN,
    BLUSHING_LEVEL_MAX,
    BLASHING_LEVEL_TEXT,
    PUPILLARY_DILATIOIN_MIN,
    PUPILLARY_DILATIOIN_MAX,
    PUPILLARY_DILATIOIN_TEXT,
)


class Condition:
    """Physiological conditions and their indicators.

    Attributes:
        respiration (float):
            The cumulative respiration value.
        heart_rate (float):
            The cumulative heart rate value.
        blushing_level (float):
            The cumulative blushing level value.
        pupillary_dilation (float):
            The cumulative pupillary dilation value.
        count (int):
            The count of recorded conditions.

    Methods:
        - get_avg_condition() -> dict:
            Calculates and returns the average values of respiration,
            heart rate, blushing level, and pupillary dilation.
        - set_condition() -> None:
            Collects user input for physiological indicators
            and updates cumulative values.
        - is_valid_indicator(indicator: str, min_value: int,
                           max_value: int) -> bool:
            Validates if the given indicator is within the specified range.
        - get_indicator(min_value: int, max_value: int, text: str) -> float:
            Prompts the user for an indicator input, validates it,
            and returns the indicator as a float.
    """

    def __init__(self) -> None:
        """Initializes a Condition object with default attribute values.

        """
        self.respiration: float = 0
        self.heart_rate: float = 0
        self.blushing_level: float = 0
        self.pupillary_dilation: float = 0
        self.count: int = 0

    def get_avg_condition(self) -> dict[str, float]:
        """Calculates and returns the average values of respiration,
        heart rate, blushing level, and pupillary dilation.

        Returns:
            dict:
                A dictionary containing average values for each physiological
                indicator.
        """
        return {
            'respiration': self.respiration / self.count,
            'heart rate': self.heart_rate / self.count,
            'blushing level': self.blushing_level / self.count,
            'pupillaty dilation': self.pupillary_dilation / self.count,
        }

    def set_condition(self) -> None:
        """Collects user input for physiological indicators,
        validates the input, and updates cumulative values.
        """
        self.count += 1
        self.respiration += self.get_indicator(
            RESPIRATION_MIN,
            RESPIRATION_MAX,
            RESPIRATION_TEXT,
        )
        self.heart_rate += self.get_indicator(
            HEART_RATE_MIN,
            HEART_RATE_MAX,
            HEART_RATE_TEXT,
        )
        self.blushing_level += self.get_indicator(
            BLUSHING_LEVEL_MIN,
            BLUSHING_LEVEL_MAX,
            BLASHING_LEVEL_TEXT,
        )
        self.pupillary_dilation += self.get_indicator(
            PUPILLARY_DILATIOIN_MIN,
            PUPILLARY_DILATIOIN_MAX,
            PUPILLARY_DILATIOIN_TEXT,
        )

    def is_valid_indicator(
        self,
        indicator: str,
        min_value: int,
        max_value: int
    ) -> bool:
        """Validates if the given indicator is within the specified range.

        Args:
            indicator (str):
                The input value to be validated.
            min_value (int):
                The minimum acceptable value.
            max_value (int):
                The maximum acceptable value.

        Returns:
            bool:
                True if the indicator is valid, False otherwise.
        """
        try:
            indicator_f: float = float(indicator)
            return indicator_f >= min_value and indicator_f <= max_value
        except ValueError:
            return False

    def get_indicator(
        self,
        min_value: int,
        max_value: int,
        text: str
    ) -> float:
        """Prompts the user for an indicator input, validates it,
        and returns the indicator as a float.

        Args:
            min_value (int):
                The minimum acceptable value.
            max_value (int):
                The maximum acceptable value.
            text (str):
                The prompt message for the user.

        Returns:
            float:
                The validated indicator value.
        """
        result: str = input(text)
        while not self.is_valid_indicator(result, min_value, max_value):
            result = input(text)
        return float(result)
