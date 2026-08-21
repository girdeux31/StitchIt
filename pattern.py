from pathlib import Path

from image import Image
from pattern_composer import PatternComposer

SVG_UNIT_SIZE = 10


class Pattern:

    def __init__(self, color: bool=True, symbols: bool=True) -> None:
        """Init object"""
        self.color = color
        self.symbols = symbols
        self.dmc_palette = None
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

    def get_palette(self) -> list[dict[str, tuple | str]]:
        """Return image palette with color indexes"""
        if self.dmc_palette is None:
            raise ValueError('To obtain a palette first call process_image method')
        return self.dmc_palette
    
    def generate(self):
        """Generate SVG info"""
        width = self.width * SVG_UNIT_SIZE
        height = self.height * SVG_UNIT_SIZE
        self.pattern_composer.add_header(width, height)
        for y_idx, row in enumerate(self.dmc_pattern):  # TODO: these loops take a long time for stitches_per_row > 100
            y_pos = (y_idx+1) * SVG_UNIT_SIZE  # +1 allows space for midpoint arrows
            for x_idx, c_idx in enumerate(row):
                x_pos = (x_idx+1) * SVG_UNIT_SIZE
                self.pattern_composer.add_color(self.dmc_palette, c_idx, x_pos, y_pos, SVG_UNIT_SIZE)
                self.pattern_composer.add_symbol(c_idx, x_pos, y_pos, SVG_UNIT_SIZE)
        self.pattern_composer.add_gridlines(SVG_UNIT_SIZE, width, height)
        self.pattern_composer.add_numbers(SVG_UNIT_SIZE, width, height)
        self.pattern_composer.add_arrows(SVG_UNIT_SIZE, width, height)
        self.pattern_composer.add_tail()

    def save(self, out_file: Path, formats: list[str]=['pdf'], png_scale: float=1.0) -> None:
        self.pattern_composer.save(out_file, formats, png_scale)