import numpy as np
from pathlib import Path

from image import Image
from pattern_composer import PatternComposer

SVG_UNIT_SIZE = 10
BACKGROUND_INDEX = 99  # must be between n_colors and 255 inclusive since pattern is uint8


class Pattern:

    background_wo_symbols = True

    def __init__(self, color: bool=True, symbols: bool=True) -> None:
        """Init object"""
        self.color = color
        self.symbols = symbols
        self.dmc_palette = None
        self.width = 0
        self.height = 0
        self.pattern_composer = PatternComposer(color, symbols)

    def process_image(self, img_file: Path, n_colors: int, stitches_per_row: int, method: str) -> None:
        """Create image, process it (resize, pixelate, quantize), then get palette and pattern"""
        image = Image(img_file)
        self.dmc_palette, self.dmc_pattern = image.process(n_colors, stitches_per_row, method)
        self.width = self.dmc_pattern.shape[1]
        self.height = self.dmc_pattern.shape[0]
    
    def generate(self):
        """Generate SVG info"""
        width = (self.width+1) * SVG_UNIT_SIZE  # +1 because of outer margin
        height = (self.height+1) * SVG_UNIT_SIZE
        self.pattern_composer.add_header(width, height)
        if self.background_wo_symbols:
            self._set_background_index()
        for y_idx, row in enumerate(self.dmc_pattern):  # TODO: these loops take a long time for stitches_per_row > 100
            y_pos = (y_idx+1) * SVG_UNIT_SIZE  # +1 allows space for midpoint arrows
            for x_idx, c_idx in enumerate(row):
                x_pos = (x_idx+1) * SVG_UNIT_SIZE
                self.pattern_composer.add_color(self.dmc_palette, c_idx, x_pos, y_pos, SVG_UNIT_SIZE)
                if self.symbols:
                    self.pattern_composer.add_symbol(c_idx, x_pos, y_pos, SVG_UNIT_SIZE)
        self.pattern_composer.add_grids(SVG_UNIT_SIZE, width, height)
        self.pattern_composer.add_numbers(SVG_UNIT_SIZE, width, height)
        self.pattern_composer.add_arrows(SVG_UNIT_SIZE, width, height)
        self.pattern_composer.add_tail()

    def _set_background_index(self) -> None:
        """Set color index of background to special index, also reduce in 1 indexes bigger than original 
        background index so symbols can be reused"""
        background_idx = self._get_background_idx()
        color_idxs = self.dmc_palette.keys()
        for c_idx in color_idxs:
            if c_idx == background_idx:
                # change bkgd idx in pattern and palette
                self.dmc_pattern[self.dmc_pattern==background_idx] = BACKGROUND_INDEX  # change idx in pattern
                self.dmc_palette[BACKGROUND_INDEX] = self.dmc_palette.pop(background_idx)  # change idx in palette
            elif c_idx > background_idx:
                # reduce idx in 1 for idx bigger than bkgd idx
                self.dmc_pattern[self.dmc_pattern==c_idx] = c_idx - 1
                self.dmc_palette[c_idx-1] = self.dmc_palette.pop(c_idx)

    def _get_background_idx(self) -> int:
        """Get index representing background (check 4 corners, if they match it is the background idx)"""
        idx = [
            self.dmc_pattern[0, 0],
            self.dmc_pattern[self.height-1, 0],
            self.dmc_pattern[0, self.width-1],
            self.dmc_pattern[self.height-1, self.width-1],
        ]
        return int(idx[0]) if idx.count(idx[0]) == 4 else None  # same color in all corners?

    def save(self, out_file: Path, formats: list[str]=['pdf'], png_scale: float=1.0) -> None:
        self.pattern_composer.save(out_file, formats, png_scale)