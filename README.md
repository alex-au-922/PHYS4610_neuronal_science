<head>
  <style>
    .center_div{
      display: flex;
      justify-content: center;
      align-items: center;
    }
  </style>
</head>
# PHYS4610_neuronal_science
## Current Status

---
## Basics of Neuronal Science

Reference: [Click this link](http://www.columbia.edu/cu/appliedneuroshp/Spring2018/Spring18SHPAppliedNeuroLec5.pdf)

### Introduction
Neurons are the elementary processing units in the brain and central nervous system. When a neuron receives an appropriate stimulus, it produces **action potentials** (electrical impulses) that are propagated along its axon. When the pulse reaches the end of the neuron, other neurons or muscle cells may be activated.

The sending neuron is called the ***pre-synaptic*** cell and the receiving neuron is called the ***post-synaptic*** cell. A neuron consists of three functionally distinct parts:

- Dendrites (input): collects signals from other neurons and transmits them to the soma
- Soma (processing): if the total **non-linear input** signal from the dendrites is **greater than some threshold**, an output signal is generated
- Axon (output): electric signals are propagated away from the soma to other neurons across junctions called *synapses*.

The inside of the axon is filled with an ionic fluid that is separated from the surrounding body fluid by a thin membrane. The ionic solutes in the extracellular fluid are primarily Na+ and Cl- ions. The intracellular fluid is dominated by **K+**
and **large organic anions**.

<img src = 'https://www.irastoworldhealth.com/web/uploads/editor_uploads/neuron2.jpg?v217' style = 'text-align: center;'></img>

In the resting state, the axon membrane is **highly permeable** to **K+** ions, **slightly** permeable to **Na+** ions, and **impermeable** to large **organic** anions. Since more K+ ions leak out of the cell than Na+ ions that leak into the cell, the inside of the cell is **more negative** than the outside. 

This potential difference is called the membrane potential v_m(t). The outside of the cell is taken as the reference potential 0V. The **resting membrane potential** is often -65 mV.
<br>
### Simulating Action Potential
When a neuron receives a sufficient stimulus from other neuron, the permeability of the cell membrane changes. There is an **influx of Na+** ions into the cell while **K+ ions leave**. The movement of ions across the membrane constitute an **electric current signal**, which propagates along the axon to its terminals.

These membrane currents **depolarize the cell** and **generates a voltage signal**, which are called **spikes**. The duration of each spike is **less than a few milliseconds** or less and has a peak voltage of about +100 mV.
<br>
### Izhikevich Model
Most neurons are excitable in that they can fire a voltage spike when stimulated. We will explore the model proposed by ***Eugene Izhikevich***. The Izhikevich model does not account for the biophysics of neurons. It uses mathematical equations to compute a wide range of spiking patterns for cortical neurons. The output is **incredibly realistic** and **biologically plausible**.

4 hyperparameters, a, b, c and d are used in the Izhikevich model to determine the spiking and bursting behavior of the known types of cortical neurons. The time evolution of membrane potential v is described by the differential equations:

![](https://latex.codecogs.com/svg.latex?%5Cdot%7Bv%7D%20%3D%20c_1v%5E2%20+%20c_2v%20+%20c_3%20-%20c_4u%20+%20c_5I)
<br>
![](https://latex.codecogs.com/svg.latex?%5Cdot%7Bu%7D%20%3D%20a%28bv%20-%20u%29)
<br>
The after-spike setting relationship is that **if** v >= +30 mV **then** v tends to c **and** u tends to u + d, where c, d are **hyperparameters** and u is the **membrane recovery variable**.
<br>

### Description of Izhikevich Model
The dimensions and the variables inside the model are:
| Variable   | Description | Unit |
| ----------- | ----------- |------|
| v    |Membrane Potential| mV|
| t   | Time        | ms |
| dv/dt| Time rate of change <br> in membrane potential| mV/ms|
| u | Recovery Variable| mV |
| I | External Currents to the cell <br> (synaptic current or DC) | A |
<br>

For **regular spiking neurons**, the hyperparameters are:

| Hyperparameters  |Value | 
| ----------- | ----------- |
| a| 0.02| 
| b   | 0.20| 
| c| -65.0| 
| d | 8.00| 

<br>

For **fast spiking neurons**, the hyperparameters are:

| Hyperparameters  |Value | 
| ----------- | ----------- |
| a    | 0.10| 
| b   | 0.20| 
| c| -65.0| 
| d | 2.00| 

