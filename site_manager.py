# -*- coding: utf-8 -*-

from __future__ import annotations
import argparse, re
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).parent

# 拆分标题中的全角/半角括号副标题
def _split_title_with_subtitle(title: str):
    """
    输入: "主标题（副标题）" 或 "Main title (subtitle)"
    返回: (main, sub)；若无副标题则 sub 为空串
    """
    if not title:
        return "", ""
    # 尝试匹配 "xxx（yyy）" 或 "xxx (yyy)"
    m = re.match(r'^\s*(.*?)\s*(?:（|\()\s*(.+?)\s*(?:）|\))\s*$', title)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return title.strip(), ""

# ========== 你只需要改这里的 CONFIG ==========
CONFIG = {
    "github_user": "luoxinlan322-sudo",

    "zh": {
        "title": "罗歆兰 | 个人主页",
        "author": "罗歆兰",
        "info": "行为 · 城市 · AI Agent\\n空间系统建模与智能模拟",
        "desc": "城市空间行为、ABM、RL、LLM",
    },
    "en": {
        "title": "Xinlan Luo | Home",
        "author": "Xinlan Luo",
        "info": "Behavior · Cities · AI Agents\\nSpatial System Modeling & Simulation",
        "desc": "Spatial behavior, ABM, RL, LLM",
    },

    # 静态资源（放 static 下）
    "avatar_url": "images/avatar.jpg",
    "resume_pdf": "files/resume.pdf",

    # 字体来源：google / loli / none(自托管)
    "css_cdn": "google",
    # 样式版本（会拼进文件名用于缓存刷新）
    "css_version": "v7",
    # 首页简介
    "home": {
        "zh": {
            "title": "你好，我是罗歆兰",
            "body": "城市空间行为 × 智能体模拟（ABM）× RL × LLM  \n查看我的 [项目](/projects/) ｜ 下载我的 [简历](/resume/)"
        },
        "en": {
            "title": "Hi, I'm Xinlan Luo",
            "body": "Urban spatial behavior × ABM × RL × LLM  \nSee my [Projects](/en/projects/) ｜ Get my [Resume](/en/resume/)"
        }
    },

    # 首页社交图标（Font Awesome）
    "social": [
        {"name": "GitHub",   "icon": "fa-brands fa-github",   "url": "https://github.com/luoxinlan322-sudo"},
        {"name": "LinkedIn", "icon": "fa-brands fa-linkedin", "url": "https://www.linkedin.com/in/歆兰-罗-268a3138b"},
        {"name": "Gmail",    "icon": "fa-regular fa-envelope",  "url": "mailto:luoxinlan322@gmail.com"},
        {"name": "Xiaohongshu", "icon": "fa-solid fa-book", "iconSVG": "icons/xhs.svg", "url": "https://www.xiaohongshu.com/user/profile/5c064b1a0000000007008f52"},
        {"name": "YouTube", "icon": "fa-brands fa-youtube", 
     "url": "https://www.youtube.com/channel/UCPAgZAesIccxQmRA6OkBaGQ"}
    ],

    "projects": [
        {   
            "slug": "campus-agent",
            "date": "2025-11-01",
            "tags": ["LLM", "RL", "ABM", "Collective Behavior", "Info Provision"],

            # 标题
            "title_zh": "校园餐饮群体行为模拟系统 LLM-Agent × ABM",
            "title_en": "Campus Dining Collective Behavior Simulation LLM-Agent × ABM",

            # 一句话摘要（lede）
            "pitch_zh": "在高密度校园中，以认知 LLM-Agents 驱动群体的“出发–就餐窗口–方式–路径”联动决策，评估信息策略对群体队列与道路负载的再分配与峰值削减效果。",
            "pitch_en": "In a dense campus, cognitive LLM-Agents drive collective time–place–mode–route decisions to quantify how information strategies redistribute queues and road loads and shave peaks at the population level.",

            # 背景与价值
            "value_zh": [
                "群体视角：统一刻画上万人在高峰期的链式决策并度量整体空间利用与峰值压力。",
                "可解释：每次决策均附来源标签与理由，支持从个体到群体的因果溯源与模式归纳。",
                "可干预：对比全局/碑牌等信息策略，量化群体排队事件与道路方差 σ 的改善幅度。"
            ],
            "value_en": [
                "Population view: unify chain decisions for thousands during peaks, measuring aggregate space use and peak pressure.",
                "Interpretability: per-decision rationales with provenance enable causal tracing from individuals to the crowd.",
                "Actionability: compare global vs. beaconed information to quantify reductions in queue incidents and flow variance σ."
            ],

            # 方法（条目）
            "method_zh": [
                "LLM Agent 的决策框架：决策框架：围绕“何时出发、去哪就餐、采用何种方式、沿何路径”的四类选择，弱耦合协同。每一步均承接上一步的短期记忆（STM）与环境快照，输出可解释的理由；个体层面可追踪，群体层面可聚合评估。",
                "记忆与信息感知系统：以‘长期偏好摘要 + 近期事件’构成粘性记忆，逐步吸收对距离、价格、拥挤度与通行负载等要素的偏好；在相关信息策略开启时，餐厅拥挤与道路拥堵以‘上一仿真步（约5分钟之前）’的快照形式注入 LLM-Agent 的输入，用作当步决策的情境先验。",
                """给 LLM 的提示词：<br>
                <table>
                <thead>
                    <tr><th>评估维度</th><th>含义</th><th>示例提示词表述（所属决策）</th></tr>
                </thead>
                <tbody>
                    <tr>
                    <td>联合权衡（通用）</td>
                    <td>不设固定优先级，综合考虑时间、距离/价格、偏好、拥挤/拥堵与环境上下文</td>
                    <td>“Consider all signals jointly with no fixed priority.”（四类通用）</td>
                    </tr>
                    <tr>
                    <td>信息语义与来源（通用）</td>
                    <td>拥挤/拥堵为“上一仿真步”快照；未知≠为零；在理由中标注来源</td>
                    <td>“Crowding/road info are previous-step snapshots; unknown ≠ zero; tag provenance in reasons, e.g., [crowd_provenance: global_prev_step] / [road_provenance: beacon_prev_step]。”（四类通用）</td>
                    </tr>
                    <tr>
                    <td>公平性与可解释（通用）</td>
                    <td>避免无依据的身份推断；输出可追踪、可聚合的理由</td>
                    <td>“Fairness: avoid unsupported identity claims; provide transparent reasoning.”（四类通用）</td>
                    </tr>
                    <tr>
                    <td>显著性微调（通用）</td>
                    <td>作出小幅偏好更新，作为粘性记忆的温和调节，而非硬规则</td>
                    <td>“Apply small salience adjustments in [-0.15, 0.15] as gentle memory updates.”（四类通用）</td>
                    </tr>
                    <tr>
                    <td>可行性约束与网格（出发）</td>
                    <td>在允许时间网格内选择，严格满足课表边界；优先完整连续时段</td>
                    <td>“Choose from the allowed time grid under class constraints; prefer a contiguous block around the target length.”（出发）</td>
                    </tr>
                    <tr>
                    <td>近似等效时的裁决（出发）</td>
                    <td>候选短名单可作为软性平局裁决，必要时引入轻度随机一致性</td>
                    <td>“When options are close, use the shortlist as a soft tie-breaker, with a consistent stochastic token if needed.”（出发）</td>
                    </tr>
                    <tr>
                    <td>时间压力与偏好（就餐地点）</td>
                    <td>与距离/价格/个体偏好共同权衡；已知高拥挤（≈≥0.90）时更保守，但可在强理由下例外</td>
                    <td>“Balance distance, price, preferences, and time pressure; be conservative under clearly high crowding unless explicitly justified.”（就餐地点）</td>
                    </tr>
                    <tr>
                    <td>路线要素与天气（方式）</td>
                    <td>结合路程、拥堵总量、转弯数、天气与骑行开销；高拥堵时减少暴露</td>
                    <td>“Trade off distance, route features (length/congestion/turns), weather, and biking overhead; under high congestion, reduce exposure.”（方式）</td>
                    </tr>
                    <tr>
                    <td>长度—拥堵—转向（路径）</td>
                    <td>在总长度、拥堵（含可观测比例）与转向复杂度间共同优化；未知时避免过度自信</td>
                    <td>“Balance total length, known congestion (and coverage ratio), and turns; avoid overconfidence when congestion is unknown.”（路径）</td>
                    </tr>
                </tbody>
                </table>"""
                            ],
            "method_en": [
                "Decision framework: four loosely coupled choices—departure time, dining destination, travel mode, and route—coordinated end-to-end. Each step carries over short-term memory (STM) and prior-step environment snapshots, emits transparent rationales, and remains traceable at the individual level and aggregable at the population level.",
                "Memory & sensing: a sticky memory formed by a long-term preference summary plus recent events incrementally assimilates preferences over distance, price, crowding, and road load. When information strategies are enabled, dining-crowding and road-congestion enter the LLM-Agent as previous-step snapshots (≈5 minutes earlier), serving as contextual priors for the current decision.",
                """Prompt–data contract: <br>
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
                </table>"""
            ],

            # 方法：逐条可选配图（核心图表 #1）
            "method_fig_map": [
                {},
                {
                    "index": 1,
                    "src": "/images/method/decision.png",
                    "cap_zh": "LLM-Agent的就餐出行决策框架",
                    "cap_en": "Decision framework for dining and travel with LLM agents"
                }
            ],
           
            # 如有“方法总览图”，可放这里（可选）
            "method_images": [
             #   {"src": "/images/method/overview.jpg", "cap_zh": "方法流程总览", "cap_en": "Method overview"}
            ],

            # 研究区域与数据（上半区）
            "study_area_zh": "实证场地为同济大学四平路校区（上海，100.98 公顷，服务 31,653 人），为高密度校园，含 7 个餐饮场所与 16 个功能分区。",
            "study_area_en": "The empirical setting is Tongji University’s Siping Road Campus in Shanghai (100.98 ha; 31,653 users), a high-density campus with seven dining facilities and 16 functional zones.",
            "study_data_zh": "数据包括 2023 年 5 月 21 个工作日的校园一卡通日志（约 614 万条；午餐 10:00–13:30 时段覆盖约 27,800 人、约 25 万次就餐交易），并辅以 198 份行为偏好问卷（用时、策略接受度、信息意愿与可接受调整幅度等）。",
            "study_data_en": "Data comprise 21 weekdays of Campus Smart Card System logs from May 2023 (~6.14M records; ~27,800 diners with ~250k lunch transactions, 10:00–13:30), supplemented by 198 behavioral-preference surveys capturing dining duration, strategy acceptance, information willingness, and adjustment tolerances.",

            "study_images": [
                {"src": "/images/crossriver/area-campus.png", "cap_zh": "研究区域——同济大学四平路校区", "cap_en": "Tongji University’s Siping Road Campus in Shanghai (Study Area)"}
            ],
            # 新增：方法之后的“使用与场景”板块（仅 urban-flow）
            "usage_sections_zh": [
                {"title": "使用功能与流程",
                "body": "选择信息策略（全局/道路/碑牌坐标与半径）→ 运行群体仿真 → 查看地图（轨迹/道路热度）、曲线（拥挤/队列）、日志（个体理由）→ 一键导出评估 HTML 与回放结果。"},
                {"title": "应用场景",
                "body": "将信息干预与需求侧政策（如错峰引导、方式/路径建议）嵌入群体行为仿真，量化对拥堵暴露、时间损失、可达性与公平性等指标的影响；后续拟扩展至供给侧情景（如动态定价、临时便当点布设），以支撑一体化政策评估与福利/弹性指标（如 VOT、消费剩余、需求弹性）估计。"}
            ],
            "usage_sections_en": [
                {"title": "Usage & Workflow",
                "body": "Configure information (global/road/beacons x-y-r) → run collective simulation → inspect map/curves/logs → export evaluation HTML and playback."},
                {"title": "Use Cases",
                "body": "Embed information interventions and demand-side policies (e.g., staggering, mode/route guidance) into an agent-based behavioral simulation to quantify impacts on congestion exposure, travel-time loss, accessibility, and equity; future extensions will cover supply-side scenarios (e.g., dynamic pricing, pop-up takeaway stations) to enable integrated policy appraisal and the estimation of welfare/elasticity indicators (e.g., VOT, consumer surplus, demand elasticities)."}
            ],
            
            "gif_grid": [
            {
                "src": "/assets/video/flow.mp4",
                "cap_zh": "交互平台使用流程（视频）",
                "cap_en": "Platform Usage Workflow (Video)",
                "type": "video",
                "poster": "/assets/video/flow_poster.jpg",
                "autoplay": True
            }
            ],
            "suppress_gif_grid": False,

            # 仅“研究结果”支持分节（核心图表 #2 #3 放这里）
            "results_sections_zh": [
                {
                    "title": "初步结果",
                    "body": "LLM-Agent 日志展示（下表为不同信息情景下的简要对比）。",
                    "table_md": """
            | Agent | 策略情景 | 理由 |
            |---|---|---|
            | 1 | NONE | Depart 11:50；Place 北苑_107；Mode walk；在允许时间网格内选取连续30分钟块；距离与既有偏好占优；UNKNOWN 拥挤不作乐观假设（UNKNOWN≠0）。 |
            | 1 | GLOBAL | Depart 11:50；Place 西苑_203；Mode walk；全局快照显示 11:50–12:00 北苑拥挤上升 ⇒ 侧向转移至相近距离窗口；保持 30 分钟完整性。[prov: global_prev_step] |
            | 2 | NONE | Depart 11:10；Place 北苑_105；Mode walk；为避开 11:30 下课拥堵提前出发；时间网格可行且步行成本最低。 |
            | 2 | GLOBAL | Depart 11:20；Place 北苑_201；Mode walk；全局信息提示 11:10–11:20 段拥挤更高 ⇒ 在网格内右移10分钟并换相邻窗口，仍满足连续时段与到课前约束。[prov: global_prev_step] |
            | 3 | NONE | Depart 12:00；Place 西苑_203；Mode walk；正午偏好与距离折中；未知拥挤不按低值处理。 |
            | 3 | GLOBAL | Depart 12:00；Place 西苑_205；Mode walk；全局快照显示 203 队列增长、205 略低 ⇒ 同区微调窗口以降低等待，保持出发时刻与行程完整性。[prov: global_prev_step] |
            """
                }
            ],
            "results_sections_en": [
                {
                    "title": "Mechanism Finding",
                    "body": "LLM-Agent log excerpts (table summarizes decisions across information scenarios).",
                    "table_md": """
            | Agent | Scenario | Rationale |
            |---|---|---|
            | 22230854542 | NONE | Depart 11:50; Place Beiyuan_107; Mode walk; selects a contiguous 30-min block in the allowed grid; distance & existing preference dominate; UNKNOWN crowding is not assumed low. |
            | 22230854542 | GLOBAL | Depart 11:50; Place Xiyuan_203; Mode walk; global snapshot shows rising crowding at Beiyuan (11:50–12:00) ⇒ lateral switch to a similar-distance window; 30-min integrity preserved. [prov: global_prev_step] |
            | 22232494942 | NONE | Depart 11:10; Place Beiyuan_105; Mode walk; leaves earlier to avoid the 11:30 class-end surge; feasible in the time grid with lowest walking cost. |
            | 22232494942 | GLOBAL | Depart 11:20; Place Beiyuan_201; Mode walk; global info indicates higher crowding for 11:10–11:20 ⇒ shift 10 min within grid and switch to an adjacent window, still satisfying continuity and pre-class constraints. [prov: global_prev_step] |
            | 222310001012 | NONE | Depart 12:00; Place Xiyuan_203; Mode walk; balances noon preference and distance; UNKNOWN crowding not treated as low. |
            | 222310001012 | GLOBAL | Depart 12:00; Place Xiyuan_205; Mode walk; global snapshot: growing queue at 203 while 205 slightly lower ⇒ micro-switch within the same hall to cut wait, preserving departure time & block integrity. [prov: global_prev_step] |
            """
                }

            ],

            # 研究结果的标题关键字内联图（可选；此处无需也可保留空）
            "inline_figs": [
                # 例如：{"match": "优化效果", "src": "/images/results/summary.png", "cap_zh": "优化效果总览", "cap_en": "Optimization overview"}
            ],

            # 页脚按钮/声明（可选）
            "report_demo_url": "/files/campus_report.html",
            "report_demo_text_zh": "查看示例报告",
            "report_demo_text_en": "View Sample Report",
            "copyright_zh": "",
            "copyright_en": "",
        },
        
        {
            "slug": "urban-flow",
            "date": "2024-03-07",
            "tags": ["Traffic Behavior", "ABM", "Vis", "Policy Sandbox"],
            "title_zh": "城市道路交通流量溯源与优化交互平台",
            "title_en": "Interactive Urban Flow Analysis & Optimization",

            "pitch_zh": "把“行为—网络—用地”耦合起来：可解释的时空分析、拥堵源溯源与策略沙盒（时间错峰/空间引导），以 σ 下降与 y=x 参照散点评估干预效果。",
            "pitch_en": "Couples behavior–network–land-use for explainable spacetime analysis, congestion-source tracing, and a policy sandbox (time shifting / spatial guidance), with evaluation via variance (σ) reduction and y=x reference scatter.",

            "value_zh": [
                "行为视角：将通勤时段、就业中心与网格化流量统一到同一时空坐标，解释‘因谁、何时、何地’产生拥堵",
                "可落地：两类干预（时间错峰 / 空间引导），以 σ（离散度）与 y=x 参照散点的整体偏移作为量化依据",
                "可解释：每个网格提供源贡献分解（中心 vs 非中心），支撑与管理者的证据化沟通"
            ],
            "value_en": [
                "Behavioral lens: align work-time, employment centers, and grid flows on a unified spatiotemporal coordinate to explain who/when/where congestion emerges",
                "Actionable: two interventions (time-shifting / spatial scaling) with quantitative assessment by variance σ and shifts of scatter relative to y=x",
                "Explainable: per-grid source attribution (centers vs. non-centers) for evidence-based communication with stakeholders"
            ],

            "method_zh": [
                "Grid-based 时空视图：按 HH:MM 渲染网格流量、点击联动多图与时序曲线",
                "拥堵挖掘：用高分位阈值识别早高峰拥堵网格并统计出现频率与持续性",
                "拥堵源溯源：按“就业中心贡献比”排序并划分腹地，量化源—汇关系",
                "策略沙盒：设置时间 ±30min 与中心规模系数 0.0–2.0，比较 σ 前后变化与散点整体偏移"
            ],
            "method_en": [
                "Grid-based spacetime rendering with linked charts and time series per grid",
                "Congestion mining via high-quantile thresholding for peak-hour detection, frequency and persistence",
                "Source attribution by employment-center contribution ratios with hinterland delineation",
                "Policy sandbox: ±30 min time-shift and center scaling (0.0–2.0); compare σ pre/post and the aggregate shift of scatter vs. y=x"
            ],

            "method_fig_map": [],
            "method_images": [],

            "study_area_zh": "研究区域：城市主城区道路网格（可扩展到多城区或都会区尺度）。",
            "study_area_en": "Study area: urban core road grids (extendable to multi-district or metropolitan scale).",

            "study_data_zh": "数据：道路网格化流量（分钟级或更细粒度）、就业中心 POI/区域边界与强度指标、日历/天气/事件等辅助变量，统一编码到相同空间参考与时间索引以利叠加分析。",
            "study_data_en": "Data: grid-based road flows (minute-level or finer), employment-center POIs/regions with intensity, and auxiliary variables (calendar/weather/events). All datasets are harmonized to a common spatial reference and time index for superposition and analysis.",
            
            "study_images": [],

            # 新增：方法之后的“使用与场景”板块（仅 urban-flow）
            "usage_sections_zh": [
                {"title": "使用功能与流程",
                "body": "① 选择分析时段与空间范围；② 以高分位阈值筛选拥堵网格并查看频次/持续性；③ 查看源贡献与腹地分布；④ 在策略沙盒中设置时间错峰（±30min）与中心规模系数（0.0–2.0）；⑤ 生成“σ 前后对比”与 y=x 参照散点报告。"},
                {"title": "应用场景",
                "body": "晨高峰拥堵成因诊断、局部瓶颈溯源、中心扩容或去集中化评估、时间错峰政策组合优选、建设方案的交通影响对比等。"}
            ],
            "usage_sections_en": [
                {"title": "Usage & Workflow",
                "body": "(1) Select time window and spatial extent; (2) Filter congested grids via high-quantile thresholds and inspect frequency/persistence; (3) Examine source contributions and hinterlands; (4) In the policy sandbox, set time-staggering (±30 min) and center scaling (0.0–2.0); (5) Export reports with pre/post σ and scatter vs. y=x."},
                {"title": "Use Cases",
                "body": "Morning-peak diagnosis, local bottleneck tracing, center expansion or de-concentration assessment, optimal time-staggering portfolios, and before/after comparisons for infrastructure proposals."}
            ],
            
            "gif_grid": [
                {"src": "/assets/gif/flow.gif", "cap_zh": "交互平台使用流程（动图）", "cap_en": "Platform Usage Workflow (GIF)"}
            ],

            "inline_figs": [],
            "report_demo_url": "/files/urban_flow_demo_report.html",
            "report_demo_text_zh": "查看示例报告",
            "report_demo_text_en": "View Sample Report",
            "copyright_zh": "本平台已完成相关软件著作权登记（软著）。",
            "copyright_en": "Software copyright registered."
        },

        
        {   
            "slug": "cross-river-network-balance",
            "date": "2023-10-15",
            "tags": ["network equilibrium", "optimization", "behavior modeling", "Shanghai"],

            # 标题
            "title_zh": "基于时空关联的越江通道群协同优化与网络均衡策略",
            "title_en": "Space-Time Association Model for Coordinated Optimization and Network Balancing of Cross-River Tunnel Systems",

            # 一句话摘要（lede）
            "pitch_zh": "构建时空叠加与关联模型，将功能区上班时间参数化为“流量脉冲”，以智能优化求解越江通道群协同错峰策略，最小化系统总经过时长并实现网络负荷动态均衡。",
            "pitch_en": "We develop a space–time association model that parameterizes working hours as traffic pulses. Intelligent optimization yields coordinated staggering strategies across cross-river systems, minimizing total system travel time and dynamically balancing network loads.",

            # 背景与价值
            "value_zh": [
                "范式突破：突破传统交通工程瓶颈，将拥堵治理提升至需求侧的时空结构治理，提供基于时间分配的根本解决方案。",
                "行为建模：利用高精度大数据，构建结构—行为耦合模型，定量解耦功能布局对个体出行的塑造作用，为政策建模提供机制基础。",
                "政策价值：提供前瞻性政策指导，支撑城市交通的协同优化与可持续发展，在效率与公平下最大化网络效益。"
            ],
            "value_en": [
                "Paradigm Shift: Moving beyond traditional traffic engineering, this research elevates congestion management to demand-side space–time structure governance, offering a fundamental solution based on temporal allocation.",
                "Behavioral Modeling: Utilizing high-resolution big data, we build a Structure–Behavior Coupling Model to quantitatively decouple how functional layouts shape individual trip behavior, providing a mechanistic foundation for policy modeling.",
                "Policy Value: Delivering proactive policy guidance, the work supports cooperative optimization and sustainable development, maximizing network efficiency under equity principles."
            ],

            # 方法（条目）
            "method_zh": [
                "行为参数化：利用大数据拟合，将每一股通勤流量抽象为高斯分布（流量脉冲），以中心时间 μ 与时间弹性 σ 作为可调控参数。",
                "时空叠加与关联：将各功能区产生的流量脉冲在所有通道上叠加，并通过共享参数建立网络关联，确保单点调整反馈至全系统。",
                "智能求解：以系统总经过时长最小化为目标函数，迭代求解功能区的协同错峰时间组合。"
            ],
            "method_en": [
                "Behavioral Parameterization: Utilizing big data, each commuting flow is abstracted into a Gaussian distribution (traffic pulse) with adjustable mean (μ) and temporal elasticity (σ).",
                "Space–Time Overlap & Association: Pulses from all functional areas are superimposed across all channels; shared parameters establish network association, ensuring single-point adjustments feed back system-wide.",
                "Intelligent Solution: The objective is to minimize total system travel time by iteratively searching for the best coordinated time-staggering combination."
            ],

            # 方法：逐条可选配图（核心图表 #1）
            "method_fig_map": [
                {
                    "index": 1,
                    "src": "/images/method/pulse-gaussian.jpg",
                    "cap_zh": "具体时空约束下的流量分布模型的各参数控制示意",
                    "cap_en": "Parameter-control schematic of the flow-distribution model under specific spatiotemporal constraints"
                }
                # 第2、3条如无需配图则不写；需要时再添加 index 或 match 规则
            ],
            # 如有“方法总览图”，可放这里（可选）
            "method_images": [
                {"src": "/images/method/overview.jpg", "cap_zh": "方法流程总览", "cap_en": "Method overview"}
            ],

            # 研究区域与数据（上半区）
            "study_area_zh": "以上海市主要越江通道群为研究对象（隧道与跨江桥梁）。",
            "study_area_en": "Focused on Shanghai's primary cross-river tunnel and bridge systems.",
            "study_data_zh": "高精度手机信令/GPS 大数据，用于反演与标定流量脉冲的实际行为参数（μ, σ）。",
            "study_data_en": "High-resolution mobile signaling/GPS big data are used to invert and calibrate the actual behavioral parameters (μ, σ) of traffic pulses.",
            "study_images": [
                {"src": "/images/crossriver/area-shanghai.jpg", "cap_zh": "研究区域——上海主要越江隧道的经过人群的出行分布", "cap_en": "Distribution of trips via Shanghai’s major cross-river tunnels (Study Area)"}
            ],

            # GIF 四宫格（如不需要可删除或 suppress）
            "gif_grid": [
                {"src": "/images/crossriver/pulse-fit.gif", "cap_zh": "脉冲拟合", "cap_en": "Pulse fitting"},
                {"src": "/images/crossriver/overlap.gif",   "cap_zh": "时空叠加", "cap_en": "Spatiotemporal overlap"},
                {"src": "/images/crossriver/assoc.gif",     "cap_zh": "网络关联", "cap_en": "Network association"},
                {"src": "/images/crossriver/opt.gif",       "cap_zh": "协同优化", "cap_en": "Coordinated optimization"}
            ],
            "suppress_gif_grid": True,

            # 仅“研究结果”支持分节（核心图表 #2 #3 放这里）
            "results_sections_zh": [
                {
                    "title": "机制发现",
                    "body": "越江通道与功能区呈多对多耦合：一条通道受多功能区影响，一处功能区也作用于多通道的流量分布。"
                },
                {
                    "title": "优化效果",
                    "children": [
                        {
                            "title": "总流量曲线（协同前后）",
                            "body": "20分钟调整方案显著提升流量分布均衡性：各越江通道的标准差同步下降，曲线更平缓、更分散——外环隧道 46.9→33.8（−27.93%）、翔殷路隧道 32.3→25.2（−21.98%）、军工路隧道 53.9→44.0（−18.37%）、杨浦大桥 34.6→26.0（−24.86%）。",
                            "images": [
                                {
                                    "src": "/images/results/flow-before-after.jpg",
                                    "cap_zh": "协同优化前后：通道群总流量曲线对比",
                                    "cap_en": "Before vs. after coordination: total cross-river flow"
                                }
                            ]
                        },
                        {
                            "title": "系统总经过时长对比",
                            "body": "20分钟调整方案显著降低系统总经过时长：人均节省约1.12分钟；分通道看，外环隧道人均节省约1.22分钟、杨浦大桥约1.09分钟、翔殷路隧道约0.96分钟、军工路隧道约0.80分钟，时间节省与波动收敛幅度基本一致。",
                        }
                    ]
                }
            ],
            "results_sections_en": [
                {
                    "title": "Mechanism Finding",
                    "body": "A many-to-many coupling exists between tunnels and functional areas: each tunnel is influenced by multiple areas, and each area affects flows across multiple tunnels."
                },
                {
                    "title": "Optimization Effect",
                    "children": [
                        {
                            "title": "Total Flow Curves (Before vs. After)",
                            "body": "Under the 20-minute adjustment scheme, flow balance improves markedly: standard deviations decline across corridors, yielding smoother and more even profiles—Outer Ring Tunnel 46.9→33.8 (−27.93%), Xiangyin Road Tunnel 32.3→25.2 (−21.98%), Jungong Road Tunnel 53.9→44.0 (−18.37%), and Yangpu Bridge 34.6→26.0 (−24.86%).",
                            "images": [
                                {
                                    "src": "/images/results/flow-before-after.jpg",
                                    "cap_en": "Before vs. after coordination: total cross-river flow",
                                    "cap_zh": "协同优化前后：通道群总流量曲线对比"
                                }
                            ]
                        },
                        {
                            "title": "System Travel Time Comparison",
                            "body": "The 20-minute adjustment scheme markedly reduces total system travel time, yielding ~1.12 minutes saved per person. By corridor: Outer Ring Tunnel ~1.22 min, Yangpu Bridge ~1.09 min, Xiangyin Road Tunnel ~0.96 min, and Jungong Road Tunnel ~0.80 min—mirroring the reduction in variability across corridors.",
                        }
                    ]
                }
            ],

            # 研究结果的标题关键字内联图（可选；此处无需也可保留空）
            "inline_figs": [
                # 例如：{"match": "优化效果", "src": "/images/results/summary.png", "cap_zh": "优化效果总览", "cap_en": "Optimization overview"}
            ],

            # 页脚按钮/声明（可选）
            "report_demo_url": "",
            "report_demo_text_zh": "",
            "report_demo_text_en": "",
            "copyright_zh": "",
            "copyright_en": "",
        }


    ],

    "resume": {
        "zh": {
            "name": "罗歆兰",
            "headline": "城市空间行为 · ABM · RL · LLM",
            "contacts": [
                {"label": "GitHub", "url": "https://github.com/luoxinlan322-sudo"},
                {"label": "Email", "url": "mailto:luoxinlan322@gmail.com"},
                {"label": "LinkedIn", "url": "https://www.linkedin.com/in/歆兰-罗-268a3138b"}
            ],
            "education": [
                {
                    "school": "同济大学 建筑与城市规划学院",
                    "degree": "城乡规划 硕士(学术型，保送)在读",
                    "period": "2023年9月 – 2026年4月",
                    "gpa": "均分 87/100，绩点 4.21/5.0",   # ← 新增：右侧第一行显示
                    "rank": "",                           # 没有可留空或删掉
                    "detail": "相关课程：地理空间信息分析方法(96/100)；时空行为与规划(92/100)；规划定量分析(87/100)"
                },
                {
                    "school": "同济大学 建筑与城市规划学院",
                    "degree": "城乡规划 学士",
                    "period": "2018年9月 – 2023年7月",
                    "gpa": "均分 92/100，绩点 4.7/5.0",
                    "rank": "年级 6/81",  
                    "detail": "相关课程：Python 程序设计导论；城市分析方法；城市道路与交通"
                }
            ],
            "projects": [
                {
                    "org": "项目一：高密度校园就餐行为建模与智能体仿真",
                    "role": "项目负责人",             
                    "lab": "同济大学王德课题组",          
                    "location": "上海，中国", 
                    "period": "2024年1月 – 至今",
                    "bullets": [
                        "阶段一（2024.01–2025.05）：融合 600万+ 刷卡、课表、门禁、天气、距离等数据，重建 ≈2.78万名学生就餐序列；提出熵型时空集中指数；建立 MNL 与 IRL 进行时间/地点选择建模。",
                        "遗传算法评估需求管理策略（如错峰上课、宿舍调整），峰时排队事件降至约 57%，空间失衡下降约 18.5%。",
                        "阶段二（2024.07–）：将 Mesa ABM 与 LLM（DeepSeek）耦合为认知引擎，覆盖出发时刻/地点/方式/路径；引入记忆增强推理与可解释文本理据；实现拥挤与步/骑行通道拥堵动态感知；时间–地点联合预测 Top-3≈54%，优于 MNL、接近 IRL。"
                    ]
                },
                {
                    "org": "项目二：城市通勤拥堵行为分析与仿真平台",
                    "role": "成员",
                    "lab": "同济大学王德课题组",          
                    "location": "上海，中国", 
                    "period": "2023年9月 – 2024年3月",
                    "bullets": [
                        "移动信令数据预处理：停留点识别、通勤路径序列抽象、栅格化时空表征。",
                        "搭建轨迹可视化与行为模式对比看板，识别通勤链与同步化出行行为。",
                        "配置仿真情景并解读结果，共同完成平台开发并获得软著登记。"
                    ]
                },
                {
                    "org": "课程《城市分析方法》",
                    "role": "助教",
                    "lab": "同济大学建筑与城市规划学院",
                    "period": "2023年秋季",
                    "bullets": [
                        "批改 SPSS/NLOGIT 统计作业并在课堂汇总讲评与答疑。"
                    ]
                }
            ],
            "publications": [
                "Luo, X., Hu, Y., Zhu, W., & Wang, D. (2025). Behavioral Demand Management for Sustainable Campus Dining: An Integrated Spatiotemporal Optimization Approach. Socio-Economic Planning Sciences.（在审）",
                "Hu, Y., Luo, X., Liu, Y., Wei, D., & Wang, D. (2025). 从分化到整合：规划范式的时空转向与策略探索. 《城市发展研究》.（已接收）",
                "Chen, Z., Luo, X., Wang, D., You, Z., & Zhou, X. (2024). 上海地铁9号线早高峰拥挤缓解的时空行为规划策略研究. 《上海城市规划》, 4:132–139."
            ],
            "awards": [
                "上海市优秀毕业生（本科），2023",
                "同济大学本科生一等奖学金，2019、2022",
                "同济大学本科生二等奖学金，2020、2021"
            ],
            "skills": [
                "研究与建模：时空行为分析；离散选择/逆强化学习；智能体仿真；基于 LLM 的决策仿真",
                "技术栈：Python（pandas、geopandas、NumPy、PyTorch）、LangChain、Mesa ABM、Bokeh/Plotly",
                "语言：中文（母语）、英文（IELTS 6.5）"
            ]
        },
        "en": {
            "name": "Xinlan Luo",
            "headline": "Urban spatial behavior · ABM · RL · LLM",
            "contacts": [
                {"label": "GitHub", "url": "https://github.com/luoxinlan322-sudo"},
                {"label": "Email", "url": "mailto:luoxinlan322@gmail.com"},
                {"label": "LinkedIn", "url": "https://www.linkedin.com/in/歆兰-罗-268a3138b"}
            ],
            "education": [
                {
                    "school": "Tongji University | College of Architecture and Urban Planning",
                    "degree": "M.Sc. in Urban and Rural Planning (in progress)",
                    "gpa": "Avg 87/100, GPA 4.21/5.0",
                    "rank": "",
                    "period": "Sept. 2023 – Apr. 2026",
                    "detail": "Relevant: Geo-spatial Information Analysis Methods (96/100); Spatio-Temporal Behavior and Planning (92/100); Quantitative Analytics for Planning (87/100)"
                },
                {
                    "school": "Tongji University | College of Architecture and Urban Planning",
                    "degree": "B.Sc. in Urban and Rural Planning",
                    "gpa": "Avg 92/100, GPA 4.7/5.0",
                    "rank": "Rank 6/81",
                    "period": "Sept. 2018 – Jul. 2023",
                    "detail": "Relevant: Introduction to Python Programming; Urban Analytical Methods; Urban Roads and Transportation"
                }
            ],
            "projects": [
                {
                    "org": "Project 1 — Behavioral Modeling and Agentic Simulation of High-Density Campus Dining Dynamics",
                    "role": "Project Leader",
                    "lab": "Prof. De Wang’s Lab, Tongji University",
                    "location": "Shanghai, China",
                    "period": "Jan. 2024 – Present",
                    "bullets": [
                        "Phase I (Jan. 2024 – May 2025): Reconstructed ≈27,800 students’ dining sequences from >6M smart-card records fused with class, access, weather, and distance data; built entropy-based concentration index; estimated MNL & IRL for time/venue choice under constraints.",
                        "Evaluated demand-management strategies (e.g., staggered classes, dorm reassignment) via genetic algorithm: up to ~57% fewer peak waiting incidents and ~18.5% lower spatial imbalance.",
                        "Phase II (Jul. 2024 – Present): Integrated Mesa ABM with an LLM (DeepSeek) as cognitive engine for departure time, venue, mode, and route; memory-augmented reasoning with interpretable rationale traces; dynamic perception of dining congestion and walkway/bikeway crowding; ~54% Top-3 joint accuracy in time–venue prediction, outperforming MNL and approaching IRL."
                    ]
                },
                {
                    "org": "Project 2 — Urban Commuting Congestion Behavioral Analysis and Simulation Platform",
                    "role": "Team Member",
                    "lab": "Prof. De Wang’s Lab, Tongji University",
                    "location": "Shanghai, China",
                    "period": "Sept. 2023 – Mar. 2024",
                    "bullets": [
                        "Processed large-scale mobile signaling: stay-point extraction, commuting route abstraction, grid-based spatiotemporal representation.",
                        "Built trajectory visualization & behavioral pattern dashboard to identify recurrent chains and temporal synchronization.",
                        "Configured simulation scenarios and interpreted outputs; co-developed platform (software copyright registered)."
                    ]
                },
                {
                    "org": "Class “Urban Analytical Methods”",
                    "role": "Teaching Assistant",
                    "lab": "College of Architecture and Urban Planning, Tongji University",
                    "period": "Fall 2023",
                    "bullets": [
                        "Graded SPSS/NLOGIT statistical assignments for senior undergraduates and delivered in-class feedback summaries."
                    ]
                }
            ],
            "publications": [
                "Luo, X., Hu, Y., Zhu, W., & Wang, D. (2025). Behavioral Demand Management for Sustainable Campus Dining: An Integrated Spatiotemporal Optimization Approach. Socio-Economic Planning Sciences. (Under Review).",
                "Hu, Y., Luo, X., Liu, Y., Wei, D., & Wang, D. (2025). From Differentiation to Integration: The Spatiotemporal Turn and Strategic Exploration of Planning Paradigms. Urban Development Studies. (Accepted). [in Chinese]",
                "Chen, Z., Luo, X., Wang, D., You, Z., & Zhou, X. (2024). Study on Spatio-Temporal Behavior Planning Strategies for Alleviating Morning Peak Congestion in Shanghai's Urban Rail Transit: A Case Study of Metro Line 9. Shanghai Urban Planning Review, 4, 132–139. [in Chinese]"
            ],
            "awards": [
                "Outstanding Graduate of Shanghai (Undergraduate Level), 2023",
                "First-Class Undergraduate Scholarship for Outstanding Students, Tongji University, 2019 & 2022",
                "Second-Class Undergraduate Scholarship for Outstanding Students, Tongji University, 2020 & 2021"
            ],
            "skills": [
                "Research & Modeling: Spatiotemporal behavior analysis; discrete-choice & inverse RL; agent-based simulation; LLM-based decision simulation",
                "Technical: Python (pandas, geopandas, NumPy, PyTorch), LangChain, Mesa ABM, Bokeh/Plotly",
                "Language: Mandarin Chinese (native), English (IELTS 6.5)"
            ]
        }

    },
}
# ========== 以上是你平时要改的部分 ==========


# 把 social 列表渲染成 [[params.social]] 片段（Coder 会自动显示为图标）
def render_social_toml(items):
    lines = []
    for s in items or []:
        name = toml_esc(str(s.get("name", "")))
        icon = toml_esc(str(s.get("icon", "")))
        url  = toml_esc(str(s.get("url", "")))
        icon_svg = s.get("iconSVG")  # 注意驼峰

        block = (
            '[[params.social]]\n'
            f'  name = "{name}"\n'
            f'  icon = "{icon}"\n'
            f'  url  = "{url}"\n'
        )
        if icon_svg:
            block += f'  iconSVG = "{toml_esc(str(icon_svg))}"\n'
        block += '  weight = 10\n'

        lines.append(block)

    return ("\n".join(lines) + "\n") if lines else ""

def ensure_icons():
    """
    写入小红书 SVG：黑底白字（固定颜色，不受 CSS color 影响）
    - 文件名：static/icons/xhs_black.svg
    - 每次 build 强制覆盖，避免旧缓存
    """
    icons_dir = ROOT / "static" / "icons"
    icons_dir.mkdir(parents=True, exist_ok=True)

    svg_path = icons_dir / "xhs_black.svg"   # ← 用新文件名规避浏览器缓存
    svg_text = """<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256"
  viewBox="0 0 256 256" role="img" aria-label="Xiaohongshu">
  <!-- 固定黑底白字，不跟随 CSS color -->
  <rect x="16" y="16" width="224" height="224" rx="32" ry="32" fill="#000000"/>
  <text x="50%" y="54%" text-anchor="middle"
        font-family="Arial, Helvetica, sans-serif"
        font-weight="800" font-size="92" fill="#FFFFFF">RED</text>
</svg>
"""
    # 强制覆盖，避免旧图残留
    svg_path.write_text(svg_text, encoding="utf-8")
    print(f"[write] {svg_path.relative_to(ROOT)}")

    # 同步把 CONFIG 里的 iconSVG 指向新文件（带版本参数，继续防缓存）
    # 注意：这里只改当前运行时的 cfg，不回写源码里的 CONFIG 常量
    for s in CONFIG.get("social", []):
        if s.get("name") == "Xiaohongshu":
            s["iconSVG"] = "icons/xhs_black.svg?v=1"  # 你改样式时把 v=1 换 v=2

def ensure_social_partial():
    """
    覆写主题社交图标模板：
    - 优先 iconSVG，回退 Font Awesome 的 icon
    - 同时写入 2 个路径：home/social.html 与 social.html
    - 在 HTML 里打可见的 DEBUG 注释，方便 Ctrl+U 搜索确认是否命中
    """
    targets = [
        ROOT / "layouts" / "partials" / "home" / "social.html",
        ROOT / "layouts" / "partials" / "social.html",
    ]
    tpl = r"""<!-- DEBUG: project social override (layouts/partials/**/social.html) -->
{{/* Also emit a Go template comment to be double-sure:
     if you only see this in page source, override is active. */}}
{{- $social := site.Params.social -}}
{{- if $social }}
<ul class="social list-inline">
  {{- range $s := $social }}
  <li class="list-inline-item">
    {{- $u := printf "%v" $s.url -}}
    <a href="{{ if or (hasPrefix $u "http") (hasPrefix $u "mailto:") (hasPrefix $u "tel:") }}{{ $u }}{{ else }}{{ $u | relURL }}{{ end }}" target="_blank" rel="noopener" aria-label="{{ $s.name }}">
      {{- with $s.iconSVG }}
        <img class="icon-svg" src="{{ . | relURL }}" alt="{{ $s.name }}" />
      {{- else }}
        {{- with $s.icon }}
          <i class="{{ . }}" aria-hidden="true"></i>
        {{- end }}
      {{- end }}
    </a>
  </li>
  {{- end }}
</ul>
{{- end }}
"""
    for p in targets:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(tpl, encoding="utf-8")
        print(f"[write] {p.relative_to(ROOT)}")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"[write] {path.relative_to(ROOT)}")


def toml_esc(s: str) -> str:
    return s.replace('"', '\\"')


def render_hugo_toml(cfg: dict) -> str:
    def multi(s: str) -> str:
        """把 CONFIG 中的 \\n 替换为真实换行，并用 TOML 三引号包裹。"""
        s = (s or "").replace("\\n", "\n")
        return f'"""\n{s}\n"""'   # TOML 多行字符串

    baseURL = f"https://{cfg['github_user']}.github.io/"
    zh = cfg["zh"]; en = cfg["en"]; avatar = cfg["avatar_url"]

    # ✅ apply multiline conversion here
    zh_info_ml = multi(zh.get("info"))
    en_info_ml = multi(en.get("info"))

    social = cfg.get("social", [])
    social_block = render_social_toml(social)  # 保留社交区块

    head = dedent(f"""
        baseURL = "{baseURL}"
        title = "{toml_esc(zh['author'])}"
        theme = "hugo-coder"
        languageCode = "zh-cn"
        defaultContentLanguage = "zh-cn"
        defaultContentLanguageInSubdir = true
        enableRobotsTXT = true

        buildDrafts = false
        buildFuture = true
        buildExpired = false


        [pagination]
        pagerSize = 20

        [params]
        colorScheme = "auto"
        customCSS = ["css/typography.{cfg.get('css_version','v1')}.css"]
        mainSections = ["projects", "posts"]

        # 允许 Markdown 中渲染原生 HTML（否则你的 <div class="cv"> 会被当作文本）
        [markup]
        [markup.goldmark]
            [markup.goldmark.renderer]
            unsafe = true
    """).strip() + "\n\n"

    langs = dedent(f"""
    [languages]

      [languages.zh-cn]
        languageName = "中文"
        weight = 1
        title = "{toml_esc(zh['title'])}"
        [languages.zh-cn.params]
          author = "{toml_esc(zh['author'])}"
          info = {zh_info_ml}
          # description = "{toml_esc(zh['desc'])}"
          avatarURL = "{avatar}"
        [[languages.zh-cn.menu.main]]
          name = "项目"
          url  = "/projects/"
          weight = 1
        [[languages.zh-cn.menu.main]]
          name = "简历"
          url  = "/resume/"
          weight = 2
        [[languages.zh-cn.menu.main]]
          name = "关于"
          url  = "/about/"
          weight = 3

      [languages.en]
        languageName = "EN"
        weight = 2
        title = "{toml_esc(en['title'])}"
        [languages.en.params]
          author = "{toml_esc(en['author'])}"
          info = {en_info_ml}
          description = "{toml_esc(en['desc'])}"
          avatarURL = "{avatar}"
        [[languages.en.menu.main]]
          name = "Projects"
          url  = "/projects/"
          weight = 1
        [[languages.en.menu.main]]
          name = "Resume"
          url  = "/resume/"
          weight = 2
        [[languages.en.menu.main]]
          name = "About"
          url  = "/about/"
          weight = 3
    """).strip() + "\n"

    # ✅ 把三段拼起来（保持你原本逻辑）
    return head + social_block + "\n" + langs + "\n"



def md_front(title: str) -> str:
    return f'+++\ntitle = "{title}"\n+++\n\n'


def render_home(lang: str, page: dict) -> str:
    return md_front(page["title"]) + page["body"] + "\n"


def render_projects_index(title: str) -> str:
    # 把该分区及其子页面的渲染类型“伪装”为 posts，以复用 hugo-coder 的文章列表外观
    return (
        f'+++\n'
        f'title = "{title}"\n'
        f'[cascade]\n'
        f'  type = "posts"\n'
        f'+++\n\n'
    )


def render_resume(lang: str, pdf: str) -> str:
    # 标题 & 按钮文案
    title = "简历" if lang == "zh" else "Resume"
    btn   = "下载 PDF" if lang == "zh" else "Download PDF"

    # 读 CONFIG
    r = CONFIG.get("resume", {})
    blk = r.get(lang, {})

    # 兜底
    header_name = (blk.get("name") or (CONFIG["zh"]["author"] if lang=="zh" else CONFIG["en"]["author"]))
    header_info = blk.get("headline") or ""
    contacts    = blk.get("contacts") or []
    edu         = blk.get("education") or []
    exp         = blk.get("projects") or blk.get("experience") or []
    pubs        = blk.get("publications") or []
    skills      = blk.get("skills") or []
    awards      = blk.get("awards") or []

    # PDF 链接（中英各自路由）
    link = f"/{pdf}" if lang == "zh" else f"/en/{pdf}"

    # 简历头（Front matter）
    md = [f'+++\ntitle = "{title}"\n+++\n']

    # 头部区：姓名 / tagline / 联系方式 / PDF按钮
    header_html = [
        '<div class="cv-page"><div class="cv cv-wide">',
        '  <header class="cv-header">',
        f'    <h1 class="cv-name">{header_name}</h1>',
        f'    <p class="cv-headline">{header_info}</p>',
    ]
    if contacts:
        links = []
        for c in contacts:
            label = c.get("label","")
            url   = c.get("url")
            links.append(f'<a href="{url}">{label}</a>' if url else f'<span>{label}</span>')
        header_html.append(f'    <p class="cv-contacts">{" · ".join(links)}</p>')
    header_html.append(f'    <p class="cv-download"><a class="cv-btn" href="{link}" target="_blank" rel="noopener">{btn}</a></p>')
    header_html.append('  </header>')

    # ========== 一个条目渲染器（左：时间/课题组/地点；右：标题+正文） ==========
    def render_rows(items, section_class=""):
        rows = []
        for it in items:
            org      = it.get("org","")
            role     = it.get("role","")
            period   = it.get("period","")
            lab      = it.get("lab") or it.get("group", "")
            location = it.get("location") or it.get("place", "")
            detail   = it.get("detail","")
            bullets  = it.get("bullets", [])

            # —— 仅教育区块用到的附加字段（右侧第一行显示在 detail 上面）
            is_edu = (section_class == "cv-edu")
            edu_gpa  = it.get("gpa", "") if is_edu else ""
            edu_rank = it.get("rank","")  if is_edu else ""

            # 右侧标题（经验：org + [role]；教育一般不用这两个就会跳过）
            title_html = []
            if org or role:
                title_html.append('<h3 class="cv-title">')
                if org:
                    title_html.append(f'<span class="cv-org">{org}</span>')
                if role:
                    title_html.append(f' <span class="cv-role">[{role}]</span>')
                title_html.append('</h3>')

            # 右侧“教育附加信息”行：出现在 detail 前面
            edu_info_html = []
            if is_edu and (edu_gpa or edu_rank):
                parts = []
                if edu_gpa:  parts.append(str(edu_gpa))
                if edu_rank: parts.append(str(edu_rank))
                edu_info_html.append(f'<p class="cv-edu-meta">{" · ".join(parts)}</p>')

            # 右侧描述 detail
            sub_html = [f'<p class="cv-sub">{detail}</p>'] if detail else []

            # 右侧要点列表
            blt_html = []
            if bullets:
                blt_html.append('<ul class="cv-bullets">')
                for b in bullets:
                    blt_html.append(f'  <li>{b}</li>')
                blt_html.append('</ul>')

            # 左侧 meta（时间 / 课题组 / 地点）
            meta_html = [
                '  <aside class="cv-meta">',
                f'    <div class="cv-period">{period}</div>',
                '    <div class="cv-where">'
            ]
            if lab:
                meta_html.append(f'      <div class="cv-lab">{lab}</div>')
            if location:
                meta_html.append(f'      <div class="cv-place">{location}</div>')
            meta_html.append('    </div>')
            meta_html.append('  </aside>')

            row = [
                f'<div class="cv-row {section_class}">',
                *meta_html,
                '  <section class="cv-body">',
                *title_html,
                *edu_info_html,   # ← 这行确保“GPA/排名”在 detail 上面
                *sub_html,
                *blt_html,
                '  </section>',
                '</div>'
            ]
            rows.append("\n".join(row))
        return "\n".join(rows)

    # 教育
    if edu:
        header_html.append('<section class="cv-section"><h2 class="cv-h2">{}</h2>'.format("教育背景" if lang=="zh" else "Education"))
        header_html.append(render_rows(edu, "cv-edu"))
        header_html.append('</section>')

    # 经历
    if exp:
        header_html.append('<section class="cv-section"><h2 class="cv-h2">{}</h2>'.format("项目/经历" if lang=="zh" else "Projects / Experience"))
        header_html.append(render_rows(exp, "cv-exp"))
        header_html.append('</section>')
    # 发表
    if pubs:
        header_html.append('<section class="cv-section"><h2 class="cv-h2">{}</h2>'.format("论文与发表" if lang=="zh" else "Publications"))
        header_html.append('<ul class="cv-list cv-dots">')
        for p in pubs:
            header_html.append(f'  <li>{p}</li>')
        header_html.append('</ul></section>')

    # 技能
    if skills:
        header_html.append('<section class="cv-section"><h2 class="cv-h2">{}</h2>'.format("技能" if lang=="zh" else "Skills"))
        header_html.append('<ul class="cv-list cv-dots">')
        if isinstance(skills, list):
            for s in skills:
                header_html.append(f'  <li>{s}</li>')
        else:
            header_html.append(f'  <li>{skills}</li>')
        header_html.append('</ul></section>')
    # 奖项
    if awards:
        header_html.append('<section class="cv-section"><h2 class="cv-h2">{}</h2>'.format("荣誉与奖项" if lang=="zh" else "Awards"))
        header_html.append('<ul class="cv-list cv-dots">')
        for a in awards:
            header_html.append(f'  <li>{a}</li>')
        header_html.append('</ul></section>')

    header_html.append('</div></div>')  # .cv 结束 + .cv-page 结束
    md.append("\n".join(header_html) + "\n")
    return "\n".join(md)


def render_about(lang: str) -> str:
    # 标题
    title = "关于" if lang == "zh" else "About"

    # 从 CONFIG 自动拿 GitHub 链接；Email 直接明文（不超链接）
    gh_user = CONFIG.get("github_user", "").strip()
    gh_url  = f"https://github.com/{gh_user}" if gh_user else "https://github.com/"
    email   = "luoxinlan322@gmail.com"  # 明文显示，不加链接

    if lang == "zh":
        body = (
            "我关注城市空间行为与智能体模拟（ABM），结合大模型认知代理（LLM Agents），"
            "构建**可解释、可干预、可推演**的行为模拟框架，用于理解与改进高密度场景中的时空决策。  \n\n"
            "欢迎与我交流/合作。  \n"
            f"**Email**：{email}  ｜  **GitHub**：[ {gh_user} ]({gh_url})"
        )
    else:
        body = (
            "I work on urban spatial behavior and agent-based modeling (ABM) with LLM-based cognitive agents, "
            "aiming to build **interpretable, intervenable, and scenario-extrapolable** behavioral simulations "
            "for high-density environments.  \n\n"
            "Open to collaboration and conversations.  \n"
            f"**Email**: {email}  |  **GitHub**: [{gh_user}]({gh_url})"
        )

    return md_front(title) + body + "\n"



def render_project_item(p: dict, lang: str) -> str:
    """
    结构：
      上半区（一次性渲染，不分节）：
        - 标题拆分/副标题/导语
        - 背景与价值（列表）
        - 方法概览（编号条目；支持“逐条可选配图”与“方法总览配图”）
        - 研究区域与数据（简洁区块，可含图片）
        - GIF 四宫格（可关）
        - 徽章（版权/报告）
      下半区：
        - 研究结果（唯一支持分节/二级小标题/表格/链接/图片）
        - 仅在“研究结果”里支持 inline_figs 的标题关键字内联图
    """
    out: list[str] = [] 
    # --- i18n 小工具 ---
    _t = (lambda zh, en: zh if lang == "zh" else en)
    def _captext(d): return d.get("cap_zh") if lang == "zh" else d.get("cap_en")

    # --- 标题 & frontmatter ---
    raw_title = p["title_zh"] if lang == "zh" else p["title_en"]
    title_main, title_sub = _split_title_with_subtitle(raw_title)
    title = title_main or raw_title

    tags_list = p.get("tags", [])
    tags_yaml = ", ".join([f'"{t}"' if (" " in t or ":" in t) else t for t in tags_list])

    head = [
        "---",
        f'title: "{title}"',
        f"date: {p['date']}",
        f"tags: [{tags_yaml}]",
        # 'url: /projects/{p["slug"]}/',  # ← 一般不需要；如你以后把文件移到 content/post/ 再启用它保留 /projects/ 路径
        "---",
        ""
    ]

    # --- 副标题（小号、淡色） ---
    #if title_sub:
    #    sub = f"（{title_sub}）" if lang == "zh" else f"({title_sub})"
    #    out.append(f'<p class="proj-subtitle">{sub}</p>')

    # --- 导语（lede） ---
    pitch = p.get("pitch_zh") if lang == "zh" else p.get("pitch_en")
    if pitch:
        out.append(f'<p class="lede">{pitch}</p>')

    # --- 背景与价值 ---
    valist = p.get("value_zh") if lang == "zh" else p.get("value_en")
    if valist:
        out += ["", _t("## 背景与价值", "## Research Background & Value")]
        out += [f"- {it}" for it in valist]

    # --- 方法概览（支持逐条可选配图 + 总览配图）---
    mlist = p.get("method_zh") if lang == "zh" else p.get("method_en")
    if mlist:
        out += ["", _t("## 方法概览", "## Research Methodology")]
        fig_map = p.get("method_fig_map") or []   # 可选

        def _figs_for(i1, text):
            """返回该条方法的图片列表（可能为空）。index优先；其次match关键字；支持单图或多图。"""
            hits = []
            for r in fig_map:
                if "index" in r and int(r["index"]) == i1:
                    hits.append(r)
            for r in fig_map:
                m = (r.get("match") or "").strip()
                if m and m in (text or ""):
                    hits.append(r)
            imgs = []
            for r in hits:
                if r.get("images"):
                    imgs.extend(r["images"])
                elif r.get("src"):
                    imgs.append(r)
            return imgs

        for i, it in enumerate(mlist, 1):
            out.append(f"{i}. {it}")
            for im in _figs_for(i, it):  # 命中才渲染
                src = im.get("src")
                if not src: 
                    continue
                cap = _captext(im) or ""
                out.append(f'<figure><img src="{src}" alt="{cap}"><figcaption>{cap}</figcaption></figure>')
                out.append("")

        # 方法总览配图（可选，统一追加在方法条目之后）
        for im in (p.get("method_images") or []):
            src = im.get("src")
            if src:
                cap = _captext(im) or ""
                out.append(f'<figure><img src="{src}" alt="{cap}"><figcaption>{cap}</figcaption></figure>')
                out.append("")

    # --- 研究区域与数据（一次性区块；可配图）---
    study_area = p.get("study_area_zh") if lang == "zh" else p.get("study_area_en")
    study_data = p.get("study_data_zh") if lang == "zh" else p.get("study_data_en")
    study_imgs = p.get("study_images") or []
    if study_area or study_data or study_imgs:
        out += ["", _t("## 研究区域与数据", "## Study Area & Data")]
        items = []
        if study_area:
            items.append(_t(f"- **区域：** {study_area}", f"- **Area:** {study_area}"))
        if study_data:
            items.append(_t(f"- **数据：** {study_data}", f"- **Data:** {study_data}"))
        out += items
        for im in study_imgs:
            src = im.get("src")
            if src:
                cap = _captext(im) or ""
                out.append(f'<figure><img src="{src}" alt="{cap}"><figcaption>{cap}</figcaption></figure>')
                out.append("")
    # --- 使用与场景（放在“方法概览”之后；可选） ---
    usage_secs = p.get("usage_sections_zh") if lang == "zh" else p.get("usage_sections_en")
    if usage_secs and isinstance(usage_secs, list) and len(usage_secs) > 0:
        # 一级标题：使用与场景
        out += ["", _t("## 使用与场景", "## Usage & Scenarios")]
        for sec in usage_secs:
            t = (sec.get("title") or "").strip()
            b = (sec.get("body") or "").strip()
            if t:
                out += ["", f"### {t}"]
            if b:
                out += [b, ""]
    # --- GIF / 视频 四宫格（如有）---
    gifs = p.get("gif_grid") or []

    def _media_tag(item, single=False):
        src = item.get("src")
        if not src:
            return ""
        cap = _captext(item) or ""
        # 识别视频：显式 type=video 或后缀匹配
        is_video = (str(item.get("type", "")).lower() == "video") or src.lower().endswith((".mp4", ".webm", ".ogg"))
        poster = item.get("poster")
        autoplay = bool(item.get("autoplay", False))

        if is_video:
            attrs = ['controls', 'playsinline', 'loop', 'muted']  # muted 便于自动播放
            if autoplay:
                attrs.append('autoplay')
            # 轻量预加载更省流
            attrs.append('preload="metadata"')
            if poster:
                attrs.append(f'poster="{poster}"')
            tag = f'<video src="{src}" {" ".join(attrs)}></video>'
        else:
            tag = f'<img src="{src}" alt="{cap}">'

        if single:
            return f'<figure class="gif-single">{tag}<figcaption>{cap}</figcaption></figure>'
        return f'<figure>{tag}<figcaption>{cap}</figcaption></figure>'

    if gifs and not p.get("suppress_gif_grid", False):
        if len(gifs) == 1:
            out += ["", _media_tag(gifs[0], single=True)]
        else:
            out += ["", '<div class="gif-grid">']
            for g in gifs:
                out.append("  " + _media_tag(g, single=False))
            out.append("</div>")

    # --- 徽章（版权/报告按钮）---
    badges = []
    cr_txt = p.get("copyright_zh") if lang == "zh" else p.get("copyright_en")
    if cr_txt:
        badges.append(f'<span class="badge badge-soft">{cr_txt}</span>')
    rpt_url = p.get("report_demo_url")
    if rpt_url:
        rpt_txt = (p.get("report_demo_text_zh") if lang == "zh" else p.get("report_demo_text_en")) or _t("查看示例报告","View Report")
        badges.append(f'<a class="btn btn-report" href="{rpt_url}" target="_blank" rel="noopener">{rpt_txt}</a>')
    if badges:
        out += ["", '<p class="proj-badges">' + " ".join(badges) + "</p>"]

    # === 研究结果（唯一支持分节/二级小标题/表格/链接/图片）===
    results = p.get("results_sections_zh") if lang == "zh" else p.get("results_sections_en")

    # 仅用于“研究结果”的标题关键字内联图
    inline_map = p.get("inline_figs") or []
    def _find_inline_fig(title_text: str):
        t = (title_text or "").strip()
        for rule in inline_map:
            m = (rule.get("match") or "").strip()
            if m and m in t:
                src = rule.get("src")
                cap = _captext(rule)
                if (not src) and ("gif_index" in rule):
                    i = int(rule["gif_index"])
                    if 0 <= i < len(gifs):
                        g = gifs[i]; src = g.get("src"); cap = cap or _captext(g)
                if src: return src, (cap or "")
        return None, None

    def _append_images(images):
        for im in (images or []):
            src = im.get("src")
            if src:
                cap = _captext(im) or ""
                out.append(f'<figure><img src="{src}" alt="{cap}"><figcaption>{cap}</figcaption></figure>')
                out.append("")

    def _block(title_text=None, body=None, table_md=None, link_href=None, link_text=None, images=None):
        nonlocal out  # ✅ 关键：使用外层 out
        if title_text: 
            out.extend(["", f"## {title_text}"])
        if body:
            b = body.strip()
            if b:
                out.append(b)
                out.append("")
        if title_text:
            _src, cap_inline = _find_inline_fig(title_text)
            if _src:
                out.append(f'<figure><img src="{_src}" alt="{cap_inline or title_text}"><figcaption>{cap_inline or ""}</figcaption></figure>')
                out.append("")
        _append_images(images)
        if table_md:
            out.append("")
            out.append(dedent(table_md).strip("\n"))
            out.append("")
        if link_href:
            out.append(f'[{link_text or _t("打开 HTML","Open HTML")}]({link_href})')
            out.append("")

    if results and isinstance(results, list):
        out += ["", _t("## 研究核心结论", "## Core Conclusions")]
        for sec in results:
            title2 = (sec.get("title") or "").strip()
            body2  = sec.get("body")
            _block(title_text=title2, body=body2,
                   table_md=sec.get("table_md"),
                   link_href=sec.get("link_href"),
                   link_text=sec.get("link_text"),
                   images=sec.get("images"))
            children = sec.get("children")
            if children and isinstance(children, list):
                for ch in children:
                    st = (ch.get("title") or "").strip()
                    if st:
                        out += ["", f"### {st}"]
                    cbody = ch.get("body")
                    if cbody: out += [cbody.strip(), ""]
                    # 子标题也可匹配 inline_figs（回落到父标题）
                    _src, cap_inline = _find_inline_fig(st or title2)
                    if _src:
                        out.append(f'<figure><img src="{_src}" alt="{cap_inline or st or title2}"><figcaption>{cap_inline or ""}</figcaption></figure>')
                        out.append("")
                    _append_images(ch.get("images"))
                    if ch.get("table_md"):
                        out += ["", dedent(ch["table_md"]).strip("\n"), ""]
                    if ch.get("link_href"):
                        out += [f'[{ch.get("link_text") or _t("打开 HTML","Open HTML")}]({ch["link_href"]})', ""]

    # --- 兜底 ---
    if not any(s.strip() for s in out):
        body_fallback = p.get("body_zh") if lang == "zh" else p.get("body_en")
        out.append(body_fallback or _t("（内容待补充）", "*(content pending)*"))

    return "\n".join(head + out + [""])

# ================= 字体与排版（写入 assets/ 并走主题 customCSS） =================
def render_typography_css(font_cdn: str = "google") -> str:
    if font_cdn == "loli":
        inter  = '@import url("https://fonts.loli.net/css2?family=Inter:opsz,wght@14..32,400..800&display=swap");'
        source = '@import url("https://fonts.loli.net/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400..700;1,8..60,400..700&display=swap");'
        notosc = '@import url("https://fonts.loli.net/css2?family=Noto+Serif+SC:wght@400;600&display=swap");'
    elif font_cdn == "google":
        inter  = '@import url("https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400..800&display=swap");'
        source = '@import url("https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400..700;1,8..60,400..700&display=swap");'
        notosc = '@import url("https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600&display=swap");'
    else:
        inter = source = notosc = ""

    return f"""/* Web fonts (cdn={font_cdn}) */

{inter}
{source}
{notosc}

/* 自托管时改用 @font-face：
@font-face{{font-family:"Inter";src:url("/fonts/Inter-Variable.woff2") format("woff2");font-weight:100 900;font-style:normal;font-display:swap;}}
@font-face{{font-family:"Source Serif 4";src:url("/fonts/SourceSerif4Var-Roman.woff2") format("woff2");font-weight:300 800;font-style:normal;font-display:swap;}}
@font-face{{font-family:"Noto Serif SC";src:url("/fonts/NotoSerifSC-Regular.woff2") format("woff2");font-weight:400;font-style:normal;font-display:swap;}}
*/

:root{{
  --font-en-sans:"Inter",ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans","Apple Color Emoji","Segoe UI Emoji";
  --font-en-serif:"Source Serif 4","Iowan Old Style","Palatino Linotype","Palatino","URW Palladio L",serif;
  --font-zh-serif:"Source Han Serif SC","Noto Serif CJK SC","Noto Serif SC","Songti SC","SimSun",serif;
  --font-mono:ui-monospace,SFMono-Regular,Menlo,Monaco,"JetBrains Mono",Consolas,"Liberation Mono","Courier New",monospace;

  --max-text-width: 72ch;
  --line-height: 1.7;
  --h1-weight: 700;
  --h2-weight: 650;
  --h3-weight: 600;
  --muted: 0.62;
}}
html{{font-feature-settings:"liga","kern","calt","ss01","cv05";-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;}}
body{{font-family:var(--font-en-serif),var(--font-zh-serif);font-size:17px;line-height:var(--line-height);max-width:var(--max-text-width);margin:0 auto;padding:0 1.2rem;}}
.container,.content{{max-width:100%;}}
.post,.page,.single,.list{{max-width:var(--max-text-width);margin:auto;}}
h1,h2,h3,h4{{font-family:var(--font-en-sans),var(--font-zh-serif);line-height:1.25;letter-spacing:.2px;}}
h1{{font-weight:var(--h1-weight);font-size:clamp(2rem,3vw,2.4rem);margin:1.2em 0 .5em;}}
h2{{font-weight:var(--h2-weight);font-size:clamp(1.5rem,2.2vw,1.8rem);margin:1.1em 0 .5em;}}
/* === 让首页副标题 info 按 \n 换行显示（Coder 多种选择器兜底） === */
.home-info h2,
.profile .info,
.profile .description,
.home .content .info {{
  white-space: pre-line !important;
  display: block;
}}
h3{{font-weight:var(--h3-weight);font-size:1.25rem;margin:1em 0 .4em;}}
p,ul,ol{{margin:.8em 0;}} ul,ol{{padding-left:1.2em;}}
a{{color:inherit;text-decoration-thickness:.06em;text-underline-offset:.2em;opacity:.92;transition:opacity .15s,text-decoration-color .15s;}}
a:hover{{opacity:1;text-decoration-color:currentColor;}}
blockquote{{border-left:2px solid color-mix(in srgb,currentColor 35%,transparent);padding:.6em 1em;margin:1em 0;background:color-mix(in srgb,currentColor var(--muted),transparent);border-radius:6px;}}
table{{border-collapse:collapse;width:100%;font-size:.98em;}}
th,td{{border-bottom:1px solid color-mix(in srgb,currentColor 30%,transparent);padding:.6em .4em;}}
code,kbd,pre{{font-family:var(--font-mono);font-size:.95em;}}
pre{{background:color-mix(in srgb,currentColor 12%,transparent);padding:.8em 1em;border-radius:8px;overflow:auto;}}

/* === 顶部导航：更柔和优雅，和中文标题更搭 === */
/* Coder 主题常见结构：.navigation / .menu a / .navigation-title */
.header .navigation a,
.navigation .menu a,
.menu a {{
  font-family: var(--font-en-sans), var(--font-zh-serif) !important;
  font-weight: 500 !important;          /* 比默认更柔，不那么“粗硬” */
  letter-spacing: 0.2px !important;     /* 轻微字距，英文更清爽 */
  text-transform: none !important;      /* 避免主题把字母强制大写 */
  color: inherit !important;
}}

.navigation .menu a {{
  padding: 0 .55rem !important;         /* 菜单项留白更舒适 */
  opacity: .92;
  transition: opacity .15s ease, color .15s ease;
}}
.navigation .menu a:hover {{
  opacity: 1;
}}

/* 导航标题（左上角站点名）更稳重一点 */
.navigation .navigation-title,
.site-title {{
  font-family: var(--font-en-sans), var(--font-zh-serif) !important;
  font-weight: 620 !important;          /* 介于常规与粗体之间 */
  letter-spacing: .1px !important;
}}

/* === 首页主副标题的中英文协调 === */
/* 主页一般结构：.home-info 内含 h1(标题)、h2(副标题)、ul(社交) */
.home-info h1 {{
  font-family: var(--font-en-sans), var(--font-zh-serif) !important;
  font-weight: 700 !important;          /* 标题仍然醒目 */
  font-size: clamp(2.2rem, 4.5vw, 3.4rem) !important;
}}
/* === 首页主标题（你的名字） === */
.home-info h1,
.container.centered .about h1 {{
  font-family: var(--font-en-sans), var(--font-zh-serif) !important;
  font-weight: 700 !important;
  letter-spacing: 0.3px !important;

  /* ← 主标题字号在这里调 */
  font-size: clamp(2.2rem, 4.5vw, 3.4rem) !important;
  line-height: 1.22 !important;

  margin-bottom: 0.45em !important;
}}
/* === 首页副标题（两行换行 + 中英样式区分） === */
.container.centered .about h2 {{
  white-space: pre-line !important;      /* ✅ 支持 \\n 换行 */
  display: block;
  line-height: 1.55 !important;
  margin-top: -0.2em !important;
  margin-bottom: 0.9em !important;
}}
/* 英文页面的副标题（你的 “Urban Planning × AI”）去粗体、加字距 */
body[lang="en"] .home-info h2 {{
  font-family: var(--font-en-serif), var(--font-zh-serif) !important; /* 英文用衬线，和中文更搭 */
  font-weight: 100 !important;          /* 去粗体，更学术、更优雅 */
  letter-spacing: 0.3px !important;     /* 英文略加字距可读性更好 */
  opacity: .92;
}}
/* 中文页面副标题：保持略重，搭中文气质 */
body[lang="zh-cn"] .home-info h2 {{
  font-family: var(--font-en-sans), var(--font-zh-serif) !important;
  font-weight: 100 !important;
  letter-spacing: 0.15px !important;
}}


/* —— 卡片/项目轻交互 —— */
.post-card,.project-item{{
  border:1px solid color-mix(in srgb,currentColor 18%,transparent);
  border-radius:12px;
  padding:1rem;
  transition:transform .12s,box-shadow .12s,border-color .12s;
}}
.post-card:hover,.project-item:hover{{
  transform:translateY(-1px);
  box-shadow:0 4px 18px color-mix(in srgb,currentColor 12%,transparent);
  border-color:color-mix(in srgb,currentColor 30%,transparent);
}}

/* === 自定义 SVG 图标（iconSVG）统一尺寸 & 纯黑 === */
.social img.icon-svg,
.social a svg.icon-svg {{
  width: 3.2rem !important;
  height: 3.2rem !important;
  display: inline-block !important;
  vertical-align: middle !important;
  margin: 0 0.55rem !important;
}}

/* === Force FA <i> icons to scale + pure black === */
ul li a,
.social a,
.social-icons a {{
  color:#000 !important;
  opacity:1 !important;
}}

.social i[class^="fa-"],
.social i[class*=" fa-"] {{
  font-size:2.9rem !important;
  line-height:3rem !important;
  width:3rem !important;
  height:3rem !important;
  color:#000 !important;
  margin:0 0.55rem !important;
  vertical-align:middle !important;
  transition:transform .15s ease, opacity .15s ease;
}}

/* Post meta (date / reading time / tags) icon size: smaller */
.single .post-meta i,
.post .post-meta i,
.single .tags i,
.post .tags i {{
  font-size: .92rem !important;
  width: 1.1em !important;
  height: 1.1em !important;
  line-height: 1.1em !important;
  margin-right: .35em !important;
  opacity: .85 !important;
}}

/* meta 行里别把文字也放大 */
.single .post-meta,
.post .post-meta,
.single .tags,
.post .tags {{
  font-size: .96rem !important;
}}


/* === Hover: 不上跳 → 变红 === */
i[class^="fa-"]:hover,
i[class*=" fa-"]:hover {{
  transform:none !important;
  color:#8A1C32 !important;
  opacity:1 !important;
}}

/* 小红书 SVG hover 同步变红（可选） */
.social img.icon-svg:hover {{
  filter: invert(8%) sepia(92%) saturate(3600%) hue-rotate(-8deg) brightness(90%) contrast(112%) !important;
}}

/* 轻微按压感（80ms），不“跳”，更像原生 App */
.social .list-inline-item a:active i[class^="fa-"],
.social .list-inline-item a:active i[class*=" fa-"],
.social .list-inline-item a:active img.icon-svg {{
  transform: scale(.98);
  transition: transform 80ms ease;
}}

/* ========= 简历页核心排版（统一字体层级 + 整体加宽 + 左右布局稳） ========= */

/* 页面主体加宽 */
.cv-page {{
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 16px;
  font-size: 18px;
  line-height: 1.72;
}}
.cv-page .post,
.cv-page .page,
.cv-page .single,
.cv-page .list,
.cv-page .content {{
  max-width: 100% !important;
}}

/* 区块容器加宽 */
.cv-wide {{
  max-width: min(1400px, 96vw);
  margin: 0 auto;
}}

/* ========== 字号层级（你要的优先顺序） ========== */
/* 1) 区块标题：最大（Education / Experience / Publications / Skills） */
.cv-page h2,
.cv-page .cv-h2 {{
  font-size: 3rem;
  font-weight: 750;
  margin: 1.1em 0 .6em;
  font-family: var(--font-en-sans), var(--font-zh-serif);
}}

/* 2) 项目标题（org — role），中号且加粗 */
.cv-page .cv-title {{
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0 0 .25rem;
}}

/* 3) 正文内容（detail、bullets、技能条目等）：最小 */
.cv-page .cv-body,
.cv-page .cv-body p,
.cv-page .cv-sub,
.cv-page .cv-bullets,
.cv-page .cv-bullets li,
.cv-page .cv-list,
.cv-page .cv-list li {{
  font-size: 1.5rem;
  line-height: 1.65;
}}

/* 左侧时间/地点与正文同级、同大小 */
.cv-page .cv-meta,
.cv-page .cv-period,
.cv-page .cv-place {{
  font-size: 1.5rem;
  line-height: 1.65;
  color: color-mix(in srgb,currentColor 80%,transparent);
}}

.cv-role {{
  font-weight: 500;     /* 比 org 弱一点 */
  opacity: .85;
}}
/* ========== 两栏主栅格（左：时间，右：正文） ========== */
.cv-row {{
  display: grid;
  grid-template-columns: 100px minmax(0,1fr); /* ← 左列略缩短，正文更宽 */
  column-gap: 28px;
  padding: 14px 0;
  border-top: 1px solid color-mix(in srgb,currentColor 18%,transparent);
}}
.cv-row:first-of-type {{ border-top: 0; }}

/* ========== 发表 / 技能 两栏对齐 + 有分点 ========= */
.cv-col-2 {{
  column-count: 2;
  column-gap: 2.2rem;
  column-fill: balance;
}}
.cv-list {{
  list-style: disc;
  list-style-position: outside;
  margin: .2rem 0;
  padding-left: 1.2rem;
}}
.cv-list li {{
  break-inside: avoid;
  margin-bottom: .35rem;
}}

/* 仅用于“技能/发表”的单栏小圆点列表 */
.cv-dots {{
  list-style: none;           /* 去掉默认圆点 */
  padding-left: 1.1rem;       /* 留出自定义圆点位置 */
  margin: .2rem 0;
}}
.cv-dots li {{
  position: relative;
  margin: .3rem 0 .35rem;
  line-height: 1.65;
}}
.cv-dots li::before {{
  content: "•";               /* 小圆点 */
  position: absolute;
  left: -1.1rem;              /* 与 padding-left 对齐 */
  top: 0;
  /* 可选：若想更小/更淡，可以加：
     opacity: .85; font-size: .9em;
  */
}}


/* ========== 移动端响应 ========== */
@media (max-width: 900px) {{
  .cv-row {{
    grid-template-columns: 1fr;
    row-gap: .2rem;
  }}
  .cv-meta {{
    order: -1;
    display: flex;
    gap: .8rem;
    margin-bottom: .2rem;
  }}
  .cv-col-2 {{
    column-count: 1;
  }}
}}

/* === Project GIF grid & badges === */
.gif-grid {{
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
  margin: 12px 0 8px;
}}
.gif-grid figure {{ margin: 0; border: 1px solid color-mix(in srgb, currentColor 18%, transparent); border-radius: 10px; overflow: hidden; background: color-mix(in srgb, currentColor 6%, transparent); }}
.gif-grid img, .gif-grid video {{ width: 100%; display: block; aspect-ratio: 16/9; object-fit: cover; }}
.gif-grid figcaption {{ padding: 8px 10px; font-size: .96rem; opacity: .85; }}

.proj-badges {{ margin: 10px 0 2px; display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }}
.badge-soft {{
  display: inline-block;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid color-mix(in srgb, currentColor 22%, transparent);
  background: color-mix(in srgb, currentColor 6%, transparent);
  font-size: .92rem;
  opacity: .96;
}}
.btn.btn-report {{
  display: inline-block;
  padding: 8px 12px;
  border-radius: 10px;
  border: 1px solid color-mix(in srgb, currentColor 28%, transparent);
  text-decoration: none;
  font-weight: 600;
  opacity: 1;
}}
.btn.btn-report:hover {{
  background: color-mix(in srgb, currentColor 10%, transparent);
}}

/* Mobile */
@media (max-width: 700px) {{
  .gif-grid {{ grid-template-columns: 1fr; }}
}}

/* Single GIF figure (when only one image is provided) */
.gif-single {{
  margin: 12px 0 8px;
  border: 1px solid color-mix(in srgb, currentColor 18%, transparent);
  border-radius: 10px;
  overflow: hidden;
  background: color-mix(in srgb, currentColor 6%, transparent);
}}
.gif-single img, .gif-single video {{
  width: 100%;
  display: block;
  aspect-ratio: 16/9;
  object-fit: cover;
}}
.gif-single figcaption {{
  padding: 8px 10px;
  font-size: .96rem;
  opacity: .85;
}}


/* ===== Project 页面：自定义 Hero 标题 + 副标题（括号） + 一句话总结 ===== */

/* 小一号副标题：放在正文第一行，不与主题 H1 冲突 */
.proj-subtitle{{
  font-size: 2.5rem;
  line-height: 1.4;
  margin: -0.4rem 0 0.6rem;
  color: color-mix(in srgb, currentColor 58%, transparent);
  font-style: italic; /* 可去掉 */
}}

/* 一句话总结卡片（加大字号 + 斜体加粗） */
.lede{{
  font-size: 1.5rem;         /* 比之前更大 */
  font-weight: 700;          /* 加粗 */
  font-style: italic;        /* 斜体 */
  color: #333;
  margin: 12px 0 18px;
  padding: 12px 16px;
  border-left: 6px solid #E6E6E6;
  background: #fafafa;
  border-radius: 8px;
}}

/* --- Project 小标题（含子小标题）：覆盖 h3–h5，命中 Coder 常见容器 --- */
.single .content h3,
.single .content h4,
.single .content h5,
.post .content h3,
.post .content h4,
.post .content h5,
.content h3,
.content h4,
.content h5 {{
  font-family: var(--font-en-serif), var(--font-zh-serif) !important;
  font-weight: 700 !important;          /* 比正文略重 */
  font-size: 1.7rem !important;        /* ≈ 18.4px */
  line-height: 1.6 !important;
  margin: 0.9em 0 0.55em !important;
  opacity: .96 !important;
}}


/* === 表格：细灰线 + 按内容自动列宽 === */
table{{
  border-collapse: collapse;
  table-layout: auto;        /* 关键：按内容分配列宽 */
  width: auto;               /* 关键：不强制充满整行 */
  max-width: 100%;
  font-size: .9em;
  overflow-x: auto;          /* 防止超出时溢出 */
  display: block;            /* 允许横向滚动 */
}}
table th,table td{{
  border: 0.5px solid #E6E6E6; /* 细灰线 */
  padding: .55em .6em;
  white-space: nowrap;       /* 列宽由内容决定，不换行挤压 */
}}

/* === Project 公共：通用 figure 样式（不影响简历页） === */
.single .content figure {{
  margin: 12px 0 18px;
  border: 1px solid color-mix(in srgb, currentColor 18%, transparent);
  border-radius: 10px;
  background: color-mix(in srgb, currentColor 6%, transparent);
  overflow: hidden;
}}
.single .content figure img, .single .content figure video {{ display: block; width: 100%; height: auto; }}
.single .content figure figcaption {{ padding: 8px 10px; font-size: .96rem; opacity: .85; }}

/* 方法区（可选容器）：若渲染时包了 <div class="method-area"> */
.method-area figure {{ max-width: 780px; margin: 10px 0 16px; }}
.method-area figcaption {{ opacity: .85; }}

/* 研究区域与数据：与 GIF 网格保持一致的视觉 */
.single .content .study-area figure,
.single .content .study-data figure {{ max-width: 880px; }}

/* 研究结果：子小节与图片间距微调 */
.single .content h3 + figure,
.single .content h4 + figure {{ margin-top: 6px; }}

/* 避免多图连续出现时贴太近 */
.single .content figure + figure {{ margin-top: 10px; }}

/* 表格在 Project 页也走“细灰线 + 自动列宽”风格（保底兼容某些主题） */
.single .content table {{ width: auto !important; max-width: 100%; }}

/* ===== 可选：Safari 旧版对 color-mix 的回退，不改变视觉，仅加兜底 ===== */
.badge-soft {{
  background: rgba(0,0,0,.03); /* fallback */
  background: color-mix(in srgb, currentColor 6%, transparent);
  border-color: rgba(0,0,0,.12); /* fallback */
  border-color: color-mix(in srgb, currentColor 22%, transparent);
}}


"""


def ensure_typography(css_cdn: str = "google"):
    # 生成 CSS 文本
    css_text = render_typography_css(css_cdn)

    # 计算版本化文件名
    css_name = f"typography.{CONFIG.get('css_version','v1')}.css"

    # 写入 assets/css（给 customCSS / Hugo Pipes 用）
    assets_css = ROOT / "assets" / "css"
    assets_css.mkdir(parents=True, exist_ok=True)
    write_text(assets_css / css_name, css_text)

    # 同步一份到 static/css（本地预览或外链兜底，也便于直接访问）
    static_css = ROOT / "static" / "css"
    static_css.mkdir(parents=True, exist_ok=True)
    write_text(static_css / css_name, css_text)

    # （可选）删除旧版本样式，避免混淆
    for p in (assets_css, static_css):
        for old in p.glob("typography.*.css"):
            if old.name != css_name:
                try:
                    old.unlink()
                except Exception:
                    pass

    # 不再注入 extend_head 的 <link>（hugo-coder 会按 params.customCSS 自动加载）
    # 若你之前写过 layouts/partials/extend_head.html，可保留，无需新增任何 link。

    # 清 Hugo Pipes 缓存（防止旧样式残留）
    resources_dir = ROOT / "resources"
    if resources_dir.exists():
        for p in resources_dir.rglob("*"):
            try:
                if p.is_file():
                    p.unlink()
            except Exception:
                pass



# ================== 站点骨架 ==================
def ensure_skeleton():
    (ROOT / "static" / "images").mkdir(parents=True, exist_ok=True)
    (ROOT / "static" / "files").mkdir(parents=True, exist_ok=True)
    gi = ROOT / ".gitignore"
    if not gi.exists():
        write_text(gi, "/public/\n/resources/\n.DS_Store\n*.log\n")
    wf = ROOT / ".github" / "workflows" / "hugo.yml"
    if not wf.exists():
        write_text(wf, dedent("""\
        name: Deploy Hugo site to Pages
        on:
          push:
            branches: ["main"]
        permissions:
          contents: read
          pages: write
          id-token: write
        concurrency:
          group: "pages"
          cancel-in-progress: true
        jobs:
          build:
            runs-on: ubuntu-latest
            steps:
              - name: Checkout
                uses: actions/checkout@v4
                with:
                  submodules: true
                  fetch-depth: 0
              - name: Setup Hugo
                uses: peaceiris/actions-hugo@v3
                with:
                  hugo-version: "latest"
                  extended: true
              - name: Build
                run: hugo --minify
              - name: Upload artifact
                uses: actions/upload-pages-artifact@v3
                with:
                  path: ./public
          deploy:
            environment:
              name: github-pages
              url: ${{ steps.deployment.outputs.page_url }}
            runs-on: ubuntu-latest
            needs: build
            steps:
              - name: Deploy to GitHub Pages
                id: deployment
                uses: actions/deploy-pages@v4
        """))


def build(cfg: dict):
    
    ensure_skeleton()
    ensure_icons()
    ensure_social_partial()  # ← 新增：覆写主题的社交模板
    ensure_typography(css_cdn=cfg.get("css_cdn", "google"))

    # hugo.toml
    write_text(ROOT / "hugo.toml", render_hugo_toml(cfg))

    # 首页
    write_text(ROOT / "content" / "_index.md",    render_home("zh", cfg["home"]["zh"]))
    write_text(ROOT / "content" / "_index.en.md", render_home("en", cfg["home"]["en"]))

    # Projects Index
    write_text(ROOT / "content" / "projects" / "_index.md",    render_projects_index("项目"))
    write_text(ROOT / "content" / "projects" / "_index.en.md", render_projects_index("Projects"))

    # Resume
    write_text(ROOT / "content" / "resume" / "_index.md",    render_resume("zh", cfg["resume_pdf"]))
    write_text(ROOT / "content" / "resume" / "_index.en.md", render_resume("en", cfg["resume_pdf"]))

    # About
    write_text(ROOT / "content" / "about" / "_index.md",    render_about("zh"))
    write_text(ROOT / "content" / "about" / "_index.en.md", render_about("en"))

    # 项目
    for p in cfg.get("projects", []):
        write_text(ROOT / "content" / "projects" / f"{p['slug']}.md",    render_project_item(p, "zh"))
        write_text(ROOT / "content" / "projects" / f"{p['slug']}.en.md", render_project_item(p, "en"))

    print("\n✅ Build finished.")
    print("把头像放到 static/images/avatar.jpg；把简历 PDF 放到 static/files/resume.pdf")


# ================== 便捷命令 ==================
def load_config_from_py() -> dict:
    return CONFIG


def add_project(args):
    proj = {
        "slug": args.slug,
        "date": args.date,
        "tags": args.tags or [],
        "title_zh": args.title_zh,
        "title_en": args.title_en,
        "body_zh": args.body_zh or "",
        "body_en": args.body_en or "",
    }
    write_text(ROOT / "content" / "projects" / f"{proj['slug']}.md",    render_project_item(proj, "zh"))
    write_text(ROOT / "content" / "projects" / f"{proj['slug']}.en.md", render_project_item(proj, "en"))
    print("✅ 已生成项目：", proj["slug"])


def set_github_user(u: str):
    cfg_text = Path(__file__).read_text(encoding="utf-8")
    new_text = re.sub(r'("github_user":\s*")([^"]+)(")', rf'\1{u}\3', cfg_text, count=1)
    Path(__file__).write_text(new_text, encoding="utf-8")
    print(f"✅ 已把 github_user 改为：{u}")


def set_resume(p: str):
    cfg_text = Path(__file__).read_text(encoding="utf-8")
    new_text = re.sub(r'("resume_pdf":\s*")([^"]+)(")', rf'\1{p}\3', cfg_text, count=1)
    Path(__file__).write_text(new_text, encoding="utf-8")
    print(f"✅ 已把 resume_pdf 改为：{p}")


def set_avatar(p: str):
    cfg_text = Path(__file__).read_text(encoding="utf-8")
    new_text = re.sub(r'("avatar_url":\s*")([^"]+)(")', rf'\1{p}\3', cfg_text, count=1)
    Path(__file__).write_text(new_text, encoding="utf-8")
    print(f"✅ 已把 avatar_url 改为：{p}")


def main():
    ap = argparse.ArgumentParser(description="Manage Hugo Coder site with a single Python file.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("build", help="Generate or update hugo.toml and bilingual pages from CONFIG")

    sp = sub.add_parser("add-project", help="Add a bilingual project page")
    sp.add_argument("--slug", required=True)
    sp.add_argument("--date", required=True, help="YYYY-MM-DD")
    sp.add_argument("--tags", nargs="*")
    sp.add_argument("--title-zh", required=True)
    sp.add_argument("--title-en", required=True)
    sp.add_argument("--body-zh", default="")
    sp.add_argument("--body-en", default="")

    spg = sub.add_parser("set-github-user")
    spg.add_argument("user")

    spc = sub.add_parser("set-resume")
    spc.add_argument("path")

    spa = sub.add_parser("set-avatar")
    spa.add_argument("path")

    args = ap.parse_args()

    if args.cmd == "build":
        build(load_config_from_py())
    elif args.cmd == "add-project":
        add_project(args)
    elif args.cmd == "set-github-user":
        set_github_user(args.user)
    elif args.cmd == "set-resume":
        set_resume(args.path)
    elif args.cmd == "set-avatar":
        set_avatar(args.path)


if __name__ == "__main__":
    main()
