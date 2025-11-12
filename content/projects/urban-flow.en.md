---
title: "Interactive Urban Flow Analysis & Optimization"
date: 2024-03-07
tags: ["Traffic Behavior", ABM, Vis, "Policy Sandbox"]
---

<p class="lede">Couples behavior–network–land-use for explainable spacetime analysis, congestion-source tracing, and a policy sandbox (time shifting / spatial guidance), with evaluation via variance (σ) reduction and y=x reference scatter.</p>

## Research Background & Value
- Behavioral lens: align work-time, employment centers, and grid flows on a unified spatiotemporal coordinate to explain who/when/where congestion emerges
- Actionable: two interventions (time-shifting / spatial scaling) with quantitative assessment by variance σ and shifts of scatter relative to y=x
- Explainable: per-grid source attribution (centers vs. non-centers) for evidence-based communication with stakeholders

## Research Methodology
1. Grid-based spacetime rendering with linked charts and time series per grid
2. Congestion mining via high-quantile thresholding for peak-hour detection, frequency and persistence
3. Source attribution by employment-center contribution ratios with hinterland delineation
4. Policy sandbox: ±30 min time-shift and center scaling (0.0–2.0); compare σ pre/post and the aggregate shift of scatter vs. y=x

## Study Area & Data
- **Area:** Study area: urban core road grids (extendable to multi-district or metropolitan scale).
- **Data:** Data: grid-based road flows (minute-level or finer), employment-center POIs/regions with intensity, and auxiliary variables (calendar/weather/events). All datasets are harmonized to a common spatial reference and time index for superposition and analysis.

## Usage & Scenarios

### Usage & Workflow
(1) Select time window and spatial extent; (2) Filter congested grids via high-quantile thresholds and inspect frequency/persistence; (3) Examine source contributions and hinterlands; (4) In the policy sandbox, set time-staggering (±30 min) and center scaling (0.0–2.0); (5) Export reports with pre/post σ and scatter vs. y=x.


### Use Cases
Morning-peak diagnosis, local bottleneck tracing, center expansion or de-concentration assessment, optimal time-staggering portfolios, and before/after comparisons for infrastructure proposals.


<figure class="gif-single"><img src="/assets/gif/flow.gif" alt="Platform Usage Workflow (GIF)"><figcaption>Platform Usage Workflow (GIF)</figcaption></figure>

<p class="proj-badges"><span class="badge badge-soft">Software copyright registered.</span> <a class="btn btn-report" href="/files/urban_flow_demo_report.html" target="_blank" rel="noopener">View Sample Report</a></p>
