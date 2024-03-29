if !has("python3")
  echo "vim has to be compiled with +python3 to run this"
  finish
endif

if exists('g:vim_wiktionary_python_plugin_loaded')
  finish
endif

let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

python3 << EOF
import sys
from os.path import normpath, join
import vim
plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '..', 'python'))
sys.path.insert(0, python_root_dir)
# Works with local path
import plugin
EOF

let g:vim_wiktionary_python_plugin_loaded = 1

" add language, and comma separated keep keys arg

function! WiktionaryEtymology()
  python3 plugin.wiktionary_parse_etymology()
endfunction

function! WiktionaryDefinitions()
  python3 plugin.wiktionary_parse_definitions()
endfunction

function! WiktionaryPronunciations()
  python3 plugin.wiktionary_parse_pronunciations()
endfunction

command! -nargs=0 WiktionaryPronunciations call WiktionaryPronunciations()
command! -nargs=0 WiktionaryDefinitions call WiktionaryDefinitions()
command! -nargs=0 WiktionaryEtymology call WiktionaryEtymology()
