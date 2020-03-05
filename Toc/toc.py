import sublime
import sublime_plugin
import re

def MarkdownToc(self, edit,  maxLevel):
	lines = self.view.substr(sublime.Region(0, self.view.size())).splitlines()
	ignoreCount = 2 # Doc name, Toc itself
	indentSize = 4
	lowest_level = 1000

	headlines = []
	for line in lines:
		if not line.startswith("#"):
			continue

		if ignoreCount>0:
			ignoreCount-=1
			continue

		level = line.count('#')
		if level == 0 or level>maxLevel:
			continue

		headline = line[level+1:].strip()
		ref = headline.lower().replace(" ", "-")
		ref = re.sub(r'[^_a-zA-Z0-9-]', "", ref)
		headlines.append((level, "* [{}](#{})".format(headline,ref)))
		if level < lowest_level:
			lowest_level = level

	if len(headlines)==0:
		sublime.message_dialog("Markdown - Table of Contents:\n\nNo sections found")
		return

	toc=''
	for h in headlines:
		indent = " "*indentSize*(h[0] - lowest_level)
		toc+=indent+h[1]+"\n"

	tocHeader = "# Table of Contents"
	tocSection = self.view.find(tocHeader, 0)
	if tocSection.a<0 :
		sublime.message_dialog("""Markdown - Table of Contents:
No \"{}\" section found.
Result put in clipboard.""".format(tocHeader))
		sublime.set_clipboard(toc)
	else:
		# Remove existing Toc
		r, c = self.view.rowcol(tocSection.a)
		pt = self.view.text_point(r + 1, 0)
		line_region = self.view.full_line(pt)
		while self.view.substr(line_region).lstrip().startswith("*"):
			self.view.erase(edit, line_region)
			line_region = self.view.full_line(pt)
		# Insert new ToC
		self.view.insert(edit, pt, toc)

#----------------------------------------
# Commands
#----------------------------------------
class MarkdownTocAboutCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		sublime.message_dialog("""Markdown - Table of Contents.:
Scans file (typically .md file) and populates Table of Contents section.

If no such section is found, result is placed in clipboard.

First two headlines are ignored, as they are considered the
document name and the ToC itself.""")

class MarkdownToc2Command(sublime_plugin.TextCommand):
	def run(self, edit):
		MarkdownToc(self, edit,  2)

class MarkdownToc3Command(sublime_plugin.TextCommand):
	def run(self, edit):
		MarkdownToc(self, edit,  3)

class MarkdownToc4Command(sublime_plugin.TextCommand):
	def run(self, edit):
		MarkdownToc(self, edit,  4)

class MarkdownToc5Command(sublime_plugin.TextCommand):
	def run(self, edit):
		MarkdownToc(self, edit,  5)

class MarkdownToc6Command(sublime_plugin.TextCommand):
	def run(self, edit):
		MarkdownToc(self, edit,  6)
