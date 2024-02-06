if !has("python3")
  echo "vim has to be compiled with +python3 to run this"
  finish
endif

if exists('g:vim_wiktionary_python_plugin_loaded')
  finish
endif

let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')


let g:vim_wiktionary_python_plugin_loaded = 1

function! Wiktionary(...)
  " add language, and comma separated keep keys arg
  let language = a:0 > 0 ? a:1 : 'english'
  let keys = a:0 > 1 ? a:2 : 'definitions,pronunciations,etymology'
  " Pass the arguments to Python
  python3 << EOF
import sys
from os.path import normpath, join
import vim
plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '..', 'python'))
sys.path.insert(0, python_root_dir)
# Works with local path
import vim
import plugin
# Your Python code here using language and keys
EOF
endfunction

command! -nargs=1 Wiktionary call Wiktionary(<f-args>)
