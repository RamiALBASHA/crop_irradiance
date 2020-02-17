Irradiance absorption by the sunlit and shaded fractions at the leaf layer scale
================================================================================
Let's recall first that sunlit leaves receive irradiance that comes both from the solar beam, from sky-diffused, and
from leaf irradiance scattering ("second-hand" irradiance), while shaded leaves receive only
sky-diffused and leaf-scattered irradiance. On a leaf area basis, irradiance absorption by each of both sunlit
and shade leaves writes:

.. math::
    :label: sunlit_abs_on_leaf_basis

    I_{abs, \ sun} = I_{abs, \ b} + I_{abs, \ d} + I_{abs, \ s}

.. math::
    :label: shaded_abs_on_leaf_basis

    I_{abs, \ shade} = I_{abs, \ d} + I_{abs, \ s}

where
:math:`I_{abs, \ sun}` and :math:`I_{abs, \ shade \ [W \ m^{-2}_{leaf}]}` are total irradiance
flux densities absorbed respectively by sunlit and shaded leaves at depth :math:`L \ [m^2_{leaf} \ m^{-2}_{ground}]`,
:math:`I_{abs, \ b}`, :math:`I_{abs, \ d}`, and :math:`I_{abs, \ s \ [W \ m^{-2}_{leaf}]}` are the absorbed irradiance
flux densities from solar beam, sky-diffused and leaf-scattered irradiance components, respectively.

Among the aforementioned irradiance components, beam irradiance is the only one that is constant across depth for a
given time step: we deal here with sunflecks that are all characterized by the same irradiance flux density:

.. math::
    :label: beam_abs

    I_{abs, \ b} = I_{dir} \cdot (1 - \sigma) \cdot k^{'}_{dir}


where
:math:`I_{dir} \ [W \ m^{-2}_{ground}]` is the horizontal solar direct (beam) irradiance incident on the top of the
canopy.

What does changes with depth, however, is the fraction of sunlit leaf surface with respect to the total leaf surface at
the depth :math:`L`, :math:`\phi_{sun} \ [-]`. This fraction translates the probability that incident beam flux may not
be intercepted at :math:`L`, and may be described by the Beer-Lambert’s law for black leaves **(cf. Eq. 4)**:

.. math::
    :label: sunlit_fraction_leaf_basis

    \phi_{sun} = \exp \left( - k^{'}_{dir} \cdot L \right)

which implies that the fraction of shaded leaves (:math:`\phi_{shade} \ [-]`)) is:

.. math::
    :label: shaded_fraction_leaf_basis

    \phi_{shade} = 1 - \phi_{sun}


The sky-diffused irradiance is distributed within the canopy following practically an exponential trend.
At depth :math:`L`, the absorbed sky-diffused irradiance per unit leaf area is given as:

.. math::
    :label: diffuse_abs

    I_{abs \ d}} = I_{dif} \cdot \right( 1 - \rho_{dif} \left) \cdot k_{dif} \cdot \exp \left( -k_{dif} \cdot L \right)

where
:math:`I_{dif} \ [W \ m^{-2}_{ground}]` is the horizontal sky-diffused irradiance incident on the top of the canopy.

Finally, the absorption of the leaf-scattered irradiance (:math:`I_{abs, \ s}`) is given as:

.. math::
    :label: scattered_abs

    I_{abs \ s}} = I_{dir} \cdot
                        \left[
                            (1 - \rho_{dir}) \cdot k_{dir} \exp (-k_{dif} \cdot L)
                            -(1 - \sigma) \cdot k^{'}_{dir} \cdot \exp (-k^{'}_{dir} \cdot L)

                        \right]