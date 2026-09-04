import numpy as np

from src.stitchit.color_tools import ColorTools
from src.stitchit.constants import (BACKGROUND_INDEX, BACKSTITCH_INDEX,
                                    INVERSE_BACKSTITCH_DELTA_INDEX)
from src.stitchit.data_classes import Backstitch, DMCColor


class BackstitchDetector:

    def __init__(self, pattern):
        """Init object"""
        self.pattern = pattern
        self.backstitches = []
        self._add_backstitch_colors_to_palette()

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
                    if self.pattern.other_config.backstitch_option == 'constant' or \
                        self.pattern.general_config.show_colors is False:
                        color = self.pattern.palette.get_color_by_idx(BACKSTITCH_INDEX)
                    else:  # inverse
                        dx = 1 if mask[0] == self.pattern.bg_idx else 0
                        c_idx = self.pattern.array[y_idx, x_idx+dx] + INVERSE_BACKSTITCH_DELTA_INDEX
                        color = self.pattern.palette.get_color_by_idx(c_idx)
                    self._add_backstitch(start, end, color)

    def _scann_vertically(self) -> None:
        """Scann vertically for horizontal backstitches"""
        for y_idx in range(self.pattern.array.shape[0]-1):
            for x_idx in range(self.pattern.array.shape[1]):
                mask = self.pattern.array[y_idx:y_idx+2, x_idx]
                if len(np.unique(mask)) == 2 and any(mask==self.pattern.bg_idx):  # two different colors and one is bg
                    start = (x_idx, y_idx+1)
                    end = (x_idx+1, y_idx+1)
                    if self.pattern.other_config.backstitch_option == 'constant' or \
                        self.pattern.general_config.show_colors is False:
                        color = self.pattern.palette.get_color_by_idx(BACKSTITCH_INDEX)
                    else:  # inverse
                        dy = 1 if mask[0] == self.pattern.bg_idx else 0
                        c_idx = self.pattern.array[y_idx+dy, x_idx] + INVERSE_BACKSTITCH_DELTA_INDEX
                        color = self.pattern.palette.get_color_by_idx(c_idx)
                    self._add_backstitch(start, end, color)

    def _add_backstitch_colors_to_palette(self) -> None:
        """Add backstitch color to palete by dmc code"""
        if self.pattern.general_config.show_colors is True:
            if self.pattern.other_config.backstitch_option == 'constant':
                code = self.pattern.other_config.backstitch_code
                self.pattern.palette.add_color_by_code(BACKSTITCH_INDEX, code, is_backstitch=True)
            else:  # inverse
                colors = [color for color in self.pattern.palette if color.idx != BACKGROUND_INDEX]
                for color in colors:  # warning: increasing list in loop of same list
                    inv_rgb = ColorTools.inverse_rgb(color.dmc_rgb)
                    self.pattern.palette.add_color_by_rgb(
                        color.idx+INVERSE_BACKSTITCH_DELTA_INDEX,
                        inv_rgb,
                        is_backstitch=True
                    )
        else:
            code = self.pattern.other_config.backstitch_code_no_colors
            self.pattern.palette.add_color_by_code(BACKSTITCH_INDEX, code, is_backstitch=True)

    def _add_backstitch(self, start: tuple[int], end: tuple[int], color: DMCColor) -> None:
        """Create backstitch and append to list"""
        bs = Backstitch(start, end, color)
        self.backstitches.append(bs)
