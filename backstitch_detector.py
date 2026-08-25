import numpy as np

from dataclasses import dataclass

from palette import Palette, DMCColor


BACKSTITCH_DMC_CODE = 498  # red
BACKSTITCH_DMC_CODE_NO_COLOR = 310  # black
BACKSTITCH_INDEX = 100  # TODO refactor?

@dataclass
class Backstitch:
    start: tuple[int, int]
    end: tuple[int, int]
    color: DMCColor

class BackstitchDetector:

    def __init__(self, pattern: np.ndarray[int], palette: Palette, bg_idx: int, show_colors: bool=True) -> None:
        """Init object"""
        self.pattern = pattern
        self.palette = palette
        self.bg_idx = bg_idx
        self.show_colors = show_colors
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
                if len(np.unique(mask)) == 2 and any(mask==self.bg_idx):  # two different colors and one is bg
                    start = (x_idx+1, y_idx)
                    end = (x_idx+1, y_idx+1)
                    color = self.palette.get_color_by_idx(BACKSTITCH_INDEX)
                    self._add_backstitch(start, end, color)

    def _scann_vertically(self) -> None:
        """Scann vertically for horizontal backstitches"""
        for y_idx in range(self.pattern.shape[0]-1):
            for x_idx in range(self.pattern.shape[1]):
                mask = self.pattern[y_idx:y_idx+2, x_idx]
                if len(np.unique(mask)) == 2 and any(mask==self.bg_idx):  # two different colors and one is bg
                    start = (x_idx, y_idx+1)
                    end = (x_idx+1, y_idx+1)
                    color = self.palette.get_color_by_idx(BACKSTITCH_INDEX)
                    self._add_backstitch(start, end, color)

    def _add_backstitch_color_to_palette(self, code: str | int) -> None:
        """Add backstitch color to palete by dmc code"""
        code = BACKSTITCH_DMC_CODE if self.show_colors is True else BACKSTITCH_DMC_CODE_NO_COLOR
        self.palette.add_color_by_code(BACKSTITCH_INDEX, code, is_backstitch=True)

    def _add_backstitch(self, start: tuple[int], end: tuple[int], color: DMCColor) -> None:
        """Create backstitch and append to list"""
        bs = Backstitch(start, end, color)
        self.backstitches.append(bs)
