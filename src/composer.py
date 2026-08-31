from pathlib import Path

from src.svg import SVG
from src.backstitch_detector import Backstitch
from src.data_classes import DMCColor, LegendConfig, PatternConfig


class Composer:

    svg_title_class_name = 'title'
    svg_code_class_name = 'code'
    svg_coords_class_name = 'coordenates'
    svg_symbol_class_name = 'glyph'

    def __init__(self, legend_config: LegendConfig, pattern_config: PatternConfig) -> None:
        """Init object"""
        self.legend_config = legend_config
        self.pattern_config = pattern_config
        self.svg = SVG()

    def add_header(self, width: int, height: int) -> None:
        """Add svg header"""
        classes = {
            self.svg_title_class_name: {
                'font-size': f'{self.legend_config.title_font_size}px',
                'font-weight': self.legend_config.title_font_weight,
                'fill': self.legend_config.title_font_color,
            },
            self.svg_coords_class_name: {
                'font-size': f'{self.pattern_config.coords_font_size}px',
                'fill': self.pattern_config.coords_font_color,
            },
            self.svg_code_class_name: {
                'font-size': f'{self.legend_config.code_font_size}px',
                'fill': self.legend_config.code_font_color,
            },
            self.svg_symbol_class_name: {
                'stroke': self.pattern_config.symbol_color,
                'stroke-width': self.pattern_config.symbol_line_width,
            }
        }
        self.svg.add_xml_header(width, height, {})
        self.svg.add_xml_style(classes)

    def add_tail(self) -> None:
        """Add xml svg tag to close the file"""
        self.svg.add_xml_tail()

    def add_arrows(self, size: int, width: int, height: int) -> None:
        """Add midpoint arrows"""
        gap = -1*self.pattern_config.arrow_gap_pixels
        style = {
            'stroke': self.pattern_config.arrow_color,
            'stroke-width': self.pattern_config.arrow_line_width,
            'fill': self.pattern_config.arrow_fill_color,
            'transform': f'translate({width/2} {gap}) scale({size/15.0})',
        }
        # vertical arrow looking down
        code = "M4 4L10 16L16 4 Z"  # triangle, upside down, filled black
        self.svg.add_xml_path(code, style)
        # horizontal arrow looking right
        style['transform'] = f'translate({gap} {height/2}) scale({size/15.0})'
        code = "M4 4L16 10L4 16 Z"  # triangle, looking right, filled black
        self.svg.add_xml_path(code, style)

    def add_grids(self, size: int, width: int, height: int) -> None:
        """Add major and minor grids"""
        self._add_minor_grid(size, width, height)
        self._add_major_grid(size, width, height)

    def _add_major_grid(self, size: int, width: int, height: int) -> None:
        """Add major grid"""
        style = {
            'stroke': self.pattern_config.major_grid_color,
            'stroke-width': self.pattern_config.major_grid_width,
        }
        # horizontal lines
        for x in range(size+self.pattern_config.major_grid_step_pixels, width, self.pattern_config.major_grid_step_pixels):
            self.svg.add_xml_line(x, size, x, height, style)
        # vertical lines
        for y in range(size+self.pattern_config.major_grid_step_pixels, height, self.pattern_config.major_grid_step_pixels):
            self.svg.add_xml_line(size, y, width, y, style)

    def _add_minor_grid(self, size: int, width: int, height: int) -> None:
        """Add minor grid"""
        style = {
            'stroke': self.pattern_config.minor_grid_color,
            'stroke-width': self.pattern_config.minor_grid_width,
        }
        # horizontal lines
        for x in range(size, width+1, size):
            self.svg.add_xml_line(x, size, x, height, style)
        # vertical lines
        for y in range(size, height+1, size):
            self.svg.add_xml_line(size, y, width, y, style)

    def add_numbers(self, size: int, width: int, height: int) -> None:
        """Add numbers in top and left margins"""
        self._add_top_numbers(size, width)
        self._add_left_numbers(size, height)

    def _add_top_numbers(self, size: int, width: int) -> None:
        """Add numbers in top margin"""
        for x_pos in range(
            size*(1+self.pattern_config.coords_step_units),
            width+1,
            size*self.pattern_config.coords_step_units
        ):
            coord = int((x_pos-size) / size)
            style = {
                'transform': f'translate(0 -{self.pattern_config.coords_gap_pixels})',
                'text-anchor': 'middle',
            }
            self.svg.add_xml_text(x_pos, size, style, coord, self.svg_coords_class_name)

    def _add_left_numbers(self, size: int, height: int) -> None:
        """Add numbers in left margin"""
        for y_pos in range(
            size*(1+self.pattern_config.coords_step_units),
            height+1,
            size*self.pattern_config.coords_step_units
        ):
            coord = int((y_pos-size) / size)
            style = {
                'transform': f'translate(-{self.pattern_config.coords_gap_pixels} 0) rotate(-90 {size} {y_pos})',
                'text-anchor': 'middle',
            }
            self.svg.add_xml_text(size, y_pos, style, coord, self.svg_coords_class_name)
    
    def add_cross_stitch_entry(self, color: DMCColor, x: int, y: int, size: int, box: bool=False) -> None:
        """Add color and symbol if any"""
        self._add_color(color, x, y, size, box)
        self._add_symbol(color, x, y, size)

    def add_backstitch_entry(self, color: DMCColor, x: int, y: int, size: int) -> None:
        """Add backstitch legend entry"""
        style = {
            'stroke': f'rgb({color.get_dmc_rgb_as_str()})',
            'stroke-width': self.pattern_config.backstitch_line_width,
        }
        self.svg.add_xml_line(x, y+size*0.5, x+size, y+size*0.5, style)

    def _add_color(self, color: DMCColor, x: int, y: int, size: int, box: bool=False) -> None:
        """Add colors as "pixels" """
        style = {
            'fill': f'rgb({color.get_dmc_rgb_as_str()})',
            'stroke': 'none',
        }
        if box:
            style['stroke'] = self.legend_config.box_line_color
            style['stroke-width'] = self.legend_config.box_line_width
        self.svg.add_xml_rect(x, y, size, size, style)

    def _add_symbol(self, color: DMCColor, x: int, y: int, size: int) -> None:
        """Add symbol"""
        if color.has_symbol:
            style = {
                'transform': f'translate({x} {y}) scale({size/20.0})',
                'fill': self.pattern_config.symbol_fill_color if color.fill_symbol is True else 'none',
            }
            self.svg.add_xml_path(color.symbol_code, style, self.svg_symbol_class_name)

    def add_title(self, x: int, y: int, text: str) -> None:
        """Add title"""
        self.svg.add_xml_text(x, y, {}, text, self.svg_title_class_name)

    def add_legend_item(self, color: DMCColor, x: int, y: int, size: int) -> None:
        """Add legend entry (square color with symbol and color code)"""
        if color.is_backstitch is True:
            self.add_backstitch_entry(color, x, y, 1.5*size)
        else:
            self.add_cross_stitch_entry(color, x, y, 1.5*size, box=True)
        self.svg.add_xml_text(x+2*size, y+size, {}, color.dmc_code, self.svg_code_class_name)

    def add_backstitch(self, bs: Backstitch, pixels_per_coord: int) -> None:
        """Add backstitch as line"""
        start = [(coord+1)*pixels_per_coord for coord in bs.start]  # +1 because outer margin
        end = [(coord+1)*pixels_per_coord for coord in bs.end]
        style = {
            'stroke': f'rgb({bs.color.get_dmc_rgb_as_str()})',
            'stroke-width': self.pattern_config.backstitch_line_width,
        }
        self.svg.add_xml_line(start[0], start[1], end[0], end[1], style)

    def save(self, file: Path, formats: list[str], png_scale: float=1.0) -> None:
        """Save / export output as svg, png or pdf, scale is only applied to pngs"""
        for format_ in formats:
            if format_ == 'svg':
                self.svg.save_as_svg(file.with_suffix('.svg'))
            elif format_ == 'png':
                self.svg.save_as_png(file.with_suffix('.png'), scale=png_scale)
            elif format_ == 'pdf':
                self.svg.save_as_pdf(file.with_suffix('.pdf'))
            else:
                raise ValueError(f'File format \'{format_}\' not supported')
