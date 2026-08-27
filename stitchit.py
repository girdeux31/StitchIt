import sys
from pathlib import Path

from argument_parser import ArgumentParser
from chart import Chart
from info_file import InfoFile


# TODO:
#  - tests
#  - change readme
#  - bs with inverse rgb color
#  - get DMC codes from dmc_db.csv

def stitchit(
        input_file: Path,
        n_colors: int,
        stitches_per_row: int,
        show_colors: bool=True,
        show_symbols: bool=True,
        show_legend: bool=True,
    ):
    """
    Generates a cross stitch pattern from an image, mandatory input arguments are:

    input_file (Path): image to process
    n_colors (int): number of colors to use to stitch
    stitches_per_row (int): number of stitches (squares) per row in pattern
    """
    # argument_parser = ArgumentParser()
    # argument_parser.parse_arguments()
    # general_config, other_config, thread_config, legend_config, pattern_config = argument_parser.get_configurations()

    png_scale = 2.0  # png scale
    fabric_count = 14  # aida or squares per inch
    strands = 2  # strands for stitching
    distance_method = 'de00'  # 'euclidean', 'compuphase', 'de76', 'de00'
    save_formats = ['svg', 'png', 'pdf']

    # Generate file paths

    out_pattern_file = input_file.with_stem(f'{input_file.stem}_pattern').with_suffix('')
    out_info_file = input_file.with_stem(f'{input_file.stem}_info').with_suffix('.txt')

    # Generate pattern svg

    chart = Chart(show_colors=show_colors, show_symbols=show_symbols, show_legend=show_legend)
    chart.process(input_file, n_colors, stitches_per_row, distance_method)
    chart.generate()
    chart.save(out_pattern_file, formats=save_formats, png_scale=png_scale)

    # Write info file 

    info_file = InfoFile(fabric_count, strands)
    info_file.import_chart(chart, distance_method)
    info_file.save(out_info_file)

if __name__ == '__main__':

    # Process user arguments

    # if(len(sys.argv)<3):
    #     print("function requires an input filename, number of colors, stitch count and mode")
    #     sys.exit(0)

    # input_file = Path(sys.argv[1])       # input file name, has to be a jpg
    # n_colors = int(sys.argv[2])    # number of colors to use in the pattern
    # stitches_per_row = int(sys.argv[3])   # stitch count, number of stitches in x axis

    # input_file = Path('examples/bird.jpg')
    # n_colors = 3
    # stitches_per_row = 20

    # input_file = Path('examples/octopus.jpg')
    # n_colors = 3
    # stitches_per_row = 60

    # input_file = Path('examples/waves.jpg')
    # n_colors = 10
    # stitches_per_row = 140

    input_file = Path('examples/einstain.jpg')
    n_colors = 5
    stitches_per_row = 80

    show_colors = True
    show_symbols = True
    show_legend = True

    stitchit(
        input_file,
        n_colors,
        stitches_per_row,
        show_colors=show_colors,
        show_symbols=show_symbols,
        show_legend=show_legend
    )    
