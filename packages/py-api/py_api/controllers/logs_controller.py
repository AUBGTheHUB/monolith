from os.path import exists
from pathlib import Path
from typing import Final

from fastapi.responses import FileResponse, JSONResponse
from py_api.environment import IS_OFFLINE

LOGFILE_PATH: Final = f"{Path(__file__).parent.resolve().parent}/shared/logfile.log"


class LogsController:
    @classmethod
    def get_log_file(cls) -> JSONResponse | FileResponse:

        if IS_OFFLINE:
            content = {
                "message": "You should be in a prod environment. Log files are not present in a local one.",
            }
            status_code = 400

            return JSONResponse(content=content, status_code=status_code)

        if not exists(LOGFILE_PATH):
            return JSONResponse(content={"error": "The logs folder is empty"}, status_code=404)

        return FileResponse(
            LOGFILE_PATH, headers={
                "Content-Disposition": f"attachment; filename=logfile.log",
            },
        )
