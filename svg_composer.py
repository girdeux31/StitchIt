from pathlib import Path

from svg import SVG


class SVGComposer:

    title_font_size = '12px'
    title_font_color = 'black'
    text_font_size = '10px'
    text_font_color = 'black'
    symbol_color = 'black'
    symbol_width = 1
    svg_fill = 'none'
    svg_title_class_name = 'title_text'
    svg_text_class_name = 'pattern_text'
    svg_symbol_class_name = 'glyph'

    def __init__(self, color: bool=True, symbols: bool=True) -> None:
        """Init object"""
        self.color = color
        self.symbols = symbols
        self.svg = SVG()

    def add_header(self, width: int, height: int) -> None:
        """Add svg header"""
        style = {
            'fill': self.svg_fill,
        }
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
