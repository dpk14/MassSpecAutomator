class CommandList:

    def __init__(self, list_of_commands):
        self.executable = []
        for command in list_of_commands:
            filled_command = command.filled_command
            self.executable.append(filled_command)

    def get_strings(self):
        return self.executable

