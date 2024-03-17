# vim-wiktionary

## Description

Deliver Wiktionary within Vim so that users can look up etymologies, word definitions, and pronunciations, etc.

## How to use

1. Ensure you have Python installed - the script is configured to run a subprocess to install the following packages.
 - wiktionaryparser
 - PyYAML

2. Next run: `:WiktionaryEtymology` over the current cursor word (`cword`). This will attempt to send the `<cword>` to Wiktionary.

Currently, a new window is brought up with a `YAML` format of the Wiktionary query.

# Setting Wiktionary Language:

After installing using Plug, or Packer, or your default vim package manager, run one of the following:

## Vim Command (VimScript)

```vim
let g:wiktionary_language = 'german'
```

You can add the following to your vimrc, init.vim or init.lua file:

## Neovim Command (Lua)

```lua
vim.g.wiktionary_keep_keys = 'etymology'
vim.g.wiktionary_language = 'french'
```

Then when running, you should be able to get etymology for French language words:

E.g. running the below for “bonjour”:

```
:WiktionaryEtymology
```

Should yield something like:

```text
bonjour:
- etymology: Inherited from Middle French bonjour, from Old French bon jor (literally “good day”). By surface analysis, bon (“good”) + jour (“day”).
```

## Setup with packer

You can also setup directly from within packer:

```lua
local use = require("packer").use
require("packer").startup(function()
    use {
      "klebster2/vim-wiktionary",
        config = function()
          vim.g.wiktionary_language = 'english'
        end
    }
end)
```

## Setup with Plug

TODO

## Setup with Vundle

TODO

# Contributing

Simply open an Issue or a Pull Request.

# TODO:

* Make the options more fine grained in terms of definitions, pronunciations, and etymology.
** Make output kinder (there are some fields that are absolutely massive)
* Add custom vim keymap examples.
* Consider passing Args directly to the Wiktionary function.
* Consider adding color to words of interest / color code keys using simple YAML parser / syntax highlighter.
