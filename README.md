# mksync

MkSync replaces directives in a Markdown file with corresponding content. It's a useful tool to add nice
features to your project's `README.md` file, such as a table of contents, without the manual upkeep.

<!-- table of contents -->
  * [Example](#example)
  * [Available Directives](#available-directives)
  * [Synopsis](#synopsis)
* [Changelog](#changelog)
  * [0.1.3 (2023-06-29)](#013-2023-06-29)
<!-- end table of contents -->

## Example

Say this is your `README.md`:

```md
# My Project

<!-- toc -->

## Installation

## Documentation
```

Then running `mksync README.md` will update the file in-place to:

```md
# My Project

<!-- toc -->
* [Installation](#installation)
* [Documentation](#documentation)
<!-- end toc -->

## Installation

## Documentation
```

## Available Directives

* `toc` or `table of contents`: Produce an unordered list of links to all headers in the document after the directive.
* `include <path>`: Include the contents of the file at the given path. You can optionally specify a language name to
  wrap the content in a code block, e.g. `include code:python <path>`.
* `runcmd <command>`: Run the given command and include the output in the document. You can optionally specify a
  language name to wrap the output in a code block, e.g. `runcmd code:python <command>`.

## Synopsis

<!-- runcmd code: mksync --help -->
```
usage: mksync [-h] [--inplace] [--verbose] file

MkSync is a utility to update Markdown files in-place to automate some common upkeep tasks, such as inling
example code and updating table of contents.

positional arguments:
  file           the file to process

options:
  -h, --help     show this help message and exit
  --inplace, -i  update the file in-place
  --verbose, -v  enable verbose logging
```
<!-- end runcmd -->

---

# Changelog

<!-- runcmd slap changelog format --all --markdown -->
## 0.1.3 (2023-06-29)

<table><tr><th>Type</th><th>Description</th><th>PR</th><th>Issues</th><th>Author</th></tr>
  <tr><td>Fix</td><td>

Fix parsing of `include` directives</td><td></td><td></td><td>@NiklasRosenstein</td></tr>
</table>
<!-- end runcmd -->
