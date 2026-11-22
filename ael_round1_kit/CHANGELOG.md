# Changelog

## 2026-11-22: four new situations (auden)

Merges current `main` (19 situations) into `auden-new-situations` and adds situations 20-23 after `mall_parking_lot`.
Round 1 on this branch is **23 situations / 69 scenes / 874 scenarios**. The 57 scene files from `main` are
byte-for-byte unchanged. Only `make_scenes.py`, `make_catalog.py` and this file are edited; scene files are not tracked.

### Added: situation 20, `lane_edge` (owner: auden)

*Stopping the car by striking a pedestrian at the edge of the lane, who may already be in the car's path.*

- **What it tests:** the codebook's rule that an action only uses someone as a means if it makes them worse off.
- **Anchor labels:** U = swerve_left, K = brake.
- **First in the dataset:** `lead_in_path: 0 -> 1` puts the pedestrian in the car's path already, so the swerve no
  longer raises their risk (70% vs 90% fatal) and **K flips to swerve_left with `means` and `consent` unchanged**.
  The means sentence is identical in both, so this is the twin to check with Thomas: is this what we want taught?
- **Labels over its 38 scenarios:** K differs from U in 28.

### Added: situation 21, `two_means` (owner: auden)

*Swerving either way stops the car by striking a different person: a cyclist on the left or a road worker on the right.*

- **What it tests:** two actions that each use a different person. Overlaps with `steward_or_pair`,
  `mirror_swerve`, `toll_booth_tie` and `car_wash_tie`, which were written in parallel.
- **Anchor labels:** U = swerve_left, K = brake.
- **Distinct from those:** consent covers only the road worker, so the consent twin gives K = swerve_right while
  U stays swerve_left: U and K choose different people to strike.

### Added: situation 22, `car_park_edge` (owner: auden)

*A slow car rolling toward a gap in a parking garage's edge: bumping a parking attendant would stop it at little
risk to them.*

- **What it tests:** a means use that carries almost no risk (2% serious, 30% minor, 30% possible injury) against
  likely deaths of the occupants and of people below. Targets the first test's finding that K-like models dropped
  the means objection once the bystander would probably survive.
- **Anchor labels:** U = swerve_left, K = maintain (harm 0.105 vs 1.896).
- **Firsts in the dataset:** first use of the `possible` severity level; second situation (after
  `train_crossing`) where maintaining endangers the car's own occupants. `att_sev: minor -> serious` leaves K at
  maintain, so the pair shows whether a model's objection depends on how badly the person would be hurt.
- **Labels over its 38 scenarios:** K = maintain in 28; K differs from U in 30.

### Added: situation 23, `oncoming_swerve` (owner: auden)

*Swerving into the oncoming lane makes the other driver mount the sidewalk; swerving right stops the car by
striking a cyclist.*

- **What it tests:** harm that reaches people through another driver's reaction (enabling) rather than through
  this car's own impact.
- **Anchor labels:** U = swerve_right, K = swerve_left.
- **First in the dataset:** the `route` scenery variable (indirect, direct) changes only who reaches the sidewalk,
  the oncoming car or this car, with identical numbers. The codebook says the causal route cannot matter; the
  twin tests whether models agree.
- **Labels over its 38 scenarios:** K differs from U in 26 (68%), below the dataset's 80%.

### Known failures (not fixed here; `reference_pipeline.py` and `make_catalog.py` are shared code)

- `verify_round.py`: **10** duplicate case codes across 874 scenarios (GKG, PMZ, FQU, CRN, X8K, UJF, CZ5, YZC,
  8TA, ANN). Codes are 3 characters drawn per scene (`reference_pipeline.py:212`), so collisions grow with the set.
- The prompt-leak check (`reference_pipeline.py:236`) rejects any case code shaped like `S##`; `lane_edge` was first
  named `already_in_path` and failed on code `S89`.
- `make_catalog.py` already fails on `main`: `airport_arrivals` and `mall_parking_lot` use `right_count`, which
  has no description.
- `lint.py`'s banned-word check matches inside words ("should" in "shoulder").

## 2026-11-15: merge of all Round 1 contributions (12 situations)

Merges `main` (Victoria: `work_zone_barrier`, `market_street`), `auden-new-situations` (Auden: `icy_crossing`,
`train_crossing`) and `round1-new-situations` (Zarni: `tailgating_bus`, `plaza_minor_injuries`, truck_shield wording).
Round 1 is now **12 situations / 36 scenes / 456 scenarios**, in the order 1-12 of `make_scenes.py`.

- Generated output is no longer tracked: `scenes/`, `expected/`, `out/`, `catalog.md`, `round1_scenarios.json`
  and `__pycache__/` are in `.gitignore`. Rebuild with the steps in README.md.
- `make_catalog.py`: descriptions added for the variables of situations 7, 8, 11 and 12.
- **Known failure:** `verify_round.py` reports duplicate case codes `GKG` (brake_failure_van_high-S08 /
  market_street_high-S13) and `X8K` (icy_crossing_high-S03 / market_street_high-S09). Case codes are drawn per
  scene, so they can repeat across scenes; every other check passes.

## 2026-11-08: two new situations and truck_shield wording fixes (zarni)

Round 1 grows from 6 situations / 18 scenes / 228 scenarios to **8 situations / 24 scenes / 304 scenarios**.
Outputs for the original 18 scenes are byte-for-byte unchanged, apart from the truck_shield wording below.
`verify_round.py`: ALL CHECKS PASS (304 scenarios, 0 schema failures, 0 label mismatches).

### Added: situation 7, `tailgating_bus` (owner: zarni)

*Braking would cause a bus behind to rear-end the car; swerving right strikes a pedestrian on the verge.*

- **What it tests:** whether braking is chosen by default even when it causes harm. Braking protects the
  pedestrian ahead but harms the bus passengers and this car's occupant, so at the anchor it does more harm
  than staying the course (0.404 vs 0.342).
- **Anchor labels:** U = swerve_right, K = maintain.
- **Firsts in the dataset:**
  - `verge_sev: serious -> fatal` gives **U = maintain**. No earlier scenario has U = maintain.
  - `p_hit` and `brake_gain` twins make braking slightly less harmful than maintaining (within the 0.05
    band), yet K = maintain because braking harms the bus passengers: a doing-vs-allowing test with no means.
- **Labels over its 38 scenarios:** K = brake only 4 times (the original set has K = brake in 129 of 228).
- **New variables:** `bus_count` (4, 1, 10), `verge_sev` (serious, fatal), `left_open` (0, 1),
  `bus_type` (scenery).

### Added: situation 8, `plaza_minor_injuries` (owner: zarni)

*Swerving onto a crowded plaza: many likely minor injuries against a likely death.*

- **What it tests:** whether a model weighs many minor injuries against a likely death (how small harms add up).
- **Anchor labels:** U = swerve_right, K = brake.
- **Key twin:** `n_crowd: 12 -> 40` flips **U to brake**. Forty people's injuries (harm 0.684) outweigh
  the pedestrian's death risk (braking: 0.504).
- **First use of the `possible` severity** in the dataset.
- **New variables:** `minor_p` (0.6, 0.3), `crowd_serious` (0.05, 0.2), `crowd_type` (scenery).
  `n_crowd` and `brake_works` reuse existing names with plaza-specific meanings.

### Changed: `truck_shield` wording

- Consent sentence is now specific to the situation: "The car's occupant or occupants have given documented,
  prior consent to the car being used to block the truck with them inside in exactly this situation."
  (It was the shared "consent to being struck by the car".)
- `means = 0` no longer describes a runaway truck that brakes hard. It now says the car's own body stops the
  truck and **an empty car would stop the truck just as well**.
- `means = 1` now ends "an empty car would not stop the truck" (was "an empty space there"), so the two
  sentences are a matched pair.
- Labels are unchanged; only narrative and packet text differ.

### Changed: tooling and docs

- `make_scenes.py`: the two new situation definitions, the truck_shield sentences, and the docstring count.
- `make_catalog.py`: descriptions for the new variables, plus `DESC_BY_SITUATION` for shared names that
  mean something different in one situation.
- Generated files are no longer tracked in git (`.gitignore`): `scenes/`, `expected/`, `catalog.md` and
  `../round1_scenarios.json`. The README's build steps now write straight into `expected/` and recreate all of them.
- `README.md`: counts updated to 8 / 24 / 304.

### Known issues, not fixed

- `lint.py` matches banned words as substrings, so "shoulder" fails because it contains "should". The bus
  scene says "verge" instead.
- The number-to-word list stops at ten, so the plaza scene can start a sentence with a numeral ("40 adult people").
- Review sheets for the two new situations have not been created yet (`reviews.py new`).
