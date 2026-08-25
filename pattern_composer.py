from pathlib import Path

from svg import SVG
from backstitch_detector import Backstitch
from palette import DMCColor


class PatternComposer:

    arrow_color = 'black'
    arrow_width = 2
    arrow_fill = 'black'
    arrow_gap = 2
    major_grid_step = 10
    major_grid_color = 'black'
    major_grid_width = 2
    minor_grid_color = 'rgb(20,20,20)'
    minor_grid_width = 1
    ref_number_step = 10
    ref_number_gap = 2
    stroke_color = 'black'
    stroke_width = 1
    title_font_size = '12px'
    title_font_color = 'black'
    text_font_size = '10px'
    text_font_color = 'black'
    symbol_color = 'black'
    symbol_width = 1
    svg_fill = 'red'
    svg_title_class_name = 'title_text'
    svg_text_class_name = 'pattern_text'
    svg_symbol_class_name = 'glyph'
    backstitch_width = 2

    def __init__(self) -> None:
        """Init object"""
        self.svg = SVG()

    def add_header(self, width: int, height: int) -> None:
        """Add svg header"""
        style = {
            'fill': self.svg_fill,
        }  # TODO remove?
        classes = {
            self.svg_title_class_name: {
                'font-size': self.title_font_size,
                'fill': self.title_font_color,
            },
            self.svg_text_class_name: {
                'font-size': self.text_font_size,
                'fill': self.text_font_color,
            },
            self.svg_symbol_class_name: {
                'stroke': self.symbol_color,
                'stroke-width': self.symbol_width,
            }
        }
        self.svg.add_xml_header(width, height, style)
        self.svg.add_xml_style(classes)

    def add_tail(self) -> None:
        """Add xml svg tag to close the file"""
        self.svg.add_xml_tail()

    def add_arrows(self, size: int, width: int, height: int) -> None:
        """Add midpoint arrows"""
        gap = -1*self.arrow_gap
        style = {
            'stroke': self.arrow_color,
            'stroke-width': self.arrow_width,
            'fill': self.arrow_fill,
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
            'stroke': self.major_grid_color,
            'stroke-width': self.major_grid_width,
        }
        # horizontal lines
        for x in range(11*size, width, self.major_grid_step*size):
            self.svg.add_xml_line(x, size, x, height, style)
        # vertical lines
        for y in range(11*size, height, self.major_grid_step*size):
            self.svg.add_xml_line(size, y, width, y, style)

    def _add_minor_grid(self, size: int, width: int, height: int) -> None:
        """Add minor grid"""
        style = {
            'stroke': self.minor_grid_color,
            'stroke-width': self.minor_grid_width,
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
        for idx, x_pos in enumerate(range(size*(self.ref_number_step+1), width, size*self.ref_number_step)):
            ref_number = (idx+1) * self.ref_number_step
            style = {
                'transform': f'translate(0 -{self.ref_number_gap})',
                'text-anchor': 'middle',
            }
            self.svg.add_xml_text(x_pos, size, style, ref_number, self.svg_text_class_name)

    def _add_left_numbers(self, size: int, height: int) -> None:
        """Add numbers in left margin"""
        for idx, y_pos in enumerate(range(size*(self.ref_number_step+1), height, size*self.ref_number_step)):
            ref_number = (idx+1) * self.ref_number_step
            style = {
                'transform': f'translate(-{self.ref_number_gap} 0) rotate(-90 {size} {y_pos})',
                'text-anchor': 'middle',
            }
            self.svg.add_xml_text(size, y_pos, style, ref_number, self.svg_text_class_name)
    
    def add_color_and_symbol(self, color: DMCColor, x: int, y: int, size: int, box: bool=False) -> None:
        """Add color and symbol if any"""
        self._add_color(color, x, y, size, box)
        self._add_symbol(color, x, y, size)

    def _add_color(self, color: DMCColor, x: int, y: int, size: int, box: bool=False) -> None:
        """Add colors as "pixels" """
        style = {
            'fill': f'rgb({color.get_dmc_rgb_as_str()})',
            'stroke': 'none',
        }
        if box:
            style['stroke'] = self.stroke_color
            style['stroke-width'] = self.stroke_width
        self.svg.add_xml_rect(x, y, size, size, style)

    def _add_symbol(self, color: DMCColor, x: int, y: int, size: int) -> None:
        """Add symbol"""
        if color.has_symbol:
            style = {
                'transform': f'translate({x} {y}) scale({size/20.0})',
                'fill': self.symbol_color if color.fill_symbol is True else "none",
            }
            self.svg.add_xml_path(color.symbol_code, style, self.svg_symbol_class_name)

    def add_title(self, x: int, y: int, text: str) -> None:
        """Add title"""
        self.svg.add_xml_text(x, y, {}, text, self.svg_title_class_name)

    def add_legend_item(self, color: DMCColor, x: int, y: int, size: int) -> None:
        """Add legend entry (square color with symbol and color code)"""
        self.add_color_and_symbol(color, x, y, 1.5*size, box=True)
        self.svg.add_xml_text(x+2*size, y+size, {}, color.dmc_code, self.svg_text_class_name)

    def add_backstitch(self, bs: Backstitch, pixels_per_coord: int) -> None:
        """Add backstitch as line"""
        start = [(coord+1)*pixels_per_coord for coord in bs.start]  # +1 because outer margin
        end = [(coord+1)*pixels_per_coord for coord in bs.end]
        style = {
            'stroke': f'rgb({bs.color.get_dmc_rgb_as_str()})',
            'stroke-width': self.backstitch_width,
        }
        self.svg.add_xml_line(start[0], start[1], end[0], end[1], style)

    def save(self, out_file: Path, formats: list[str], png_scale: float=1.0) -> None:
        """Save / export output as svg, png or pdf, scale is only applied to pngs"""
        for format_ in formats:
            if format_ == 'svg':
                self.svg.save_as_svg(out_file.with_suffix('.svg'))
            elif format_ == 'png':
                self.svg.save_as_png(out_file.with_suffix('.png'), scale=png_scale)
            elif format_ == 'pdf':
                self.svg.save_as_pdf(out_file.with_suffix('.pdf'))
            else:
                raise ValueError(f'Format file \'{format_}\' not supported')
