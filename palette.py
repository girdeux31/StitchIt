from dataclasses import dataclass

from dmc_db import DMCDB


IDX_TO_SYMBOL_CODE = {
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
SYMBOLS_TO_FILL = [2, 6, 7, 10]

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
        self.dmc_name = c_info['name']

    def add_symbol(self) -> None:
        """Associate symbol to color"""
        if self.is_backstitch is False:
            self.has_symbol = self.idx in IDX_TO_SYMBOL_CODE
            self.symbol_code = IDX_TO_SYMBOL_CODE.get(self.idx)
            self.fill_symbol = self.idx in SYMBOLS_TO_FILL

    def get_dmc_rgb_as_str(self) -> None:
        """Return DMC RGB as str, such as r,g,b"""
        return ','.join([str(coord) for coord in self.dmc_rgb])

class Palette:

    def __init__(self, method: str):
        """Init object"""
        self.method = method
        self.colors = []

    # define dunder method iter so you can do 'for color in palette'
    def __iter__(self):
        return iter(self.colors)
    
    def add_color_by_rgb(
        self,
        c_idx: int,
        img_rgb: tuple[int],
        is_backstitch: bool=False,
        show_in_legend: bool=True,
    ) -> None:
        """Add color to palette by RGB"""
        self.colors.append(
            DMCColor(
                c_idx,
                img_rgb=img_rgb,
                is_backstitch=is_backstitch, 
                show_in_legend=show_in_legend,
                method=self.method,
            )
        )

    def add_color_by_code(
        self,
        c_idx: int,
        dmc_code: str | int,
        is_backstitch: bool=False,
        show_in_legend: bool=True,
    ) -> None:
        """Add color to palette by DMC code"""
        self.colors.append(
            DMCColor(
                c_idx,
                dmc_code=dmc_code,
                is_backstitch=is_backstitch,
                show_in_legend=show_in_legend,
            )
        )

    def get_color_by_idx(self, c_idx: int) -> DMCColor:
        """Get DMC color object by color index"""
        for color in self.colors:
            if color.idx == c_idx:
                return color
        raise ValueError(f'Color with index \'{c_idx}\' not found')

    def remove_color_by_idx(self, c_idx: int) -> None:
        """Remove DMC color object by color index, do not call it inside a 'for color in palette' loop"""
        list_idx = [idx for idx, color in enumerate(self.colors) if color.idx == c_idx]
        if len(list_idx) == 0:
            raise ValueError(f'Color with index \'{c_idx}\' not found')
        del self.colors[list_idx[0]]

    def replace_all_colors_by_code(self, code: int | str) -> None:
        """Replace all colors by dmc code, do no call this before quantize"""
        for color in self.colors:
            color.replace_color_by_code(code)

    def add_symbols(self) -> None:
        """If possible add symbol to all colors (there is a limit of 11)"""
        for color in self.colors:
            color.add_symbol()

    @property
    def n_colors_in_legend(self) -> int:
        """Get number of colors to show in legend"""
        return len([color for color in self.colors if color.show_in_legend])
