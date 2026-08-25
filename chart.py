from pathlib import Path

from image import Image
from composer import Composer
from pattern import Pattern


SVG_PIXELS_PER_UNIT = 10
LEGEND_TITLE = 'Mouliné DMC'
BACKSTITCH = True

class Chart:

    def __init__(self, show_colors: bool=True, show_symbols: bool=True, show_legend: bool=True) -> None:
        """Init object"""
        self.show_colors = show_colors
        self.show_symbols = show_symbols
        self.show_legend = show_legend
        self.image = None
        self.pattern = None
        self.composer = Composer()

    def _generate_pattern(self, width: int, height: int) -> None:
        """Generate pattern as SVG"""
        for y_idx, row in enumerate(self.pattern.array):  # TODO: these loops take a long time for stitches_per_row > 100
            y_pos = (y_idx+1) * SVG_PIXELS_PER_UNIT  # +1 allows space for midpoint arrows
            for x_idx, c_idx in enumerate(row):
                x_pos = (x_idx+1) * SVG_PIXELS_PER_UNIT
                color = self.image.palette.get_color_by_idx(c_idx)
                self.composer.add_cross_stitch_entry(color, x_pos, y_pos, SVG_PIXELS_PER_UNIT)
        self.composer.add_grids(SVG_PIXELS_PER_UNIT, width, height)
        self.composer.add_numbers(SVG_PIXELS_PER_UNIT, width, height)
        self.composer.add_arrows(SVG_PIXELS_PER_UNIT, width, height)

    def _generate_legend(self, start_height: int) -> None:
        """Generate legend as SVG next to pattern"""
        x_pos = 2*SVG_PIXELS_PER_UNIT
        y_pos = start_height+3*SVG_PIXELS_PER_UNIT
        title_y_pos = start_height+2*SVG_PIXELS_PER_UNIT
        self.composer.add_title(x_pos, title_y_pos, LEGEND_TITLE)
        for color in self.image.palette:
            if color.show_in_legend is True:
                self.composer.add_legend_item(color, x_pos, y_pos, SVG_PIXELS_PER_UNIT)
                y_pos += 2.5*SVG_PIXELS_PER_UNIT

    def _generate_backstitches(self) -> None:
        """Generate backstitches over pattern as SVG"""
        for bs in self.pattern.backstitches:
            self.composer.add_backstitch(bs, SVG_PIXELS_PER_UNIT)

    def _get_pattern_size(self) -> tuple[int]:
        """Calculate pattern size (width, height)"""
        width = (self.pattern.width+1) * SVG_PIXELS_PER_UNIT  # +1 because of outer margin
        height = (self.pattern.height+1) * SVG_PIXELS_PER_UNIT
        return (width, height)

    def _get_legend_size(self) -> tuple[int]:
        """Calculate legend size (width, height)"""
        p_width, _ = self._get_pattern_size()
        height = (3 + 2.5*self.image.palette.n_colors_in_legend) * SVG_PIXELS_PER_UNIT  # title + legend entries
        return (p_width, height)

    def _get_image_size(self) -> tuple[int]:
        """Calculate image size (width, height)"""
        p_width, p_height = self._get_pattern_size()
        height = p_height
        if self.show_legend is True:
            _, l_height = self._get_legend_size()
            height += l_height 
        return (p_width, height)

    def generate(self):
        """Generate SVG info"""
        pattern_width, pattern_height = self._get_pattern_size()
        image_width, image_height = self._get_image_size()
        self.composer.add_header(image_width, image_height)
        self._generate_pattern(pattern_width, pattern_height)
        if self.show_legend:
            self._generate_legend(pattern_height)
        if BACKSTITCH:
            self._generate_backstitches()
        self.composer.add_tail()

    def save(self, out_file: Path, formats: list[str]=['pdf'], png_scale: float=1.0) -> None:
        self.composer.save(out_file, formats, png_scale)

    def process(self, img_file: Path, n_colors: int, stitches_per_row: int, method: str) -> None:
        """Create image, process it (resize, pixelate, quantize), then get palette and pattern"""
        self.image = Image(show_colors=self.show_colors, show_symbols=self.show_symbols)
        self.image.process(img_file, n_colors, stitches_per_row, method)
        self.pattern = Pattern(show_colors=self.show_colors)
        self.pattern.process_from_image(self.image)
