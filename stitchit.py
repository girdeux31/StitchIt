import sys
from warnings import warn
from pathlib import Path

from pattern import Pattern
from info_file import InfoFile

MAX_STITCHES_PER_ROW_RECOMMENDED = 125  # TODO check why waves takes so much less than bird
ALLOWED_DISTANCE_METHODS = ['euclidean', 'compuphase', 'de76', 'de00']


# TODO:
#  - backstitch function
#  - user arguments: backstitch_codes
#  - use argparse
#  - way to change format options, yml or by optional arguments
#  - change readme


if __name__ == '__main__':

    # Process user arguments

    # if(len(sys.argv)<3):
    #     print("function requires an input filename, number of colors, stitch count and mode")
    #     sys.exit(0)

    # input_file = Path(sys.argv[1])       # input file name, has to be a jpg
    # n_colors = int(sys.argv[2])    # number of colors to use in the pattern
    # stitches_per_row = int(sys.argv[3])   # stitch count, number of stitches in x axis

    # Just for debugging
    input_file = Path('examples/bird.jpg')
    n_colors = 3
    stitches_per_row = 60  # FIX: there is one less stitch in output
    png_scale = 2.0  # png scale
    fabric_count = 14  # aida or squares per inch
    strands_for_stitching = 2  # strands for stitching
    distance_method = 'de00'  # 'euclidean', 'compuphase', 'de76', 'de00'

    # input_file = Path('examples/ita.jpg')
    # n_colors = 3
    # stitches_per_row = 100
    # png_scale = 2.0

    # input_file = Path('examples/waves.jpg')
    # n_colors = 10
    # stitches_per_row = 140
    # png_scale = 1.0

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

    pattern = Pattern(color=True, symbols=True, legend=True)
    pattern.process_image(input_file, n_colors, stitches_per_row, distance_method)
    pattern.generate()
    pattern.save(out_pattern_file, formats=['svg', 'png', 'pdf'], png_scale=png_scale)

    # Write info file 

    info_file = InfoFile(fabric_count, strands_for_stitching)
    info_file.import_pattern(pattern, distance_method)
    info_file.save(out_info_file)
