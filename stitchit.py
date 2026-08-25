import sys
from warnings import warn
from pathlib import Path

from pattern import Pattern
from info_file import InfoFile

MAX_STITCHES_PER_ROW_RECOMMENDED = 125  # TODO check why waves takes so much less than bird
ALLOWED_DISTANCE_METHODS = ['euclidean', 'compuphase', 'de76', 'de00']


# TODO:
#  - use argparse
#  - change readme
#  - legend as columns
#  - increase by 1 n_colors if ignore_bg is True
#  - refactor: pattern is chart, then inside a new class pattern you have things like
# _change_background_index, _get_background_idx and extract pattern from image
# new class cleaner with methods related with clean confetti

def stitchit(
        input_file: Path,
        n_colors: int,
        stitches_per_row: int,
        show_colors: bool=True,
        show_symbols: bool=True,
        show_legend: bool=True,
    ):
    """
    Generates a cross stitch pattern from an image, input arguments are:

    input_file (Path): image to process
    n_colors (int): number of colors to use to stitch
    stitches_per_row (int): number of stitches (squares) per row in pattern
    """
    png_scale = 2.0  # png scale
    fabric_count = 14  # aida or squares per inch
    strands_for_stitching = 2  # strands for stitching
    distance_method = 'de00'  # 'euclidean', 'compuphase', 'de76', 'de00'

    if not input_file.exists():
        raise FileNotFoundError(f'File \'{input_file}\' not found')
    if not 2 <= n_colors <= 256:
        raise ValueError('Parameter \'n_colors\' must be in range [2, 256]')
    if stitches_per_row > MAX_STITCHES_PER_ROW_RECOMMENDED:
        warn(
            f'Parameter \'stitches_per_row\' is over the recommended limit of {MAX_STITCHES_PER_ROW_RECOMMENDED}, '
            f'this make take some time'
        )
    distance_method = distance_method.lower()
    if distance_method not in ALLOWED_DISTANCE_METHODS:
        raise ValueError(f'Allowed distance methods are {", ".join(ALLOWED_DISTANCE_METHODS)}')

    # Generate file paths

    out_pattern_file = input_file.with_stem(f'{input_file.stem}_pattern').with_suffix('')
    out_info_file = input_file.with_stem(f'{input_file.stem}_info').with_suffix('.txt')

    # Generate pattern svg

    pattern = Pattern(show_colors=show_colors, show_symbols=show_symbols, show_legend=show_legend)
    pattern.process_image(input_file, n_colors, stitches_per_row, distance_method)
    pattern.generate()
    pattern.save(out_pattern_file, formats=['svg', 'png', 'pdf'], png_scale=png_scale)

    # Write info file 

    info_file = InfoFile(fabric_count, strands_for_stitching)
    info_file.import_pattern(pattern, distance_method)
    info_file.save(out_info_file)

if __name__ == '__main__':

    # Process user arguments

    # if(len(sys.argv)<3):
    #     print("function requires an input filename, number of colors, stitch count and mode")
    #     sys.exit(0)

    # input_file = Path(sys.argv[1])       # input file name, has to be a jpg
    # n_colors = int(sys.argv[2])    # number of colors to use in the pattern
    # stitches_per_row = int(sys.argv[3])   # stitch count, number of stitches in x axis

    input_file = Path('examples/bird.jpg')
    n_colors = 3  # includes background even if ignore_background is True
    stitches_per_row = 20

    # input_file = Path('examples/octopus.jpg')
    # n_colors = 3
    # stitches_per_row = 60

    # input_file = Path('examples/waves.jpg')
    # n_colors = 10
    # stitches_per_row = 140

    # input_file = Path('examples/einstain.jpg')
    # n_colors = 5
    # stitches_per_row = 80

    show_colors = True
    show_symbols = True
    show_legend = True

    stitchit(input_file, n_colors, stitches_per_row, show_colors=show_colors, show_symbols=show_symbols, show_legend=show_legend)    
