import os
import os.path as op
import platform


def mkdir(path):
    path = op.expanduser(path)
    if not op.exists(path):
        print('mkdir '+path)
        os.makedirs(path, mode=0o755)
        # os.chmod(path,0755)


def chk_cmd(cmd, verbose=False):   # check the command exists.
    full_path = os.path.expanduser(os.path.expandvars(cmd))
    if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
        if verbose:
            print('find {}'.format(full_path))
        return True

    if 'PATH' not in os.environ:
        if verbose:
            print("PATH isn't found in environment values.")
        return False

    if platform.uname()[0] == 'Windows':
        cmd = '{}.exe'.format(cmd)
    for path in os.environ['PATH'].split(os.pathsep):
        cmd_path = op.join(path, cmd)
        if op.isfile(cmd_path) and os.access(cmd_path, os.X_OK):
            if verbose:
                print('find {} ... {}'.format(cmd,  cmd_path))
            return True
    if verbose:
        print('command {} is not found.'.format(cmd))
    return False
