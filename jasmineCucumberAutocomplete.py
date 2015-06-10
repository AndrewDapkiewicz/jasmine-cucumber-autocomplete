import sublime, sublime_plugin

class JasminecucumberautocompleteCommand(sublime_plugin.EventListener):
  def on_query_completions(self, view, prefix, locations):
    popup_options = []

    test_strings = self.get_strings(view)
    for type in ['given', 'when', 'then']:
      for string in test_strings[type]:
        display_value = type+'-'+string
        output_value = type+"('"+string+"')";
        popup_options.append((display_value, output_value))

    return popup_options

  def get_strings(self, view):
    givens = []
    whens = []
    thens = []

    file_name = view.file_name()
    if file_name.find('.specs') >= 0:
      search_file_name = file_name.replace('.specs.js', '.steps.js')
      active_views = sublime.active_window().views()
      for view in active_views:
        if view.file_name() == search_file_name:
          all_content = sublime.Region(0, view.size())
          lines = view.split_by_newlines(all_content)
          for line in lines:
            line_text = view.substr(line)

            if line_text.find('.given(') >= 0:
              givens.append(self.parse_test_string(line_text))
            elif line_text.find('.when(') >= 0:
              whens.append(self.parse_test_string(line_text))
            elif line_text.find('.then(') >= 0:
              thens.append(self.parse_test_string(line_text))

    return {
      'given': givens,
      'when': whens,
      'then': thens
    }

  def parse_test_string(self, line):
    startIndex = line.find("'") if line.find("'") >= 0 else line.find('"')
    endIndex = line.rfind("'") if line.rfind("'") >= 0 else line.rfind('"')

    return line[startIndex+1:endIndex]
