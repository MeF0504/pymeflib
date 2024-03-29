import os
import sys
import json
from pathlib import Path
from typing import Literal, Optional, Union, Any, List, Dict, Tuple
from logging import getLogger, NullHandler, Logger

BG = {
        'k': '\033[40m',
        'w': '\033[47m',
        'r': '\033[41m',
        'g': '\033[42m',
        'b': '\033[44m',
        'm': '\033[45m',
        'c': '\033[46m',
        'y': '\033[43m'}
FG = {
        'k': '\033[30m',
        'w': '\033[37m',
        'r': '\033[31m',
        'g': '\033[32m',
        'b': '\033[34m',
        'm': '\033[35m',
        'c': '\033[36m',
        'y': '\033[33m'}
END = '\033[0m'

__col_list: Optional[Dict[str, Union[Dict[str, Union[str, int, None]],
                                     str, Tuple[float]]
                          ]] = None

ColTypes = Literal['k', 'w', 'r', 'g', 'b', 'c', 'm', 'y']

__logger = getLogger(__name__)
__null_hdlr = NullHandler()
__logger.addHandler(__null_hdlr)


def BG256(n: int) -> str:
    """
    return escape codes of background for 256-color terminal.

    Parameters
    ----------
    n: 0 - 255
        color index.

    Returns
    -------
    str
        escape code
    """
    if (0 <= n < 256):
        return '\033[48;5;%dm' % n
    else:
        return ''


def FG256(n: int) -> str:
    """
    return escape codes of foreground for 256-color terminal.

    Parameters
    ----------
    n: 0 - 255
        color index.

    Returns
    -------
    str
        escape code
    """
    if (0 <= n < 256):
        return '\033[38;5;%dm' % n
    else:
        return ''


def make_bitmap(filename: Union[str, Path], rgb: Any,
                bmp_type: Literal['Windows', 'OS/2'] = 'Windows',
                verbose: bool = False, logger: Optional[Logger] = None
                ) -> None:
    """
    create a bitmap file.

    Parameters
    ----------
    filename: str or pathlike-object
        name of saved file.
    rgb: numpy.ndarray
        image data.
        shape of this data is [width, height, color] and length of color is
        3 ([red, blue, green]) or 4 ([red, green, blue, alpha]).
        NOTE: bitmap does't support alpha values.
    bmp_type: Windows or OS/2
        bitmap type. Windows or OS/2 is selectable.
        see e.g., https://en.wikipedia.org/wiki/BMP_file_format for detail.
    verbose: bool
        print details.
    logger: None or logging.Logger
        specify logger. if None, nothing will be logged.

    Returns
    -------
    None
    """
    if logger is None:
        logger = __logger
    if rgb.shape[-1] == 4:
        rgb = rgb[:, :, [0, 1, 2]]

    height, width, cols = rgb.shape
    logger.info(f'{height}x{width}x{cols}')
    logger.info(f'bitmap type: {bmp_type}')

    # make color table (it doesn't need in 24bmp format.)
    # q_bit = 256
    color_table: List[int] = []
    # for r in range(q_bit):
    #     for g in range(q_bit):
    #         for b in range(q_bit):
    #             color_table += [int(b), int(g), int(r), int(0)]
    # logger.debug(f'color table: ({len(color_table)}); {color_table[:10]}')
    len_cols = len(color_table)
    num_cols = len(color_table) >> 2

    # make pixel data
    img_data = []
    for i in range(height):
        line_data = []
        for j in range(width):
            r, g, b = rgb[height-i-1, j]     # starts from left botom
            line_data += [b, g, r]
        # line length should be a multiple of 4 bytes (long).
        padding = 4*(int((len(line_data)-1)/4)+1)-len(line_data)
        for k in range(padding):
            line_data.append(0)
        img_data += line_data
    print_st = f'{img_data[0]}, '
    print_end = f'{img_data[-1]}'
    for i in range(1, 6):
        print_st += f'{img_data[i]}, '
        print_end = f'{img_data[-i-1]}, ' + print_end
    logger.debug(f'pixel data: ({len(img_data)}); [{print_st} ... {print_end}')
    len_data = len(img_data)

    if bmp_type == 'Windows':
        offset = 0x0e+0x28+len_cols
    elif bmp_type == 'OS/2':
        offset = 0x0e+0x0c+len_cols
    else:
        print('incorrect file format: {}.'.format(bmp_type), file=sys.stderr)
        return None
    file_size = offset+len_data

    # make binary data
    # FILE_HEADER
    b = bytearray([0x42, 0x4d])                 # signature 'BM'
    b.extend(file_size.to_bytes(4, 'little'))   # file size
    b.extend((0).to_bytes(2, 'little'))         # reserved
    b.extend((0).to_bytes(2, 'little'))         # reserved
    b.extend(offset.to_bytes(4, 'little'))      # offset

    # INFO_HEADER
    if bmp_type == 'Windows':
        b.extend((0x28).to_bytes(4, 'little'))      # size of header
        b.extend(width.to_bytes(4, 'little'))       # width [dot]
        b.extend(height.to_bytes(4, 'little'))      # height [dot]
        b.extend((1).to_bytes(2, 'little'))         # number of planes
        b.extend((8*3).to_bytes(2, 'little'))       # byte/1pixel
        b.extend((0).to_bytes(4, 'little'))         # type of compression (0=BI_RGB, no compression)
        b.extend(len_data.to_bytes(4, 'little'))     # size of image
        b.extend((0).to_bytes(4, 'little'))         # horizontal resolution
        b.extend((0).to_bytes(4, 'little'))         # vertical resolution
        b.extend(num_cols.to_bytes(4, 'little'))    # number of colors (not used for 24bmp)
        b.extend((0).to_bytes(4, 'little'))         # import colors (0=all)
    elif bmp_type == 'OS/2':
        b.extend((0x0c).to_bytes(4, 'little'))      # size of header
        b.extend(width.to_bytes(2, 'little'))       # width [dot]
        b.extend(height.to_bytes(2, 'little'))      # height [dot]
        b.extend((1).to_bytes(2, 'little'))         # number of planes
        b.extend((8*3).to_bytes(2, 'little'))       # byte/1pixel

    # COLOR_TABLES
    b.extend(color_table)

    # DATA
    b.extend(img_data)

    with open(filename, 'wb') as f:
        f.write(b)

    if verbose:
        filesize = float(os.path.getsize(filename))
        prefix = ''
        if filesize > 1024**3:
            filesize /= 1024**3
            prefix = 'G'
        elif filesize > 1024**2:
            filesize /= 1024**2
            prefix = 'M'
        elif filesize > 1024:
            filesize /= 1024
            prefix = 'k'
        print('file size: {:.1f} {}B'.format(filesize, prefix))


def convert_color_name(color_name: str, color_type: Literal['256', 'full'],
                       logger: Optional[Logger] = None
                       ) -> Union[int, str, None]:
    """
    convert color name to a color id (for 256-color terminal) or
    full-color color code.

    Parameters
    ----------
    color_name: str
        color name.
    color_type: "256" or "full"
        specify the returned value.
        if color_type = "256", it returns color id.
        if color_type = "full", it returns full-color color code.
    logger: None or logging.Logger
        specify logger. if None, nothing will be logged.

    Returns
    -------
    color id (int), color code (str) of None
        the returned value depends on the color_type.
        if color_name is not found in the data set, returns None.
    """
    if logger is None:
        logger = __logger
    if color_type not in ['256', 'full']:
        logger.warning(f'incorrect color type ({color_type})')
        logger.warning('selectable type: "256" or "full". return None.')
        return None

    global __col_list
    if __col_list is None:
        color_set = os.path.dirname(__file__)+'/color_set.json'
        if os.path.isfile(color_set):
            with open(color_set, 'r') as f:
                __col_list = json.load(f)
        else:
            print('color set file is not found.')
            __col_list = {}

        try:
            import matplotlib.colors as mcolors
        except ImportError:
            logger.warning('matplotlib is not imported.')
        else:
            named_colors = mcolors.get_named_colors_mapping()
            __col_list.update(named_colors)

        for i in range(101):
            if 'gray{:d}'.format(i) in __col_list:
                continue
            gray_level = int(255*i/100+0.5)
            full_col = f'#{gray_level:02x}{gray_level:02x}{gray_level:02x}'
            __col_list[f'gray{i:d}'] = {'256': None, 'full': full_col}
            __col_list[f'grey{i:d}'] = {'256': None, 'full': full_col}

    if color_name not in __col_list:
        logger.warning('no match color name {color_name} found. return None.')
        return None
    else:
        col = __col_list[color_name]
        if type(col) is dict:
            return col[color_type]
        elif type(col) is str:
            if color_type == 'full':
                return __col_list[color_name]
            elif color_type == '256':
                r = int(col[1:3], 16)
                g = int(col[3:5], 16)
                b = int(col[5:7], 16)
                return convert_fullcolor_to_256(r, g, b)
        else:
            r, g, b = col
            if color_type == 'full':
                return '#{:02x}{:02x}{:02x}'.format(int(255*r),
                                                    int(255*g), int(255*b))
            elif color_type == '256':
                r = int(r*255)
                g = int(g*255)
                b = int(b*255)
                return convert_fullcolor_to_256(r, g, b)


def convert_256_to_fullcolor(color_index: int) -> str:
    """
    convert 256-color terminal color index to full-color color code.

    Parameters
    ----------
    color_index: int
        256-color terminal color index. this should be less than 256.

    Returns
    -------
    full-color color code.
    """
    if color_index < 16:
        color_list = [
                'Black',
                'Maroon',
                'Green',
                'Olive',
                'Navy',
                'Purple',
                'Teal',
                'Silver',
                'Grey',
                'Red',
                'Lime',
                'Yellow',
                'Blue',
                'Fuchsia',
                'Aqua',
                'White',
        ]
        return color_list[color_index]
    elif color_index < 232:
        r_index = int((color_index-16)/36)
        g_index = int((color_index-16-36*r_index)/6)
        b_index = int(color_index-16-36*r_index-6*g_index)
        if r_index != 0:
            r_index = 55+40*r_index
        if g_index != 0:
            g_index = 55+40*g_index
        if b_index != 0:
            b_index = 55+40*b_index
        return '#{:02x}{:02x}{:02x}'.format(r_index, g_index, b_index)
    elif color_index < 256:
        gray_level = 8+10*(color_index-232)
        return '#{:02x}{:02x}{:02x}'.format(gray_level, gray_level, gray_level)


def convert_fullcolor_to_256(r: int, g: int, b: int) -> int:
    """
    convert r, g, b values to a color id for 256-color terminal.

    Parameters
    ----------
    r, g, b: int [0 - 255]
        red, green, and blue values.

    Returns
    -------
    int
        color id.
    """
    r_index = int((r-55)/40+0.5)
    if r_index < 0:
        r_index = 0
    g_index = int((g-55)/40+0.5)
    if g_index < 0:
        g_index = 0
    b_index = int((b-55)/40+0.5)
    if b_index < 0:
        b_index = 0

    return 36*r_index+6*g_index+b_index+16


def main_test(num, deci):
    print('system colors')
    for i in range(8):
        if num:
            if deci:
                if i % 2 == 0:    # even
                    tmp_st = '{}{:03d}{}|'.format(FG['w'], i, END)
                else:           # odd
                    tmp_st = '{}{:03d}{}|'.format(FG['k'], i, END)
            else:
                if i % 2 == 0:    # even
                    tmp_st = '{}{:02x}{}'.format(FG['w'], i, END)
                else:           # odd
                    tmp_st = '{}{:02x}{}'.format(FG['k'], i, END)
        else:
            tmp_st = '  '
        print('{}{}{}'.format(BG256(i), tmp_st, END), end='')
    print()
    for i in range(8, 16):
        if num:
            if deci:
                if i % 2 == 0:    # even
                    tmp_st = '{}{:03d}{}|'.format(FG['w'], i, END)
                else:           # odd
                    tmp_st = '{}{:03d}{}|'.format(FG['k'], i, END)
            else:
                if i % 2 == 0:    # even
                    tmp_st = '{}{:02x}{}'.format(FG['w'], i, END)
                else:           # odd
                    tmp_st = '{}{:02x}{}'.format(FG['k'], i, END)
        else:
            tmp_st = '  '
        print('{}{}{}'.format(BG256(i), tmp_st, END), end='')
    print('\n')

    print('6x6x6 color blocks')
    for g in range(6):
        for r in range(6):
            for b in range(6):
                i = 36*r+6*g+b+16
                if num:
                    if deci:
                        if i % 2 == 0:    # even
                            tmp_st = '{}{:03d}{}'.format(FG['w'], i, END)
                        else:           # odd
                            tmp_st = '{}{:03d}{}'.format(FG['k'], i, END)
                    else:
                        if i % 2 == 0:    # even
                            tmp_st = '{}{:02x}{}'.format(FG['w'], i, END)
                        else:           # odd
                            tmp_st = '{}{:02x}{}'.format(FG['k'], i, END)
                else:
                    tmp_st = '  '
                print('{}{}{}'.format(BG256(i), tmp_st, END), end='')
            print(' ', end='')
        print()
    print()

    print('gray scales')
    st = 6*6*6+16
    for i in range(st, 256):
        if num:
            if deci:
                tmp_st = '{}{:03d}{}|'.format(FG256(255+st-i), i, END)
            else:
                tmp_st = '{}{:02x}{}'.format(FG256(255+st-i), i, END)
        else:
            tmp_st = '  '
        print('{}{}{}'.format(BG256(i), tmp_st, END), end='')
    print('\n')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', help='show number', action='store_true')
    parser.add_argument('-d', help='show in decimal number format',
                        action='store_true')
    args = parser.parse_args()

    main_test(args.n, args.d)
