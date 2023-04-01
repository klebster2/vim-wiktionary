" Title:        Vim For Poets
" Description:  A plugin to help users Define, use, and research words.
" Last Change:  1 April 2023
" Maintainer:   klebster2 <https://github.com/klebster2>

if exists("g:loaded_example-plugin")
    finish
endif
let g:loaded_example-plugin = 1

" Exposes the plugin's functions for use as commands in Vim.
command! -nargs=0 DefineWord call example-plugin#DefineWord()
