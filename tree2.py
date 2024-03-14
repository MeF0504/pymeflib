# library that supports to show files in tree form.

from pathlib import PurePath, PurePosixPath, PureWindowsPath
from typing import Callable, Optional, Union, Tuple, List, Type
from logging import getLogger, NullHandler, Logger

branch_str = '|__ '
branch_str2 = '|   '

GC = Callable[[PurePath], Tuple[List[str], List[str]]]
AddInfo = Optional[Callable[[Union[str, PurePath]], List[str]]]
PPath = Union[Type[PurePath],
              Type[PurePosixPath],
              Type[PureWindowsPath]]


class TreeViewer():
    """

    class to treat the path-like contents

    Parameters
    ----------
    root: string
        a root path of the tree.
    get_contents: Callable
        a function to get contents of the given path.
        This function takes one argument and return directories and files
        of an any path.

        Parameters
        ----------
        path: string
            a relative path in the tree.

        Return
        ----------
        directories: list of string
            a list of directories. In this context, "directory" means
            something that contains files.
        files: list of string
            a list of files. In this context, "file" means a path that
            itself have a information.

    purepath: PurePath or PurePosixPath or PureWindowsPath
        a variable to specify the used PurePath class.

    Methods
    ----------
    show
        a function to show the tree of items.
        See the sample at the end of this file for more information.
        Parameters
        ----------
        add_info: Callable
            a function to show an additional information.

            Parameters
            ----------
            path: string
                an absolute path to an item.

            Return
            ----------
            info: string
                a string of information that you want in the tree.
                NOTE if you contain a new line code in this info, the tree
                view may collapse.

    Return
    ----------
    path: PurePath
        a relative path of the current item.
    directories: list of directories (PurePath)
        directories that is contained in the current item.
    files: list of files (PurePath)
        files that is contained in the current item.

    """

    def __init__(self, root: str, get_contents: GC,
                 purepath: PPath = PurePath,
                 logger: Optional[Logger] = None) -> None:
        assert purepath in [PurePath, PurePosixPath, PureWindowsPath]
        self.root = purepath(root)    # root path
        self.cpath = purepath('.')   # current path (relative)
        self.nextpath: Optional[PurePath] = None
        self.cnt = 0
        self.finish = False
        self.get_contents = get_contents
        self.maxcnt = -1
        if logger is None:
            _logger = getLogger(__name__)
            _null_hdlr = NullHandler()
            _logger.addHandler(_null_hdlr)
            self.logger = _logger
        else:
            self.logger = logger

    def __iter__(self) -> "TreeViewer":
        return self

    def __next__(self) -> Tuple[PurePath, List[str], List[str]]:
        if self.finish:
            raise StopIteration()
        self.cnt += 1
        if self.cnt == self.maxcnt:
            print('max count reached.')
            self.finish = True
        if self.nextpath is not None:
            self.cpath = self.nextpath
            self.logger.debug(f'set cpath: {self.cpath}')
        dirs, files = self.get_contents(self.cpath)

        # search next path.
        if dirs:
            # go down
            self.logger.debug(f'next: {dirs[0]}')
            self.nextpath = self.cpath/dirs[0]
        else:
            # go up
            tmp_path = self.cpath
            if self.is_root(tmp_path):
                # no sub directories?
                self.finish = True
            else:
                while True:
                    cur_dir = tmp_path.name
                    tmp_path = tmp_path.parent
                    self.logger.debug(f'@ {tmp_path.parts}')
                    tmp_dirs, tmp_files = self.get_contents(tmp_path)
                    self.logger.debug(f'find {cur_dir} in {tmp_dirs}')
                    if cur_dir in tmp_dirs:
                        idx = tmp_dirs.index(cur_dir)
                        if idx+1 < len(tmp_dirs):
                            self.nextpath = tmp_path/tmp_dirs[idx+1]
                            self.logger.debug(f'next path: {self.nextpath}')
                            break
                        else:
                            if self.is_root(tmp_path):
                                self.logger.debug('reached the last dir of root.')
                                self.finish = True
                                break
                    else:
                        self.logger.debug(f'{tmp_path}, {tmp_dirs}')
                        print('something wrong.')
                        raise StopIteration()
        self.logger.debug(f'return {self.cpath}, {dirs}, {files}')
        return self.cpath, dirs, files

    def is_root(self, path: Optional[PurePath] = None) -> bool:
        if path is None:
            path = self.cpath
        self.logger.debug(f'root? {path.parts}')
        if path.parts:
            return False
        else:
            return True

    def show(self, add_info: AddInfo = None) -> None:
        fullpath = self.root/self.cpath
        dirs, files = self.get_contents(self.cpath)
        self.logger.debug(f'show: {self.cpath.parts} !!')
        if self.is_root():
            # root
            print('{}/'.format(self.root))
            for f in files:
                if add_info is None:
                    add_info_pre, add_info_post = ['', '']
                else:
                    add_info_pre, add_info_post = add_info(fullpath/f)

                print('{}{}{}{}'.format(branch_str, add_info_pre,
                                        f, add_info_post))
        else:
            if add_info is None:
                add_info_pre, add_info_post = ['', '']
            else:
                add_info_pre, add_info_post = add_info(fullpath)

            dnum = len(self.cpath.parts)-1
            print('{}{}{}{}/{}'.format(branch_str2*(dnum), branch_str,
                                       add_info_pre, self.cpath.name,
                                       add_info_post))
            for f in files:
                if add_info is None:
                    add_info_pre, add_info_post = ['', '']
                else:
                    add_info_pre, add_info_post = add_info(fullpath/f)

                print('{}{}{}{}{}'.format(branch_str2*(dnum+1), branch_str,
                                          add_info_pre, f, add_info_post))


def show_tree(root: str, get_contents: GC,
              add_info: AddInfo = None, purepath: PPath = PurePath) -> None:
    tree_view = TreeViewer(root, get_contents, purepath)
    for cpath, dirs, files in tree_view:
        tree_view.show(add_info)


if __name__ == '__main__':
    from pathlib import Path
    from functools import partial

    def get_contents(root, cpath):
        fullpath = Path(root)/cpath
        dirs = []
        files = []
        for f in fullpath.glob('*'):
            if f.is_file():
                files.append(f.name)
            elif f.is_dir():
                dirs.append(f.name)
        return dirs, files

    show_tree('.', partial(get_contents, '.'))
