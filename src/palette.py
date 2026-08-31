from src.data_classes import DMCColor


class Palette:

    def __init__(self, method):
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
