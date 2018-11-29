import sublime
import sublime_plugin

def MarkdownToc(self, edit,  maxLevel):
	contents = self.view.substr(sublime.Region(0, self.view.size()))
	lines = contents.splitlines()

	ignoreCount = 2 # Doc name, Toc itself

	lowest_level = 1000

	result = []
	for line in lines:
		level = len(line) - len(line.lstrip("#"))
		if level > 0 and level <=maxLevel:
			if ignoreCount<1:
				if level < lowest_level:
					lowest_level = level

				indent = "    " * (level -1)
				headline = line[level+1:].strip()
				headlineref = headline.lower()
				for s in [" ",":","(",")", "/", "&", "'", "---", "--"]:
					headlineref=headlineref.replace(s, "-")

				txt = indent + "* [" + headline + "](#" + headlineref+ ")"
				result.append(txt)

			ignoreCount = ignoreCount-1

	if len(result)==0:
		sublime.message_dialog("Markdown - Table of Contents:\n\nNo sections found")
	else:
		# sublime.message_dialog("lowest_level:" + str(lowest_level))
		if lowest_level>1:
			for i, _ in enumerate(result):
				result[i] = result[i][2*(lowest_level-1):]

		result = "\n".join(result)

		tocSection = self.view.find("# Table of Contents", 0)
		if tocSection.a<0 :
			sublime.message_dialog("""Markdown - Table of Contents:
No \"# Table of contents\" section found.
Result put in clipboard.""")
			sublime.set_clipboard(result)
		else:
			# Remove existing Toc
			r, c = self.view.rowcol(tocSection.a)
			pt = self.view.text_point(r + 1, 0)
			line_region = self.view.full_line(pt)
			while self.view.substr(line_region).lstrip().startswith("*"):
				self.view.erase(edit, line_region)
				line_region = self.view.full_line(pt)
			# Insert new ToC
			self.view.insert(edit, pt, result + "\n")

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

