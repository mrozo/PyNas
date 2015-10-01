import subprocess
import re
from abc import ABCMeta

__author__ = 'm'

_RootPass = None
_remove_caret_return_translation = dict.fromkeys(
    map(ord, '\r'),
    None
)


def set_root_password(password):
    """
    Remember a root password to be used to elevate permissions when required
    :param password: string containing only the password
    """
    global _RootPass
    _RootPass = password


class ShellCmdWrapper(metaclass=ABCMeta):
    """
    Base, abstract class used to simplify creation of command line application
    wrappers
    """

    @staticmethod
    def parse_table(source, columns, field_separator=' \t'):
        """
        Find and parse table in the string. Table has to start with a header and
        end with either an empty line or end of input
        :param source: string containing the table
        :param columns:  list of columns names
        :param field_separator: string containing all possible separators
        :return: list of dictionaries containing parsed data
        """
        #
        # create regexp separator class representation, use it in conduction
        # with table headers definition to create regexp matching table header
        # and find it
        #
        separator_class = '[' + field_separator + ']'
        regexp_src = (separator_class + '+').join(
            columns) + separator_class + '?'
        header_regexp = re.compile(regexp_src)
        header_match = header_regexp.search(source)

        column_separator = re.compile(separator_class + '+')
        table = []
        table_body = source[header_match.end():-1]
        table_body = table_body.strip()

        for row_src in table_body.splitlines():
            row_src = row_src.strip()
            if len(row_src) == 0:
                break

            table_row = column_separator.split(row_src)
            table_row = table_row + ([''] * (len(columns) - len(table_row)))
            row_dict = dict(zip(columns, table_row))
            table.append(row_dict)

        return table

    @staticmethod
    def get_info_field(regexp, infostr):
        result = regexp.search(infostr)
        if result:
            return result.group(1)
        return None

    @staticmethod
    def process_command_output(output):
        """
        Encode escape characters and remove '\r' sequences.
        :param output: the string to be processed
        :return: string containing encoded escape sequences and without '\r'
                 sequences.
        """
        output = output.decode("unicode_escape")
        output = output.translate(
            _remove_caret_return_translation
        )
        return output

    @staticmethod
    def execute_command(
                        command,
                        stdin = None,
                        elevate_permissions=False,
                        ):
        """
        Executes the specified command
        :param command: command to run. Can be either a single string or list of
                        strings to be contacted with an IFS
        :param stdin: either or single string or list of lines to be joined
                      together using '\n'. Will be passed as stdin stream to
                      the command.
        :param elevate_permissions:
        :return: string containing the stdout stream of the command
        """

        stdin_str = str()
        commands_list = list()
        outputs = list()

        if elevate_permissions:
            stdin_str = _RootPass + '\n' + stdin_str
            commands_list = ['sudo', '-S'] + commands_list

        if isinstance(command, str):
            commands_list.append(command)
        else:
            commands_list += command

        if isinstance(stdin, str):
            stdin_str += stdin
        else:
            stdin_str += '\n'.join(stdin) + '\n'

        shell = subprocess.Popen(
            commands_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE
        )

        outputs = shell.communicate(
            bytes(stdin_str, 'utf-8')
        )

        outputs = list(map(
            ShellCmdWrapper.process_command_output,
            outputs
        ))

        return outputs
