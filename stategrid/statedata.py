'''
@author: dhawkins
'''

import matplotlib.pyplot as plt
from matplotlib.table import Table
from matplotlib import cm
import matplotlib as mpl
import pandas as pd
import numpy as np

from stategrid.position import POSITION

class FormatError(Exception):
    '''User data incorrect format'''
    pass

class DuplicateDataError(Exception):
    '''Same state appears twice'''
    pass

class StateData(object):
    '''
    Essentially a dataframe containing the states and their positioning
    as well as user_data in columns
    '''

    def __init__(self, datapath):
        self.datapath = datapath
        self.pos_data = pd.DataFrame.from_dict(POSITION)

        self.user_data = pd.DataFrame.from_csv(self.datapath, index_col=None)
        self.user_data.columns = map(str.lower, self.user_data.columns)

        self._check_input_data()

        self.merged_data = self._merge_data()

    def plot_grid(self, colname, cmap=cm.jet, fname=None):
        '''
        @param colname: column to be plotted
        @param fname: dest for plot
        '''
        StateGrid(self.merged_data, colname.lower(), cmap)
        if fname:
            plt.savefig(fname)
        else:
            plt.show()

    def _check_input_data(self):
        # Check 'state' column exists
        try:
            self.user_data['state']
        except KeyError:
            raise FormatError('data must contain "state" column label containing state names '
                              'or abbreviations')

        # Check no duplicate data
        if any(self.user_data.duplicated(subset='state')):
            raise DuplicateDataError('Duplicate states in "state" column')

        # Check states are all strings
        if any(self.user_data['state'].apply(np.isreal)):
            raise ValueError('"state" column has numeric/NaN/None data')

    def _is_abbrevs(self, series):
        avg_len = sum([len(i.strip()) for i in series]) / len(self.user_data)
        return avg_len == 2.0

    def _merge_data(self):
        # try and detect if the column is state abbrevs or full state name
        is_abbrevs = self._is_abbrevs(self.user_data['state'])
        self.user_data['state'] = self.user_data['state'].apply(str.lower)

        if is_abbrevs:
            self.pos_data.drop('state', axis=1, inplace=True)
            return self.pos_data.merge(self.user_data, how='left', left_on='abbrev',
                                       right_on='state')
        else:
            return self.pos_data.merge(self.user_data, how='left', left_on='state',
                                       right_on='state')

class StateGrid(object):
    '''
    Plot numeric user_data by state on a grid where every state occupies the same visible space.
    Opposed to a typical choropleth where the largest (and typically least dense) states occupy
    the most space ... and attention.

    Matplotlib Table is used heavily in this implementation
    mpl.Table docs (2004): http://doc.astro-wise.org/matplotlib.table.html
    '''

    def __init__(self, data, colname, cmap=cm.jet):
        '''
        @param user_data - pandas.DataFrame containing state location and values to plot
        @param colname - str column to be plotted, must be numeric user_data
        TODO: implement factor user_data, may already be some pandas built-in for this?
        '''
        self.data = data
        self.colname = colname
        self.cmap = cmap

        self.mn = min(self.data[self.colname].dropna().astype(float))
        self.mx = max(self.data[self.colname].dropna().astype(float))

        self.fig = plt.figure()
        self._build_states()
        self._build_colorbar()
        self._color_states()
        # TODO: some future method should check the 'darkness'
        # TODO: of a cell and invert the text color
        self._recolor_state_labels()

    def _build_states(self):
        self.t_ax = self.fig.add_axes([0.05, 0.05, .75, .9])
        self.t_ax.set_axis_off()

        nrows = max(self.data['row'])
        ncols = max(self.data['column'])
        width = 1.0 / ncols
        height = 1.0 / nrows

        tb = Table(self.t_ax)
        for abb, row, col in zip(self.data['abbrev'], self.data['row'], self.data['column']):
            tb.add_cell(row-1, col-1, width, height, text=abb.upper(), edgecolor='b',
                        loc='center')

        tb.set_fontsize(20)
        self.tb = self.t_ax.add_table(tb)

    def _build_colorbar(self):
        self.cb_ax = self.fig.add_axes([0.85, 0.05, 0.05, 0.9])
        norm = mpl.colors.Normalize(vmin=self.mn, vmax=self.mx)
        cb = mpl.colorbar.ColorbarBase(self.cb_ax, cmap=self.cmap,
                                       norm=norm,
                                       orientation='vertical')
        cb.set_label(self.colname)

    def _color_states(self):
        for c in self.tb.get_celld():
            cell = self.tb.get_celld()[c]
            val = self.data[self.data['abbrev'] == cell.get_text().get_text().lower()][self.colname]
            org_value = float(val.iloc[0])

            if np.isnan(org_value):
                # If the state is missing data, put hatches through it
                cell.set_hatch('x')
            else:
                norm_value = (org_value-self.mn) / (self.mx-self.mn) * 255
                col = self.cmap(int(norm_value))
                cell.set_color(col)

            cell.set_edgecolor('k')

    def _invert_text(self, color='white'):
        for c in self.tb.get_celld():
            cell = self.tb.get_celld()[c]
            text = cell.get_text()
            text.set_color(color)

    def _invert_bckgrnd(self, color='black'):
        for c in self.tb.get_celld():
            cell = self.tb.get_celld()[c]
            cell.set_color(color)

    def _recolor_state_labels(self):
        '''invert labels if cell background too dark'''
        pass
