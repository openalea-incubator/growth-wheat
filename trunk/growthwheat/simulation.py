# -*- coding: latin-1 -*-

from __future__ import division # use "//" to do integer division

"""
    growthwheat.simulation
    ~~~~~~~~~~~~~~~~~~

    The module :mod:`growthwheat.simulation`.

    :copyright: Copyright 2014-2015 INRA-ECOSYS, see AUTHORS.
    :license: TODO, see LICENSE for details.

    .. seealso:: Barillot et al. 2015.
"""

"""
    Information about this versioned file:
        $LastChangedBy$
        $LastChangedDate$
        $LastChangedRevision$
        $URL$
        $Id$
"""

import numpy as np
import pandas as pd

import model
import logging
import copy

from respiwheat.model import RespirationModel

#: the inputs needed by GrowthWheat
HIDDENZONE_INPUTS = ['leaf_L', 'delta_leaf_L', 'SSLW', 'SSSW', 'leaf_is_emerged', 'sucrose', 'amino_acids', 'mstruct']
ORGAN_INPUTS = ['is_growing', 'mstruct', 'green_area', 'sucrose', 'amino_acids']
ROOT_INPUTS = ['sucrose', 'amino_acids', 'mstruct', 'Nstruct']

#: the outputs computed by GrowthWheat
HIDDENZONE_OUTPUTS = ['sucrose', 'amino_acids', 'mstruct']
ORGAN_OUTPUTS = ['sucrose', 'amino_acids', 'mstruct']
ROOT_OUTPUTS = ['sucrose', 'amino_acids', 'mstruct', 'Nstruct']

#: the inputs and outputs of GrowthWheat.
HIDDENZONE_INPUTS_OUTPUTS = sorted(set(HIDDENZONE_INPUTS + HIDDENZONE_OUTPUTS))
ORGAN_INPUTS_OUTPUTS = sorted(set(ORGAN_INPUTS + ORGAN_OUTPUTS))


class SimulationError(Exception): pass
class SimulationRunError(SimulationError): pass


class Simulation(object):
    """The Simulation class permits to initialize and run a simulation.
    """

    def __init__(self, delta_t=1):

        #: The inputs of growth-Wheat.
        #:
        #: `inputs` is a dictionary of dictionaries:
        #:     {'hiddenzone': {(plant_index, axis_label, metamer_index): {hiddenzone_input_name: hiddenzone_input_value, ...}, ...},
        #:      'organs': {(plant_index, axis_label, metamer_index, organ_label): {organ_input_name: organ_input_value, ...}, ...},
        #:      'roots': {(plant_index, axis_label): {root_input_name: root_input_value, ...}, ...}}
        #: See :TODO?
        #: for more information about the inputs.
        self.inputs = {}

        #: The outputs of growth-Wheat.
        #:
        #: `outputs` is a dictionary of dictionaries:
        #:     {'hiddenzone': {(plant_index, axis_label, metamer_index): {hiddenzone_input_name: hiddenzone_input_value, ...}, ...},
        #:      'organs': {(plant_index, axis_label, metamer_index, organ_label): {organ_input_name: organ_input_value, ...}, ...}
        #:      'roots': {(plant_index, axis_label): {root_input_name: root_input_value, ...}, ...}}
        #: See :TODO?
        #: for more information about the inputs.
        self.outputs = {}

        #: the delta t of the simulation (in seconds)
        self.delta_t = delta_t


    def initialize(self, inputs):
        """
        Initialize :attr:`inputs` from `inputs`.

        :Parameters:

            - `inputs` (:class:`dict`)
              `inputs` must be a dictionary with the same structure as :attr:`inputs`.
        """
        self.inputs.clear()
        self.inputs.update(inputs)

    def run(self):
        # Copy the inputs into the output dict
        self.outputs.update({inputs_type: copy.deepcopy(all_inputs) for inputs_type, all_inputs in self.inputs.iteritems() if inputs_type in set(['hiddenzone', 'organs', 'roots'])})

        # Hidden growing zones
        all_hiddenzone_inputs = self.inputs['hiddenzone']
        all_hiddenzone_outputs = self.outputs['hiddenzone']

        # organs
        all_organs_inputs = self.inputs['organs']
        all_organs_outputs = self.outputs['organs']

        # roots
        all_roots_inputs = self.inputs['roots']
        all_roots_outputs = self.outputs['roots']

        # hidden zones and organs
        for hiddenzone_id, hiddenzone_inputs in all_hiddenzone_inputs.iteritems():
            curr_hiddenzone_outputs = all_hiddenzone_outputs[hiddenzone_id]

            # Initialisation of the exports towards the growing lamina or sheath
            delta_lamina_mstruct, delta_sheath_mstruct, export_sucrose, export_amino_acids = 0, 0, 0, 0

            ## delta hidden growing zone mstruct (=delta leaf mstruct at this stage)
            delta_mstruct = model.calculate_delta_mstruct_preE(hiddenzone_inputs['leaf_L'], hiddenzone_inputs['delta_leaf_L'])

            #: Lamina has emerged and is growing
            if hiddenzone_inputs['leaf_is_emerged']:
                lamina_id = hiddenzone_id + tuple(['blade'])
                if all_organs_inputs[lamina_id]['is_growing']:
                    curr_organ_inputs = all_organs_inputs[lamina_id]
                    curr_organ_outputs = all_organs_outputs[lamina_id]
                    ## Delta mstruct of the emerged lamina
                    delta_lamina_mstruct = model.calculate_delta_mstruct_postE(hiddenzone_inputs['SSLW'], curr_organ_inputs['mstruct'], curr_organ_inputs['green_area'])
                    ## Export of sucrose from hiddenzone towards emerged lamina
                    export_sucrose = model.calculate_export_sucrose(delta_lamina_mstruct, hiddenzone_inputs['sucrose'], hiddenzone_inputs['mstruct'])
                    ## Export of amino acids from hiddenzone towards emerged lamina
                    export_amino_acids = model.calculate_export_amino_acids(delta_lamina_mstruct, hiddenzone_inputs['amino_acids'], hiddenzone_inputs['mstruct'])

                    # Update of lamina outputs
                    curr_organ_outputs['mstruct'] += delta_lamina_mstruct
                    curr_organ_outputs['sucrose'] += export_sucrose
                    curr_organ_outputs['amino_acids'] += export_amino_acids
                    self.outputs['organs'][lamina_id] = curr_organ_outputs

                else: #: Mature lamina, growing sheath
                    sheath_id = hiddenzone_id + tuple(['sheath'])
                    curr_organ_inputs = all_organs_inputs[sheath_id]
                    curr_organ_outputs = all_organs_outputs[sheath_id]
                    ## Delta mstruct of the emerged sheath
                    delta_sheath_mstruct = model.calculate_delta_mstruct_postE(hiddenzone_inputs['SSSW'], curr_organ_inputs['mstruct'], curr_organ_inputs['area'])
                    ## Export of sucrose from hiddenzone towards emerged sheath
                    export_sucrose = model.calculate_export_sucrose(delta_sheath_mstruct, hiddenzone_inputs['sucrose'], hiddenzone_inputs['mstruct'])
                    ## Export of amino acids from hiddenzone towards emerged sheath
                    export_amino_acids = model.calculate_export_amino_acids(delta_sheath_mstruct, hiddenzone_inputs['amino_acids'], hiddenzone_inputs['mstruct'])

                    # Update of sheath outputs
                    curr_organ_outputs['mstruct'] += delta_sheath_mstruct
                    curr_organ_outputs['sucrose'] += export_sucrose
                    curr_organ_outputs['amino_acids'] += export_amino_acids
                    self.outputs['organs'][sheath_id] = curr_organ_outputs

            # Update of leaf outputs
            sucrose_consumption_mstruct = model.calculate_s_mstruct_sucrose(delta_mstruct, delta_lamina_mstruct, delta_sheath_mstruct) #: Consumption of sucrose due to mstruct growth
            AA_consumption_mstruct = model.calculate_s_mstruct_amino_acids(delta_mstruct, delta_lamina_mstruct, delta_sheath_mstruct)  #: Consumption of amino acids due to mstruct growth
            Respi_growth = RespirationModel.R_growth(sucrose_consumption_mstruct)                                                      #: Respiration growth
            curr_hiddenzone_outputs['mstruct'] += delta_mstruct
            curr_hiddenzone_outputs['sucrose'] -= (sucrose_consumption_mstruct + Respi_growth + export_sucrose)
            curr_hiddenzone_outputs['amino_acids'] -= (AA_consumption_mstruct + export_amino_acids)
            self.outputs['hiddenzone'][hiddenzone_id] = curr_hiddenzone_outputs


        # Roots
        for root_id, root_inputs in all_roots_inputs.iteritems():
            curr_root_outputs = all_roots_outputs[root_id]
            # Growth
            mstruct_C_growth, mstruct_growth, Nstruct_growth, Nstruct_N_growth = model.calculate_roots_mstruct_growth(root_inputs['sucrose'], root_inputs['amino_acids'], root_inputs['mstruct'], self.delta_t)
            # Respiration growth
            Respi_growth = RespirationModel.R_growth(mstruct_C_growth)
            # Update of root outputs
            curr_root_outputs['mstruct'] += mstruct_growth
            curr_root_outputs['sucrose'] -= (mstruct_C_growth)
            curr_root_outputs['Nstruct'] += Nstruct_growth
            curr_root_outputs['amino_acids'] -= (Nstruct_N_growth)
            self.outputs['roots'][root_id] = curr_root_outputs