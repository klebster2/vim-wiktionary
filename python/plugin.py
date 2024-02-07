# Title:        Vim Wiktionary
# Description:  A plugin to help users Define, Use, and Research words.
# Last Change:  6th February 2024
# Maintainer:   klebster2 <https://github.com/klebster2>
# Imports Python modules to be used by the plugin.
import subprocess
import sys


def install(package: str):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    from wiktionaryparser import WiktionaryParser
except:
    print("Trying to install package: wiktionaryparser")
    install("wiktionaryparser")
    from wiktionaryparser import WiktionaryParser

try:
    import yaml
except:
    print("Trying to install package: PyYAML")
    install("PyYAML")
    import yaml

try:
    import vim  # type:ignore
except Exception as e:
    print(e)
    print("No vim module available outside vim")
    pass


def wiktionary_parse() -> None:
    """
    Description
    -----------
    Return information to vim about the word definitions / etymologies / pronunciations
    """
    wiktionary_parser = WiktionaryParser()
    # TODO: fix this when the user wants to use a different language
    wiktionary_parser.set_default_language(
        vim.eval("g:wiktionary_language")  # type:ignore <= from function arg passing in plugin/wiktionary-vim.vim
    )

    cword = vim.eval("expand('<cword>')")  # type:ignore
    # strip and clean the word
    cword = cword.strip()
    assert isinstance(cword, str)

    word_wiktionary_new = []
    for word in wiktionary_parser.fetch(cword):
        definitions = []
        word_new = {}
        # TODO: add more keys / parsing rules / options
        # and decide whether to limit the number of items returned
        for key in vim.eval("g:wiktionary_keep_keys").split(","):  # type:ignore

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

            elif key == "pronunciations":
                word_new.update({"pronunciations": word["pronunciations"]})

            elif key == "etymology":
                word_new.update({"etymology": word["etymology"]})

        word_wiktionary_new.append(word_new)

    word_wiktionary_yaml = yaml.safe_dump(
        {cword: word_wiktionary_new}, allow_unicode=True, width=4096
    )
    # Attempt a simple text cleanup: remove the (often inconsistent) quotes, which add highlighting, 
    # makin the entries more difficult to read)
    # TODO: understand if syntax highlighting is possible, e.g. bold, italic, etc. and also highlight the `<cword>` itself
    word_wiktionary_yaml_noquotes_nonl_clean = (
        word_wiktionary_yaml.replace("'", "")
        .replace('"', "")
        .replace("\n\n", "\n")
        .replace("...", "…")
    )
    vim.command("echom")  # type:ignore
    [
        vim.command('echom "%s"' % line)  # type:ignore
        for line in word_wiktionary_yaml_noquotes_nonl_clean.split("\n")
    ]
