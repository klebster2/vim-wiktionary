# vim-wiktionary

## Description

Use Wiktionary within Vim (To look up etymologies, word definitions, and pronunciations, etc.)

## How to use

1. Run the following command within your python3 neovim environment

```bash
python -m pip install wiktionaryparser PyYAML
```

Note - I still need to figure out exactly what this translates to in terms of packer, plug, etc.

(do not worry if you _don't_ do this, as the script is configured to run a subprocess to install those packages if you don't)

2. Next run: `:WiktionaryParser` which will attempt to send the `<cword>` to Wiktionary.

Note that the `<cword>` is the word under the cursor in your vim editor.

Currently, a new window is brought up with a `YAML` format of the Wiktionary query.

# Setting Wiktionary Language:

After installing using Plug, or Packer, or your default vim package manager, run one of the following:

## Vimscript command (Classic Vim)

E.g. Setting the language to Portuguese

```vim
let g:wiktionary_language = 'portuguese'
```

## Neovim command

```
lua vim.api.nvim_exec([[ let g:wiktionary_language = 'portuguese' ]], true)
```

hence you could set the following somewhere

```lua
vim.api.nvim_exec([[ let g:wiktionary_language = 'portuguese' ]], true)
```

# Setting the Keys returned from wiktionary

Wiktionary can return a lot of data for a single word.
It is for this reason that limiting the keys returned can be a good idea.

## Vimscript command (Classic Vim)

```vim
let g:wiktionary_keys = 'etymology,pronunciations'
let g:wiktionary_keys = 'etymology'
" etc
```

## Neovim Command

```
lua vim.api.nvim_exec([[ let g:wiktionary_keys = 'etymology' ]], true)
```

Since a user may be utilizing wiktionary for a specific purpose, one can set the keys like the following

```lua
vim.api.nvim_exec([[ let g:wiktionary_keys = 'etymology' ]], true)
```

# Contributing

Simply open an Issue or a Pull Request

# TODO:

Customize user language
Customize parsing options e.g. definitions, pronunciations, etymology
Add color to words of interest / color code keys using simple YAML parser

