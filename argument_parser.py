import argparse

from PIL import ImageColor
from pathlib import Path
from warnings import warn

from data_classes import GeneralConfig, OtherConfig, ThreadConfig, LegendConfig, PatternConfig


METHOD_OPTIONS = ['euclidean', 'compuphase', 'de76', 'de00']  # TODO remove compuphase?
CONFETTI_CLEANER_OPTIONS = ['none', 'moderate', 'strong']
BACKSTITCH_OPTIONS = ['none', 'constant']
FONT_WEIGHT_OPTIONS = ['normal', 'bold']
N_COLOR_RANGE = [2, 100]
MAX_STITCHES_PER_ROW_RECOMMENDED = 125  # TODO check why waves takes so much less than bird

def is_valid_color(value):
    try:
        ImageColor.getrgb(value)
        return True
    except (ValueError, TypeError):
        return False

class ArgumentParser:

    def __init__(self):
        """Init object"""
        self.parser = argparse.ArgumentParser(
            description='Generates a cross stitch pattern from an image'
        )
        self._add_arguments()

    def parse_arguments(self) -> list:
        """Parse user arguments"""
        self.args = self.parser.parse_args()
        self._postprocess_arguments()
        self._check_arguments()

    def get_configurations(self) -> tuple:
        """Get configurations as dataclasses"""
        self.general_config = self._get_general_config()
        self.other_config = self._get_other_config()
        self.thread_config = self._get_thread_config()
        self.legend_config = self._get_legend_config()
        self.pattern_config = self._get_pattern_config()
        return (
            self.general_config,
            self.other_config,
            self.thread_config,
            self.legend_config,
            self.pattern_config,
        )

    def _add_arguments(self):
        """Define input arguments in parser"""

        # GENERAL PARAMETERS

        self.parser.add_argument(
            'input_file', type=str, help='Image file to convert.'
        )
        self.parser.add_argument(
            'n_colors', type=int, help=f'Colors to use in chart (backstitch colors are not included). Parameter must be between {N_COLOR_RANGE[0]} and {N_COLOR_RANGE[1]}, both included.'
        )
        self.parser.add_argument(
            'stitches_per_row', type=int, help='Number of stitches (squares/pixels) per row in chart.'
        )
        self.parser.add_argument(
            '--no_colors', dest='show_colors', action='store_false', help='Produces chart without colors (color specified in parameter \'--background_code\' is used). By default colors are user.'
        )
        self.parser.add_argument(
            '--no_symbols', dest='show_symbols', action='store_false', help='Produces chart without symbols. By default symbols are user.'
        )
        self.parser.add_argument(
            '--no_legend', dest='show_legend', action='store_false', help='Produces chart without legend. By default legend is shown.'
        )
        self.parser.add_argument(
            '--no_svg', dest='save_as_svg', action='store_false', help='Do not save chart as svg file. By default a svg file is generated.'
        )
        self.parser.add_argument(
            '--no_png', dest='save_as_png', action='store_false', help='Do not save chart as png file. By default a png file is generated.'
        )
        self.parser.add_argument(
            '--no_pdf', dest='save_as_pdf', action='store_false', help='Do not save chart as pdf file. By default a pdf file is generated.'
        )
        self.parser.add_argument(
            '--png_scale', type=float, default=2.0, help='Scale factor for the png generated file if \'--no_png\' parameter is not used. Default is \'2.0\'.'
        )

        # OTHER PARAMETERS

        self.parser.add_argument(
            '--method', default='de00', choices=METHOD_OPTIONS, help='Method to compute color distance. Options are: \'euclidean\', \'compuphase\' (similar to euclidean distance but with weighting factors depending on red), \'de76\' (deltaE CIE76, like euclidean distance but with LAB coordinates), \'de00\' (deltaE CIELAB2000, more accurate method as it measure color difference as human perception). Default is \'de00\'.'
        )
        self.parser.add_argument(
            '--confetti_cleaner', default='strong', choices=CONFETTI_CLEANER_OPTIONS, help='Level of confetti (bad pixels) cleaning. Options are \'none\', \'moderate\' (cleans isoleted pixels) and \'strong\' (same as \'moderate\' plus cleans pixels with just one diagonal neighbor). Dafault is \'strong\'.'
        )
        self.parser.add_argument(
            '--ignore_background', action='store_true', help='Stitches detected as background are drown with color specified in parameter \'--background_code\', without symbols and its color is not shown in legend. Background is detected as the mode of outer rim in input file. By default background is not ignored.'
        )
        self.parser.add_argument(
            '--background_code', type=str, default='B5200', help='DMC code for background color when parameter \'--ignore_background\' is used. See available codes in https://artpatt.com/dmc-color-chart. Default is \'B5200\' (snow white).'
        )
        self.parser.add_argument(
            '--backstitch_option', default='constant', choices=BACKSTITCH_OPTIONS, help='Level of backstitching. Options are \'none\' and \'constant\' (backstitches with constant color between objects and background). Default is \'none\'.'
        )
        self.parser.add_argument(
            '--backstitch_code', type=str, default='498', help='DMC code for backstitches when parameter \'--backstitch_option\' is \'constant\'. See available codes in https://artpatt.com/dmc-color-chart. Default is \'498\' (dark red).'
        )
        self.parser.add_argument(
            '--backstitch_code_no_colors', type=str, default='310', help='DMC code for backstitches when parameter \'--backstitch_option\' is not \'none\' and \'--no_colors\' is used. See available codes in https://artpatt.com/dmc-color-chart. Default is \'310\' (black).'
        )
        self.parser.add_argument(
            '--backstitch_line_width', type=int, default=2, help='Backstitch line width when parameter \'--backstitch_option\' is not \'none\'. Default is 2.'
        )

        # THREAD PARAMETERS

        self.parser.add_argument(
            '--fabric_count', type=int, default=14, help='AIDA number of squares per inch. Only used to compute thread usage. Default is 14.'
        )
        self.parser.add_argument(
            '--strands', type=int, default=2, help='Strands used for stitching. Only used to compute thread usage. Default is 2.'
        )
        self.parser.add_argument(
            '--skein_length', type=float, default=8.0, help='Skein length in meters. Only used to compute thread usage. Default is 8.0.'
        )
        self.parser.add_argument(
            '--strands_per_skein', type=int, default=6, help='Strands in a skein. Only used to compute thread usage. Default is 6.'
        )

        # LEGEND PARAMETERS

        self.parser.add_argument(
            '--legend_title', type=str, default='Mouliné DMC', help='Legend title. Default is \'Mouliné DMC\'.'
        )
        self.parser.add_argument(
            '--legend_title_font_size', type=int, default=12, help='Legend title font size. Default is 12.'
        )
        self.parser.add_argument(
            '--legend_title_font_color', type=str, default='black', help='Legend title font color. Colors can be specified with names as \'gray\', RGB coordinates as \'128,128,128\' or HEX codes as \'#808080\'. See available colors in https://www.w3.org/TR/css-color-4/#named-colors.  Default is \'black\'.'
        )
        self.parser.add_argument(
            '--legend_title_font_weight', type=str, default='bold', choices=FONT_WEIGHT_OPTIONS, help='Legend title font weight. Options are \'normal\' and \'bold\'. Default is \'bold\'.'
        )
        self.parser.add_argument(
            '--legend_title_x_pixels', type=int, default=20, help='Horizontal space before legend title in pixels. Default is 20.'
        )
        self.parser.add_argument(
            '--legend_title_y_pixels', type=int, default=30, help='Vertical space before legend title in pixels. Default is 30.'
        )
        self.parser.add_argument(
            '--legend_item_x_pixels', type=int, default=20, help='Horizontal space before first legend item in pixels. Default is 20.'
        )
        self.parser.add_argument(
            '--legend_item_y_pixels', type=int, default=20, help='Vertical space before first legend item in pixels. Default is 20.'
        )
        self.parser.add_argument(
            '--legend_column_width_pixels', type=int, default=100, help='Horizontal space between legend columns in pixels. Default is 100.'
        )
        self.parser.add_argument(
            '--legend_column_height_pixels', type=int, default=30, help='Vertical space between legend rows in pixels. Default is 30.'
        )
        self.parser.add_argument(
            '--legend_code_font_color', type=str, default='black', help='Font color for each legend item. Colors can be specified with names as \'gray\', RGB coordinates as \'128,128,128\' or HEX codes as \'#808080\'. See available colors in https://www.w3.org/TR/css-color-4/#named-colors.  Default is \'black\'.'
        )
        self.parser.add_argument(
            '--legend_code_font_size', type=int, default=10, help='Font size for each legend item. Default is 10.'
        )
        self.parser.add_argument(
            '--legend_box_line_color', type=str, default='black', help='Box line color for each legend item. Colors can be specified with names as \'gray\', RGB coordinates as \'128,128,128\' or HEX codes as \'#808080\'. See available colors in https://www.w3.org/TR/css-color-4/#named-colors.  Default is \'black\'.'
        )
        self.parser.add_argument(
            '--legend_box_line_width', type=int, default=1, help='Box line width for each legend item. Default is 1.'
        )

        # PATTERN PARAMETERS

        self.parser.add_argument(
            '--major_grid_color', type=str, default='black', help='Major grid color. Colors can be specified with names as \'gray\', RGB coordinates as \'128,128,128\' or HEX codes as \'#808080\'. See available colors in https://www.w3.org/TR/css-color-4/#named-colors.  Default is \'black\'.'
        )
        self.parser.add_argument(
            '--major_grid_step_pixels', type=int, default=100, help='Space between major gird lines in pixels. Default is 100.'
        )
        self.parser.add_argument(
            '--major_grid_width', type=int, default=2, help='Major gird line width. Default is 2.'
        )
        self.parser.add_argument(
            '--minor_grid_color', type=str, default='#323232', help='Minor grid color. Colors can be specified with names as \'gray\', RGB coordinates as \'128,128,128\' or HEX codes as \'#808080\'. See available colors in https://www.w3.org/TR/css-color-4/#named-colors.  Default is \'#323232\'.'
        )
        self.parser.add_argument(
            '--minor_grid_step_pixels', type=int, dest='svg_pixels_per_unit', default=10, help='Space between minor gird lines in pixels. Default is 10.'
        )
        self.parser.add_argument(
            '--minor_grid_width', type=int, default=1, help='Minor gird line width. Default is 1.'
        )
        self.parser.add_argument(
            '--coords_font_color', type=str, default='black', help='Coordinates color in outer margin. Colors can be specified with names as \'gray\', RGB coordinates as \'128,128,128\' or HEX codes as \'#808080\'. See available colors in https://www.w3.org/TR/css-color-4/#named-colors.  Default is \'black\'.'
        )
        self.parser.add_argument(
            '--coords_font_size', type=int, default=10, help='Coordinatess font size. Default is 10.'
        )
        self.parser.add_argument(
            '--coords_step_pixels', type=int, default=100, help='Space between coordinate numbers in pixels. Default is 100.'
        )
        self.parser.add_argument(
            '--coords_gap_pixels', type=int, default=2, help='Space between coordinates and chart in pixels. Default is 2.'
        )
        self.parser.add_argument(
            '--arrow_color', type=str, default='black', help='Arrow color in outer margin. Colors can be specified with names as \'gray\', RGB coordinates as \'128,128,128\' or HEX codes as \'#808080\'. See available colors in https://www.w3.org/TR/css-color-4/#named-colors.  Default is \'black\'.'
        )
        self.parser.add_argument(
            '--arrow_gap_pixels', type=int, default=2, help='Space before arrow and chart in pixels. Default is 2.'
        )
        self.parser.add_argument(
            '--symbol_color', type=str, default='black', help='Symbol color when parameter \'--no_symbols\' is not used. Colors can be specified with names as \'gray\', RGB coordinates as \'128,128,128\' or HEX codes as \'#808080\'. See available colors in https://www.w3.org/TR/css-color-4/#named-colors.  Default is \'black\'.'
        )
        self.parser.add_argument(
            '--symbol_line_width', type=int, default=1, help='Symbol line width when parameter \'--no_symbols\' is not used. Default is 1.'
        )

    def _postprocess_arguments(self):
        """Tune some arguments depending on user options"""
        self._postprocess_colors()
        self.args.input_file = Path(self.args.input_file)
        self.args.show_backstitch = True if self.args.backstitch_option != 'none' else False
        self.args.clean_confetti_wout_neighbors = True if self.args.confetti_cleaner in ['moderate', 'strong'] else False
        self.args.clean_confetti_w1_diagonal_neighbor = True if self.args.confetti_cleaner == 'strong' else False
        self.args.arrow_fill_color = self.args.arrow_color  # user don't need such detail
        self.args.arrow_line_width = 2  # user don't need such detail
        self.args.symbol_fill_color = self.args.symbol_color  # user don't need such detail
        self.args.save_formats = []
        if self.args.save_as_svg is True:
            self.args.save_formats.append('svg')
        if self.args.save_as_png is True:
            self.args.save_formats.append('png')
        if self.args.save_as_pdf is True:
            self.args.save_formats.append('pdf')

    def _postprocess_colors(self):
        """Convert RGB coords 20,20,20 to rgb(20,20,20)"""
        for arg in vars(self):
            if arg.endswith('_color'):
                value = getattr(self, arg)
                if value.count(',') == 2:  # then RGB coords
                    setattr(self, arg, f'rgb({arg})')

    def _check_arguments(self) -> None:
        """Check some user arguments"""
        if not self.args.input_file.exists():
            raise FileNotFoundError(f'File \'{self.args.input_file}\' not found')
        if not N_COLOR_RANGE[0] <= self.args.n_colors <= N_COLOR_RANGE[1]:
            raise ValueError(f'Parameter \'n_colors\' must be between {N_COLOR_RANGE[0]} and {N_COLOR_RANGE[1]}')
        if self.args.stitches_per_row > MAX_STITCHES_PER_ROW_RECOMMENDED:
            warn(
                f'Parameter \'stitches_per_row\' is over the recommended limit of {MAX_STITCHES_PER_ROW_RECOMMENDED}, '
                f'this make take some time'
            )
        self._check_colors()

    def _check_colors(self) -> None:
        """Check if colors are valid"""    
        for arg in vars(self):
            if arg.endswith('_color'):
                value = getattr(self, arg)
                if is_valid_color(value) is False:
                    raise ValueError(f'Parameter {arg} is not a valid color')

    def _get_general_config(self) -> GeneralConfig:
        """Get general config as dataclass"""
        return GeneralConfig(
            input_file = self.args.input_file,
            n_colors = self.args.n_colors,
            stitches_per_row = self.args.stitches_per_row,
            show_colors = self.args.show_colors,
            show_symbols = self.args.show_symbols,
            show_legend = self.args.show_legend,
            save_formats = self.args.save_formats,
            png_scale = self.args.png_scale,
        )

    def _get_other_config(self) -> OtherConfig:
        """Get other config as dataclass"""
        return OtherConfig(
            method = self.args.method,
            clean_confetti_wout_neighbors = self.args.clean_confetti_wout_neighbors,
            clean_confetti_w1_diagonal_neighbor = self.args.clean_confetti_w1_diagonal_neighbor,
            ignore_background = self.args.ignore_background,
            background_code = self.args.background_code,
            show_backstitch = self.args.show_backstitch,
            backstitch_option = self.args.backstitch_option,
            backstitch_code = self.args.backstitch_code,
            backstitch_code_no_colors = self.args.backstitch_code_no_colors,
            backstitch_line_width = self.args.backstitch_line_width,
        )

    def _get_thread_config(self) -> ThreadConfig:
        """Get thread config as dataclass"""
        return ThreadConfig(
            fabric_count = self.args.fabric_count,
            strands = self.args.strands,
            skein_length = self.args.skein_length,
            strands_per_skein = self.args.strands_per_skein,
        )
    def _get_legend_config(self) -> LegendConfig:
        """Get legend config as dataclass"""
        return LegendConfig(
            title = self.args.legend_title,
            title_font_size = self.args.legend_title_font_size,
            title_font_color = self.args.legend_title_font_color,
            title_font_weight = self.args.legend_title_font_weight,
            title_x_pixels = self.args.legend_title_x_pixels,
            title_y_pixels = self.args.legend_title_y_pixels,
            item_x_pixels = self.args.legend_item_x_pixels,
            item_y_pixels = self.args.legend_item_y_pixels,
            column_width_pixels = self.args.legend_column_width_pixels,
            column_height_pixels = self.args.legend_column_height_pixels,
            code_font_color = self.args.legend_code_font_color,
            code_font_size = self.args.legend_code_font_size,
            box_line_color = self.args.legend_box_line_color,
            box_line_width = self.args.legend_box_line_width,
        )

    def _get_pattern_config(self) -> PatternConfig:
        """Get pattern config as dataclass"""
        return PatternConfig(
            svg_pixels_per_unit = self.args.svg_pixels_per_unit,
            major_grid_step_pixels = self.args.major_grid_step_pixels,
            major_grid_color = self.args.major_grid_color,
            major_grid_width = self.args.major_grid_width,
            minor_grid_color = self.args.minor_grid_color,
            minor_grid_width = self.args.minor_grid_width,
            coords_font_size = self.args.coords_font_size,
            coords_font_color = self.args.coords_font_color,
            coords_step_pixels = self.args.coords_step_pixels,
            coords_gap_pixels = self.args.coords_gap_pixels,
            arrow_color = self.args.arrow_color,
            arrow_line_width = self.args.arrow_line_width,
            arrow_fill_color = self.args.arrow_fill_color,
            arrow_gap_pixels = self.args.arrow_gap_pixels,
            symbol_color = self.args.symbol_color,
            symbol_fill_color = self.args.symbol_fill_color,
            symbol_line_width = self.args.symbol_line_width,
        )

if __name__ == '__main__':

    argument_parser = ArgumentParser()
    argument_parser.parse_arguments()
    general_config, other_config, thread_config, legend_config, pattern_config = argument_parser.get_configurations()
    pass