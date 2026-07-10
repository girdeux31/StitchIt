import sys
from warnings import warn
from pathlib import Path

from legend import Legend
from pattern import Pattern
from thread import Thread

MAX_STITCHES_PER_ROW_RECOMMENDED = 125  # TODO check why waves takes so much less than bird


# TODO:
#  1. average pixel colors "by hand"
#  2. user arguments: codes_wo_symbols, backstich_codes
#  3. help function
#  4. backstitch function
#  5. change readme
#  6. LAB distance
#  7. add numbers multiple of 10 in outer square

if __name__ == '__main__':

    # Process user arguments

    # if(len(sys.argv)<3):
    #     print("function requires an input filename, number of colors, stitch count and mode")
    #     sys.exit(0)

    # input_file = Path(sys.argv[1])       # input file name, has to be a jpg
    # colors = int(sys.argv[2])    # number of colors to use in the pattern
    # stitches_per_row = int(sys.argv[3])   # stitch count, number of stitches in x axis

    # Just for debugging
    input_file = Path('examples/bird.jpg')
    colors = 3
    stitches_per_row = 60  # FIX there is one less stitch in output
    scale = 2.0  # png scale
    fabric_count = 14  # aida or squares per inch
    strands_for_stitching = 2  # strands for stitching

    # input_file = Path('examples/ita.jpg')
    # colors = 3
    # stitches_per_row = 100
    # scale = 2.0

    # input_file = Path('examples/waves.jpg')
    # colors = 10
    # stitches_per_row = 140
    # scale = 1.0

    if not input_file.exists():
        raise FileNotFoundError(f'File \'{input_file}\' not found')
    if not 2 <= colors <= 256:
        raise ValueError('Parameter \'colors\' must be in range [2, 256]')
    if stitches_per_row > MAX_STITCHES_PER_ROW_RECOMMENDED:
        warn(
            f'Parameter \'stitches_per_row\' is over the recommended limit of {MAX_STITCHES_PER_ROW_RECOMMENDED}, '
            f'this make take some time'
        )

    # Generate file paths

    out_pattern_file = input_file.with_stem(f'{input_file.stem}_pattern').with_suffix('')
    out_legend_file = input_file.with_stem(f'{input_file.stem}_legend').with_suffix('')

    # Generate pattern svg

    pattern = Pattern(color=True, symbols=True)
    pattern.process_image(input_file, colors, stitches_per_row)
    pattern.generate()
    pattern.save(out_pattern_file, formats=['svg', 'png', 'pdf'], png_scale=scale)

    # Generate legend svg

    legend = Legend(color=True, symbols=True)
    legend.generate(pattern)
    legend.save(out_legend_file)

    # Print thread info

    thread = Thread(fabric_count, strands_for_stitching)
    thread.import_pattern(pattern)
    thread.print_info()
