from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from ..utils import make_rgba
from .geom import geom


class geom_ribbon(geom):
    DEFAULT_AES = {'alpha': 1, 'color': None, 'fill': '#333333',
                   'linetype': 'solid', 'size': 1.0}
    REQUIRED_AES = {'x', 'ymax', 'ymin'}
    DEFAULT_PARAMS = {'stat': 'identity', 'position': 'identity'}
    guide_geom = 'polygon'

    _aes_renames = {'linetype': 'linestyle', 'ymin': 'y1', 'ymax': 'y2',
                    'size': 'linewidth', 'fill': 'facecolor',
                    'color': 'edgecolor'}
    _units = {'alpha', 'edgecolor', 'facecolor', 'linestyle', 'linewidth'}

    def draw_groups(self, data, scales, coordinates, ax, **params):
        """
        Plot all groups
        """
        pinfos = self._make_pinfos(data, params)
        for pinfo in pinfos:
            self.draw(pinfo, scales, coordinates, ax, **params)

    @staticmethod
    def draw(pinfo, scales, coordinates, ax, **params):
        for key in ('y', 'weight', 'group'):
            try:
                del pinfo[key]
            except KeyError:
                pass

        # To match ggplot2, the alpha only affects the
        # fill color
        pinfo['facecolor'] = make_rgba(
            pinfo['facecolor'], pinfo.pop('alpha'))
        if pinfo['facecolor'] is None:
            pinfo['facecolor'] = ''

        ax.fill_between(**pinfo)
