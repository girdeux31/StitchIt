from src.argument_parser import ArgumentParser
from src.chart import Chart
from src.info_file import InfoFile


def stitchit():
    """
    Generates a cross stitch pattern from an image.

    Usage:

        python3 stitchit.py -i input_file -n n_colors -s stitches_per_row

    Arguments:

        - input_file (str): image to process
        - n_colors (int): number of DMC colors
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

    info_file = InfoFile(other_config, thread_config)
    info_file.import_chart(chart)
    info_file.save(txt_file)

if __name__ == '__main__':

    stitchit()    
