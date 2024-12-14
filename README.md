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
1) dev remembers to insert in correct location
2) dev forgets and PR reviewers have to leave comment about it (just another thing prolonging PR time)
3) the list falls out of sorting for a while then gets included as a refactor in a PR, adding many lines changed which inflates PR size and leads to unnecessary merge conflicts

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
It even works with json if you do `"_comment": "alphasort: on"`


### Setup
```shell
pip install alphasort
```

### Usage
```bash
alphasort
```

You can also pass arguments to select a path (with glob) and ignore a path.

### Automating
Also recommend adding it
- to your IDE on-save commands
- to your pre-commit
- to your CI checks

(psss. check out the github repo to see how we've done all 3 of these to run alphasort on `alphasort`)

### Argcomplete
This project is equiped with argcomplete which you can enable via running:

`eval "$(register-python-argcomplete alphasort)"`


### P.S.
This is inspired by other such macros like:
```
# fmt: off
mylist = [3, 2, 1]  # Black will not touch this line.
# fmt: on
```

I’m honestly surprised something like this doesn’t exist. But here it is now. So, you're welcome 😁

Feel free to contribute if you'd like to see any additional features! 🎉
