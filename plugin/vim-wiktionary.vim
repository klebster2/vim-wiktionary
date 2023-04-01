" Title:        Vim Wiktionary
" Description:  A plugin to help users Define, Use, and Research words.
" Last Change:  1 April 2023
" Maintainer:   klebster2 <https://github.com/klebster2>

if exists("g:loaded_wiktionary")
    finish
endif
let g:loaded_wiktionary = 1

" Calls the Python 3 function.
function! WikiDefineWord()
    let cursorWord = expand('<cword>')
python3 << EOF
# Imports Python modules to be used by the plugin.
import vim
import json
import requests
import re

html_tag_pattern = re.compile('<.*?>')

# Sets up variables for the HTTP requests the
# plugin makes to fetch word definitions from
# the Wiktionary dictionary.
request_headers = { "accept": "application/json" }
request_base_url = "https://en.wiktionary.org/api/rest_v1/page/definition/"
request_url_options = "?redirect=true"

# Fetches available definitions for a given word.
word_defs=[]
response = requests.get(request_base_url + vim.eval('cursorWord') + request_url_options, headers=request_headers)

if not (response.status_code != 200):

    definition_json = json.loads(response.text)

    for definition_item in definition_json["en"]:
        pos=definition_item["partOfSpeech"]

        for definition in definition_item["definitions"]:
            definitions.append(re.sub(html_tag_pattern, "", definition["definition"]))

        word_defs.append({"pos": definitions})

    vim.command("let sWikiDefinitionJson = '%s'" % json.dumps(word_defs))
EOF

    let l:data = json_decode(join(sWikiDefinitionJson))
    for m in l:data
    "
    " Check if it matches what we're trying to complete; in this case we
    " want to match against the start of both the first and second list
    " entries (i.e. the name and email address)
    " forq this dict.
        call add(l:res, {
            \ 'icase': 1,
            \ 'word': l:m['neighbor'],
            \ 'info': l:m['score'],
        \ })
    endfor

    " Now say the complete() function
    call complete(l:start + 1, l:res)
    return ''
endfunction

" Exposes the plugin's functions for use as commands in Vim.
inoremap <silent> <Plug>WikiDefineWord <C-R>=<SID>WikiDefineWord()<CR>
