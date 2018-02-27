#!/usr/bin/env python3

import os

from pypact.reader import Reader

filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '..', 'reference', 'test31.out')

dr = Reader()(filename)[2].dose_rate

print(dr.json_serialize())
