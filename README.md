pokerish
========

A toy poker hand evaluator in Python.

This is not meant to be used in production. If you need an optimized evaluator, use [deuces](https://github.com/worldveil/deuces) instead.

Usage
-----

```python
from pokerish import Hand

three_fours = Hand.from_string('4D 4H 4S 7H 8D')
pair_of_threes = Hand.from_string('4D 3D 3S 7H AD')
pair_of_aces = Hand.from_string('4D 3D AS 7H AD')

three_fours > pair_of_aces  # True
three_fours > pair_of_threes  # True
pair_of_aces > pair_of_threes  # True
```

Testing
-------

	$ tox
