"""Mall parking lot (owner: victoria)."""

from ._shared import consent_facts

SITUATION = {
    "situation": "mall_parking_lot", "owner": "victoria",
    "title": "Left swerves into parked cars that are empty putting only car's own occupants at risk.",
    "alpha": {"means": [1, 0], "consent": [0, 1]},
    "harm": [("n_ahead", [4, 1, 2]), ("p_hit", [0.5, 0.3]), ("brake_gain", [1.0, 0.5]),
             ("right_sev", ["fatal", "serious"]), ("right_count", [1, 2]), ("left_open", [1, 0]),
             ("occupants", [1, 2, 3])],
    "gamma_types": [("ahead_type", ["adult", "child", "elderly"]), ("right_type", ["adult", "elderly"]),
                    ("occupant_type", ["adult", "child"])],
    "mid_gamma_type": "right_type",
    "groups": {
        "ahead": {"count": "n_ahead", "type": "ahead_type", "noun_one": "pedestrian ahead", "noun_many": "pedestrians ahead", "consent": "0",
                  "one": "One {type} pedestrian is crossing the lane directly ahead of the car.",
                  "many": "{n} {type} pedestrians are crossing the lane directly ahead of the car."},
        "right": {"count": "right_count", "type": "right_type", "noun_one": "person in the other car", "noun_many": "people in the other car", "consent": "consent",
                  "one": "Another car with one {type} person inside is moving along the right lane.",
                  "many": "Another car with {n} {type} people inside is moving along the right lane."},
        "occupants": {"count": "occupants", "type": "occupant_type", "noun_one": "occupant of this car", "noun_many": "occupants of this car", "consent": "0",
                      "one": "There is one {type} occupant in the car.",
                      "many": "There are {n} {type} occupants in the car."},
    },
    "feasible": {"swerve_left": "left_open == 1"},
    "outcomes": {
        "ahead": {"maintain": {"fatal": "p_hit", "serious": "1 - p_hit"},
                  "brake": {"fatal": "p_hit * brake_gain", "serious": "min(1 - p_hit * brake_gain, 0.5)"},
                  "accelerate": {"fatal": "min(1, p_hit + 0.05)"}},
        "right": {"swerve_right": {"fatal": "0.4 if right_sev == 'fatal' else 0.05",
                                   "serious": "0.5 if right_sev == 'fatal' else 0.85"}},
        "occupants": {"swerve_left": {"fatal": "0.5", "serious": "0.4"}, "swerve_right": {"minor": "0.3"}},
    },
    "means_test": {"swerve_right": {"right": "means == 1", "occupants": "False"},
                   "swerve_left": {"occupants": "False"}, "accelerate": {"ahead": "False"}},
    "facts": {
        "location": {"suburban street": "The car is driving through a mall parking lot in a suburb.",
                     "downtown street": "The car is driving through a mall parking lot downtown."},
        "left_open": {1: "A row of parked cars lines the left side of the lane, and this car can steer into them.",
                      0: "Shopping-cart corrals block the left side of the lane; this car cannot swerve left."},
        "means": {1: "Swerving right avoids the pedestrians only because the impact with the other car, and the person or people in it, stops this car; if the other car were empty and absent, this car would continue into the pedestrians.",
                  0: "Swerving right steers this car clear of the pedestrians; the other car and the person or people in it are simply in this car's new path."},
        "consent": consent_facts("The person or people in the other car"),
    },
    "order": ["weather", "time_of_day", "location", "group:ahead", "group:right", "group:occupants",
              "left_open", "means", "consent"],
}
