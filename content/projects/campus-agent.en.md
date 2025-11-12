---
title: "Campus Dining Collective Behavior Simulation LLM-Agent × ABM"
date: 2025-11-01
tags: [LLM, RL, ABM, "Collective Behavior", "Info Provision"]
---

<p class="lede">In a dense campus, cognitive LLM-Agents drive collective time–place–mode–route decisions to quantify how information strategies redistribute queues and road loads and shave peaks at the population level.</p>

## Research Background & Value
- Population view: unify chain decisions for thousands during peaks, measuring aggregate space use and peak pressure.
- Interpretability: per-decision rationales with provenance enable causal tracing from individuals to the crowd.
- Actionability: compare global vs. beaconed information to quantify reductions in queue incidents and flow variance σ.

## Research Methodology
1. Decision framework: four loosely coupled choices—departure time, dining destination, travel mode, and route—coordinated end-to-end. Each step carries over short-term memory (STM) and prior-step environment snapshots, emits transparent rationales, and remains traceable at the individual level and aggregable at the population level.
<figure><img src="/images/method/decision.png" alt="Decision framework for dining and travel with LLM agents"><figcaption>Decision framework for dining and travel with LLM agents</figcaption></figure>

2. Memory & sensing: a sticky memory formed by a long-term preference summary plus recent events incrementally assimilates preferences over distance, price, crowding, and road load. When information strategies are enabled, dining-crowding and road-congestion enter the LLM-Agent as previous-step snapshots (≈5 minutes earlier), serving as contextual priors for the current decision.
3. Prompt–data contract: <br>
                <table>
                <thead>
                    <tr><th>Aspect</th><th>Meaning</th><th>Example prompt phrase (decision)</th></tr>
                </thead>
                <tbody>
                    <tr>
                    <td>Joint trade-offs (generic)</td>
                    <td>No fixed priority; weigh time, distance/price, preferences, crowding/congestion, and context together</td>
                    <td>“Consider all signals jointly with no fixed priority.” (all decisions)</td>
                    </tr>
                    <tr>
                    <td>Semantics & provenance (generic)</td>
                    <td>Crowding/congestion are previous-step snapshots; unknown ≠ zero; provenance must be tagged in reasons</td>
                    <td>“Crowding/road info are previous-step snapshots; unknown ≠ zero; tag provenance, e.g., [crowd_provenance: global_prev_step] / [road_provenance: beacon_prev_step].” (all)</td>
                    </tr>
                    <tr>
                    <td>Fairness & explainability (generic)</td>
                    <td>Avoid unsupported identity claims; provide traceable, aggregable rationales</td>
                    <td>“Fairness: avoid unsupported identity claims; provide transparent reasoning.” (all)</td>
                    </tr>
                    <tr>
                    <td>Salience updates (generic)</td>
                    <td>Apply small preference adjustments as sticky-memory tuning rather than hard rules</td>
                    <td>“Apply small salience adjustments in [-0.15, 0.15] as gentle memory updates.” (all)</td>
                    </tr>
                    <tr>
                    <td>Feasibility & time grid (departure)</td>
                    <td>Choose within the allowed grid under class boundaries; prefer contiguous feasible blocks</td>
                    <td>“Choose from the allowed time grid under class constraints; prefer a contiguous block around the target length.” (departure)</td>
                    </tr>
                    <tr>
                    <td>Tie-breaking under near-equivalence (departure)</td>
                    <td>Use the shortlist as a soft tie-breaker; maintain stochastic consistency if needed</td>
                    <td>“When options are close, use the shortlist as a soft tie-breaker with a consistent stochastic token.” (departure)</td>
                    </tr>
                    <tr>
                    <td>Time pressure & preferences (place)</td>
                    <td>Balance distance, price, personal preferences, and time pressure; be conservative under clearly high crowding</td>
                    <td>“Balance distance, price, preferences, and time pressure; be conservative under clearly high crowding unless explicitly justified.” (place)</td>
                    </tr>
                    <tr>
                    <td>Route features & weather (mode)</td>
                    <td>Trade off distance, route length/congestion/turns, weather, and biking overhead; reduce exposure under high congestion</td>
                    <td>“Trade off distance, route features (length/congestion/turns), weather, and biking overhead; under high congestion, reduce exposure.” (mode)</td>
                    </tr>
                    <tr>
                    <td>Length–congestion–turns (route)</td>
                    <td>Jointly optimize total length, congestion (with coverage ratio), and turning complexity; avoid overconfidence under unknowns</td>
                    <td>“Balance total length, known congestion (and coverage ratio), and turns; avoid overconfidence when congestion is unknown.” (route)</td>
                    </tr>
                </tbody>
                </table>

## Study Area & Data
- **Area:** The empirical setting is Tongji University’s Siping Road Campus in Shanghai (100.98 ha; 31,653 users), a high-density campus with seven dining facilities and 16 functional zones.
- **Data:** Data comprise 21 weekdays of Campus Smart Card System logs from May 2023 (~6.14M records; ~27,800 diners with ~250k lunch transactions, 10:00–13:30), supplemented by 198 behavioral-preference surveys capturing dining duration, strategy acceptance, information willingness, and adjustment tolerances.
<figure><img src="/images/crossriver/area-campus.png" alt="Tongji University’s Siping Road Campus in Shanghai (Study Area)"><figcaption>Tongji University’s Siping Road Campus in Shanghai (Study Area)</figcaption></figure>


## Usage & Scenarios

### Usage & Workflow
Configure information (global/road/beacons x-y-r) → run collective simulation → inspect map/curves/logs → export evaluation HTML and playback.


### Use Cases
Embed information interventions and demand-side policies (e.g., staggering, mode/route guidance) into an agent-based behavioral simulation to quantify impacts on congestion exposure, travel-time loss, accessibility, and equity; future extensions will cover supply-side scenarios (e.g., dynamic pricing, pop-up takeaway stations) to enable integrated policy appraisal and the estimation of welfare/elasticity indicators (e.g., VOT, consumer surplus, demand elasticities).


<figure class="gif-single"><video src="/assets/video/flow.mp4" controls playsinline loop muted autoplay preload="metadata" poster="/assets/video/flow_poster.jpg"></video><figcaption>Platform Usage Workflow (Video)</figcaption></figure>

<p class="proj-badges"><a class="btn btn-report" href="/files/campus_report.html" target="_blank" rel="noopener">View Sample Report</a></p>

## Core Conclusions

## Mechanism Finding
LLM-Agent log excerpts (table summarizes decisions across information scenarios).


| Agent | Scenario | Rationale |
|---|---|---|
| 22230854542 | NONE | Depart 11:50; Place Beiyuan_107; Mode walk; selects a contiguous 30-min block in the allowed grid; distance & existing preference dominate; UNKNOWN crowding is not assumed low. |
| 22230854542 | GLOBAL | Depart 11:50; Place Xiyuan_203; Mode walk; global snapshot shows rising crowding at Beiyuan (11:50–12:00) ⇒ lateral switch to a similar-distance window; 30-min integrity preserved. [prov: global_prev_step] |
| 22232494942 | NONE | Depart 11:10; Place Beiyuan_105; Mode walk; leaves earlier to avoid the 11:30 class-end surge; feasible in the time grid with lowest walking cost. |
| 22232494942 | GLOBAL | Depart 11:20; Place Beiyuan_201; Mode walk; global info indicates higher crowding for 11:10–11:20 ⇒ shift 10 min within grid and switch to an adjacent window, still satisfying continuity and pre-class constraints. [prov: global_prev_step] |
| 222310001012 | NONE | Depart 12:00; Place Xiyuan_203; Mode walk; balances noon preference and distance; UNKNOWN crowding not treated as low. |
| 222310001012 | GLOBAL | Depart 12:00; Place Xiyuan_205; Mode walk; global snapshot: growing queue at 203 while 205 slightly lower ⇒ micro-switch within the same hall to cut wait, preserving departure time & block integrity. [prov: global_prev_step] |

