import os
import os.path as op
import platform
from logging import getLogger, NullHandler, Logger
from typing import Optional

__logger = getLogger(__name__)
__null_hdlr = NullHandler()
__logger.addHandler(__null_hdlr)


def mkdir(path: str) -> None:
    """
    make a directory safely.

    Parameters
    ----------
    path: str
        directory path.

    Returns
    -------
    None
    """
    path = op.expanduser(path)
    if not op.exists(path):
        print('mkdir '+path)
        os.makedirs(path, mode=0o755)
        # os.chmod(path,0755)


def chk_cmd(cmd: str, logger: Optional[Logger] = None) -> bool:
    """
    check the command exists and is executable.

    Parameters
    ----------
    cmd: str
        the checked command.
        both the command itself or full path of that command is acceptable.

    Returns
    -------
    None
    """
    if logger is None:
        logger = __logger
    full_path = os.path.expanduser(os.path.expandvars(cmd))
    if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
        logger.info(f'find {full_path}')
        return True

    if 'PATH' not in os.environ:
        logger.warning("PATH isn't found in environment values.")
        return False

    if platform.uname()[0] == 'Windows':
        cmd = '{}.exe'.format(cmd)
    for path in os.environ['PATH'].split(os.pathsep):
        cmd_path = op.join(path, cmd)
        if op.isfile(cmd_path) and os.access(cmd_path, os.X_OK):
            logger.info(f'find {cmd} ... {cmd_path}')
            return True
    logger.info(f'command {cmd} is not found.')
    return False
