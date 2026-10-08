# Validation

Run from `generalized/`:

`python -m unittest -v test_schedule_gate.py`

Run from `validation/`:

`python -m unittest -v test_original_characterization.py`

The preserved-source characterization has 3 assertions. The generalized suite has 9 tests covering grammar, ambiguity rejection, timezone validation, grace boundaries, future timestamps, naive datetime rejection, once-per-slot daily/weekly behavior and a daylight-saving transition.
