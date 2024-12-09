"""Additional helpers for sqlalchemy."""

from sqlalchemy.types import UserDefinedType


class JSONPath(UserDefinedType):
    """Used to define json path when casting."""

    @property
    def python_type(self):
        """Return the python type."""
        return str

    def get_col_spec(self):
        """Return the column specification."""
        return "jsonpath"