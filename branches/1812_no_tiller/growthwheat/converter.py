# -*- coding: latin-1 -*-

from __future__ import division  # use "//" to do integer division
import pandas as pd

import simulation

"""
    growthwheat.converter
    ~~~~~~~~~~~~~~~~~~~~~

    The module :mod:`growthwheat.converter` defines functions to convert 
    :class:`dataframes <pandas.DataFrame>` to/from GrowthWheat inputs or outputs format.
    
    :copyright: Copyright 2014-2016 INRA-ECOSYS, see AUTHORS.
    :license: TODO, see LICENSE for details.

    .. seealso:: Barillot et al. 2016.
"""

"""
    Information about this versioned file:
        $LastChangedBy$
        $LastChangedDate$
        $LastChangedRevision$
        $URL$
        $Id$
"""

#: the columns which define the topology in the input/output dataframe
HIDDENZONE_TOPOLOGY_COLUMNS = ['plant', 'axis', 'metamer']
ELEMENT_TOPOLOGY_COLUMNS = ['plant', 'axis', 'metamer', 'organ', 'element']
ROOT_TOPOLOGY_COLUMNS = ['plant', 'axis', 'organ']
SAM_TOPOLOGY_COLUMNS = ['plant', 'axis']


def from_dataframes(hiddenzone_inputs, element_inputs, root_inputs, SAM_inputs):
    """
    Convert inputs/outputs from Pandas dataframe to Growth-Wheat format.

    :Parameters:

        - `hiddenzone_inputs` (:class:`pandas.DataFrame`) - Hidden zone inputs dataframe to convert, with one line by hidden zone.
        - `element_inputs` (:class:`pandas.DataFrame`) - Element inputs dataframe to convert, with one line by element.
        - `root_inputs` (:class:`pandas.DataFrame`) - Root inputs dataframe to convert, with one line by root.
        - `SAM_inputs` (:class:`pandas.DataFrame`) - SAM inputs dataframe to convert, with one line by SAM.

    :Returns:
        The inputs in a dictionary.

    :Returns Type:
        :class:`dict` of :class:`dict`

    .. seealso:: see :attr:`simulation.Simulation.inputs` for the structure of Growth-Wheat inputs.

    """
    all_hiddenzone_dict = {}
    all_element_dict = {}
    all_root_dict = {}
    all_SAM_dict = {}
    hiddenzone_inputs_columns = hiddenzone_inputs.columns.difference(HIDDENZONE_TOPOLOGY_COLUMNS)
    element_inputs_columns = element_inputs.columns.difference(ELEMENT_TOPOLOGY_COLUMNS)
    root_inputs_columns = root_inputs.columns.difference(ROOT_TOPOLOGY_COLUMNS)
    SAM_inputs_columns = SAM_inputs.columns.difference(SAM_TOPOLOGY_COLUMNS)

    for element_inputs_id, element_inputs_group in element_inputs.groupby(ELEMENT_TOPOLOGY_COLUMNS):
        # element
        element_inputs_series = element_inputs_group.loc[element_inputs_group.first_valid_index()]
        element_inputs_dict = element_inputs_series[element_inputs_columns].to_dict()
        all_element_dict[element_inputs_id] = element_inputs_dict

    hiddenzone_inputs_grouped = hiddenzone_inputs.groupby(HIDDENZONE_TOPOLOGY_COLUMNS)
    for hiddenzone_inputs_id, hiddenzone_inputs_group in hiddenzone_inputs_grouped:
        # hiddenzone
        hiddenzone_inputs_series = hiddenzone_inputs_group.loc[hiddenzone_inputs_group.first_valid_index()]
        hiddenzone_inputs_dict = hiddenzone_inputs_series[hiddenzone_inputs_columns].to_dict()
        all_hiddenzone_dict[hiddenzone_inputs_id] = hiddenzone_inputs_dict

    for root_inputs_id, root_inputs_group in root_inputs.groupby(ROOT_TOPOLOGY_COLUMNS):
        # root
        root_inputs_series = root_inputs_group.loc[root_inputs_group.first_valid_index()]
        root_inputs_dict = root_inputs_series[root_inputs_columns].to_dict()
        all_root_dict[root_inputs_id] = root_inputs_dict

    for SAM_inputs_id, SAM_inputs_group in root_inputs.groupby(SAM_TOPOLOGY_COLUMNS):
        # SAM
        SAM_inputs_series = SAM_inputs_group.loc[SAM_inputs_group.first_valid_index()]
        SAM_inputs_dict = SAM_inputs_series[SAM_inputs_columns].to_dict()
        all_SAM_dict[SAM_inputs_id] = SAM_inputs_dict

    return {'hiddenzone': all_hiddenzone_dict, 'elements': all_element_dict, 'roots': all_root_dict, 'SAM': all_SAM_dict }


def to_dataframes(data_dict):
    """
    Convert outputs from Growth-Wheat format to Pandas dataframe.

    :Parameters:

        - `data_dict` (:class:`dict`) - The outputs in Growth-Wheat format.

    :Returns:
        One dataframe for hiddenzone outputs and one dataframe for element outputs.

    :Returns Type:
        :class:`tuple` of :class:`pandas.DataFrame`

    .. seealso:: see :attr:`simulation.Simulation.outputs` for the structure of Growth-Wheat outputs.

    """
    dataframes_dict = {}
    for (current_key, current_topology_columns, current_outputs_names) in (('hiddenzone', HIDDENZONE_TOPOLOGY_COLUMNS, simulation.HIDDENZONE_OUTPUTS),
                                                                           ('elements', ELEMENT_TOPOLOGY_COLUMNS, simulation.ELEMENT_OUTPUTS),
                                                                           ('roots', ROOT_TOPOLOGY_COLUMNS, simulation.ROOT_OUTPUTS)):
        current_data_dict = data_dict[current_key]
        current_ids_df = pd.DataFrame(current_data_dict.keys(), columns=current_topology_columns)
        current_data_df = pd.DataFrame(current_data_dict.values())
        current_df = pd.concat([current_ids_df, current_data_df], axis=1)
        current_df.sort_values(by=current_topology_columns, inplace=True)
        current_columns_sorted = current_topology_columns + current_outputs_names
        current_df = current_df.reindex(current_columns_sorted, axis=1, copy=False)
        current_df.reset_index(drop=True, inplace=True)
        dataframes_dict[current_key] = current_df
    return dataframes_dict['hiddenzone'], dataframes_dict['elements'], dataframes_dict['roots']
