from typing import Annotated

from pydantic import StringConstraints

# Common reusable input type: non-empty string trimmed of whitespace
NonEmptyStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
