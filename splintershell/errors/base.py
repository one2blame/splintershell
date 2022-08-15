"""The base splintershell exception type."""


class SplinterShellError(Exception):
    def __init__(self, message, *args):
        self._message = message
        super(SplinterShellError, self).__init__(self._message, *args)

    @property
    def message(self):
        """A helpful message intended to be shown to the end user.
        :type: :class:`str <python:str>`
        """
        return self._message
