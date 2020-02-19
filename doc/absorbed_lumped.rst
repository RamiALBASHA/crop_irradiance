Absorbed lumped irradiance
==========================
**Monsi and Saeki (1953)** were probably the first to use Beer-Lambert's law in order to simulate irradiance transfer
through crop canopies. Following this approach, leaves are assumed to form a continuous turbid medium that intercepts the incident
irradiance :math:`I_{inc} \ [W \cdot m^{-2}_{ground}]` and the ability of the canopy to transfer irradiance is
represented by the so-called so-called extinction coefficient property
:math:`k_{lumped} \ [m^2_{ground} \cdot m^{-2}_{leaf}]`.

Below a given depth :math:`L \ [m^2_{leaf} \cdot m^{-2}_{ground}]` inside the canopy, the flux density of the
transmitted irradiance :math:`I_{trans} \ [W \cdot m^{-2}_{ground}]` is calculated as:

.. math::
    :label: lumped_beer_transmitted

    I_{trans} = I_{inc} \cdot \exp \left( -k_{lumped} \cdot L \right)

Given a finite leaf layer of a thickness :math:`dL \ [m^2_{leaf} \cdot m^{-2}_{ground}]` at depth :math:`L` , the
absorbed *lumped* irradiance :math:`d I_{abs} \ [W \cdot m^{-2}_{ground}]` can be calculated as:

.. math::
    :label: lumped_beer_absorbed_finite_layer

    \frac{d I_{abs, \ lumped}}{d L} =& - \frac{d I_{trans}}{d L}  \\
                                    =&  k_{lumped} \cdot I_{inc} \cdot \exp(-k_{lumped} \cdot L)



Layered canopies
----------------

.. _fig_absorption_lumped:

.. figure:: figs/absorption_lumped.png
    :align: center

    Illustration of the different leaf depths considered for the calculation of the absorbed lumped irradiance.

The rate of the absorbed irradiance of a leaf layer that spands between an upper depth
:math:`L_u \ [m^2_{leaf} \cdot m^{-2}_{ground}]` and a lower depth :math:`L_l \ [m^2_{leaf} \cdot m^{-2}_{ground}]`
(:numref:`fig_absorption_lumped`) is obtained from :eq:`lumped_beer_absorbed_finite_layer` as:

.. math::
    :label: lumped_absorbed_layer_integral

    I_{abs, \ lumped} = \int_{L_u}^{L_l} {k_{lumped} \cdot I_{inc} \cdot \exp(-k_{lumped} \cdot L) \ dL}

which yields:

.. math::
    :label: lumped_absorbed_layered

    I_{abs, \ lumped} = I_{inc} \cdot \left[ \exp(-k_{lumped} \cdot L_u) - exp(-k_{lumped} \cdot L_l) \right]

Bigleaf canopies
----------------
Irradiance absorption by a *bigleaf* canopy is simply derived from :eq:`lumped_absorbed_layered` by replacing
:math:`L_u` and :math:`L_l` by 0 and the total leaf area index :math:`L_{t} \ [m^2_{leaf} \cdot m^{-2}_{ground}]`,
respectively, which yields:

.. math::
    :label: lumped_absorbed_big_leaf

    I_{abs, \ lumped} = I_{inc} \cdot \left[1 - \exp(-k_{lumped} \cdot L_t) \right]

