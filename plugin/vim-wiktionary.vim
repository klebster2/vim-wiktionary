" Title:        Vim For Poets
" Description:  A plugin to help users Define, use, and research words.
" Last Change:  1 April 2023
" Maintainer:   klebster2 <https://github.com/klebster2>

if exists("g:loaded_vim_wiktionary")
    finish
endif
let g:loaded_vim_wiktionary = 1

" Exposes the plugin's functions for use as commands in Vim.
command! -nargs=0 DefineWord call vim_wiktionary#DefineWord()
"if !exists("g:potion_command")
"    let g:potion_command = "potion"
"endif

"function! PotionCompileAndRunFile()
"    silent !clear
"    execute "!" . g:potion_command . " " . bufname("%")
"endfunction

nnoremap <buffer> <localleader>d :call DefineWord()<cr>
