---
title: "Space-Time Association Model for Coordinated Optimization and Network Balancing of Cross-River Tunnel Systems"
date: 2023-10-15
tags: ["network equilibrium", optimization, "behavior modeling", Shanghai]
---

<p class="lede">We develop a space–time association model that parameterizes working hours as traffic pulses. Intelligent optimization yields coordinated staggering strategies across cross-river systems, minimizing total system travel time and dynamically balancing network loads.</p>

## Research Background & Value
- Paradigm Shift: Moving beyond traditional traffic engineering, this research elevates congestion management to demand-side space–time structure governance, offering a fundamental solution based on temporal allocation.
- Behavioral Modeling: Utilizing high-resolution big data, we build a Structure–Behavior Coupling Model to quantitatively decouple how functional layouts shape individual trip behavior, providing a mechanistic foundation for policy modeling.
- Policy Value: Delivering proactive policy guidance, the work supports cooperative optimization and sustainable development, maximizing network efficiency under equity principles.

## Research Methodology
1. Behavioral Parameterization: Utilizing big data, each commuting flow is abstracted into a Gaussian distribution (traffic pulse) with adjustable mean (μ) and temporal elasticity (σ).
<figure><img src="/images/method/pulse-gaussian.jpg" alt="Parameter-control schematic of the flow-distribution model under specific spatiotemporal constraints"><figcaption>Parameter-control schematic of the flow-distribution model under specific spatiotemporal constraints</figcaption></figure>

2. Space–Time Overlap & Association: Pulses from all functional areas are superimposed across all channels; shared parameters establish network association, ensuring single-point adjustments feed back system-wide.
3. Intelligent Solution: The objective is to minimize total system travel time by iteratively searching for the best coordinated time-staggering combination.
<figure><img src="/images/method/overview.jpg" alt="Method overview"><figcaption>Method overview</figcaption></figure>


## Study Area & Data
- **Area:** Focused on Shanghai's primary cross-river tunnel and bridge systems.
- **Data:** High-resolution mobile signaling/GPS big data are used to invert and calibrate the actual behavioral parameters (μ, σ) of traffic pulses.
<figure><img src="/images/crossriver/area-shanghai.jpg" alt="Distribution of trips via Shanghai’s major cross-river tunnels (Study Area)"><figcaption>Distribution of trips via Shanghai’s major cross-river tunnels (Study Area)</figcaption></figure>


## Core Conclusions

## Mechanism Finding
A many-to-many coupling exists between tunnels and functional areas: each tunnel is influenced by multiple areas, and each area affects flows across multiple tunnels.


## Optimization Effect

### Total Flow Curves (Before vs. After)
Under the 20-minute adjustment scheme, flow balance improves markedly: standard deviations decline across corridors, yielding smoother and more even profiles—Outer Ring Tunnel 46.9→33.8 (−27.93%), Xiangyin Road Tunnel 32.3→25.2 (−21.98%), Jungong Road Tunnel 53.9→44.0 (−18.37%), and Yangpu Bridge 34.6→26.0 (−24.86%).

<figure><img src="/images/results/flow-before-after.jpg" alt="Before vs. after coordination: total cross-river flow"><figcaption>Before vs. after coordination: total cross-river flow</figcaption></figure>


### System Travel Time Comparison
The 20-minute adjustment scheme markedly reduces total system travel time, yielding ~1.12 minutes saved per person. By corridor: Outer Ring Tunnel ~1.22 min, Yangpu Bridge ~1.09 min, Xiangyin Road Tunnel ~0.96 min, and Jungong Road Tunnel ~0.80 min—mirroring the reduction in variability across corridors.

