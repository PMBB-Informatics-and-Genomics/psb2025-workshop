#!/usr/bin/env python
x="Hello world!"
for i, word in enumerate(x.split()):
    with open(f"chunk_{i}", "w") as f:
        f.write(word)
