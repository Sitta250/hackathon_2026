# Bremo — Strategic Approach Document

## BMW Digital Excellence Hub Hackathon 2026

**Team approach for GenAI & Multi-Agent Hackathon**
**Document version**: 1.0 | March 2026

---

## 1. Understanding What BMW Actually Wants

### 1.1 The Core Thesis (from the slides)

BMW's hackathon is NOT about building an AI tool. It's about solving a **decision problem**: selecting the right leaders for the right roles at the right time.

The slides are explicit:
- "This is not a technical problem — it is a decision problem."
- "This is not about showing AI. This is about improving decisions."
- "AI should not replace human judgment. It should augment decision quality."

**What this means for us**: Every feature, every agent, every UI element must trace back to "does this help a VP of HR make a better leadership hiring decision?" If it doesn't, cut it.

### 1.2 The Seven Problems BMW Called Out

These are the pain points from slide 3. Our system must visibly attack at least 5 of them.

| # | Problem | Our Attack |
|---|---------|------------|
| 1 | Experience-driven, intuition-heavy | Structured multi-criteria evaluation with evidence citations |
| 2 | Rating inflation (everyone is 7 or 8) | Anti-inflation scoring rules enforced in CV Agent |
| 3 | Limited scenario simulation | Scenario toggle with live re-ranking |
| 4 | Speed over fit (fastest available, not best) | Explicit speed-vs-fit analysis in Decision Agent output |
| 5 | Past over future fit | Scenario Agent reweights for future context, not just track record |
| 6 | Ignoring leadership combinations | Leadership Agent models team dynamics with existing team |
| 7 | Weak downstream visibility | Counterfactual engine shows cost of wrong decision |

### 1.3 Scoring Strategy

| Category | Points | Our Strategy |
|----------|--------|--------------|
| Business Relevance | 30 | BMW-specific role, automotive scenarios, language that resonates with BMW judges |
| Working Functionality | 25 | Full end-to-end pipeline, real LLM calls, scenario toggle changes rankings live |
| AI & Agent Quality | 20 | 5 core agents + Challenger Agent + deliberation loop + sensitivity analysis |
| Technical Implementation | 10 | Clean Python, Pydantic schemas, separated prompts, GitHub with README |
| User Experience | 10 | Lovable frontend, clean dashboard, ranking animations on scenario switch |
| Video Clarity | 5 | 3-min structure matching their exact template |

**Heavy penalty avoidance**: Must have working backend (not Lovable-only), GitHub repo, real logic (not hardcoded), working execution.

### 1.4 Judge Profile

**Dr. Ishansh Gupta** — Head of Digital Excellence Hub at BMW Group HQ, Causal AI Lecturer, Lindau Nobel Laureate Top Young Scientist.

Implications:
- He will look for **causal reasoning chains**, not just correlation-based scoring
- He values **scientific rigor** in agent decomposition and reasoning structure
- He will notice if "AI" is just a single prompt wrapped in a pipeline aesthetic
- **Counterfactual reasoning** (what would have happened under different conditions) will resonate deeply
- **Adversarial validation** (testing conclusions by trying to disprove them) is core to his field

---

## 2. Product Definition

### 2.1 Product Name & Positioning

**Bremo** — Context-Aware Leadership Decision Engine

**One-liner**: When business priorities shift, your candidate rankings should shift too — and the system should explain exactly why, challenge its own recommendation, and show you how confident it is.

### 2.2 Challenge Selection

We are building **Challenge 4 (Scenario-Based Ranking)** as the primary use case, with elements of Challenge 1 (Speed vs Right Hire), Challenge 3 (Leadership Personality Fit), and Challenge 6 (Leadership Combination Impact) folded in.

**Why this combination wins**: It's the only approach that naturally demonstrates **decision improvement under shifting conditions** while also addressing the most pain points from slide 3. It subsumes the core logic of multiple challenges, creating density of value in a single focused product.

### 2.3 The Use Case Story

A VP of HR at BMW has 6 shortlisted candidates for **Head of Production — Electric Vehicle Division, EMEA**. This is a critical leadership role overseeing the production ramp-up of the Neue Klasse platform across Munich, Leipzig, Dingolfing, and Debrecen plants.

The original JD prioritized manufacturing efficiency and process excellence. But the business context is shifting: a semiconductor supplier is at risk, the board wants to accelerate EV timelines, and Tesla/Amazon are poaching BMW's production engineers.

Bremo:
1. Parses the JD and extracts 10 weighted evaluation criteria
2. Adapts those weights when the user selects a business scenario
3. Scores each candidate against adapted criteria with specific CV evidence
4. Profiles each candidate's leadership style and team compatibility
5. Ranks candidates with full causal reasoning chains
6. Challenges its own recommendation (Challenger Agent)
7. Tests ranking stability (Sensitivity Analysis)
8. Shows the cost of wrong assumptions (Counterfactual Engine)

### 2.4 The Demo Moment

The single most important moment in the demo: the user selects "Semiconductor Supply Crisis" from the scenario dropdown, and the candidate rankings visibly reorder. Dr. Stefan Keller (the safe internal pick) drops from #1 to #3. Maria Santos (the crisis specialist) jumps to #1. The reasoning panel shows exactly why — which criteria shifted, which evidence drove the re-ranking, and the Challenger Agent's dissenting opinion.

Then the user sees the counterfactual: "If you had hired Stefan for normal operations but a crisis actually hit, here's the 2.5-point fitness gap and what that means for the first 6 months."

---

## 3. Architecture — What Everyone Builds vs What We Build

### 3.1 The Baseline (What every team will build)

A linear pipeline: JD Agent → Scenario Agent → CV Agent → Leadership Agent → Decision Agent. Input goes in, scores come out, rankings change when you toggle scenario.

The judges will see this 10-15 times. By the 5th demo, it's wallpaper.

### 3.2 Our Edge: Three Architectural Upgrades

We keep the 5-agent core (matching BMW's reference architecture exactly) but add three layers that no other team will build:

#### Upgrade 1: The Challenger Agent (Devil's Advocate)

**What it does**: After the Decision Agent produces its ranking, the Challenger Agent receives the full ranking + reasoning chain and actively tries to destroy the recommendation. It asks: "What's the strongest argument AGAINST hiring #1? What blind spot could reverse this ranking? What evidence is the pipeline over-weighting?"

**Why it wins**:
- Mirrors real BMW board dynamics — someone always plays devil's advocate in a leadership appointment
- Directly attacks the "good-looking decisions that are not optimal" problem from slide 3
- Dr. Gupta will recognize this as **adversarial validation** — testing a conclusion by trying to disprove it

**How it works in the pipeline**:
1. Challenger receives Decision Agent output
2. Identifies weakest assumptions in the ranking
3. Sends specific re-evaluation requests back to CV Agent (e.g., "Re-score Stefan's crisis management considering his 18 years of BMW supplier relationships")
4. If scores change meaningfully → Decision Agent re-ranks
5. If scores hold → original ranking confirmed, but challenge + response included in output

**This creates a deliberation loop, not just a pipeline.** The demo moment: user sees initial ranking → Challenger's critique appears → either "ranking confirmed after challenge" or "ranking adjusted after re-evaluation."

#### Upgrade 2: Sensitivity Analysis (Ranking Fragility)

**What it does**: Tests how stable the ranking is by perturbing scores and weights.

**Why it wins**:
- No other team will do this because they're thinking in "agents" — we're thinking in decision science
- The output is: "Maria's #1 position is robust — 47 of 50 perturbations maintain her rank. But #2 and #3 are within 0.3 points — a single criterion re-score could swap them."
- Gives the VP of HR language to defend the recommendation: "This is a high-confidence recommendation."

**How it works** (pure Python, zero LLM calls):
1. Take final scores matrix (6 candidates × 10 criteria × weights)
2. Perturb each score ±1, each weight ±15%
3. Recompute weighted rankings for each perturbation
4. Track which perturbations cause rank swaps
5. Output fragility map per ranking position

#### Upgrade 3: Counterfactual Engine (What-If Cost Analysis)

**What it does**: Shows the cost of wrong assumptions. "If you hired for Scenario 1 but Scenario 2 actually happened, here's the decision cost."

**Why it wins**:
- **Counterfactual reasoning is the core of causal inference** — Dr. Gupta's field
- Directly attacks slide 3: "good-looking decisions that are not optimal"
- No other team will model the cost of being wrong — they'll just show the "right" answer

**How it works**:
1. Run pipeline for Scenario A → get Candidate X as #1
2. Take Candidate X's raw scores
3. Apply Scenario B's adapted weights to Candidate X
4. Compare against Scenario B's actual #1
5. Output: "Hiring for stability when a crisis hits creates a 2.5-point fitness gap — equivalent to missing crisis management and supplier pressure experience in the critical first 6 months."

### 3.3 Full Architecture Flow

```
Phase 1: Analysis (standard)
  JD → JD Agent → Criteria
  Scenario → Scenario Agent → Adapted Criteria (with causal reasoning)

Phase 2: Evaluation (standard)
  CVs + Adapted Criteria → CV Agent → Scores (anti-inflation enforced)
  CVs + Scores + Team Profile → Leadership Agent → Leadership Profiles + Combination Analysis

Phase 3: Decision (standard)
  All outputs → Decision Agent → Initial Ranking + Reasoning + Trade-offs

Phase 4: Challenge (OUR EDGE)
  Initial Ranking → Challenger Agent → Critique + Re-evaluation Requests
  Re-evaluation → CV Agent (targeted re-score) → Updated Scores
  Updated Scores → Decision Agent → Final Ranking (confirmed or adjusted)

Phase 5: Confidence (OUR EDGE)
  Final Scores Matrix → Sensitivity Analysis (Python, no LLM) → Fragility Map
  Multi-Scenario Results → Counterfactual Engine (Python, no LLM) → Decision Cost Analysis

Output: Decision Package
  = Final Ranking + Reasoning Chains + Challenger Dissent + Fragility Map + Counterfactual Costs
```

### 3.4 Agent-by-Agent Specification

#### Agent 1: JD Analysis Agent
- **Role**: Extract structured evaluation criteria from job description
- **BMW-specific**: Must understand automotive terminology (SOP, BPS, IATF 16949, quality gates, ramp-up)
- **Input**: Raw JD text
- **Output**: 10 criteria with default weights, evidence markers, anti-patterns, minimum thresholds
- **Key design choice**: Categorizes criteria into hard_skill / soft_skill / leadership_competency / contextual — this distinction matters for the Leadership Agent downstream

#### Agent 2: Scenario Agent
- **Role**: Reweight criteria based on business scenario with causal reasoning
- **Key differentiator**: Every weight change must include a **causal chain**: pressure → impact on role → criterion change → reasoning
- **Must also identify**: Emergent criteria (things that only matter under this scenario) and the risk of hiring for the wrong scenario's priorities
- **Input**: Criteria from Agent 1 + scenario description
- **Output**: Adapted criteria with causal reasoning + emergent criteria + risk profile

#### Agent 3: CV Evaluation Agent
- **Role**: Score each candidate 0-10 on each criterion with evidence
- **Anti-inflation rules** (hard-coded in system prompt):
  - Maximum 2 candidates can score 8+ on any single criterion
  - At least 1 candidate must score below 5 on each criterion
  - Standard deviation across candidates per criterion must be ≥ 1.5
  - No evidence = score ≤ 4 with "insufficient evidence" flag
- **Input**: Adapted criteria + candidate CVs
- **Output**: Full score matrix with evidence, confidence levels, and differentiation check

#### Agent 4: Leadership Profiling Agent
- **Role**: Profile leadership style, assess team compatibility, evaluate scenario alignment
- **Leadership dimensions**: Archetype (Visionary/Operator/Fixer/Builder/Diplomat/Innovator), Decision Style (Data-driven/Intuitive/Consensus/Directive), Change Orientation (Transformer/Stabiliser/Adapter), Risk Profile (Conservative/Calculated/Aggressive)
- **Team combination**: Must assess how each candidate would interact with the specific existing team (SVP Production, Head of Quality, Head of Supply Chain, Head of HR Manufacturing, CFO Manufacturing)
- **Input**: CVs + scores + existing team profiles
- **Output**: Leadership profiles + combination analysis + scenario alignment scores

#### Agent 5: Decision Synthesis Agent
- **Role**: Produce final ranking with full causal reasoning chains
- **Must include**: Speed-vs-fit analysis, trade-off matrix (top 2 comparison), combination warnings, confidence assessment, data gaps
- **Key requirement**: Every ranking must trace the full chain: scenario pressures → adapted criteria → evidence from CV → leadership fit → final rank
- **Input**: All outputs from Agents 1-4
- **Output**: Ranked candidates with comprehensive decision package

#### Agent 6: Challenger Agent (Our Edge)
- **Role**: Adversarial validation of the Decision Agent's recommendation
- **System prompt framing**: "You are a skeptical board member at BMW Group. Your job is to find the weakest link in this recommendation. You are not contrarian — you are rigorous."
- **Three attack vectors**:
  1. **Evidence challenge**: Is a high score supported by strong evidence, or just inferred?
  2. **Assumption challenge**: What scenario assumption could be wrong?
  3. **Underrated candidate**: Who might the pipeline be systematically undervaluing?
- **Input**: Decision Agent output + all scores + reasoning chains
- **Output**: Critique with specific re-evaluation requests + risk the current ranking is wrong

---

## 4. Synthetic Data Design

### 4.1 Design Philosophy

The synthetic data is not filler — it's the **demonstration vehicle**. Every candidate, scenario, and score difference must be designed to produce the demo moments that win points. The data must be realistic enough that a BMW judge thinks "this could be a real hiring committee discussion."

### 4.2 Job Description

**Role**: Head of Production — Electric Vehicle Division, EMEA
**Company**: BMW Group Manufacturing
**Reports to**: SVP of Production
**Location**: Munich, with oversight of Leipzig, Dingolfing, Debrecen plants
**Context**: Scaling EV production (iX, i4, Neue Klasse platform), 3,000-person workforce across 3 plants

**10 Criteria** (the JD Agent should extract these):

| ID | Criterion | Category | Default Weight |
|----|-----------|----------|----------------|
| C1 | EV/automotive production management | Hard skill | 0.15 |
| C2 | Production ramp-up & SOP expertise | Hard skill | 0.12 |
| C3 | Supply chain risk management | Hard skill | 0.10 |
| C4 | Quality management (IATF 16949, BMW QMS) | Hard skill | 0.10 |
| C5 | Team leadership at scale (1000+) | Leadership competency | 0.12 |
| C6 | P&L and budget ownership (€100M+) | Hard skill | 0.08 |
| C7 | Digital manufacturing / Industry 4.0 | Hard skill | 0.08 |
| C8 | Stakeholder management (board, unions, gov) | Soft skill | 0.08 |
| C9 | Crisis management & rapid problem-solving | Leadership competency | 0.08 |
| C10 | Change management & cultural transformation | Leadership competency | 0.09 |

### 4.3 Candidates — Designed for Ranking Shifts

Each candidate is engineered to be the clear winner under ONE scenario and competitive under others. This ensures every scenario toggle produces a different #1.

| ID | Name | Archetype | Background Summary | Wins Under |
|----|------|-----------|-------------------|------------|
| C1 | Dr. Stefan Keller | The Proven Operator | 18yr BMW veteran, ran 3 Series production at Dingolfing, Six Sigma Black Belt, deep process knowledge, conservative leader, strong union relations | Normal Operations |
| C2 | Maria Santos | The Crisis Commander | Ex-Stellantis turnaround lead, managed semiconductor shortage response for 14 plants, military logistics background, decisive under pressure, limited EV-specific experience | Semiconductor Crisis |
| C3 | Dr. Anika Lindström | The Digital Transformer | Ex-Tesla Gigafactory Berlin launch team, Industry 4.0 pioneer, AI-driven quality systems, startup mentality, strong technical vision, less experience managing at BMW scale | EV Acceleration |
| C4 | Takeshi Nakamura | The Quality Architect | Toyota Production System master, 20yr quality leadership, IATF lead auditor, methodical and patient, may be slow in crisis, deep automotive knowledge | Niche (quality scenarios) |
| C5 | James Ashworth | The External Disruptor | Amazon VP of Operations (EU), tech-scale logistics, data-driven, magnetic leadership, zero automotive experience, but exactly the profile that retains tech talent | Talent War |
| C6 | Fatima Al-Rashidi | The Internal Rising Star | 8yr BMW, currently Head of i4 production line Leipzig, fast-tracked talent, excellent union relations, less senior, lower risk hire for cost, strong internal network | Cost-conscious / Continuity |

### 4.4 Expected Ranking Shifts

| Rank | Normal Ops | Semiconductor Crisis | EV Acceleration | Talent War |
|------|-----------|---------------------|-----------------|------------|
| #1 | Stefan Keller | Maria Santos | Anika Lindström | James Ashworth |
| #2 | Fatima Al-Rashidi | Stefan Keller | James Ashworth | Fatima Al-Rashidi |
| #3 | Takeshi Nakamura | Fatima Al-Rashidi | Stefan Keller | Anika Lindström |
| #4 | Anika Lindström | Takeshi Nakamura | Fatima Al-Rashidi | Stefan Keller |
| #5 | Maria Santos | Anika Lindström | Maria Santos | Maria Santos |
| #6 | James Ashworth | James Ashworth | Takeshi Nakamura | Takeshi Nakamura |

**Key demo insight**: James Ashworth (Amazon VP) goes from dead last (#6) under normal operations to #1 under the talent war scenario. This is the most dramatic shift and the best demo moment for "the right person depends entirely on the context."

### 4.5 Existing Leadership Team (for Combination Analysis)

| Role | Name | Profile | Interaction Dynamics |
|------|------|---------|---------------------|
| SVP Production (boss) | Klaus Richter | Conservative, process-oriented, ex-Audi, values stability | Will clash with disruptors, mesh well with operators |
| Head of Quality | Dr. Hans-Peter Winkler | Detail-obsessed perfectionist, 25yr BMW, German engineering mindset | Will love Takeshi, clash with James (speed over precision) |
| Head of Supply Chain | Sophie Laurent | Aggressive dealmaker, ex-McKinsey, moves fast, high-pressure | Will mesh with Maria (crisis energy), clash with Stefan (too measured) |
| Head of HR Manufacturing | Thomas Brenner | People-first, union liaison, consensus builder | Will support Fatima (internal), resist James (external disruption) |
| CFO Manufacturing | Dr. Eva Hoffmann | Numbers-driven, zero tolerance for budget overruns | Will scrutinize any expensive external hire, favor internal candidates |

### 4.6 Business Scenarios

**Scenario 1: Normal Operations**
BMW is executing its current EV production plan. No unusual pressures. The Neue Klasse timeline is on track. Supplier relationships are stable. The focus is operational excellence, continuous improvement, and steady ramp-up.

Criteria weight multipliers: All at 1.0x (baseline)

---

**Scenario 2: Semiconductor Supply Crisis**
A fire at a key semiconductor supplier (providing 50% of BMW's automotive chips) creates a 6-month disruption. All three plants face production cuts. BMW must decide how to allocate limited chips across models, renegotiate with alternative suppliers, and maintain delivery commitments to dealers.

Criteria weight multipliers:
- C9 Crisis management: 3.0x
- C3 Supply chain risk: 2.5x
- C8 Stakeholder management: 2.0x
- C5 Team leadership: 1.5x
- C6 P&L: 1.5x (budget pressure from lost production)
- C7 Digital manufacturing: 0.5x (not the priority right now)
- C10 Change management: 0.3x (not the time for transformation)

---

**Scenario 3: Neue Klasse EV Acceleration**
The board mandates that BMW's next-generation EV platform (Neue Klasse) launches 6 months ahead of schedule at the new Debrecen plant. This requires aggressive SOP timelines, rapid deployment of new production technology (800V architecture, round cells), massive hiring and training, and tight coordination with R&D on design-for-manufacturing.

Criteria weight multipliers:
- C2 Ramp-up & SOP: 3.0x
- C7 Digital manufacturing: 2.5x
- C10 Change management: 2.0x
- C5 Team leadership: 1.5x
- C1 EV production: 1.5x
- C9 Crisis management: 0.5x (planned acceleration, not a crisis)
- C4 Quality: 0.8x (still matters but can't slow the timeline)

---

**Scenario 4: Talent War — Tech Company Disruption**
Amazon and Tesla are aggressively recruiting BMW's production engineers and leaders. Manufacturing leadership attrition hits 15% (normally 5%). The next Head of Production must not only manage production but become a talent magnet — someone who makes BMW manufacturing feel like the most exciting place to work. The board wants to "out-innovate the innovators" to retain talent.

Criteria weight multipliers:
- C5 Team leadership: 2.5x
- C10 Change management: 2.5x
- C7 Digital manufacturing: 2.0x
- C8 Stakeholder management: 1.5x
- C1 EV production: 1.0x
- C4 Quality: 0.7x
- C3 Supply chain: 0.5x

---

## 5. Technical Architecture

### 5.1 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Agent orchestration | Python 3.11+ | Core pipeline logic |
| Data contracts | Pydantic v2 | Type-safe I/O between agents |
| LLM calls | Claude Sonnet 4 / GPT-4o | Agent reasoning (via config toggle) |
| API layer | FastAPI | Backend endpoints for frontend |
| Frontend | Lovable | Rapid UI prototyping |
| Version control | GitHub | Required deliverable |

### 5.2 Project Structure

```
Bremo/
├── README.md
├── requirements.txt
├── config.py
├── main.py                     # CLI: run full pipeline
├── orchestrator.py             # Chains agents, manages deliberation loop
├── sensitivity.py              # Perturbation-based ranking stability
├── counterfactual.py           # What-if scenario cost analysis
├── agents/
│   ├── __init__.py
│   ├── base_agent.py           # LLM call + retry + validation + logging
│   ├── jd_agent.py
│   ├── scenario_agent.py
│   ├── cv_agent.py
│   ├── leadership_agent.py
│   ├── decision_agent.py
│   └── challenger_agent.py     # Our edge
├── models/
│   ├── __init__.py
│   └── schemas.py              # All Pydantic models
├── data/
│   ├── job_description.json
│   ├── existing_team.json
│   ├── candidates/             # 6 candidate CV files
│   └── scenarios/              # 4 scenario files
├── prompts/                    # System prompts stored separately
├── api/
│   └── server.py               # FastAPI endpoints
└── tests/
    ├── test_pipeline.py        # End-to-end verification
    └── test_agents.py          # Unit tests per agent
```

### 5.3 Key Technical Decisions

**Why Python over n8n**: Code-level control for anti-inflation rules, causal chain enforcement, deliberation loop, sensitivity analysis. Clean GitHub visibility. The judge reads code, not drag-and-drop canvases.

**Why separated system prompts** (`/prompts/` folder): Easy to iterate on prompts without touching code. Each prompt is expert-level — written as if briefing a real specialist, not a generic "you are a helpful assistant."

**Why Pydantic at every boundary**: Validates agent output before passing to the next agent. Catches malformed JSON before it propagates. Makes the I/O contracts visible and auditable in the code.

**Why FastAPI + Lovable**: FastAPI is the minimal backend that gives us typed endpoints, auto-generated docs, and CORS for Lovable. Lovable gives us a polished UI in hours, not days. The two-layer architecture (Python backend + Lovable frontend) is clean, visible on GitHub, and clearly "not Lovable-only."

### 5.4 Orchestrator Flow (with Deliberation Loop)

```python
# Simplified orchestrator logic

# Phase 1: Analysis (cacheable — JD analysis is scenario-independent)
jd_result = jd_agent.run(job_description)

# Phase 2: For each scenario...
scenario_result = scenario_agent.run(jd_result.criteria, scenario)
adapted_criteria = scenario_result.adapted_criteria

# Phase 3: Evaluation
cv_scores = cv_agent.run(adapted_criteria, candidates)
leadership_profiles = leadership_agent.run(candidates, cv_scores, existing_team)

# Phase 4: Initial Decision
initial_ranking = decision_agent.run(cv_scores, leadership_profiles, scenario_result)

# Phase 5: Deliberation (OUR EDGE)
challenge = challenger_agent.run(initial_ranking, cv_scores, leadership_profiles)

if challenge.requests_reevaluation:
    # Targeted re-scoring with challenge context
    updated_scores = cv_agent.rescore(
        challenge.reevaluation_targets,
        challenge.reasoning,
        adapted_criteria,
        candidates
    )
    final_ranking = decision_agent.run(updated_scores, leadership_profiles, scenario_result)
    final_ranking.challenge_result = "adjusted"
else:
    final_ranking = initial_ranking
    final_ranking.challenge_result = "confirmed"

final_ranking.challenger_dissent = challenge

# Phase 6: Confidence Analysis (pure Python, no LLM)
fragility = sensitivity_analysis(cv_scores, adapted_criteria)
counterfactuals = counterfactual_engine(all_scenario_results)

# Package everything
decision_package = DecisionPackage(
    ranking=final_ranking,
    fragility_map=fragility,
    counterfactual_costs=counterfactuals,
    challenger_dissent=challenge
)
```

---

## 6. Frontend / UX Approach

### 6.1 Dashboard Layout

Three-panel layout:

**Left panel — Scenario Selector**
- Dropdown or card selector for 4 scenarios
- Brief scenario description when selected
- Visual indicator of which criteria weights changed (small bar chart showing weight deltas)

**Center panel — Candidate Rankings**
- Ranked list of 6 candidates with scores
- Each candidate card shows: rank, name, weighted score, headline reason, leadership archetype badge
- When scenario changes: animated reorder of candidate cards (this is the demo moment)
- Expandable per-candidate: full score breakdown per criterion, evidence citations, leadership profile

**Right panel — Decision Intelligence**
- Tab 1: Reasoning Chain — full causal trace for #1 ranked candidate
- Tab 2: Challenger — the dissenting opinion and whether ranking was adjusted
- Tab 3: Sensitivity — fragility map showing ranking stability
- Tab 4: What-If — counterfactual costs across scenarios

### 6.2 Key UX Moments (for the demo video)

1. **Scenario switch** → candidate cards animate into new positions
2. **Expand reasoning** → see the full causal chain from scenario pressure to final rank
3. **View challenge** → see what the Challenger found and how the system responded
4. **View what-if** → see the cost of hiring for the wrong scenario

---

## 7. Build Sequence (Priority Order)

| Step | Task | Time Estimate | Why This Order |
|------|------|--------------|----------------|
| 1 | Synthetic data (JD, 6 CVs, 4 scenarios, team profiles) | 2-3 hours | Unblocks everything else |
| 2 | Pydantic schemas | 1 hour | Defines all contracts before coding agents |
| 3 | Base agent (LLM call infra) | 1 hour | Foundation for all agents |
| 4 | JD Agent | 1 hour | First in pipeline |
| 5 | Scenario Agent | 1.5 hours | Depends on JD Agent output |
| 6 | CV Agent (with anti-inflation) | 2 hours | Hardest agent — scoring quality matters |
| 7 | Leadership Agent | 1.5 hours | BMW's differentiator |
| 8 | Decision Agent | 1.5 hours | Synthesis — needs all upstream data |
| 9 | Challenger Agent | 1.5 hours | Our edge #1 |
| 10 | Sensitivity Analysis | 1 hour | Pure Python, no LLM |
| 11 | Counterfactual Engine | 1 hour | Pure Python, no LLM |
| 12 | Orchestrator (with deliberation loop) | 2 hours | Chains everything |
| 13 | FastAPI server | 1.5 hours | Backend for frontend |
| 14 | Lovable frontend | 3-4 hours | UI layer |
| 15 | Verification (run all 4 scenarios, verify shifts) | 1 hour | Must pass before submission |
| 16 | Demo video | 2 hours | Last step |

**Total estimated**: ~22-24 hours of focused work

### 7.1 Cut List (If Running Out of Time)

Priority of what to cut (last = most expendable):

1. **Never cut**: 5 core agents + scenario toggle + working pipeline (this IS the product)
2. **Never cut**: GitHub repo with README
3. **Cut reluctantly**: Challenger Agent (reduces from "wow" to "solid")
4. **Cut if needed**: Counterfactual Engine (nice to have, not core)
5. **Cut if needed**: Sensitivity Analysis (enhances confidence, not core)
6. **Cut if needed**: Animated ranking transitions in UI (static reorder is fine)

---

## 8. Risk Mitigation

| Risk | Mitigation |
|------|------------|
| LLM returns malformed JSON | 3x retry with error feedback appended to prompt |
| Rankings don't shift across scenarios | Design candidate profiles to ensure shifts (Section 4.4). Test early. |
| CV Agent produces inflated scores | Anti-inflation rules in system prompt + post-validation check |
| Pipeline too slow for live demo | Cache JD Agent output. Pre-compute 2-3 scenarios before demo. |
| Lovable frontend can't call FastAPI | Deploy FastAPI to a simple host (Railway, Render). CORS enabled. |
| Challenger Agent always agrees or always disagrees | Calibrate system prompt to challenge only when there's a defensible counter-argument |
| Video exceeds 3 minutes | Script it to the second using BMW's exact structure |

---

## 9. What Makes This Win

### 9.1 Versus Other Teams

| What Other Teams Do | What We Do |
|---------------------|------------|
| Linear pipeline: 5 agents in a row | Deliberation loop with adversarial challenge |
| "Here's the ranking" | "Here's the ranking + the strongest argument against it + how stable it is + what happens if you're wrong" |
| Generic HR scenario | BMW-specific role, plants, scenarios, automotive terminology |
| Scores with brief explanations | Full causal chains: scenario pressure → criteria shift → evidence → leadership fit → rank |
| Rating inflation (everyone is 7-8) | Anti-inflation rules with enforced score spread |
| Ignore existing team | Leadership combination analysis with named team members |
| One output view | Decision package: ranking + challenge + sensitivity + counterfactual |

### 9.2 How We Score Maximum Points

**Business Relevance (30 pts)**: BMW role, BMW scenarios, BMW team members, language that resonates ("Neue Klasse ramp-up," "Debrecen plant," "IATF 16949"). The judges hear their own world.

**Working Functionality (25 pts)**: Full pipeline runs end-to-end. Every button does something real. Scenario toggle changes rankings with different results each time. No hardcoded outputs.

**AI & Agent Quality (20 pts)**: 6 agents (5 core + Challenger), deliberation loop, causal reasoning chains, anti-inflation rules, sensitivity analysis. This is the deepest agent system any team will build.

**Technical Implementation (10 pts)**: Clean Python, Pydantic schemas, separated prompts, FastAPI, GitHub with architecture diagram in README.

**User Experience (10 pts)**: Clean three-panel dashboard. Scenario toggle is the primary interaction. Animated ranking reorder. Expandable reasoning.

**Video Clarity (5 pts)**: Exact match to BMW's 3-minute structure. Problem → Input → Live Demo → AI/Agents → Business Value.

---

## 10. The Elevator Pitch (for the video opening)

"Every year, organizations make leadership hiring decisions based on intuition, inflated ratings, and static job descriptions — and the wrong hire costs 12-18 months of damage. Bremo is a multi-agent decision engine that evaluates leadership candidates against the business context that actually matters. When priorities shift — a supply crisis, an EV acceleration, a talent war — the rankings shift too, and the system explains exactly why, challenges its own recommendation, and tells you how confident you should be in the decision. This isn't AI replacing human judgment. This is AI making human judgment defensible."
