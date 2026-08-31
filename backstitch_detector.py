import numpy as np

from palette import DMCColor
from data_classes import Backstitch
from constants import BACKSTITCH_INDEX


class BackstitchDetector:

    def __init__(self, pattern):
        """Init object"""
        self.pattern = pattern
        self.backstitches = []
        self._add_backstitch_color_to_palette()

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
        for y_idx in range(self.pattern.array.shape[0]):
            for x_idx in range(self.pattern.array.shape[1]-1):
                mask = self.pattern.array[y_idx, x_idx:x_idx+2]
                if len(np.unique(mask)) == 2 and any(mask==self.pattern.bg_idx):  # two different colors and one is bg
                    start = (x_idx+1, y_idx)
                    end = (x_idx+1, y_idx+1)
                    color = self.pattern.palette.get_color_by_idx(BACKSTITCH_INDEX)
                    self._add_backstitch(start, end, color)

    def _scann_vertically(self) -> None:
        """Scann vertically for horizontal backstitches"""
        for y_idx in range(self.pattern.array.shape[0]-1):
            for x_idx in range(self.pattern.array.shape[1]):
                mask = self.pattern.array[y_idx:y_idx+2, x_idx]
                if len(np.unique(mask)) == 2 and any(mask==self.pattern.bg_idx):  # two different colors and one is bg
                    start = (x_idx, y_idx+1)
                    end = (x_idx+1, y_idx+1)
                    color = self.pattern.palette.get_color_by_idx(BACKSTITCH_INDEX)
                    self._add_backstitch(start, end, color)

    def _add_backstitch_color_to_palette(self) -> None:
        """Add backstitch color to palete by dmc code"""
        if self.pattern.general_config.show_colors is True:
            code = self.pattern.other_config.backstitch_code
        else:
            code = self.patter.other_config.backstitch_code_no_colors
        self.pattern.palette.add_color_by_code(BACKSTITCH_INDEX, code, is_backstitch=True)

    def _add_backstitch(self, start: tuple[int], end: tuple[int], color: DMCColor) -> None:
        """Create backstitch and append to list"""
        bs = Backstitch(start, end, color)
        self.backstitches.append(bs)
