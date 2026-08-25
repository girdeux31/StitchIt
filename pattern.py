import numpy as np
from pathlib import Path

from image import Image
from pattern_composer import PatternComposer
from backstitch_detector import BackstitchDetector


SVG_UNIT_SIZE = 10
BACKGROUND_INDEX = 99  # must be between n_colors and 255 inclusive since pattern is uint8
BACKGROUND_CODE = 'B5200'
IGNORE_BACKGROUND = True  # bg is set white with no symbol and not shown in legend
LEGEND_TITLE = 'Mouliné DMC'
BACKSTITCH = True

class Pattern:

    def __init__(self, show_colors: bool=True, show_symbols: bool=True, show_legend: bool=True) -> None:
        """Init object"""
        self.show_colors = show_colors
        self.show_symbols = show_symbols
        self.show_legend = show_legend
        self.dmc_palette = None
        self.dmc_pattern = None
        self.base_rgb_pattern = None
        self.backstitches = []
        self.width = 0
        self.height = 0
        self.pattern_composer = PatternComposer()

    def _change_background_index(self) -> None:
        """Set color index of background to special index"""
        self.bg_idx = self._get_background_idx()
        if IGNORE_BACKGROUND:
            self.dmc_pattern[self.dmc_pattern==self.bg_idx] = BACKGROUND_INDEX  # change idx in pattern
            self.dmc_palette.remove_color_by_idx(self.bg_idx)  # remove old bg color
            self.dmc_palette.add_color_by_code(BACKGROUND_INDEX, BACKGROUND_CODE, show_in_legend=False)  # add bg color
            self.bg_idx = BACKGROUND_INDEX  # change bg idx

    def _get_background_idx(self) -> int:
        """Get index representing background (mode of outer rim)"""
        rim = np.concatenate(
            [
                self.dmc_pattern[0, :],  # top
                self.dmc_pattern[-1, :],  # bottom
                self.dmc_pattern[1:-1, 0],  # left
                self.dmc_pattern[1:-1, -1],  # right
            ]
        )
        values, counts = np.unique(rim, return_counts=True)
        return values[np.argmax(counts)]

    def _generate_pattern(self, width: int, height: int) -> None:
        """Generate pattern as SVG"""
        for y_idx, row in enumerate(self.dmc_pattern):  # TODO: these loops take a long time for stitches_per_row > 100
            y_pos = (y_idx+1) * SVG_UNIT_SIZE  # +1 allows space for midpoint arrows
            for x_idx, c_idx in enumerate(row):
                x_pos = (x_idx+1) * SVG_UNIT_SIZE
                color = self.dmc_palette.get_color_by_idx(c_idx)
                self.pattern_composer.add_color_and_symbol(color, x_pos, y_pos, SVG_UNIT_SIZE)
        self.pattern_composer.add_grids(SVG_UNIT_SIZE, width, height)
        self.pattern_composer.add_numbers(SVG_UNIT_SIZE, width, height)
        self.pattern_composer.add_arrows(SVG_UNIT_SIZE, width, height)

    def _generate_legend(self, start_height: int) -> None:
        """Generate legend as SVG next to pattern"""
        x_pos = 2*SVG_UNIT_SIZE
        y_pos = start_height+3*SVG_UNIT_SIZE
        title_y_pos = start_height+2*SVG_UNIT_SIZE
        self.pattern_composer.add_title(x_pos, title_y_pos, LEGEND_TITLE)
        for color in self.dmc_palette:
            if color.show_in_legend is True:
                self.pattern_composer.add_legend_item(color, x_pos, y_pos, SVG_UNIT_SIZE)
                y_pos += 2.5*SVG_UNIT_SIZE

    def _generate_backstitches(self) -> None:
        """Generate backstitches over pattern as SVG"""
        for bs in self.backstitches:
            self.pattern_composer.add_backstitch(bs, SVG_UNIT_SIZE)

    def process_image(self, img_file: Path, n_colors: int, stitches_per_row: int, method: str) -> None:
        """Create image, process it (resize, pixelate, quantize), then get palette and pattern"""
        image = Image(img_file, show_colors=self.show_colors, show_symbols=self.show_symbols)
        self.dmc_palette, self.dmc_pattern, self.base_rgb_pattern = image.process(n_colors, stitches_per_row, method)
        self.width = self.dmc_pattern.shape[1]
        self.height = self.dmc_pattern.shape[0]
        self._change_background_index()
        if BACKSTITCH:
            backstitch_detector = BackstitchDetector(self.dmc_pattern, self.dmc_palette, self.bg_idx, show_colors=self.show_colors)
            self.backstitches = backstitch_detector.detect()

    def get_pattern_size(self) -> tuple[int]:
        """Calculate pattern size (width, height)"""
        width = (self.width+1) * SVG_UNIT_SIZE  # +1 because of outer margin
        height = (self.height+1) * SVG_UNIT_SIZE
        return (width, height)

    def get_legend_size(self) -> tuple[int]:
        """Calculate legend size (width, height)"""
        p_width, _ = self.get_pattern_size()
        height = (3 + 2.5*self.dmc_palette.n_colors_in_legend) * SVG_UNIT_SIZE  # title + legend entries
        return (p_width, height)

    def get_image_size(self) -> tuple[int]:
        """Calculate image size (width, height)"""
        p_width, p_height = self.get_pattern_size()
        height = p_height
        if self.show_legend is True:
            _, l_height = self.get_legend_size()
            height += l_height 
        return (p_width, height)

    def generate(self):
        """Generate SVG info"""
        pattern_width, pattern_height = self.get_pattern_size()
        image_width, image_height = self.get_image_size()
        self.pattern_composer.add_header(image_width, image_height)
        self._generate_pattern(pattern_width, pattern_height)
        if self.show_legend:
            self._generate_legend(pattern_height)
        if BACKSTITCH:
            self._generate_backstitches()
        self.pattern_composer.add_tail()

    def save(self, out_file: Path, formats: list[str]=['pdf'], png_scale: float=1.0) -> None:
        self.pattern_composer.save(out_file, formats, png_scale)
