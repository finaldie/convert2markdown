convert2markdown
================

Convert doxygen xml output to markdown format, which will be useful for writing github api wiki.

# How to Install
No need to install it, just clone it is enough.
```
git clone git@github.com:finaldie/convert2markdown.git
```

# How to Use it
## Prepare doxygen config
Take [flibs][1] as an example
```bash
doxygen -s -g

```
Then modify it like [this][2]

## Generate the doxygen xml format output
```bash
doxygen doxy.config
```

## Convert xml to markdown format
```bash
src/xml2markdown.py -f doc/xml/target.xml > out.md
```

[1]: https://github.com/finaldie/final_libs
[2]: 
