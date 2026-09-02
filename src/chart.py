import math
from pathlib import Path

from src.image import Image
from src.composer import Composer
from src.pattern import Pattern
from src.data_classes import GeneralConfig, OtherConfig, LegendConfig, PatternConfig


class Chart:

    def __init__(
        self,
        general_config: GeneralConfig,
        other_config: OtherConfig,
        legend_config: LegendConfig,
        pattern_config: PatternConfig
    ) -> None:
        """Init object"""
        self.general_config = general_config
        self.other_config = other_config
        self.legend_config = legend_config
        self.pattern_config = pattern_config
        self.image = None
        self.pattern = None
        self.composer = Composer(self.legend_config, self.pattern_config)

    def _generate_pattern(self, width: int, height: int) -> None:
        """Generate pattern as SVG"""
        for y_idx, row in enumerate(self.pattern.array):  # TODO: these loops take a long time for stitches_per_row > 100
            y_pos = (y_idx+1) * self.pattern_config.svg_pixels_per_unit  # +1 allows space for midpoint arrows
            for x_idx, c_idx in enumerate(row):
                x_pos = (x_idx+1) * self.pattern_config.svg_pixels_per_unit
                color = self.image.palette.get_color_by_idx(c_idx)
                self.composer.add_cross_stitch_entry(color, x_pos, y_pos, self.pattern_config.svg_pixels_per_unit)
        self.composer.add_grids(self.pattern_config.svg_pixels_per_unit, width, height)
        self.composer.add_numbers(self.pattern_config.svg_pixels_per_unit, width, height)
        self.composer.add_arrows(self.pattern_config.svg_pixels_per_unit, width, height)

    def _generate_legend(self) -> None:
        """Generate legend as SVG next to pattern"""
        column = 1
        pattern_width, pattern_height = self._get_pattern_size()
        x_pos = self.legend_config.item_x_pixels
        y_pos = pattern_height + self.legend_config.title_y_pixels + self.legend_config.item_y_pixels
        title_x_pos = self.legend_config.title_x_pixels
        title_y_pos = pattern_height + self.legend_config.title_y_pixels
        self.composer.add_title(title_x_pos, title_y_pos, self.legend_config.title)
        n_columns = int((pattern_width - self.legend_config.item_x_pixels) / self.legend_config.column_width_pixels)
        for color in self.image.palette:
            if color.show_in_legend is True and color.n_stitches > 0:
                self.composer.add_legend_item(color, x_pos, y_pos, self.pattern_config.svg_pixels_per_unit)
                column += 1
                if column <= n_columns:
                    x_pos = x_pos + self.legend_config.column_width_pixels
                else:
                    column = 1
                    x_pos = self.legend_config.item_x_pixels
                    y_pos += self.legend_config.column_height_pixels

    def _generate_backstitches(self) -> None:
        """Generate backstitches over pattern as SVG"""
        for bs in self.pattern.backstitches:
            self.composer.add_backstitch(bs, self.pattern_config.svg_pixels_per_unit)

    def _get_pattern_size(self) -> tuple[int]:
        """Calculate pattern size (width, height)"""
        width = (self.pattern.width+1) * self.pattern_config.svg_pixels_per_unit  # +1 because of outer margin
        height = (self.pattern.height+1) * self.pattern_config.svg_pixels_per_unit
        return (width, height)

    def _get_legend_size(self) -> tuple[int]:
        """Calculate legend size (width, height)"""
        p_width, _ = self._get_pattern_size()
        if self.general_config.show_legend is True:
            n_columns = int((p_width - self.legend_config.item_x_pixels) / self.legend_config.column_width_pixels)
            n_columns = n_columns if n_columns > 0 else 1
            n_rows = math.ceil(self.image.palette.n_colors_in_legend / n_columns)
            height = (self.legend_config.title_y_pixels + self.legend_config.item_y_pixels + self.legend_config.column_height_pixels*n_rows)  # title + legend entries
            width = self.legend_config.item_x_pixels + n_columns*self.legend_config.column_width_pixels
        else:
            width, height = p_width, 0
        return (width, height)

    def _get_image_size(self) -> tuple[int]:
        """Calculate image size (width, height)"""
        p_width, p_height = self._get_pattern_size()
        l_width, l_height = self._get_legend_size()
        width = max(p_width, l_width)
        height = p_height + l_height 
        width += self.pattern_config.svg_pixels_per_unit  # add right outer margin
        return (width, height)

    def generate(self):
        """Generate SVG info"""
        pattern_width, pattern_height = self._get_pattern_size()
        image_width, image_height = self._get_image_size()
        self.composer.add_header(image_width, image_height)
        self._generate_pattern(pattern_width, pattern_height)
        if self.general_config.show_legend is True:
            self._generate_legend()
        if self.other_config.show_backstitch is True:
            self._generate_backstitches()
        self.composer.add_tail()

    def save(self, out_file: Path) -> None:
        self.composer.save(out_file, self.general_config.save_formats, self.general_config.png_scale)

    def process(self) -> None:
        """Create image, process it (resize and quantize), then get palette and pattern"""
        self.image = Image(self.general_config, self.other_config)
        self.image.process()
        self.pattern = Pattern(self.general_config, self.other_config)
        self.pattern.process_from_image(self.image)
