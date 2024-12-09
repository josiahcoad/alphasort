# Alphasort

### Problem Statement
Keeping lines (alphabetically) sorted is always a pain. Say we have a long list that we want to maintain alphabetical sorting on (for the sake of readability and maintenance). 


```
animals = [
    "alligator",
    "monkey",
    "zebra",
]
```

Now We want to add “cat” to this list...

Either:
1) dev remembers to insert in correct location (or insert anywhere and then sort)
2) dev forgets and PR reviewers have to leave comment about it (just another thing prolonging PR time)
3) the list falls out of sorting for a while then gets included as a refactor in a PR, adding many lines changed and inflating PR size

### Introducing _Alphasort_

We add macros (directives) and a tool that can parse the files for this and to sort


```
animals = [
    # alphasort: on
    "apple",
    "monkey",
    "zebra",
    # alphasort: off
]
```

And yes, it works on most other files too, including comment deliminators like `//` and more.


### Setup
```shell
pip install alphasort
```

### Usage
```bash
alphasort "./path/**/*.py"
```

Also recommend adding it
- to your IDE on-save commands
- to your pre-commit
- to your CI checks

### P.S.
This is inspired by other such macros like:
```
# fmt: off
mylist = [3, 2, 1]  # Black will not touch this line.
# fmt: on

```

I’m honestly surprised something like this doesn’t exist. But here it is now.

