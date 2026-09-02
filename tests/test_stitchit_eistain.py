from pathlib import Path
from src.stitchit import stitchit

from base_test import assert_output, setup_method


INP_NAME = Path('einstain.jpg')
DEFAULT_N_COLORS = 5
DEFAULT_STITCHES_PER_ROW = 80

def test_default_values(request):
    args = {
        'n-colors': DEFAULT_N_COLORS,
        'stitches-per-row': DEFAULT_STITCHES_PER_ROW,
    }
    tmp_file = setup_method(request, INP_NAME, args)
    stitchit()
    assert_output(INP_NAME, tmp_file)

def test_method_euclidean(request):
    args = {
        'n-colors': DEFAULT_N_COLORS,
        'stitches-per-row': DEFAULT_STITCHES_PER_ROW,
        'method': 'euclidean',
    }
    tmp_file = setup_method(request, INP_NAME, args)
    stitchit()
    assert_output(INP_NAME, tmp_file)

def test_method_de76(request):
    args = {
        'n-colors': DEFAULT_N_COLORS,
        'stitches-per-row': DEFAULT_STITCHES_PER_ROW,
        'method': 'de76',
    }
    tmp_file = setup_method(request, INP_NAME, args)
    stitchit()
    assert_output(INP_NAME, tmp_file)

def test_n_colors_20(request):
    args = {
        'n-colors': 20,
        'stitches-per-row': DEFAULT_STITCHES_PER_ROW,
    }
    tmp_file = setup_method(request, INP_NAME, args)
    stitchit()
    assert_output(INP_NAME, tmp_file)

def test_all_args(request):
    args = {
        'n-colors': 20,
        'stitches-per-row': DEFAULT_STITCHES_PER_ROW,
        'background-code': 211,
        'backstitch-option': 'inverse',
        'backstitch-code': 349,
        'fabric-count': 20,
        'strands': 10,
        'skein-length-meters': 10,
        'strands-per-skein': 10,
        'legend-title': 'Dummy title',
        'legend-title-font-size': 30,
        'legend-title-font-color': 'blue',
        'legend-title-font-weight': 'normal',
        'legend-title-x-pixels': 50,
        'legend-title-y-pixels': 50,
        'legend-item-x-pixels': 50,
        'legend-item-y-pixels': 50,
        'legend-column-width-pixels': 300,
        'legend-column-height-pixels': 100,
        'legend-code-font-color': '#0000ff',
        'legend-code-font-size': 20,
        'legend-box-line-color': '#ff0000',
        'legend-box-line-width': 2,
        'major-grid-step-pixels': 80,
        'major-grid-color': "#6a00ff",
        'major-grid-width': 4,
        'minor-grid-step-pixels': 30,
        'minor-grid-color': '#aaaaaa',
        'minor-grid-width': 2,
        'coords-font-size': 20,
        'coords-font-color': '#00ff00',
        'coords-step-units': 9,
        'coords-gap-pixels': 7,
        'arrow-color': "#ff9900",
        'arrow-gap-pixels': 10,
        'symbol-color': 'darkred',
        'symbol-line-width': 2,
        'backstitch-line-width': 3, 
    }
    tmp_file = setup_method(request, INP_NAME, args)
    stitchit()
    assert_output(INP_NAME, tmp_file)