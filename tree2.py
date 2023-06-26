# library that supports to show files in tree form.

from pathlib import PurePath
from typing import Callable, Optional

branch_str = '|__ '
branch_str2 = '|   '


class TreeViewer():
    """
    TreeViewer(root, get_contents)

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

    def __init__(self, root: str,
                 get_contents: Callable[[PurePath],
                                        tuple[list[str], list[str]]]) -> None:
        self.root = PurePath(root)    # root path
        self.cpath = PurePath('.')   # current path (relative)
        self.nextpath = None
        self.cnt = 0
        self.finish = False
        self.get_contents = get_contents
        self.maxcnt = -1
        self.debug = False

    def __iter__(self) -> None:
        return self

    def __next__(self) -> tuple[str, list[str], list[str]]:
        if self.finish:
            raise StopIteration()
        self.cnt += 1
        if self.cnt == self.maxcnt:
            print('max count reached.')
            self.finish = True
        if self.nextpath is not None:
            self.cpath = self.nextpath
            self.debugprint('set cpath: {}'.format(self.cpath))
        dirs, files = self.get_contents(self.cpath)
        # self.debugprint('{} {}'.format(dirs, files))

        # search next path.
        if dirs:
            # go down
            self.debugprint('next: {}'.format(dirs[0]))
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
                    self.debugprint('@ {}'.format(tmp_path.parts))
                    tmp_dirs, tmp_files = self.get_contents(tmp_path)
                    self.debugprint('find {} in {}'.format(cur_dir, tmp_dirs))
                    if cur_dir in tmp_dirs:
                        idx = tmp_dirs.index(cur_dir)
                        if idx+1 < len(tmp_dirs):
                            self.nextpath = tmp_path/tmp_dirs[idx+1]
                            self.debugprint('next path: {}'.format(self.nextpath))
                            break
                        else:
                            if self.is_root(tmp_path):
                                self.debugprint('reached the last dir of root.')
                                self.finish = True
                                break
                    else:
                        self.debugprint('{}, {}'.format(tmp_path, tmp_dirs))
                        print('something wrong.')
                        raise StopIteration()
        self.debugprint('return {}, {}, {}'.format(self.cpath, dirs, files))
        return self.cpath, dirs, files

    def debugprint(self, msg: str) -> None:
        if self.debug:
            print(msg)

    def is_root(self, path: Optional[PurePath] = None) -> bool:
        if path is None:
            path = self.cpath
        self.debugprint('root? {}'.format(path.parts))
        if path.parts:
            return False
        else:
            return True

    def show(self,
             add_info: Optional[Callable[[str], list[str]]] = None) -> None:
        fullpath = self.root/self.cpath
        dirs, files = self.get_contents(self.cpath)
        self.debugprint('show: {} !!'.format(self.cpath.parts))
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


def show_tree(root: str, get_contents: Callable[[PurePath],
                                                tuple[list[str], list[str]]],
              add_info=None) -> None:
    tree_view = TreeViewer(root, get_contents)
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
