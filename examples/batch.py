# SPDX-Identifier: CC0-1.0

import torch
import tad_dftd3 as d3

sample1 = dict(
    numbers=d3.util.to_number("Pb H H H H Bi H H H".split()),
    positions=torch.tensor(
        [
            [-0.00000020988889, -4.98043478877778, +0.00000000000000],
            [+3.06964045311111, -6.06324400177778, +0.00000000000000],
            [-1.53482054188889, -6.06324400177778, -2.65838526500000],
            [-1.53482054188889, -6.06324400177778, +2.65838526500000],
            [-0.00000020988889, -1.72196703577778, +0.00000000000000],
            [-0.00000020988889, +4.77334244722222, +0.00000000000000],
            [+1.35700257511111, +6.70626379422222, -2.35039772300000],
            [-2.71400388988889, +6.70626379422222, +0.00000000000000],
            [+1.35700257511111, +6.70626379422222, +2.35039772300000],
        ]
    ),
)
sample2 = dict(
    numbers=d3.util.to_number("C C C C C C I H H H H H S H C H H H".split(" ")),
    positions=torch.tensor(
        [
            [-1.42754169820131, -1.50508961850828, -1.93430551124333],
            [+1.19860572924150, -1.66299114873979, -2.03189643761298],
            [+2.65876001301880, +0.37736955363609, -1.23426391650599],
            [+1.50963368042358, +2.57230374419743, -0.34128058818180],
            [-1.12092277855371, +2.71045691257517, -0.25246348639234],
            [-2.60071517756218, +0.67879949508239, -1.04550707592673],
            [-2.86169588073340, +5.99660765711210, +1.08394899986031],
            [+2.09930989272956, -3.36144811062374, -2.72237695164263],
            [+2.64405246349916, +4.15317840474646, +0.27856972788526],
            [+4.69864865613751, +0.26922271535391, -1.30274048619151],
            [-4.63786461351839, +0.79856258572808, -0.96906659938432],
            [-2.57447518692275, -3.08132039046931, -2.54875517521577],
            [-5.88211879210329, 11.88491819358157, +2.31866455902233],
            [-8.18022701418703, 10.95619984550779, +1.83940856333092],
            [-5.08172874482867, 12.66714386256482, -0.92419491629867],
            [-3.18311711399702, 13.44626574330220, -0.86977613647871],
            [-5.07177399637298, 10.99164969235585, -2.10739192258756],
            [-6.35955320518616, 14.08073002965080, -1.68204314084441],
        ]
    ),
)
numbers = d3.util.pack(
    (
        sample1["numbers"],
        sample2["numbers"],
    )
)
positions = d3.util.pack(
    (
        sample1["positions"],
        sample2["positions"],
    )
)
ref = d3.reference.Reference()
rcov = d3.data.covalent_rad_d3[numbers]
rvdw = d3.data.vdw_rad_d3[numbers.unsqueeze(-1), numbers.unsqueeze(-2)]
r4r2 = d3.data.sqrt_z_r4_over_r2[numbers]
param = dict(a1=0.49484001, s8=0.78981345, a2=5.73083694)

cn = d3.ncoord.coordination_number(numbers, positions, rcov, d3.ncoord.exp_count)
weights = d3.model.weight_references(numbers, cn, ref, d3.model.gaussian_weight)
c6 = d3.model.atomic_c6(numbers, weights, ref)
energy = d3.disp.dispersion(
    numbers, positions, c6, rvdw, r4r2, d3.disp.rational_damping, **param
)

torch.set_printoptions(precision=10)
print(torch.sum(energy, dim=-1))
