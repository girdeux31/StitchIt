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

    def __init__(self, pattern: np.ndarray[int], palette: dict[int, dict[str, str | tuple]]) -> None:
        """Init object"""
        self.pattern = pattern
        self.palette = palette
        self.backstitches = []
        self._add_backstitch_color_to_palette(BACKSTITCH_DMC_CODE)

    def detect(self) -> list[Backstitch]:
        """
        Detect potential backstitches, it performs two passes:
        first horizontally to dectect vertical backstitches,
        then vertically to dectect horizontal backstitches, 
        """
        self._scann_horizontally()
        self._scann_vertically()
        return self.backstitches

    def _scann_horizontally(self) -> None:
        """Scann horizontally for vertical backstitches"""
        for y_idx in range(self.pattern.shape[0]):
            for x_idx in range(self.pattern.shape[1]-1):
                mask = self.pattern[y_idx, x_idx:x_idx+2]
                if len(np.unique(mask)) == 2 and any(mask==BACKGROUND_INDEX):  # two different colors and one is bg
                    start = (x_idx+1, y_idx)
                    end = (x_idx+1, y_idx+1)
                    c_info = self._get_backstitch_color()
                    self._add_backstitch(start, end, c_info)

    def _scann_vertically(self) -> None:
        """Scann vertically for horizontal backstitches"""
        for y_idx in range(self.pattern.shape[0]-1):
            for x_idx in range(self.pattern.shape[1]):
                mask = self.pattern[y_idx:y_idx+2, x_idx]
                if len(np.unique(mask)) == 2 and any(mask==BACKGROUND_INDEX):  # two different colors and one is bg
                    start = (x_idx, y_idx+1)
                    end = (x_idx+1, y_idx+1)
                    c_info = self._get_backstitch_color()
                    self._add_backstitch(start, end, c_info)

    def _add_backstitch_color_to_palette(self, code: str | int) -> None:
        """Add backstitch color to palete by dmc code"""
        dmc = DMC()
        self.palette[100] = dmc.get_color_by_code(str(code))
        self.palette[100]['code'] = code

    def _get_backstitch_color(self) -> dict[str, str | tuple]:
        """Get color info for backstitch"""
        c_idx = 0
        return self.palette[100+c_idx]

    def _add_backstitch(self, start: tuple[int], end: tuple[int], c_info: dict[str, str | tuple]) -> None:
        """Create backstitch and append to list"""
        bs = Backstitch(start, end, c_info['rgb'])
        self.backstitches.append(bs)
