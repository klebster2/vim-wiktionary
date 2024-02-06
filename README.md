# vim-wiktionary

## Description

Aim: Deliver Wiktionary within Vim (to look up etymologies, word definitions, and pronunciations, etc.)

## How to use

1. Run the following command within your python3 neovim environment

```bash
python -m pip install wiktionaryparser PyYAML
```

Note that it remains to be figured out exactly what this translates to in terms of a subcommand for packer, plug, etc.

Also, do not worry if you _don't_ do this, as the script is configured to run a subprocess to install those packages if you don't.

2. Next run: `:WiktionaryParser` which will attempt to send the `<cword>` to Wiktionary.

Note that the `<cword>` is the word under the cursor in your vim editor.

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
:Wiktionary
```

Should yield something like:

```text
bonjour:
- etymology: Inherited from Middle French bonjour, from Old French bon jor (literally “good day”). By surface analysis, bon (“good”) +<200e> jour (“day”).
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
          vim.g.wiktionary_keep_keys = 'etymology,definitions'
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
