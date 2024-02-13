import os
import sys
import subprocess
from typing import Union

from .color import FG, BG, END, FG256, BG256

__debug = False


def __cprint(msg, fg, bg, **kwargs):
    if type(fg) is str and fg in FG:
        fg_str = FG[fg]
    elif type(fg) is int and 0 <= fg <= 255:
        fg_str = FG256(fg)
    elif fg is None:
        fg_str = ''
    else:
        if __debug:
            print(f'incorrect type for fg: {fg}')
        fg_str = ''
    if type(bg) is str and bg in BG:
        bg_str = BG[bg]
    elif type(bg) is int and 0 <= bg <= 255:
        bg_str = BG256(bg)
    elif bg is None:
        bg_str = ''
    else:
        if __debug:
            print(f'incorrect type for bg: {bg}')
        bg_str = ''
    if len(fg_str+bg_str) != 0:
        end_str = END
    else:
        end_str = ''
    print_str = f'{fg_str}{bg_str}{msg}{end_str}'
    print(print_str, **kwargs)


def __err_msg(root, cmd, fg, bg):
    __cprint('failed to run command {}. please check {}'.format(
        cmd, root),
        fg=fg, bg=bg, file=sys.stderr)


def run(root: str,
        msg_fg: Union[int, str, None] = None,
        msg_bg: Union[int, str, None] = None,
        err_fg: Union[int, str, None] = None,
        err_bg: Union[int, str, None] = None,
        def_br: str = 'main'):
    """
    update git repository at root.

    Parameters
    ----------
    root: str
        root directory.
    msg_fg, msg_bg: w, k, r, g, b, c, m, y, color code [0-255], or None
        foreground and background color of messages.
    err_fg, err_bg: w, k, r, g, b, c, m, y, color code [0-255], or None
        foreground and background color of error messages.
    def_br: str
        name of default branch. default: "main"

    Returns
    -------
    None
    """
    os.chdir(root)
    # ~~~~~~~~~~~~~~~ fetch ~~~~~~~~~~~~~~~
    cmd = 'git fetch'.split()
    __cprint('running "{}"...'.format(' '.join(cmd)), fg=msg_fg, bg=msg_bg)
    stat = subprocess.run(cmd)
    if stat.returncode != 0:
        __err_msg(root, cmd, err_fg, err_bg)
        return
    # ~~~~~~~~~~~~~~~ get branch ~~~~~~~~~~~~~~~
    cmd = 'git branch'.split()
    stat = subprocess.run(cmd, capture_output=True)
    if stat.returncode != 0:
        __err_msg(root, cmd, err_fg, err_bg)
        return
    branches = stat.stdout.decode().split()
    cur_branch = branches[branches.index('*')+1]
    if cur_branch != def_br:
        __cprint(f'checkout to {def_br}...', fg=msg_fg, bg=msg_bg)
        cmd = f'git checkout {def_br}'.split()
        stat = subprocess.run(cmd)
        if stat.returncode != 0:
            __err_msg(root, cmd, err_fg, err_bg)
            return
    # ~~~~~~~~~~~~~~~ show log ~~~~~~~~~~~~~~~
    cmd = ['git', 'log', f'HEAD..origin/{def_br}',
           '--pretty=format:%h (%ai); %s', '--graph']
    stat = subprocess.run(cmd, capture_output=True)
    if stat.returncode != 0:
        __err_msg(root, cmd, err_fg, err_bg)
        return
    if __debug:
        print('log std out: \n{}'.format(stat.stdout.decode()))
    if __debug:
        print('log std err: \n{}'.format(stat.stderr.decode()))
    if len(stat.stderr+stat.stdout) == 0:
        # no update
        __cprint('already updated.', fg=msg_fg, bg=msg_bg)
        return
    else:
        __cprint('update log;', fg=msg_fg, bg=msg_bg)
        for out in [stat.stdout.decode(), stat.stderr.decode()]:
            if out:
                if out.endswith('\n'):
                    end = ''
                else:
                    end = '\n'
                print(out, end=end)
    # ~~~~~~~~~~~~~~~ merge ~~~~~~~~~~~~~~~
    cmd = 'git merge'.split()
    __cprint('running "{}"...'.format(' '.join(cmd)), fg=msg_fg, bg=msg_bg)
    stat = subprocess.run(cmd)
    if stat.returncode != 0:
        __err_msg(root, cmd, err_fg, err_bg)
        return
    # ~~~~~~~~~~~~~~~ submodule update ~~~~~~~~~~~~~~~
    # 開発時は↓をつけないとだけど，user的には上で十分？
    # cmd = 'git submodule update --remote --merge'.split()
    cmd = 'git submodule update'.split()
    __cprint('running "{}"...'.format(' '.join(cmd)), fg=msg_fg, bg=msg_bg)
    stat = subprocess.run(cmd)
    if stat.returncode != 0:
        __err_msg(root, cmd, err_fg, err_bg)
        return
