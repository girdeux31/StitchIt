from pathlib import Path
from src.stitchit import stitchit

from base_test import assert_output, setup_method


INP_NAME = Path('einstain.jpg')
DEFAULT_N_COLORS = 5
DEFAULT_STITCHES_PER_ROW = 80

def test_default_values(request):
    args = {
        'n_colors': DEFAULT_N_COLORS,
        'stitches_per_row': DEFAULT_STITCHES_PER_ROW,
    }
    tmp_file = setup_method(request, INP_NAME, args)
    stitchit()
    assert_output(INP_NAME, tmp_file)

def test_method_euclidean(request):
    args = {
        'n_colors': DEFAULT_N_COLORS,
        'stitches_per_row': DEFAULT_STITCHES_PER_ROW,
        'method': 'euclidean',
    }
    tmp_file = setup_method(request, INP_NAME, args)
    stitchit()
    assert_output(INP_NAME, tmp_file)

def test_method_de76(request):
    args = {
        'n_colors': DEFAULT_N_COLORS,
        'stitches_per_row': DEFAULT_STITCHES_PER_ROW,
        'method': 'de76',
    }
    tmp_file = setup_method(request, INP_NAME, args)
    stitchit()
    assert_output(INP_NAME, tmp_file)

def test_n_colors_20(request):
    args = {
        'n_colors': 20,
        'stitches_per_row': DEFAULT_STITCHES_PER_ROW,
    }
    tmp_file = setup_method(request, INP_NAME, args)
    stitchit()
    assert_output(INP_NAME, tmp_file)

def test_all_args(request):
    args = {
        'n_colors': 20,
        'stitches_per_row': DEFAULT_STITCHES_PER_ROW,
        'backstitch_option': 'inverse',
        'backstitch_code': 349,
        'fabric_count': 20,
        'strands': 10,
        'skein_length': 10,
        'strands_per_skein': 10,
        'legend_title': 'Dummy title',
        'legend_title_font_size': 30,
        'legend_title_font_color': 'blue',
        'legend_title_font_weight': 'normal',
        'legend_title_x_pixels': 50,
        'legend_title_y_pixels': 50,
        'legend_item_x_pixels': 50,
        'legend_item_y_pixels': 50,
        'legend_column_width_pixels': 300,
        'legend_column_height_pixels': 100,
        'legend_code_font_color': '#0000ff',
        'legend_code_font_size': 20,
        'legend_box_line_color': '#ff0000',
        'legend_box_line_width': 2,
        'major_grid_step_pixels': 80,
        'major_grid_color': "#6a00ff",
        'major_grid_width': 4,
        'minor_grid_step_pixels': 30,
        'minor_grid_color': '#aaaaaa',
        'minor_grid_width': 2,
        'coords_font_size': 20,
        'coords_font_color': '#00ff00',
        'coords_step_units': 9,
        'coords_gap_pixels': 7,
        'arrow_color': "#ff9900",
        'arrow_gap_pixels': 10,
        'symbol_color': 'darkred',
        'symbol_line_width': 2,
        'backstitch_line_width': 3, 
    }
    tmp_file = setup_method(request, INP_NAME, args)
    stitchit()
    assert_output(INP_NAME, tmp_file)