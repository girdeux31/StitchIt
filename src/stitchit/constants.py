MIN_STITCHES_PER_ROW = 10
MAX_STITCHES_PER_ROW_RECOMMENDED = 125  # TODO check why waves takes so much less than bird
BACKGROUND_INDEX = 255  # must be between n_colors and 255 inclusive since pattern is uint8
BACKSTITCH_INDEX = 254
INVERSE_BACKSTITCH_DELTA_INDEX = 100
CM_PER_INCH = 2.54  # cm/inch
CM_PER_M = 100  # cm/m
TABLE_FORMAT = 'simple'
CSV_REL_PATH = 'data/dmc_db.csv'

METHOD_OPTIONS = ['euclidean', 'de76', 'de00']
CLEANER_OPTIONS = ['none', 'moderate', 'strong']
BACKSTITCH_OPTIONS = ['none', 'constant', 'inverse']
FONT_WEIGHT_OPTIONS = ['normal', 'bold']
N_COLOR_RANGE = [2, 100]

SYMBOLS_TO_FILL = [2, 6, 7, 10]
TABLE_HEADER = [
    'DMC code',
    'DMC color',
    'DMC RGB',
    'Stitches',
    'Length (m)',
    'Skeins',
    'MSE'
]

METHOD_TO_COLOR_THRESHOLD = {
    'euclidean': 30,
    'de76': 10,
    'de00': 10,
}  # increase if colors in chart are too similar
FABRIC_COUNT_TO_STITCH_LENGTH = {
    11: 2.10,  # number of squares (or stitches) per inch, thread length in cm
    14: 1.80,
    16: 1.60,
    18: 1.45,
    20: 1.30,
}
IDX_TO_SYMBOL_CODE = {
    0: "M4 4L16 16", # backslash
    1: "M4 16L16 4M4 10L 16 10", # forward slash
    2: "M7 7L7 13 13 13 13 7Z", # little square, filled black
    3: "M4 4L10 16L16 4 Z", # triangle, upside down
    4: "M4 4L16 16M4 16 L16 4", # diagonal cross
    5: "M4 4L4 16 16 16 16 4Z", # square
    6: "M4 4L10 16L16 4 Z", # triangle, upside down, filled black
    7: "M10 4L6 10 10 16 14 10Z", # diamond, filled black
    8: "M8 8L8 12 12 12 12 8Z", # little square
    9: "M4 4L16 16M4 16 L16 4M10 4L10 16M4 10L16 10", # 8 way cross
    10: "M4 4L4 16 16 16 16 4Z", # square, filled black
}
