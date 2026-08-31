from pathlib import Path

import cairosvg


class SVG:
    
    def __init__(self):
        """Init object"""
        self.xml = ''

    def _write_xml_line(self, xml: str, indent: int=0) -> None:
        """Add xml code as string"""
        self.xml += indent*'\t' + xml + '\n'

    def add_xml_rect(
        self,
        x: int | float,
        y: int | float,
        width: int | float,
        height: int | float,
        style_dict: dict[str, str]
    ) -> None:
        """Add xml rect tag"""
        xml_code = f'<rect x="{x}" y="{y}" width="{width}" height="{height}" style="'
        for style_arg, style_value in style_dict.items():
            xml_code += f'{style_arg}:{style_value};'
        xml_code += '"/>'
        self._write_xml_line(xml_code, indent=1)

    def add_xml_header(
        self,
        width: int | float,
        height: int | float,
        style_dict: dict[str, dict[str, str]],
    ) -> None:
        """Add xml svg tag"""
        xml_code = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" style="'
        for style_arg, style_value in style_dict.items():
            xml_code += f'{style_arg}:{style_value};'
        xml_code += '">'
        self._write_xml_line(xml_code)

    def add_xml_style(self, class_dict: dict[str, dict[str, str]]) -> None:
        """Add xml style tag"""
        xml_code = '<style>'
        for class_name, class_style in class_dict.items():
            xml_code += f'.{class_name}{{'
            for style_arg, style_value in class_style.items():
                xml_code += f'{style_arg}:{style_value};'
            xml_code += '}'
        xml_code += '</style>'
        self._write_xml_line(xml_code, indent=1)

    def add_xml_path(self, code: str, style_dict: dict[str, str], class_name: str='') -> None:
        """Add xml path tag"""
        xml_code = '<path '
        if class_name:
            xml_code += f'class="{class_name}" '
        xml_code += f'd="{code}"'
        for style_arg, style_value in style_dict.items():
            xml_code += f' {style_arg}="{style_value}"'
        xml_code += '/>'
        self._write_xml_line(xml_code, indent=1)

    def add_xml_text(self, x: int | float, y: int | float, style_dict: dict[str, str], text: str, class_name: str='') -> None:
        """Add xml text tag"""
        xml_code = '<text '
        if class_name:
            xml_code += f'class="{class_name}" '
        xml_code += f'x="{x}" y="{y}"'
        for style_arg, style_value in style_dict.items():
            xml_code += f' {style_arg}="{style_value}"'
        xml_code += f'>{text}</text>'
        self._write_xml_line(xml_code, indent=1)

    def add_xml_line(self, x1: int | float, y1: int | float, x2: int | float, y2: int | float, style_dict: dict[str, str]) -> None:
        """Add xml line tag"""
        xml_code = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" style="'
        for style_arg, style_value in style_dict.items():
            xml_code += f'{style_arg}:{style_value};'
        xml_code += '"/>'
        self._write_xml_line(xml_code, indent=1)

    def add_xml_tail(self) -> None:
        """Add xml svg tag to close the file"""
        self._write_xml_line('</svg>')

    def save_as_svg(self, svg_file: Path) -> None:
        """Save as svg file"""
        f = open(svg_file,'w')
        f.write(self.xml)
        f.close()

    def save_as_png(self, png_file: Path, scale: float=1.0) -> None:
        """Save as png file, scale can be applied"""
        with open(png_file, "wb") as f:
            cairosvg.svg2png(
                bytestring=self.xml.encode("utf-8"),
                scale=scale,
                write_to=f,
            )

    def save_as_pdf(self, pdf_file: Path) -> None:
        """Save as pdf file"""
        with open(pdf_file, "wb") as f:
            cairosvg.svg2pdf(
                bytestring=self.xml.encode("utf-8"),
                write_to=f,
            )
