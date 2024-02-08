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


def format_output(word_wiktionary_filtered) -> None:
    word_wiktionary_yaml = yaml.safe_dump(
        word_wiktionary_filtered, allow_unicode=True, width=4096
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

def query_wiktionary() -> WiktionaryParser:
    wiktionary_parser = WiktionaryParser()

    wiktionary_parser.set_default_language(
        vim.eval("g:wiktionary_language")  # type:ignore <= from function arg passing in plugin/wiktionary-vim.vim
    )
    cword = vim.eval("expand('<cword>')")  # type:ignore
    # Strip and clean the word
    cword = cword.strip()
    assert isinstance(cword, str)
    return wiktionary_parser.fetch(cword)


def wiktionary_parse_pronunciation() -> None:
    """
    Description
    -----------
    Return information to vim about the word pronunciation
    """
    word_wiktionary_new = []
    for word in query_wiktionary():
        word_new = {}
        word_new.update({"pronunciations": word["pronunciations"]})

        word_wiktionary_new.append(word_new)

    format_output(word_wiktionary_filtered=word_wiktionary_new)


def wiktionary_parse_etymology() -> None:
    """
    Description
    -----------
    Return information to vim about the word etymology
    """
    word_wiktionary_new = []
    for word in query_wiktionary():
        word_new = {}
        word_new.update({"etymology": word["etymology"]})

        word_wiktionary_new.append(word_new)

    format_output(word_wiktionary_filtered=word_wiktionary_new)


def wiktionary_parse_definitions() -> None:
    """
    Description
    -----------
    Return information to vim about the word definitions
    """
    word_wiktionary_new = []
    for word in query_wiktionary():
        definitions = []
        word_new = {}
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
        word_wiktionary_new.append(word_new)

    format_output(word_wiktionary_filtered=word_wiktionary_new)
