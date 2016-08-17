# -*- coding: latin-1 -*-

from __future__ import division # use "//" to do integer division

"""
    growthwheat.parameters
    ~~~~~~~~~~~~~~~~~~~~~~

    The module :mod:`growthwheat.parameters` defines the constant parameters.

    :copyright: Copyright 2015 INRA-ECOSYS, see AUTHORS.
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

hour_to_second_conversion_factor = 3600. #: TODO: temporary

c1 = 0.56 #: Coeeficient de forme, partie distale de la feuille (SU)
c2 = 268274 #: Coefficient de forme de la feuille. Partie basale de la feuille (SU)
EC_wmax = 0.3 #: variation de + ou - 15% de maximal leaf width (SU)
Klig = 0.6 #: ratio reliant la largeur maximale et la largeur de la gaine
alpha_mass_growth = 1.73e-05 # Param�tre de croissance massique. Utilis� dans la relation de puissance entre la longueur L et la matiere seche. g.mm^(-beta). Issu Williams (1975).
beta_mass_growth = 1.74 # Param�tre de croissance massique. Utilis� dans la relation de puissance entre la longueur L et la matiere seche. Issu Williams (1975).
RATIO_MSTRUCT_DM = 0.8 #: Ratio Mstruc/Mseche
Y0 = 137 #: Facteur agrandissement feuille en mode automate (SU)
K = 0.0239 #: Parameter of the growth function after previous leaf emergence
N = 0.4612 #: Parameter of the growth function after previous leaf emergence
Ksslw = 10000 #: Affinit� SSLW aux fructanes
Kc = 350 #: affinit� du RER au C (�mol/g)
Kn = 40 #: affinit� du RER � N (�mol/g)
L0 = 0.04 #: Initial leaf length (mm)
min_SSLW = 2.2e-05 #: g/mm�
max_SSLW = 5e-05 #: g/mm�
ratio_SSSW_SSLW = 5 # ratio gaine/limbe des matieres seches structurales sp�cifiques (calcul� depuis les donn�es de J. Bertheloot, 2004)
N_feuille = 5 #:rang de la feuille
RERmax = 4e-06 #: s-1
taux_respi = 890 #: Taux de respiration due � l'accroissement de la feuille (�mol sucrose respir� / g cr��). Cela fait env. 0.13g de C perdu par respi pour 1 g de mstruct creee
Swmax = (-N_feuille / 30) + (103 / 150) # 'Param pour Position de Wmax le long du limbe
RATIO_CN_MSTRUCT = 0.416 #: Pourcentage de masse structurale d�e uniquement aux atomes de C et de N (SU)
ratio_sucrose_mstruct =  58656.667      #: Amount of C sucrose (�mol C) in 1 g of mstruct (of CN), calculation = ( (92.3e-2)/(12) - (7.7*4.15e-2)/(14*1.25) ) *1e6
ratio_amino_acids_mstruct = 5500.0      #: Amount of N amino acids (�mol N) in 1 g of mstruct (of CN), calculation = (7.7e-2)/(14)* 1e6
NB_C_SUCROSE = 12                       #: Number of C in 1 mol of sucrose