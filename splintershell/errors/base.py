"""The base splintershell exception type."""


class SplinterShellError(Exception):
    """Base splintershell Exception class for inheritance to implement more
    specific Exception classes.

    :param message: A related error message
    :type message: str
    """

    def __init__(self, message, *args) -> None:
        self._message = message
        super(SplinterShellError, self).__init__(self._message, *args)

    @property
    def message(self) -> str:
        """A helpful message intended to be shown to the end user.

        :return: A related error message
        :rtype: str
        """
        return self._message
