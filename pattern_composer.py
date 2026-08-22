from svg_composer import SVGComposer


class PatternComposer(SVGComposer):

    idx_to_symbol_code = {
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
    arrow_color = 'black'
    arrow_width = 2
    arrow_fill = 'black'
    arrow_gap = 2
    major_grid_color = 'black'
    major_grid_width = 2
    minor_grid_color = 'rgb(20,20,20)'
    minor_grid_width = 1
    ref_number_step = 10
    ref_number_gap = 2

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
        for x in range(11*size, width, 10*size):
            self.svg.add_xml_line(x, size, x, height, style)
        # vertical lines
        for y in range(11*size, height, 10*size):
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
            }
            self.svg.add_xml_text(x_pos, size, style, ref_number, self.svg_pattern_text_class_name)

    def _add_left_numbers(self, size: int, height: int) -> None:
        """Add numbers in left margin"""
        for idx, y_pos in enumerate(range(size*(self.ref_number_step+1), height, size*self.ref_number_step)):
            ref_number = (idx+1) * self.ref_number_step
            style = {
                'transform': f'translate(-{self.ref_number_gap} 0) rotate(-90 {size} {y_pos})',
            }
            self.svg.add_xml_text(size, y_pos, style, ref_number, self.svg_pattern_text_class_name)
    
    def add_color(self, palette: list[dict[str, tuple | str]], idx: int, x: int, y: int, size: int) -> None:
        """Add colors as "pixels" """
        r, g, b = palette[idx] if self.color else (255, 255, 255)
        style = {
            'fill': f'rgb({r},{g},{b})',
            'stroke': 'none',
        }
        self.svg.add_xml_rect(x, y, size, size, style)

    def add_symbol(self, idx: int, x: int, y: int, size: int) -> None:
        """Add symbols"""
        code = self.idx_to_symbol_code.get(idx, '')
        style = {
            'transform': f'translate({x} {y}) scale({size/20.0})',
            'fill': self.symbol_color if idx in self.idx_to_fill else "none",
        }
        self.svg.add_xml_path(code, style, self.svg_symbol_class_name)
