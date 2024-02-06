if !has("python3")
  echo "vim has to be compiled with +python3 to run this"
  finish
endif

if exists('g:vim_wiktionary_python_plugin_loaded')
  finish
endif

let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

python3 << EOF
import subprocess

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    from wiktionaryparser import WiktionaryParser
except:
    print("Trying to install package: wiktionaryparser")
    install('wiktionaryparser')
    from wiktionaryparser import WiktionaryParser

try:
    import yaml
except:
    print("Trying to install package: PyYAML")
    install('PyYAML')
    import yaml

try:
    import vim
except Exception as e:
    print(e)
    print("No vim module available outside vim")
    pass

# Change this if you want to use a different language
DEFAULT_LANGUAGE="en"

def wiktionary_parse():
    """
    Idea
    Keep it simple, just create a new window that has the word defs / ety
    scraped from wiktionary
    """
    parser = WiktionaryParser()
    # TODO: fix this when the user wants to use a different language
    parser.set_default_language(DEFAULT_LANGUAGE)

    cword = vim.eval("expand('<cword>')")
    assert isinstance(cword, str)

    word_wiktionary = parser.fetch(cword)
    #vim.command('echo "%s"' % ", ".join(args))

    word_wiktionary_new = []
    for word in word_wiktionary:
        definitions = []
        word_new = {}
        for key in ("definitions", "pronunciations", "etymology"):
            if key == "definitions":
                for definition in word["definitions"]:
                    if definition.get("relatedWords"):
                        related_words_new = []
                        for related_word in definition["relatedWords"]:
                            related_word_new = related_word
                            related_word_new.update(
                                {"words": ", ".join(related_word["words"])}
                            )
                            related_words_new.append(related_word)
                        definition.update({"relatedWords": related_words_new})
                    definitions.append(definition)
                word_new.update({"definitions": definitions})
            #elif key == "pronunciations":
            #    word_new.update({"pronunciations": word["pronunciations"]})
            elif key == "etymology":
                word_new.update({"etymology": word["etymology"]})

        word_wiktionary_new.append(word_new)

    word_wiktionary_yaml = yaml.safe_dump(
        {cword: word_wiktionary_new}, allow_unicode=True, width=4096
    )

    # Attempt a simple text cleanup.
    # Remove quotes (they are often inconsistent and they add highlighting that make
    # the entries more difficult to read)
    word_wiktionary_yaml_noquotes_nonl_clean = (
        word_wiktionary_yaml.replace("'", "")
        .replace('"', "")
        .replace("\n\n", "\n")
        .replace("...", "…")
    )
    vim.command("new")   # type: ignore
    vim.command( # type: ignore
        "setlocal wrap nonumber norelativenumber nolist wrap linebreak breakat&vim noswapfile bufhidden=hide buftype=nofile foldmethod=indent syntax=yaml"
    )
    word_wiktionary_yaml_noquotes_nonl_clean_newlinesplit = \
        word_wiktionary_yaml_noquotes_nonl_clean.split("\n")
    vim.current.buffer[:] = [  # type: ignore
        l
        for l in word_wiktionary_yaml_noquotes_nonl_clean_newlinesplit
        if isinstance(l, str)
    ]
    # TODO: use vim.eval("winwidth({nr})") to get window width,

    # and calculate number of lines
    # The below is a guestimate
    vim.command(f"resize {len(word_wiktionary_yaml_noquotes_nonl_clean_newlinesplit)+5}")

    # [
    #    self.nvim.command("echom '%s'" % line) for line in
    #    word_wiktionary_yaml_noquotes_nonl_clean.split("\n") if line != None or line != ""
    # ]
    # self.nvim.command("messages")
EOF

let g:vim_wiktionary_python_plugin_loaded = 1

function! WiktionaryEtymology()
  python3 wiktionary_parse()
endfunction

command! -nargs=0 WiktionaryEtymology call WiktionaryEtymology()
