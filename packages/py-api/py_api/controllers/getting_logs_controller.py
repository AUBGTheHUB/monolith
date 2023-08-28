import pathlib
from os.path import exists
from traceback import format_exc
from typing import Final

from fastapi import APIRouter
from py_api.environment import IS_OFFLINE
from starlette.responses import FileResponse, JSONResponse

router = APIRouter()
LOGFILE_PATH: Final = f"{pathlib.Path(__file__).parent.resolve().parent}/shared/logfile.log"


class GettingLogsController:
    @classmethod
    def return_files(cls) -> JSONResponse | FileResponse:

        if IS_OFFLINE:
            content = {
                "message": "You should be in a prod environment. Log files are not present in a local one.",
            }
            status_code = 400

            return JSONResponse(content=content, status_code=status_code)

        return cls.get_log_file()

    @classmethod
    def get_log_file(cls) -> JSONResponse | FileResponse:
        # As this endpoint is used only for internal use, here we have an exception handler,
        # so that we could see in postman or wherever if there is a problem with downloading the file
        # This is done because when we are in prod env the errors are written to the logfile we are downloading
        try:
            if not exists(LOGFILE_PATH):
                return JSONResponse(content={"error": "The logs folder is empty"}, status_code=404)

            return FileResponse(
                LOGFILE_PATH, headers={
                    "Content-Disposition": f"attachment; filename=logfile.log",
                },
            )

        except Exception as e:
            return JSONResponse(content={"error": f"{e}", "stacktrace": format_exc()}, status_code=500)
