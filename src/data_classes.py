from pathlib import Path
from dataclasses import dataclass

from src.dmc_db import DMCDB
from src.constants import IDX_TO_SYMBOL_CODE, SYMBOLS_TO_FILL


@dataclass
class DMCColor:
    idx: int
    is_backstitch: bool
    show_in_legend: bool
    img_rgb: tuple[int] | None = None
    method: str | None = None
    dmc_code: str | None = None

    def __post_init__(self) -> None:
        """Initialize some attributs after init"""
        if self.img_rgb is None and self.dmc_code is None:
            raise ValueError('You must specify either \'img_rgb\' or \'dmc_code\'')
        if self.img_rgb is not None and self.dmc_code is not None:
            raise ValueError('You cannot specify both \'img_rgb\' and \'dmc_code\'')
        if self.img_rgb is not None and self.method is None:
            raise ValueError('If you specify \'img_rgb\', then you must also specify \'method\'')
        self.dmc = DMCDB()
        self._add_rgb()
        self.has_symbol = False

    def _add_rgb(self) -> None:
        """Add DMC RGB info"""
        if self.img_rgb is not None:
            c_info = self.dmc.get_most_similar_color(self.img_rgb, self.method)
            self.dmc_code = c_info['code']
        else:  # by code
            c_info = self.dmc.get_color_by_code(self.dmc_code)
        self.dmc_rgb = c_info['rgb']
        self.dmc_name = c_info['name']

    def replace_color_by_code(self, code: int | str) -> None:
        """Replace dmc_rgb, dmc_name (but no dmc_code), just used if show_colors is False"""
        c_info = self.dmc.get_color_by_code(code)
        self.dmc_rgb = c_info['rgb']

    def add_symbol(self) -> None:
        """Associate symbol to color"""
        if self.is_backstitch is False:
            self.has_symbol = self.idx in IDX_TO_SYMBOL_CODE
            self.symbol_code = IDX_TO_SYMBOL_CODE.get(self.idx)
            self.fill_symbol = self.idx in SYMBOLS_TO_FILL

    def get_dmc_rgb_as_str(self) -> str:
        """Return DMC RGB as str, such as r,g,b"""
        return ','.join([str(coord) for coord in self.dmc_rgb])

@dataclass
class Backstitch:
    start: tuple[int, int]
    end: tuple[int, int]
    color: DMCColor

@dataclass
class GeneralConfig:
    input_file: Path
    n_colors: int
    stitches_per_row: int
    show_colors: bool = True
    show_symbols: bool = True
    show_legend: bool = True
    ignore_background: bool = True
    save_formats: list[str] | None = None
    png_scale: float = 2.0

@dataclass
class OtherConfig:
    method: str = 'de00'  # 'euclidean', 'de76', 'de00'
    clean_confetti_wout_neighbors: bool = True
    clean_confetti_w1_diagonal_neighbor: bool = True
    background_code: str | int = 'B5200'
    show_backstitch: bool = False
    backstitch_option: str = 'constant'  # 'none', 'constant', 'inverse'
    backstitch_code: str | int = 498  # red
    backstitch_code_no_colors: str | int = 310  # black

@dataclass
class ThreadConfig:
    fabric_count: int = 14  # aida or squares per inch
    strands: int = 2  # strands used for stitching
    skein_length: float = 8.0  # m
    strands_per_skein: int = 6  # strands in a skein

@dataclass
class LegendConfig:
    title: str = 'Mouliné DMC'
    title_font_size: int = 12
    title_font_color: str = 'black'
    title_font_weight: str = 'bold'
    title_x_pixels: int = 20
    title_y_pixels: int = 30
    item_x_pixels: int = 20
    item_y_pixels: int = 20
    column_width_pixels: int = 100
    column_height_pixels: int = 30
    code_font_color: str = 'black'
    code_font_size: int = 10
    box_line_color: str = 'black'
    box_line_width: int = 1

@dataclass
class PatternConfig:
    svg_pixels_per_unit: int = 10
    major_grid_step_pixels: int = 100
    major_grid_color: str = 'black'
    major_grid_width: int = 2
    minor_grid_color: str = '#323232'
    minor_grid_width: int = 1
    coords_font_size: int = 10
    coords_font_color: str = 'black'
    coords_step_units: int = 10
    coords_gap_pixels: int = 2
    arrow_color: str = 'black'
    arrow_line_width: int = 2
    arrow_fill_color: str = 'black'
    arrow_gap_pixels: int = 2
    symbol_color: str = 'black'
    symbol_fill_color: str = 'black'
    symbol_line_width: int = 1
    backstitch_line_width: int = 2
