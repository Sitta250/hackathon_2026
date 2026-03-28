"""Two functions:
1. calculate_scenario_weighted_scores() — Agent 2 scores × Agent 3 weights
2. calculate_final_scores() — combines scenario-weighted scores with team fit scores



- Create a Code node (set language to Python)
- It needs to receive input from 3 nodes: Agent 2, Agent 3, and Agent 5
- Use a Merge node before it if needed to combine the three inputs
- Paste the two functions from score_math.py
- The node's code reads $input.all() or however n8n passes upstream data, calls the functions, and returns the result as JSON
"""


def calculate_scenario_weighted_scores(candidate_evaluations, adapted_criteria, emergent_criteria=None):
    """
    Multiply base candidate scores by scenario-adjusted weights.
    
    Args:
        candidate_evaluations: list of dicts from Agent 2 (Pass 2) output
            Each has: candidate_id, candidate_name, candidate_type, scores[]
            Each score has: criterion_id, score (int 0-10)
        
        adapted_criteria: list of dicts from Agent 3 output
            Each has: id, adjusted_weight (float, all sum to ~1.0 with emergent)
        
        emergent_criteria: list of dicts from Agent 3 output (optional)
            Each has: id, weight
            Candidates score 0 on emergent criteria by default unless
            the Candidate Fit Agent was re-run with emergent criteria included.
    
    Returns:
        list of dicts, each with:
            candidate_id, candidate_name, candidate_type,
            scenario_weighted_score (float 0-10),
            per_criterion_weighted (dict of criterion_id -> weighted contribution),
            scoring_breakdown (human-readable string)
    """
    # Build weight lookup from adapted criteria
    weights = {c["id"]: c["adjusted_weight"] for c in adapted_criteria}
    
    # Add emergent criteria weights (candidates default to 0 on these)
    if emergent_criteria:
        for ec in emergent_criteria:
            weights[ec["id"]] = ec["weight"]

    results = []

    for candidate in candidate_evaluations:
        # Build score lookup for this candidate
        score_lookup = {s["criterion_id"]: s["score"] for s in candidate["scores"]}

        weighted_sum = 0.0
        per_criterion = {}
        breakdown_parts = []

        for criterion_id, weight in weights.items():
            raw_score = score_lookup.get(criterion_id, 0)
            weighted_contribution = raw_score * weight
            weighted_sum += weighted_contribution
            per_criterion[criterion_id] = round(weighted_contribution, 3)
            breakdown_parts.append(f"{criterion_id}: {raw_score} × {weight:.2f} = {weighted_contribution:.2f}")

        results.append({
            "candidate_id": candidate["candidate_id"],
            "candidate_name": candidate["candidate_name"],
            "candidate_type": candidate["candidate_type"],
            "scenario_weighted_score": round(weighted_sum, 2),
            "per_criterion_weighted": per_criterion,
            "scoring_breakdown": " | ".join(breakdown_parts)
        })

    # Sort by scenario_weighted_score descending
    results.sort(key=lambda x: x["scenario_weighted_score"], reverse=True)

    return results


def calculate_final_scores(scenario_weighted_results, team_fit_assessments):
    """
    Apply the final scoring formula:
    final_score = (scenario_weighted_score × 0.75) + (team_fit_score × 0.25)
    
    Args:
        scenario_weighted_results: list of dicts from calculate_scenario_weighted_scores()
            Each has: candidate_id, scenario_weighted_score
        
        team_fit_assessments: list of dicts from Agent 5 output
            Each has: candidate_id, team_fit_score (float 0-10)
    
    Returns:
        list of dicts sorted by final_score descending, each with:
            rank, candidate_id, candidate_name, candidate_type,
            final_score, scenario_weighted_score, team_fit_score, formula_string
    """
    # Build team fit lookup
    team_fit_lookup = {t["candidate_id"]: t["team_fit_score"] for t in team_fit_assessments}

    results = []

    for candidate in scenario_weighted_results:
        cid = candidate["candidate_id"]
        sws = candidate["scenario_weighted_score"]
        tfs = team_fit_lookup.get(cid, 5.0)  # default 5.0 if missing

        final = round((sws * 0.75) + (tfs * 0.25), 2)

        results.append({
            "candidate_id": cid,
            "candidate_name": candidate["candidate_name"],
            "candidate_type": candidate["candidate_type"],
            "final_score": final,
            "scenario_weighted_score": sws,
            "team_fit_score": tfs,
            "formula_string": f"({sws} × 0.75) + ({tfs} × 0.25) = {final}"
        })

    # Sort by final_score descending
    results.sort(key=lambda x: x["final_score"], reverse=True)

    # Assign ranks (handle ties — within 0.1 = same rank)
    for i, candidate in enumerate(results):
        if i == 0:
            candidate["rank"] = 1
        else:
            prev = results[i - 1]
            if abs(prev["final_score"] - candidate["final_score"]) <= 0.1:
                candidate["rank"] = prev["rank"]  # tie
            else:
                candidate["rank"] = i + 1

    return results


# ---------------------------------------------------------------------------
# Example usage / test with mock data
# ---------------------------------------------------------------------------
if __name__ == "__main__":

    # Mock Agent 2 output — base scores across all 10 criteria
    mock_evaluations = [
        {
            "candidate_id": "C01",
            "candidate_name": "Dr. Stefan Keller",
            "candidate_type": "internal",
            "scores": [
                {"criterion_id": "C1", "score": 8},   # EV production
                {"criterion_id": "C2", "score": 7},   # Ramp-up / SOP
                {"criterion_id": "C3", "score": 6},   # Supply chain
                {"criterion_id": "C4", "score": 7},   # Quality
                {"criterion_id": "C5", "score": 8},   # Team leadership
                {"criterion_id": "C6", "score": 7},   # P&L
                {"criterion_id": "C7", "score": 4},   # Digital / I4.0
                {"criterion_id": "C8", "score": 7},   # Stakeholder
                {"criterion_id": "C9", "score": 6},   # Crisis mgmt
                {"criterion_id": "C10", "score": 4},  # Change mgmt
            ]
        },
        {
            "candidate_id": "C08",
            "candidate_name": "Maria Santos",
            "candidate_type": "external",
            "scores": [
                {"criterion_id": "C1", "score": 5},
                {"criterion_id": "C2", "score": 4},
                {"criterion_id": "C3", "score": 8},
                {"criterion_id": "C4", "score": 5},
                {"criterion_id": "C5", "score": 7},
                {"criterion_id": "C6", "score": 6},
                {"criterion_id": "C7", "score": 3},
                {"criterion_id": "C8", "score": 8},
                {"criterion_id": "C9", "score": 9},
                {"criterion_id": "C10", "score": 5},
            ]
        },
        {
            "candidate_id": "C06",
            "candidate_name": "Fatima Al-Rashidi",
            "candidate_type": "internal",
            "scores": [
                {"criterion_id": "C1", "score": 6},
                {"criterion_id": "C2", "score": 6},
                {"criterion_id": "C3", "score": 5},
                {"criterion_id": "C4", "score": 6},
                {"criterion_id": "C5", "score": 7},
                {"criterion_id": "C6", "score": 5},
                {"criterion_id": "C7", "score": 5},
                {"criterion_id": "C8", "score": 6},
                {"criterion_id": "C9", "score": 6},
                {"criterion_id": "C10", "score": 6},
            ]
        }
    ]

    # Normal operations — default JD weights (sum to 1.0)
    mock_normal_weights = [
        {"id": "C1", "adjusted_weight": 0.15},
        {"id": "C2", "adjusted_weight": 0.12},
        {"id": "C3", "adjusted_weight": 0.10},
        {"id": "C4", "adjusted_weight": 0.10},
        {"id": "C5", "adjusted_weight": 0.12},
        {"id": "C6", "adjusted_weight": 0.08},
        {"id": "C7", "adjusted_weight": 0.08},
        {"id": "C8", "adjusted_weight": 0.08},
        {"id": "C9", "adjusted_weight": 0.08},
        {"id": "C10", "adjusted_weight": 0.09},
    ]

    # Semiconductor crisis — C3 and C9 spike, C7 and C10 drop
    mock_crisis_weights = [
        {"id": "C1", "adjusted_weight": 0.10},
        {"id": "C2", "adjusted_weight": 0.06},
        {"id": "C3", "adjusted_weight": 0.22},
        {"id": "C4", "adjusted_weight": 0.07},
        {"id": "C5", "adjusted_weight": 0.10},
        {"id": "C6", "adjusted_weight": 0.08},
        {"id": "C7", "adjusted_weight": 0.03},
        {"id": "C8", "adjusted_weight": 0.12},
        {"id": "C9", "adjusted_weight": 0.20},
        {"id": "C10", "adjusted_weight": 0.02},
    ]

    # Team fit scores
    mock_team_fit = [
        {"candidate_id": "C01", "team_fit_score": 8.5},
        {"candidate_id": "C08", "team_fit_score": 6.5},
        {"candidate_id": "C06", "team_fit_score": 8.0},
    ]

    print("=" * 60)
    print("SEMICONDUCTOR CRISIS SCENARIO")
    print("=" * 60)
    crisis_results = calculate_scenario_weighted_scores(mock_evaluations, mock_crisis_weights)
    for r in crisis_results:
        print(f"  {r['candidate_name']:25s} scenario_weighted: {r['scenario_weighted_score']}")

    final_crisis = calculate_final_scores(crisis_results, mock_team_fit)
    print()
    for r in final_crisis:
        print(f"  #{r['rank']} {r['candidate_name']:25s} final: {r['final_score']}  ({r['formula_string']})")

    print()
    print("=" * 60)
    print("NORMAL OPERATIONS SCENARIO")
    print("=" * 60)
    normal_results = calculate_scenario_weighted_scores(mock_evaluations, mock_normal_weights)
    for r in normal_results:
        print(f"  {r['candidate_name']:25s} scenario_weighted: {r['scenario_weighted_score']}")

    final_normal = calculate_final_scores(normal_results, mock_team_fit)
    print()
    for r in final_normal:
        print(f"  #{r['rank']} {r['candidate_name']:25s} final: {r['final_score']}  ({r['formula_string']})")

    print()
    print("=" * 60)
    print("RANKING SHIFT DEMO")
    print("=" * 60)
    print(f"  Crisis #1:  {final_crisis[0]['candidate_name']}")
    print(f"  Normal #1:  {final_normal[0]['candidate_name']}")
    print(f"  Rankings shifted: {final_crisis[0]['candidate_id'] != final_normal[0]['candidate_id']}")