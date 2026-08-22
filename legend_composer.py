from svg_composer import SVGComposer


class LegendComposer(SVGComposer):

    idx_to_code = {
        0: "M4 4L16 16", # backslash
        1: "M4 16L16 4M4 10L 16 10", # forward slash
        2: "M7 7L7 13 13 13 13 7Z", # little square, filled black
        3: "M4 4L10 16L16 4 Z", # triangle, upside down
        4: "M4 4L16 16M4 16 L16 4", # diagonal cross
        5: "M4 4L4 16 16 16 16 4Z", # square
        6: "M4 4L10 16L16 4 Z", # triangle, upside down, filled black
        7: "M10 4L6 10 10 16 14 10Z", # diamond, filled black
        8: "M8 8L8 12 12 12 12 8Z", # little square
        9: "M4 4L16 16M4 16 L16 4M10 4L10 16M4 10L16 10", # 8 way cross
        10: "M4 4L4 16 16 16 16 4Z", # square, filled black
    }
    idx_to_fill = [2, 6, 7, 10]
    fill_color = 'white'
    stroke_color = 'black'
    stroke_width = 1

    def add_color_rgb(self, x_pos: int, y_pos: int, width: int, height: int, color_info: dict[str, tuple | str]) -> None:
        """Add color in first column"""
        r, g, b = color_info['rgb'] if self.color else (255, 255, 255)
        style = {
            'fill': f'rgb({r},{g},{b})',
            'stroke': self.stroke_color,
            'stroke-width': self.stroke_width,
        }
        self.svg.add_xml_rect(x_pos, y_pos, width, height, style)

    def add_symbol(self, x_pos: int, y_pos: int, height: int, idx: int) -> None:
        """Add symbol in first column"""
        code = self.idx_to_code.get(idx)
        if code:
            style = {
                'transform': f'translate({x_pos} {y_pos}) scale({height/20.0})',
                'fill': self.symbol_color if idx in self.idx_to_fill else "none",
            }
            self.svg.add_xml_path(code, style, self.svg_symbol_class_name)

    def add_color_name(self, x_pos: int, y_pos: int, width: int, height: int, color_info: dict[str, tuple | str]) -> None:
        """Add color name in second column"""
        rect_style = {
            'fill': self.fill_color,
            'stroke': self.stroke_color,
            'stroke-width': self.stroke_width,
        }
        self.svg.add_xml_rect(x_pos, y_pos, width, height, rect_style)
        self.svg.add_xml_text(x_pos + 0.5*height, y_pos + height/1.5, {}, color_info['name'], self.svg_legend_text_class_name)

    def add_color_code(self, x_pos: int, y_pos: int, width: int, height: int, color_info: dict[str, tuple | str]) -> None:
        """Add color code in third column"""
        rect_style = {
            'fill': self.fill_color,
            'stroke': self.stroke_color,
            'stroke-width': self.stroke_width,
        }
        self.svg.add_xml_rect(x_pos, y_pos, width, height, rect_style)
        self.svg.add_xml_text(x_pos + 0.5*height, y_pos + height/1.5, {}, color_info['code'], self.svg_legend_text_class_name)

    def add_stitches(self, x_pos: int, y_pos: int, width: int, height: int, color_info: dict[str, tuple | str]) -> None:
        """Add stitches in forth column"""
        rect_style = {
            'fill': self.fill_color,
            'stroke': self.stroke_color,
            'stroke-width': self.stroke_width,
        }
        self.svg.add_xml_rect(x_pos, y_pos, width, height, rect_style)
        self.svg.add_xml_text(x_pos + 0.5*height, y_pos + height/1.5, {}, f'x{color_info["stitches"]}', self.svg_legend_text_class_name)
