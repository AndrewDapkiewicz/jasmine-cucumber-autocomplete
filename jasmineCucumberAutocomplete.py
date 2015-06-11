import sublime, sublime_plugin

class JasminecucumberautocompleteCommand(sublime_plugin.EventListener):
  def on_query_completions(self, view, prefix, locations):
    popup_options = []

    test_specs = self.get_strings(view)
    for type in ['given', 'when', 'then']:
      for spec in test_specs[type]:
        display_value = type+'-'+spec['display']
        output_value = type+"('"+spec['replace']+"')";
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

            test_spec = self.parse_test_string(line_text)
            if line_text.find('.given(') >= 0:
              givens.append(test_spec)
            elif line_text.find('.when(') >= 0:
              whens.append(test_spec)
            elif line_text.find('.then(') >= 0:
              thens.append(test_spec)

    return {
      'given': givens,
      'when': whens,
      'then': thens
    }

  def parse_test_string(self, line):
    start_index = line.find("'") if line.find("'") >= 0 else line.find('"')
    end_index = line.rfind("'") if line.rfind("'") >= 0 else line.rfind('"')

    test_phrase = line[start_index+1:end_index]

    # split on variables
    variable_split = test_phrase.split('(.*)')

    # get function parameter names
    function_index = line.rfind('function(')
    function_end_index = line.rfind(')')
    function_params = line[function_index+9:function_end_index].split(',')
    param_length = len(function_params)

    # we have variables
    split_length = len(variable_split)
    while split_length > 1:
      if param_length > 0:
        variable_string = "${"+str(param_length)+":"+function_params[param_length-1].strip()+"}"
        param_length -= 1

      variable_split[split_length - 2] = variable_split[split_length - 2] + variable_string + variable_split[split_length - 1]
      variable_split.pop()
      split_length -= 1

    replace_value = variable_split[0]

    return {
      'display': test_phrase,
      'replace': replace_value
    }
