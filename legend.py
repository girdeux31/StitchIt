from pathlib import Path

from legend_composer import LegendComposer
from pattern import Pattern
from dmc import DMC

SVG_UNIT_SIZE = 40
COLUMN_WIDTHS = [SVG_UNIT_SIZE, 8*SVG_UNIT_SIZE, 3*SVG_UNIT_SIZE, 3*SVG_UNIT_SIZE]



class Legend:

    def __init__(self, color: bool=True, symbols: bool=True) -> None:
        """Init object"""
        self.color = color
        self.symbols = symbols
        self.width = 0
        self.height = 0
        self.legend_composer = LegendComposer(color, symbols)

    def _get_color_info(self, pattern: Pattern, method: str):
        """Get dict with dmc color info"""
        dmc = DMC()
        color_info = {}
        for c_idx, rgb in pattern.dmc_palette.items():
            code = dmc.get_most_similar_code_by_rgb(rgb, method=method)
            name = dmc.get_color_name_by_code(code)
            stitches = len([idx for row in pattern.dmc_pattern for idx in row if c_idx == idx])
            color_info[c_idx] = {
                'rgb': rgb,
                'code': code,
                'name': name,
                'stitches': stitches,
            }
        return color_info

    def generate(self, pattern: Pattern, method: str) -> None:
        """Generate SVG info"""
        color_info = self._get_color_info(pattern, method)
        widths = COLUMN_WIDTHS  # cell width and height
        height = SVG_UNIT_SIZE
        x_pos = [0] + [sum(COLUMN_WIDTHS[:i+1]) for i in range(len(COLUMN_WIDTHS[:-1]))]
        y_pos = 0
        self.width = sum(COLUMN_WIDTHS)  # image width and height
        self.height = len(color_info)*height
        self.legend_composer.add_header(self.width, self.height)
        for c_idx, c_info in color_info.items():
            self.legend_composer.add_color_rgb(x_pos[0], y_pos, widths[0], height, c_info)
            if self.symbols:
                self.legend_composer.add_symbol(x_pos[0], y_pos, height, c_idx)
            self.legend_composer.add_color_name(x_pos[1], y_pos, widths[1], height, c_info)
            self.legend_composer.add_color_code(x_pos[2], y_pos, widths[2], height, c_info)
            self.legend_composer.add_stitches(x_pos[3], y_pos, widths[3], height, c_info)
            y_pos += height
        self.legend_composer.add_tail()

    def save(self, out_file: Path, formats: list[str]=['pdf'], png_scale: float=1.0) -> None:
        self.legend_composer.save(out_file, formats, png_scale)