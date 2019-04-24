# -*- coding: latin-1 -*-

from __future__ import division  # use "//" to do integer division
import parameters
import numpy as np

"""
    growthwheat.model
    ~~~~~~~~~~~~~

    The module :mod:`growthwheat.model` defines the equations of the kinetic of leaf growth (mass flows) according to leaf elongation. Also includes root growth.

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

def calculate_ratio_mstruct_DM(mstruct, sucrose, fructans, amino_acids, proteins):
    """ Ratio mstruct/dry matter (dimensionless)

        :Parameters:
            - `mstruct` (:class:`float`) - Strutural mass (g)
            - `sucrose` (:class:`float`) - Sucrose amount (�mol C)
            - `fructans` (:class:`float`) - Fructans amount (�mol C)
            - `amino_acids` (:class:`float`) - Amino acids amount (�mol N)
            - `proteins` (:class:`float`) - Proteins amount (�mol N)
        :Returns:
            Ratio mstruct/dry matter (dimensionless)
        :Returns Type:
            :class:`float`
        """
    C_MOLAR_MASS = parameters.C_MOLAR_MASS
    N_MOLAR_MASS = parameters.N_MOLAR_MASS
    dry_mass = ((sucrose * 1E-6 * C_MOLAR_MASS) / parameters.HEXOSE_MOLAR_MASS_C_RATIO +
           (fructans * 1E-6 * C_MOLAR_MASS) / parameters.HEXOSE_MOLAR_MASS_C_RATIO +
           (amino_acids * 1E-6 * N_MOLAR_MASS) / parameters.AMINO_ACIDS_MOLAR_MASS_N_RATIO +
           (proteins * 1E-6 * N_MOLAR_MASS) / parameters.AMINO_ACIDS_MOLAR_MASS_N_RATIO +
           mstruct)

    return mstruct/dry_mass

def calculate_delta_leaf_enclosed_mstruct(leaf_L, delta_leaf_L, ratio_mstruct_DM):
    """ Relation between length and mstruct for the leaf segment located in the hidden zone during the exponential-like growth phase.
    Parameters alpha_mass_growth and beta_mass_growth estimated from Williams (1960) and expressed in g of dry mass)
    The actual ratio_mstruct_DM is then used to convert in g of structural dry mass.

    :Parameters:
        - `leaf_L` (:class:`float`) - Total leaf length (m)
        - `delta_leaf_L` (:class:`float`) - delta of leaf length (m)
        - `ratio_mstruct_DM` (:class:`float`) - Ratio mstruct/dry matter (dimensionless)
    :Returns:
        delta_leaf_enclosed_mstruct (g)
    :Returns Type:
        :class:`float`
    """
    return parameters.ALPHA * parameters.BETA * leaf_L**(parameters.BETA-1) * delta_leaf_L * ratio_mstruct_DM

def calculate_delta_leaf_enclosed_mstruct_postE(delta_leaf_pseudo_age, leaf_pseudo_age,leaf_pseudostem_L, enclosed_mstruct, LSSW):
    """ mstruct of the enclosed leaf from the emergence of the leaf to the end of elongation.
    Final mstruct of the enclosed leaf matches sheath mstruct calculation when it is mature.
    #TODO : Hiddenzone mstruct calculation will not work for sheath sorten than previous one.

    :Parameters:
        - `delta_leaf_pseudo_age` (:class:`float`) - Delta of Pseudo age of the leaf since beginning of automate elongation (s)
        - `leaf_pseudo_age` (:class:`float`) - Pseudo age of the leaf since beginning of automate elongation (s)
        - 'leaf_pseudostem_L' (:class:`float`) Pseudostem length (m)
        - 'leaf_Lmax' (:class:`float`) Final leaf length (m)
        - `LSSW` (:class:`float`) - Lineic Structural Sheath Weight (g m-1).
    :Returns:
        delta_leaf_enclosed_mstruct (g)
    :Returns Type:
        :class:`float`
    """
    # mstruct_init =  2.65E-08 # From elongwheat parameters
    # enclosed_mstruct0 = mstruct_init + parameters.ALPHA * parameters.RATIO_MSTRUCT_DM * (leaf_Lmax * parameters.FITTED_L0) ** parameters.BETA  # Integration of the calculate_delta_leaf_enclosed_mstruct
    enclosed_mstruct_max = leaf_pseudostem_L * LSSW

    if leaf_pseudo_age < parameters.te:
        delta_enclosed_mstruct = (enclosed_mstruct_max - enclosed_mstruct)/(parameters.te - leaf_pseudo_age) * delta_leaf_pseudo_age
    else:
        delta_enclosed_mstruct = 0

    return delta_enclosed_mstruct

def calculate_delta_internode_enclosed_mstruct(internode_L, delta_internode_L, ratio_mstruct_DM):
    """ Relation between length and mstruct for the internode segment located in the hidden zone.
    Same relationship than for enclosed leaf corrected by RATIO_ENCLOSED_LEAF_INTERNODE.
    Parameters alpha_mass_growth and beta_mass_growth estimated from Williams (1975) and expressed in g of dry mass.
    The actual ratio_mstruct_DM is then used to convert in g of structural dry mass.

    :Parameters:
        - `internode_L` (:class:`float`) - Enclosed internode length (m)
        - `delta_internode_L` (:class:`float`) - delta of enclosed internode length (m)
        - `ratio_mstruct_DM` (:class:`float`) - Ratio mstruct/dry matter (dimensionless)
    :Returns:
        delta_enclosed_internode_mstruct (g)
    :Returns Type:
        :class:`float`
    """

    return parameters.RATIO_ENCLOSED_LEAF_INTERNODE * parameters.ALPHA * parameters.BETA * internode_L**(parameters.BETA-1) * delta_internode_L * ratio_mstruct_DM

def calculate_delta_internode_enclosed_mstruct_postL(delta_internode_pseudo_age, internode_pseudo_age, internode_L, internode_pseudostem_L, internode_Lmax, LSIW, enclosed_mstruct):
    """ mstruct of the enclosed internode from the ligulation of the leaf to the end of elongation.
    Final mstruct of the enclosed internode matches internode mstruct calculation when it is mature.

    :Parameters:
        - `delta_internode_pseudo_age` (:class:`float`) - Delta of Pseudo age of the internode since beginning of automate elongation (s)
        - `internode_pseudo_age` (:class:`float`) - Pseudo age of the internode since beginning of automate elongation (s)
        - 'internode_L' (:class:`float`) Current lenght of the internode (m)
        - 'internode_pseudostem_L' (:class:`float`) Pseudostem length of the internode (m)
        - 'internode_Lmax' (:class:`float`) Final length of the internode (m)
        - `LSIW` (:class:`float`) - Lineic Structural Internode Weight (g m-1).
    :Returns:
        delta_internode_enclosed_mstruct (g)
    :Returns Type:
        :class:`float`
    """
    if np.isnan(internode_Lmax):
        # enclosed_mstruct0 = parameters.RATIO_ENCLOSED_LEAF_INTERNODE * parameters.ALPHA * parameters.RATIO_MSTRUCT_DM * internode_L ** parameters.BETA
        enclosed_mstruct_max = internode_L * LSIW
    else :
        # enclosed_mstruct0 = parameters.RATIO_ENCLOSED_LEAF_INTERNODE * parameters.ALPHA * parameters.RATIO_MSTRUCT_DM * (internode_Lmax * parameters.FITTED_L0_IN) ** parameters.BETA
        enclosed_mstruct_max = min(internode_pseudostem_L, internode_Lmax) * LSIW

    if internode_pseudo_age < parameters.te_IN:
        delta_enclosed_mstruct = (enclosed_mstruct_max - enclosed_mstruct)/(parameters.te_IN - internode_pseudo_age) * delta_internode_pseudo_age
    else:
        delta_enclosed_mstruct = 0

    return delta_enclosed_mstruct

def calculate_delta_emerged_tissue_mstruct(SW, previous_mstruct, metric):
    """ delta mstruct of emerged tissue (lamina, sheath and internode). Calculated from tissue area.

    :Parameters:
        - `SW` (:class:`float`) - For Lamina : Structural Specific Weight (g m-2); For sheath and internode : Lineic Structural Weight (g m-1)
        - `previous_mstruct` (:class:`float`) - mstruct at the previous time step i.e. not yet updated (g)
        - `metric` (:class:`float`) - For Lamina : Area at the current time step, as updated by the geometrical model (m2); For sheath and internode : Length at the current time step (m)
    :Returns:
        delta mstruct (g)
    :Returns Type:
        :class:`float`
    """
    updated_mstruct = SW * metric
    delta_mstruct = updated_mstruct - previous_mstruct
    return delta_mstruct


def calculate_delta_Nstruct(delta_mstruct):
    """ delta Nstruct of hidden zone and emerged tissue (lamina and sheath).

    :Parameters:
        - `delta_mstruct` (:class:`float`) - delta of mstruct (g)
    :Returns:
        delta Nstruct (g)
    :Returns Type:
        :class:`float`
    """
    return delta_mstruct * parameters.RATIO_AMINO_ACIDS_MSTRUCT


def calculate_export(delta_mstruct, metabolite, hiddenzone_mstruct):
    """Export of metabolite from the hidden zone towards the emerged part of the leaf integrated over delta_t.

    :Parameters:
        - `delta_mstruct` (:class:`float`) - Delta of structural dry mass of the emerged part of the leaf (g)
        - `metabolite` (:class:`float`) - Metabolite amount in the hidden zone (�mol C or N)
        - `hiddenzone_mstruct` (:class:`float`) - Structural mass of the hidden zone (g)

    :Returns:
        metabolite export (�mol N)
    :Returns Type:
        :class:`float`
    """
    return delta_mstruct * max(0, (metabolite / hiddenzone_mstruct))

def calculate_cytokinins(delta_mstruct, cytokinins, mstruct, manual_cyto_init):
    """Quantity of cytokins in the newly visible mstruct.

    :Parameters:
        - `delta_mstruct` (:class:`float`) - Delta of structural dry mass of the emerged part of the leaf (g)
        - `cytokinins` (:class:`float`) - Metabolite amount in the emerged part of the leaf (�mol)
        - `mstruct` (:class:`float`) - Structural mass of the emerged part of the leaf (g)

    :Returns:
        metabolite addition (�mol)
    :Returns Type:
        :class:`float`
    """
    cyto_init = 200
    if manual_cyto_init is not None:
        cyto_init = manual_cyto_init
    # default initial value
    if mstruct == 0:
        res = delta_mstruct * cyto_init # TODO: Set according to protein concentration ?
    else:
        res = delta_mstruct * cyto_init#  (cytokinins / mstruct)
    return res

def calculate_s_Nstruct_amino_acids(delta_hiddenzone_Nstruct, delta_lamina_Nstruct, delta_sheath_Nstruct):
    """Consumption of amino acids for the calculated mstruct growth (�mol N consumed by mstruct growth)

    :Parameters:
        - `delta_hiddenzone_Nstruct` (:class:`float`) - Nstruct growth of the hidden zone (g)
        - `delta_lamina_Nstruct` (:class:`float`) - Nstruct growth of the lamina (g)
        - `delta_sheath_Nstruct` (:class:`float`) - Nstruct growth of the sheath (g)
    :Returns:
        Amino acid consumption (�mol N)
    :Returns Type:
        :class:`float`
    """
    return (delta_hiddenzone_Nstruct + delta_lamina_Nstruct + delta_sheath_Nstruct) / parameters.N_MOLAR_MASS * 1E6


def calculate_s_mstruct_sucrose(delta_hiddenzone_mstruct, delta_lamina_mstruct, delta_sheath_mstruct, s_Nstruct_amino_acids_N):
    """Consumption of sucrose for the calculated mstruct growth (�mol C consumed by mstruct growth)

    :Parameters:
        - `delta_hiddenzone_mstruct` (:class:`float`) - mstruct growth of the hidden zone (g)
        - `delta_lamina_mstruct` (:class:`float`) - mstruct growth of the lamina (g)
        - `delta_sheath_mstruct` (:class:`float`) - mstruct growth of the sheath (g)
        - `s_Nstruct_amino_acids_N` (:class:`float`) - Total amino acid consumption (�mol N) due to Nstruct (�mol N)
    :Returns:
        Sucrose consumption (�mol C)
    :Returns Type:
        :class:`float`
    """
    s_Nstruct_amino_acids = s_Nstruct_amino_acids_N / parameters.AMINO_ACIDS_N_RATIO   #: �mol of AA
    s_mstruct_amino_acids_C = s_Nstruct_amino_acids * parameters.AMINO_ACIDS_C_RATIO   #: �mol of C coming from AA
    s_mstruct_C = (delta_hiddenzone_mstruct + delta_lamina_mstruct + delta_sheath_mstruct) * parameters.RATIO_SUCROSE_MSTRUCT / parameters.C_MOLAR_MASS * 1E6  #: Total C used for mstruct growth (�mol C)
    s_mstruct_sucrose_C = s_mstruct_C - s_mstruct_amino_acids_C                        #: �mol of coming from sucrose

    return s_mstruct_sucrose_C
"""
    s_Nstruct_amino_acids = (delta_hiddenzone_Nstruct + delta_lamina_Nstruct + delta_sheath_Nstruct) / parameters.N_MOLAR_MASS * 1E6 / parameters.AMINO_ACIDS_N_RATIO   #: �mol of AA
    s_Nstruct_amino_acids = (delta_hiddenzone_Nstruct + delta_lamina_Nstruct + delta_sheath_Nstruct) / 14 * 1E6 / 1.17   #: �mol of AA
    s_Nstruct_amino_acids = (delta_hiddenzone_Nstruct + delta_lamina_Nstruct + delta_sheath_Nstruct) * 6.105e4
    
    s_mstruct_amino_acids_C = (delta_hiddenzone_Nstruct + delta_lamina_Nstruct + delta_sheath_Nstruct) * 6.105e4 * parameters.AMINO_ACIDS_C_RATIO   #: �mol of C coming from AA
    s_mstruct_amino_acids_C = (delta_hiddenzone_mstruct + delta_lamina_mstruct + delta_sheath_mstruct) * parameters.RATIO_AMINO_ACIDS_MSTRUCT * 2.2405e5   #: �mol of C coming from AA
    s_mstruct_amino_acids_C = (delta_hiddenzone_mstruct + delta_lamina_mstruct + delta_sheath_mstruct) * 1.12e3   #: �mol of C coming from AA
    
    s_mstruct_C = (delta_hiddenzone_mstruct + delta_lamina_mstruct + delta_sheath_mstruct) * 3.2e4  #: Total C used for mstruct growth (�mol C)
    
    s_mstruct_sucrose_C = (delta_hiddenzone_mstruct + delta_lamina_mstruct + delta_sheath_mstruct) * (3.2e4  -  1.12e3)                        #: �mol of coming from sucrose
    s_mstruct_sucrose_C = delta_mstruct * 30880.0
"""

# Roots
def calculate_roots_mstruct_growth(sucrose, amino_acids, mstruct, delta_t, opt_postflo):
    """Root structural dry mass growth integrated over delta_t

    : Parameters:
        - `sucrose` (:class:`float`) - Amount of sucrose in roots (�mol C)
        - `amino_acids` (:class:`float`) - Amount of amino acids in roots (�mol N)
        - `mstruct` (:class:`float`) - Root structural mass (g)
        - 'delta_teq'(:class:`float`) - Time compensated for the effect of temperature - Time equivalent at Tref (s)
        - 'opt_postflo'(:class:`bool`) - Option : True to run a simulation with postflo parameter

    : Returns:
        mstruct_C_growth (�mol C), mstruct_growth (g), Nstruct_growth (g), Nstruct_N_growth (�mol N)

    :Returns Type:
        :class:`float`
    """
    conc_sucrose = max(0, sucrose/mstruct)

    if opt_postflo:
        Vmax =  parameters.VMAX_ROOTS_GROWTH_POSTFLO
    else :
        Vmax = parameters.VMAX_ROOTS_GROWTH_PREFLO
    N = 1.8

    #mstruct_C_growth = (conc_sucrose * parameters.VMAX_ROOTS_GROWTH) / (conc_sucrose + parameters.K_ROOTS_GROWTH) * delta_t * mstruct     #: root growth in C (�mol of C)
    mstruct_C_growth = ( (conc_sucrose**N) * Vmax) / ( (conc_sucrose**N) + (parameters.K_ROOTS_GROWTH**N) ) * delta_t * mstruct
    mstruct_growth = (mstruct_C_growth*1E-6 * parameters.C_MOLAR_MASS) / parameters.RATIO_C_MSTRUCT_ROOTS                                 #: root growth (g of structural dry mass)
    Nstruct_growth = mstruct_growth * parameters.RATIO_N_MSTRUCT_ROOTS_                                                                   #: root growth in N (g of structural dry mass)
    Nstruct_N_growth = min(amino_acids, (Nstruct_growth / parameters.N_MOLAR_MASS)*1E6)                                                   #: root growth in nitrogen (�mol N)

    return mstruct_C_growth, mstruct_growth, Nstruct_growth, Nstruct_N_growth
