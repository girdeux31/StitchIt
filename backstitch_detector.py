import numpy as np

from dataclasses import dataclass
from dmc import DMC


BACKSTITCH_DMC_CODE = 498
BACKGROUND_INDEX = 99

@dataclass
class Backstitch:
    start: tuple[int, int]
    end: tuple[int, int]
    color: tuple[int, int, int]

class BackstitchDetector:

    def __init__(self, pattern: np.ndarray[int]) -> None:
        """Init object"""
        self.pattern = pattern
        self.backstitches = []
        self.palette = self._get_backstitch_color_info()

    def _get_backstitch_color_info(self) -> dict[str, str | tuple[int]]:
        """Get color info from DMC database"""
        dmc = DMC()
        return dmc.get_color_by_code(BACKSTITCH_DMC_CODE)

    def detect(self) -> list[Backstitch]:
        """
        Detect potential backstitches, it performs two passes:
        first horizontally to dectect vertical backstitches,
        then vertically to dectect horizontal backstitches, 
        """
        self._detect_vertical_backstitches()
        self._detect_horizontal_backstitches()
        return self.backstitches

    def _detect_vertical_backstitches(self) -> None:
        """Scann horizontally for vertical backstitches"""
        for y_idx, row in enumerate(self.pattern):
            for x_idx in range(len(row[:-1])):
                mask = self.pattern[y_idx, x_idx:x_idx+2]
                if len(np.unique(mask)) == 2 and any(mask==BACKGROUND_INDEX):  # two different colors and one is bg
                    start = (x_idx+1, y_idx)
                    end = (x_idx+1, y_idx+1)
                    self._add_backstitch(start, end)

    def _detect_horizontal_backstitches(self) -> None:
        """Scann vertically for horizontal backstitches"""
        for y_idx, row in enumerate(np.transpose(self.pattern)):
            for x_idx in range(len(row[:-1])):
                mask = self.pattern[y_idx:y_idx+2, x_idx]
                if len(np.unique(mask)) == 2 and any(mask==BACKGROUND_INDEX):  # two different colors and one is bg
                    start = (x_idx, y_idx+1)
                    end = (x_idx+1, y_idx+1)
                    self._add_backstitch(start, end)

    def _add_backstitch(self, start: tuple[int], end: tuple[int]) -> None:
        """Create backstitch and append to list"""
        color = self.palette['rgb']
        bs = Backstitch(start, end, color)
        self.backstitches.append(bs)


