Absorbed lumped irradiance
==========================
**Monsi and Saeki (1953)** were probably the first to employ Beer-Lambert's law to simulate irradiance transfer through crop
canopies. Following this approach, leaves are assumed to form a continuous turbid medium that intercepts the incident
irradiance :math:`I_{inc} \ [W \cdot m^{-2}_{ground}]` following the so-called extinction coefficient property
:math:`k_{lumped} \ [m^2_{ground} \cdot m^{-2}_{leaf}]`.
Below a given depth :math:`L \ [m^2_{leaf} \cdot m^{-2}_{ground}]` inside the canopy, the rate of the transmitted
irradiance  :math:`I_{trans} \ [W \cdot m^{-2}_{ground}]` writes:

.. math::
    :label: eq:toto

    I_{trans} = I_{inc} \cdot \exp(-k_{lumped} \cdot L)

Given at this depth :math:`L` a finite leaf layer of a thickness :math:`dL \ [m^2_{leaf} \cdot m^{-2}_{ground}]`, the
absorbed irradiance :math:`dI_{abs} \ [W \cdot m^{-2}_{ground}]` can be calculated as:

.. math::
    dI_{abs, \ lumped} = k_{lumped} \cdot I_{inc} \cdot \exp(-k_{lumped} \cdot L) \ dL


Layered canopies
----------------

.. _fig_absorption_lumped:

.. figure:: figs/absorption_lumped.png
    :align: center

    Illustration of the different leaf depths considered for the calculation of the absorbed lumped irradiance.

The rate of the absorbed irradiance of a leaf layer that spands between an upper depth
:math:`L_u \ [m^2_{leaf} \cdot m^{-2}_{ground}]` and a lower depth :math:`L_l \ [m^2_{leaf} \cdot m^{-2}_{ground}]`
(:numref:`fig_absorption_lumped`) is obtained by performing the integral of :numref:`toto` as:

.. math::
    I_{abs, \ lumped} = \int_{L_u}^{L_l} {k_{lumped} \cdot I_{inc} \cdot \exp(-k_{lumped} \cdot L) \ dL}

which yields:

.. math::
    I_{abs, \ lumped} = I_{inc} \cdot \left[exp(-k_{lumped} \cdot L_u) - exp(-k_{lumped} \cdot L_l) \right]

Bigleaf canopies
----------------
Irradiance absorption by a bigleaf canopy can simply be derived from the last equation by replacing :math:`L_u` by 0
and by setting :math:`L_l` to the total leaf area index :math:`L_{t} \ [m^2_{leaf} \cdot m^{-2}_{ground}]`:

.. math::
    I_{abs, \ lumped} = I_{inc} \cdot \left[1 - exp(-k_{lumped} \cdot L_t) \right]

