# Title:        Vim Wiktionary
# Description:  A plugin to help users Define, Use, and Research words.
# Last Change:  12 April 2023
# Maintainer:   klebster2 <https://github.com/klebster2>
# Imports Python modules to be used by the plugin.
import subprocess
import sys
import json


def install(package):
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
    print("Trying to install package: yaml")
    install("yaml")
    import yaml

try:
    import vim
except Exception as e:
    print(e)
    print("No vim module available outside vim")
    pass

# Change this if you want to use a different language
DEFAULT_LANGUAGE = "english"


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
    # strip and clean the word
    cword = cword.strip()
    assert isinstance(cword, str)

    word_wiktionary = parser.fetch(cword)

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
            elif key == "pronunciations":
               word_new.update({"pronunciations": word["pronunciations"]})
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
    [vim.command('echom "%s"' % line) for line in word_wiktionary_yaml_noquotes_nonl_clean.split("\n")]  #type:ignore
