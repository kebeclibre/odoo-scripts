import sublime
import sublime_plugin

import re


class ExampleCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    sel = self.view.sel()
    selected = self.view.substr(sel[0])
    lines = []
    for line in selected.split("\n"):
      l = re.sub(r"^\s*[\"']", "", line)
      l = re.sub(r"^\s*(\+\s*[\"'])?", "", l)
      l = re.sub(r"[\"'](\s*\+)?$", "", l)
      l = re.sub(r'\\"', '"', l)
      l = re.sub(r"\\'", "'", l)
      lines.append(l)

    print(sel)
    print(sel[0])
    self.view.replace(edit, sel[0], "`" + "\n".join(lines) + "`");
