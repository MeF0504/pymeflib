#! /usr/bin/env python3

from typing import Any, Dict, Union, Optional
from pathlib import PurePosixPath

import h5py


class TreatHDF5():
    def __init__(self, filename: str):
        self.filename = filename
        self.state = 'not open'
        self.data: Union[None, h5py.File] = None

    def __repr__(self):
        return f'TreatHDF5(file={self.filename}, {self.state})'

    def __set_read(self):
        if self.state != 'read':
            if self.state == 'write':
                self.data.close()
            self.data = h5py.File(self.filename, 'r')
            self.state = 'read'

    def __set_write(self):
        if self.state != 'write':
            if self.state == 'read':
                self.data.close()
            self.data = h5py.File(self.filename, 'w')
            self.state = 'write'

    def add_data(self, path: str, data: Any):
        self.__set_write()
        ppath = PurePosixPath(path)
        if len(ppath.parts) == 1:
            group = self.data
        else:
            ppar = str(ppath.parents[0])
            if ppar not in self.data:
                self.data.create_group(ppar)
            group = self.data[ppar]
        group.create_dataset(ppath.parts[-1], data=data)

    def get_attr(self, path: str) -> Optional[Dict[str, Any]]:
        self.__set_read()
        if path not in self.data:
            return None
        res = {}
        for attr in self.data[path].attrs:
            res[attr] = self.data[path].attrs[attr]
        return res

    def get_data(self, path: str) -> Optional[Any]:
        self.__set_read()
        if path not in self.data:
            return None
        data = self.data[path]
        if isinstance(data, h5py.Group):
            return list(data.keys())
        elif isinstance(data, h5py.Dataset):
            return data[()]

    def close(self):
        if self.state != 'not open':
            self.data.close()
            self.state = 'not open'


if __name__ == '__main__':
    print('''
import numpy as np
from pymeflib.treat_hdf5 import TreatHDF5
hdf5_obj = TreatHDF5("data.hdf5")
hdf5_obj.add_data('path/to/random', np.random.rand(100))
print(hdf5_obj.get_attr('path/to/random'))
print(hdf5_obj.get_data('path/to/random'))
''')
