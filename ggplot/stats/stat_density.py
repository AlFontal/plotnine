from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import numpy as np
import pandas as pd
import pandas.core.common as com
import statsmodels.api as sm

from ..utils.exceptions import GgplotError
from .stat import stat


# NOTE: Parameter discriptions are in
# statsmodels/nonparametric/kde.py
# TODO: Update when statsmodels-0.6 is released
class stat_density(stat):
    REQUIRED_AES = {'x'}
    DEFAULT_PARAMS = {'geom': 'density', 'position': 'stack',
                      'kernel': 'gaussian', 'adjust': 1,
                      'trim': False, 'n': 512, 'gridsize': None,
                      'bw': 'normal_reference', 'cut': 3,
                      'clip': (-np.inf, np.inf)}
    CREATES = {'y'}

    @classmethod
    def compute_group(cls, data, scales, **params):
        x = data.pop('x')
        n = len(x)

        range_x = scales.x.dimension((0, 0))

        try:
            float(x.iloc[0])
        except:
            try:
                # try to use it as a pandas.tslib.Timestamp
                x = [ts.toordinal() for ts in x]
            except:
                raise GgplotError(
                    "stat_density(): aesthetic x mapping " +
                    "needs to be convertable to float!")

        # kde is computed efficiently using fft. But the fft does
        # not support weights and is only available with the
        # gaussian kernel. When weights are relevant we
        # turn off the fft.
        try:
            weight = data.pop('weight')
        except KeyError:
            weight = np.ones(n) / n

        lookup = {
            'biweight': 'biw',
            'cosine': 'cos',
            'epanechnikov': 'epa',
            'gaussian': 'gau',
            'triangular': 'tri',
            'triweight': 'triw',
            'uniform': 'uni'}
        kernel = lookup[params['kernel'].lower()]

        if kernel == 'gaussian':
            fft, weight = True, None
        else:
            fft = False

        kde = sm.nonparametric.KDEUnivariate(x)
        kde.fit(
            # kernel=kernel,        # enable after statsmodels 0.6
            # bw=params['bw'], # enable after statsmodels 0.6
            fft=fft,
            weights=weight,
            adjust=params['adjust'],
            cut=params['cut'],
            gridsize=params['gridsize'],
            clip=params['clip'],)
        x2 = np.linspace(range_x[0], range_x[1], params['n'])
        y = kde.evaluate(x2)
        new_data = pd.DataFrame({'x': x2,
                                 'y': y,
                                 'count': y * n,
                                 'scaled': y / np.max(y)})
        return new_data
