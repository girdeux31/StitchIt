import sys
from pathlib import Path

from argument_parser import ArgumentParser
from chart import Chart
from info_file import InfoFile


# TODO:
#  - tests
#  - change readme
#  - bs with inverse rgb color

def stitchit():
    """
    Generates a cross stitch pattern from an image.

    Usage:

        python3 stitchit.py input_file n_colors, stitches_per_row

    Arguments:

        - input_file (str): image to process
        - n_colors (int): number of colors to use to stitch
        - stitches_per_row (int): number of stitches (squares) per row
    """
    # Process input arguments

    argument_parser = ArgumentParser()
    argument_parser.parse_arguments()
    general_config, other_config, thread_config, legend_config, pattern_config = argument_parser.get_configurations()

    # Generate file paths

    chart_file = general_config.input_file.with_stem(f'{general_config.input_file.stem}_chart').with_suffix('')
    txt_file = general_config.input_file.with_stem(f'{general_config.input_file.stem}_info').with_suffix('.txt')

    # Generate pattern svg

    chart = Chart(general_config, other_config, legend_config, pattern_config)
    chart.process()
    chart.generate()
    chart.save(chart_file)

    # Write info file 

    info_file = InfoFile(thread_config)
    info_file.import_chart(chart)
    info_file.save(txt_file)

if __name__ == '__main__':

    stitchit()    
