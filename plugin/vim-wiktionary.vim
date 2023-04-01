" Title:        Vim For Poets
" Description:  A plugin to help users Define, use, and research words.
" Last Change:  1 April 2023
" Maintainer:   klebster2 <https://github.com/klebster2>

if exists("g:loaded_wiktionary")
    finish
endif
let g:loaded_wiktionary = 1

python3 << EOF
# Imports Python modules to be used by the plugin.
import vim
import json, requests

# Sets up variables for the HTTP requests the
# plugin makes to fetch word definitions from
# the Wiktionary dictionary.
request_headers = { "accept": "application/json" }
request_base_url = "https://en.wiktionary.org/api/rest_v1/page/definition/"
request_url_options = "?redirect=true"

# Fetches available definitions for a given word.
def get_word_definitions(word_to_define):
    response = requests.get(request_base_url + word_to_define + request_url_options, headers=request_headers)

    if (response.status_code != 200):
        print(response.status_code + ": " + response.reason)
        return

    definition_json = json.loads(response.text)

    for definition_item in definition_json["en"]:
        print(definition_item["partOfSpeech"])

        for definition in definition_item["definitions"]:
            print(" - " + definition["definition"])
EOF

" Calls the Python 3 function.
function! s:WikiDefineWord()
    let cursorWord = "test" "expand('<cword>')
    python3 get_word_definitions(vim.eval('cursorWord'))
endfunction


" Exposes the plugin's functions for use as commands in Vim.
nnoremap <silent> <Plug>WikiDefineWord :<C-U>call <SID>WikiDefineWord()<CR>
nnoremap <buffer> <localleader>d WikiDefineWord<cr>
call s:WikiDefineWord()

