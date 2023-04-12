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

    @pynvim.command("WiktionaryParser", nargs=1, sync=True)
    def parse(self, language):
        """
        Idea
        Keep it simple, just create a new window that has the word defs / ety
        scraped from wiktionary
        """
        parser = WiktionaryParser()

        parser.set_default_language(language[0])

        cword = self.nvim.eval("expand('<cword>')")
        assert isinstance(cword, str)
        word_wiktionary = parser.fetch(cword)

        word_wiktionary_yaml = yaml.safe_dump(
            word_wiktionary, allow_unicode=True, width=4096
        )

        # remove quotes (they are often inconsistent)
        word_wiktionary_yaml_noquotes_nonl = (
            word_wiktionary_yaml.replace("'", "").replace('"', "").replace("\n\n", "\n")
        )
        self.nvim.command("new")
        self.nvim.command("set syntax=yaml")
        self.nvim.command("set wrap")
        self.nvim.command("set ma")
        self.nvim.current.buffer[:] = [
            l
            for l in word_wiktionary_yaml_noquotes_nonl.split("\n")
            if isinstance(l, str)
        ]
        self.nvim.command("set ro")
        self.nvim.command("set noma")
        self.nvim.command("nnoremap <silent> q q!")
