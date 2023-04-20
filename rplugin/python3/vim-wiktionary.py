# Title:        Vim Wiktionary
# Description:  A plugin to help users Define, Use, and Research words.
# Last Change:  12 April 2023
# Maintainer:   klebster2 <https://github.com/klebster2>
# Imports Python modules to be used by the plugin.
from wiktionaryparser import WiktionaryParser
import yaml

import pynvim
from pynvim import Nvim

parser = WiktionaryParser()


@pynvim.plugin
class VimWiktionaryPlugin(object):
    def __init__(self, nvim: Nvim):
        self.nvim = nvim
        # self.nvim.vars['vim_wiktionary_plugin_sid'] = self.nvim.eval('scriptlocalvariable(v:servername . "_plugin")')

    @pynvim.command("WiktionaryParser", nargs="*", range="")
    def parse(self, args, range):
        """
        Idea
        Keep it simple, just create a new window that has the word defs / ety
        scraped from wiktionary
        """
        parser = WiktionaryParser()
        assert (
            len(args) >= 1
        ), "Error, args should include language and keys the user wishes to index on"

        # 0th list element is the language
        parser.set_default_language(args[0])

        cword = self.nvim.eval("expand('<cword>')")
        assert isinstance(cword, str)
        word_wiktionary = parser.fetch(cword)
        self.nvim.command('echo "%s"' % ", ".join(args))

        word_wiktionary_new = []
        for word in word_wiktionary:
            definitions = []
            word_new = {}
            for key in args:
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
        self.nvim.command("new")
        self.nvim.command(
            "setlocal wrap nonumber norelativenumber nolist wrap linebreak breakat&vim noswapfile bufhidden=hide buftype=nofile foldmethod=indent syntax=yaml"
        )
        word_wiktionary_yaml_noquotes_nonl_clean_newlinesplit = \
            word_wiktionary_yaml_noquotes_nonl_clean.split("\n")
        self.nvim.current.buffer[:] = [
            l
            for l in word_wiktionary_yaml_noquotes_nonl_clean_newlinesplit
            if isinstance(l, str)
        ]
        # TODO: use self.vim.eval("winwidth({nr})") to get window width,
        # and calculate number of lines
        # The below is a guestimate
        self.nvim.command(f"resize {len(word_wiktionary_yaml_noquotes_nonl_clean_newlinesplit)+5}")

        # [
        #    self.nvim.command("echom '%s'" % line) for line in
        #    word_wiktionary_yaml_noquotes_nonl_clean.split("\n") if line != None or line != ""
        # ]
        # self.nvim.command("messages")

plugin = VimWiktionaryPlugin(Nvim)
