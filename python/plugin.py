# Title:        Vim Wiktionary
# Description:  A plugin to help users Define, Use, and Research words.
# Last Change:  6th February 2024
# Maintainer:   klebster2 <https://github.com/klebster2>
# Imports Python modules to be used by the plugin.
import subprocess
import sys
import typing as t


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
    print("Trying to install package: yaml")
    install("yaml")
    import yaml

try:
    import vim  # type:ignore
except Exception as e:
    print(e)
    print("No vim module available outside vim")
    pass

# Change this if you want to use a different language
DEFAULT_LANGUAGE = "english"

# Change this if you want to include more / different keys
DEFAULT_KEYS = "definitions,pronunciations,etymology"


def wiktionary_parse(
    language: t.Optional[str] = DEFAULT_LANGUAGE, keep_keys: str = DEFAULT_KEYS
) -> None:
    """
    Description
    -----------
    Return information to vim about the word definitions / etymologies / pronunciations
    """
    parser = WiktionaryParser()
    # TODO: fix this when the user wants to use a different language
    parser.set_default_language(
        language
    )

    cword = vim.eval("expand('<cword>')")  # type:ignore
    # strip and clean the word
    cword = cword.strip()
    assert isinstance(cword, str)

    word_wiktionary = parser.fetch(cword)

    word_wiktionary_new = []
    for word in word_wiktionary:
        definitions = []
        word_new = {}
        # TODO: add more keys / parsing rules / options
        # and decide whether to limit the number of items returned
        for key in keep_keys.split(","):

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
    # TODO: understand if we can highlight syntax ( e.g. bold, italic, etc)
    #       and also highlight the cword itself
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
