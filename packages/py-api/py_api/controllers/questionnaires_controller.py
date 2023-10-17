import io

import pandas as pd
from fastapi.responses import JSONResponse, StreamingResponse
from py_api.database import a_col, q_col


class QuestionnairesController:

    @staticmethod
    def get_csv(dep: str) -> JSONResponse | StreamingResponse:
        questions = q_col.find_one({'department': dep})

        if questions is None:
            return JSONResponse(content={"message": "Questionnaire doesn't exist"}, status_code=404)

        questions = [q['title'] for q in questions['questions']]
        questions.append("Submission time")

        answers = a_col.find({'department': dep})
        answers = [list(a['answers'].values()) for a in answers]

        # I need to query the answers again because once I itereate over them then down below the answers list is empty
        submission_timestamps = [
            str(a["_id"].generation_time)
            for a in a_col.find({'department': dep})
        ]

        data = [a + [s] for a, s in zip(answers, submission_timestamps)]
        docs = pd.DataFrame(data, columns=questions).replace(
            r'^s*$', float('NaN'), regex=True,
        )

        docs.dropna(axis=0, how='all', inplace=True)

        stream = io.StringIO()
        docs.to_csv(stream, index=False)

        response = StreamingResponse(
            iter([stream.getvalue()]), media_type='text/csv',
        )
        response.headers["Content-Disposition"] = f"attachment; filename={dep}.csv"

        return response
