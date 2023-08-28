from os.path import exists
from pathlib import Path
from typing import Final

from fastapi.responses import FileResponse, JSONResponse
from py_api.environment import IS_OFFLINE


class LogsController:
    LOGFILE_PATH: Final = f"{Path(__file__).parent.resolve().parent}/shared/logfile.log"

    @classmethod
    def get_log_file(cls) -> JSONResponse | FileResponse:

        if IS_OFFLINE:
            content = {
                "message": "Log files are not available in local environments.",
            }
            status_code = 400

            return JSONResponse(content=content, status_code=status_code)

        if not exists(cls.LOGFILE_PATH):
            return JSONResponse(content={"message": "The logs folder is empty"}, status_code=404)

        return FileResponse(
            cls.LOGFILE_PATH, headers={
                "Content-Disposition": f"attachment; filename=logfile.log",
            },
        )
