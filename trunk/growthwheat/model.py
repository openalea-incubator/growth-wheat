# -*- coding: latin-1 -*-

from __future__ import division # use "//" to do integer division

"""
    growthwheat.model
    ~~~~~~~~~~~~~

    The module :mod:`growthwheat.model` defines the equations of the kinetic of leaf elongation according to CN status.

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

import math
import parameters

def calculate_hgz_length(previous_hgz_L, previous_sheath_visible_L, previous_sheath_final_hidden_L):
    """ length of the hidden growing zone given by the previous sheaths.

    :Parameters:
        - `previous_hgz_L` (:class:`float`) - Length of the previous hidden growing zone (m). Could be 0 is no previous hgz found.
        - `previous_sheath_visible_L` (:class:`float`) - Visible length of the previous sheath (m).
        - `previous_sheath_final_hidden_L` (:class:`float`) - Final hidden length of the previous sheath (m).
    :Returns:
        Hidden growing zone length (m)
    :Returns Type:
        :class:`float`
    """
    if previous_hgz_L:
        hgz_L = previous_hgz_L + previous_sheath_visible_L
    else:
        hgz_L = previous_sheath_final_hidden_L + previous_sheath_visible_L # here 'previous_sheath_visible_L' is also the final visible length of the previous sheath
    return hgz_L


def calculate_deltaL_preE(sucrose, leaf_L, amino_acids, mstruct, delta_t):
    """ delta of leaf length over delta_t as a function of sucrose and amino acids, from initiation to the emergence of the previous leaf.

    :Parameters:
        - `sucrose` (:class:`float`) - Amount of sucrose (�mol C)
        - `leaf_L` (:class:`float`) - Total leaf length (m)
        - `amino_acids` (:class:`float`) - Amount of amino acids (�mol N)
        - `mstruct` (:class:`float`) - Structural mass (g)
    :Returns:
        delta delta_leaf_L (m)
    :Returns Type:
        :class:`float`
    """
    if sucrose > 0:
        delta_leaf_L = leaf_L * ((sucrose / mstruct) / (parameters.Kc + (sucrose / mstruct))) * (((amino_acids/mstruct) **3) / (parameters.Kn**3 + (amino_acids / mstruct)**3)) * parameters.RERmax * delta_t
    else:
        delta_leaf_L = 0
    return delta_leaf_L

def calculate_deltaL_postE(leaf_L, leaf_Lmax, sucrose, delta_t):
    """ delta of leaf length, from the emergence of the previous leaf to the end of growth (predefined growth kinetic depending on leaf state).

    :Parameters:
        - `leaf_L` (:class:`float`) - Total leaf length (m)
        - `leaf_Lmax` (:class:`float`) - Final leaf length (m)
        - `sucrose` (:class:`float`) - Amount of sucrose (�mol C)
    :Returns:
        delta delta_leaf_L (m)
    :Returns Type:
        :class:`float`
    """
    if sucrose > 0:
        delta_leaf_L = parameters.K * leaf_L * max(((leaf_L / leaf_Lmax) - 1)**2, parameters.EPSILON**2)**(parameters.N) * delta_t
    else:
        delta_leaf_L = 0
    return delta_leaf_L

def calculate_leaf_Lmax(leaf_Lem_prev):
    """ Final leaf length.

    :Parameters:
        - `leaf_Lem_prev` (:class:`float`) - Leaf length at the emergence of the previous leaf (m)
    :Returns:
        Final leaf length (m)
    :Returns Type:
        :class:`float`
    """
    return leaf_Lem_prev * parameters.Y0

def calculate_SL_ratio(phytomer_rank):
    """ Sheath:Lamina final length ratio according to the rank. Parameters from Dornbush (2011).

    :Parameters:
        - `phytomer_rank` (:class:`float`)
    :Returns:
        Sheath:Lamina ratio (dimensionless)
    :Returns Type:
        :class:`float`
    """
    return -0.0021 * phytomer_rank**3 + 0.037 * phytomer_rank**2 - 0.1527 * phytomer_rank + 0.4962

def calculate_lamina_Lmax(leaf_Lmax, sheath_lamina_ratio):
    """ Final lamina length.

    :Parameters:
        - `leaf_Lmax` (:class:`float`) - Final leaf length (m)
        - `sheath_lamina_ratio` (:class:`float`) - Sheath:Lamina ratio (dimensionless)

    :Returns:
        final lamina length (m)
    :Returns Type:
        :class:`float`
    """
    return leaf_Lmax / (1 + sheath_lamina_ratio)

def calculate_sheath_Lmax(leaf_Lmax, lamina_Lmax):
    """ Final sheath length.

    :Parameters:
        - `leaf_Lmax` (:class:`float`) - Final leaf length (m)
        - `lamina_Lmax` (:class:`float`) - Final lamina length (m)

    :Returns:
        final sheath length (m)
    :Returns Type:
        :class:`float`
    """
    return leaf_Lmax - lamina_Lmax

def calculate_leaf_Wmax(lamina_Lmax, fructan, mstruct):
    """ Maximal leaf width.
    0.0575 et 0.12 issu graph Dornbush

    :Parameters:
        - `lamina_Lmax` (:class:`float`) - Maximal lamina length (m)
        - `fructan` (:class:`float`) - Fructan in the hidden growing zone at the time of the previous leaf emergence (�mol C).
        - `mstruct` (:class:`float`) - Mstruct of the hidden growing zone at the time of the previous leaf emergence (g).
    :Returns:
        maximal leaf width (m)
    :Returns Type:
        :class:`float`
    """
    return (0.0575 * lamina_Lmax - 0.00012) * (parameters.EC_wmax * 2 * parameters.Ksslw/(parameters.Ksslw + (fructan / mstruct)) + (1-parameters.EC_wmax)) #TODO: a remplacer

def calculate_SSLW(fructan, mstruct):
    """ Structural Specific Lamina Weight.

    :Parameters:
        - `fructan` (:class:`float`) - Fructan in the hidden growing zone at the time of the previous leaf emergence (�mol C).
        - `mstruct` (:class:`float`) - Mstruct of the hidden growing zone at the time of the previous leaf emergence (g).
    :Returns:
        Structural Specific Leaf Weight (g m-2)
    :Returns Type:
        :class:`float`
    """
    conc_fructan = fructan / mstruct
    return parameters.min_SSLW + (parameters.max_SSLW - parameters.min_SSLW) * conc_fructan/ (conc_fructan + parameters.Ksslw)

def calculate_SSSW(SSLW):
    """ Structural Specific Sheath Weight.

    :Parameters:
        - `SSLW` (:class:`float`) - Structural Specific Leaf Weight (g m-2).
    :Returns:
        Structural Specific Sheath Weight (g m-2)
    :Returns Type:
        :class:`float`
    """
    return SSLW * parameters.ratio_SSSW_SSLW

def calculate_leaf_emergence(leaf_L, hgz_L):
    """Calculate if a given leaf has emerged from the hidden growing zone

    :Parameters:
        - `leaf_L` (:class:`float`) - Total leaf length (m)
        - `hgz_L` (:class:`float`) - Length of the hidden growing zone (m)
    :Returns:
        Specifies if the leaf has emerged (True) or not (False)
    :Returns Type:
        :class:`bool`
    """
    return leaf_L > hgz_L

def calculate_lamina_L(leaf_L, hgz_L):
    """ Emerged lamina length given by the difference between leaf length and hidden growing zone length.

    :Parameters:
        - `leaf_L` (:class:`float`) - Total leaf length (m)
        - `hgz_L` (:class:`float`) - Length of the hidden growing zone (m)
    :Returns:
        lamina length (m)
    :Returns Type:
        :class:`float`
    """
    lamina_L = leaf_L - hgz_L
    if lamina_L <=0:
        raise Warning('the leaf is shorther than the hgz')
    return max(0, lamina_L)

def calculate_sheath_L(leaf_L, hgz_L, lamina_L):
    """ Emerged sheath length. Assumes that leaf_L = hgz_L + sheath_L + lamina_L

    :Parameters:
        - `leaf_L` (:class:`float`) - Total leaf length (m)
        - `hgz_L` (:class:`float`) - Length of the hidden growing zone (m)
        - `lamina_L` (:class:`float`) - Lamina length (m)
    :Returns:
        sheath length (m)
    :Returns Type:
        :class:`float`
    """
    return leaf_L - hgz_L - lamina_L