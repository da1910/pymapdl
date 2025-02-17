import os

from ansys.mapdl.core import __version__
from ansys.mapdl.core.misc import is_float
from ansys.mapdl.core.commands import Commands


def convert_script(filename_in, filename_out, loglevel='WARNING', auto_exit=True,
                   line_ending=None, exec_file=None, macros_as_functions=True,
                   use_function_names=True):
    """Converts an ANSYS input file to a python PyMAPDL script.

    Parameters
    ----------
    filename_in : str
        Filename of the ansys input file to read in.

    filename_out : str
        Filename of the python script to write a translation to.

    loglevel : str, optional
        Logging level of the ansys object within the script.

    auto_exit : bool, optional
        Adds a line to the end of the script to exit MAPDL.  Default
        ``True``.

    line_ending : str, optional
        When None, automatically determined by OS being used.

    macros_as_functions : bool, optional
        Attempt to convert MAPDL macros to python functions.

    use_function_names : bool, optional
        Convert MAPDL functions to ansys.mapdl.core.Mapdl class
        methods.  When ``True``, the MAPDL command "K" will be
        converted to ``mapdl.k``.  When ``False``, it will be
        converted to ``mapdl.run('k')``.

    Returns
    -------
    clines : list
        List of lines translated.

    Examples
    --------
    >>> from ansys.mapdl import core as pymapdl
    >>> from ansys.mapdl.core import examples
    >>> clines = pymapdl.convert_script(examples.vmfiles['vm1'], 'vm1.py')
    """
    translator = FileTranslator(loglevel, line_ending, exec_file=exec_file,
                                macros_as_functions=macros_as_functions,
                                use_function_names=use_function_names)
    with open(filename_in) as file_in:
        for line in file_in.readlines():
            translator.translate_line(line)

    if auto_exit:
        translator.write_exit()
    translator.save(filename_out)
    return translator.lines


class FileTranslator():
    obj_name = 'mapdl'
    indent = ''
    non_interactive = False

    def __init__(self, loglevel='INFO', line_ending=None, exec_file=None,
                 macros_as_functions=True, use_function_names=True):
        self._non_interactive_level = 0
        self.lines = []
        self._functions = []
        if line_ending:
            self.line_ending = line_ending
        else:
            self.line_ending = os.linesep
        self.macros_as_functions = macros_as_functions
        self._infunction = False
        self.use_function_names = use_function_names
        self.comment = ''

        self.write_header()
        self.initialize_mapdl_object(loglevel, exec_file)

        self._valid_commands = dir(Commands)
        self._non_interactive_commands = ['*CRE', '*VWR']

    def write_header(self):
        header = f'"""Script generated by ansys-mapdl-core version {__version__}"""'
        self.lines.append(header)

    def write_exit(self):
        self.lines.append(f'{self.obj_name}.exit()')

    def save(self, filename):
        """ Saves lines to file """
        if os.path.isfile(filename):
            os.remove(filename)

        with open(filename, 'w') as f:
            f.write(self.line_ending.join(self.lines))

    def initialize_mapdl_object(self, loglevel, exec_file):
        """ Initializes ansys object as lines """
        core_module = 'ansys.mapdl.core'  # shouldn't change
        self.lines.append(f'from {core_module} import launch_mapdl')

        if exec_file:
            exec_file_parameter = f'"{exec_file}", '
        else:
            exec_file_parameter = ''
        line = f'{self.obj_name} = launch_mapdl({exec_file_parameter}loglevel="{loglevel}")'
        self.lines.append(line)

    @property
    def line_ending(self):
        return self._line_ending

    @line_ending.setter
    def line_ending(self, line_ending):
        if line_ending not in ['\n', '\r\n']:
            raise ValueError('Line ending must be either "\\n", "\\r\\n"')
        self._line_ending = line_ending

    def translate_line(self, line):
        """Converts a single line from an ANSYS APDL script """
        self.comment = ''
        line = line.strip()
        line = line.replace('"', "'")

        # check if line contains a comment
        if '!' in line:
            if "'!'" in line or '"!"' in line:
                pass
            elif line[0] == '!':  # entire line is a comment
                self.comment = line.replace('!', '').strip()
                self.store_comment()
                return
            else:  # command and in-line comment
                split_line = line.split('!')
                line = split_line[0]
                self.comment = ' '.join(split_line[1:])
                self.comment = self.comment.lstrip()

        if not line:
            return

        if line[:4].upper() == '/COM':
            self.comment = ''.join(line.split(',')[1:]).strip()[1:]
            return self.store_comment()

        if line[:4].upper() == '/TIT':  # /TITLE
            parameters = line.split(',')[1:]
            return self.store_command('title', [''.join(parameters).strip()])

        if line[:4].upper() == 'C***':  # C***
            self.comment = line.split('C***')[1].strip()[1:]
            return self.store_comment()

        if line[:4].upper() == '*GET':
            parameters = line.split(',')[1:]
            return self.store_command('get', parameters)

        if line[:6].upper() == '/PREP7':
            return self.store_command('prep7', [])

        if '*END' in line:
            if self.macros_as_functions:
                self.store_empty_line()
                self.store_empty_line()
                self.indent = self.indent[4:]
                self._infunction = False
                self.end_non_interactive()
                return
            else:
                self.store_run_command(line)
                self.end_non_interactive()
                return

        # check for if statement
        if line[:3].upper() == '*IF' or '*IF' in line.upper():
            self.start_non_interactive()
            self.store_run_command(line)
            return

        # check if line ends non-interactive
        if line[0] == '(':
            if not self.non_interactive:
                print('Possible invalid line:\n%s\n' % line +
                      'This line requires a *VWRITE beforehand')
            self.store_run_command(line)
            self.end_non_interactive()
            return
        elif line[:4] == '*USE' and self.macros_as_functions:
            items = line.split(',')
            func_name = items[1].strip()
            if func_name in self._functions:
                args = ', '.join(items[2:])
                self.lines.append(f'{func_name}({args})')
                return

        # check if a line is setting a variable
        items = line.split(',')
        if '=' in items[0]:  # line sets a variable:
            self.store_run_command(line)
            return

        command = items[0].lower().strip()
        parameters = items[1:]
        if not command:
            self.store_empty_line()
            return

        # check valid command
        if command not in self._valid_commands:
            if line[:4] == '*CRE':  # creating a function
                if self.macros_as_functions:
                    self.start_function(items[1].strip())
                    return
                else:
                    self.start_non_interactive()
            elif line[:4] in self._non_interactive_commands:
                self.start_non_interactive()
            self.store_run_command(line)
        elif self.use_function_names:
            self.store_command(command, parameters)
        else:
            self.store_run_command(line)

    def start_function(self, func_name):
        self._functions.append(func_name)
        self.store_empty_line()
        self.store_empty_line()
        self._infunction = True
        spacing = ' '*(len(func_name) + 5)
        line = 'def %s(%s,' % (func_name, ', '.join(["ARG%d=''" % i for i in range(1, 7)]))
        line += '%s%s,' % (spacing, ', '.join(["ARG%d=''" % i for i in range(7, 13)]))
        line += '%s%s):' % (spacing, ', '.join(["ARG%d=''" % i for i in range(13, 19)]))
        self.lines.append(line)
        self.indent = self.indent + '    '

    def store_run_command(self, command):
        """Stores pyansys.ANSYS command that cannot be broken down
        into a function and parameters.
        """
        if self._infunction and 'ARG' in command:
            args = []
            for i in range(1, 19):
                arg = 'ARG%d' % i
                c = 0
                if arg in command:
                    command = command.replace(arg, '{%d:s}' % c)
                    args.append(arg)
                    c += 1

            line = '%s%s.run("%s".format(%s))' % (self.indent, self.obj_name, command,
                                                  ', '.join(args))

        elif self.comment:
            line = '%s%s.run("%s")  # %s' % (self.indent, self.obj_name, command,
                                             self.comment)
        else:
            line = '%s%s.run("%s")' % (self.indent, self.obj_name, command)
        self.lines.append(line)

    def store_comment(self):
        """Stores a line containing only a comment"""
        line = f'{self.indent}# {self.comment}'
        self.lines.append(line)

    def store_empty_line(self):
        """Stores an empty line"""
        self.lines.append('')

    def store_command(self, function, parameters):
        """Stores a valid pyansys function with parameters"""
        parsed_parameters = []
        for parameter in parameters:
            parameter = parameter.strip()
            if is_float(parameter):
                parsed_parameters.append(parameter)
            elif 'ARG' in parameter and self._infunction:
                parsed_parameters.append('%s' % parameter)
            else:
                parsed_parameters.append('"%s"' % parameter)

        parameter_str = ', '.join(parsed_parameters)
        if self.comment:
            line = '%s%s.%s(%s)  # %s' % (self.indent, self.obj_name, function,
                                          parameter_str, self.comment)
        else:
            line = '%s%s.%s(%s)' % (self.indent, self.obj_name, function,
                                    parameter_str)

        self.lines.append(line)

    def start_non_interactive(self):
        self._non_interactive_level += 1
        if self.non_interactive:
            return
        line = f'{self.indent}with {self.obj_name}.non_interactive:'
        self.lines.append(line)
        self.non_interactive = True
        self.indent = self.indent + '    '

    def end_non_interactive(self):
        self._non_interactive_level -= 1
        if self._non_interactive_level == 0:
            self.non_interactive = False
            self.indent = self.indent[4:]
