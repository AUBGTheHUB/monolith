from fastapi.responses import JSONResponse, StreamingResponse

from py_api.database import q_col, a_col
import pandas as pd
import io


class QuestionnaireController:

    @classmethod
    def get_csv(cls, dep: str) -> JSONResponse | StreamingResponse:
        questions = q_col.find_one({'department': dep})

        if questions is None:
            return JSONResponse(content={"message": "Questionnaire doesn't exist"}, status_code=404)

        questions = [q['title'] for q in questions['questions']]

        answers = a_col.find({'department': dep})

        if len(list(answers)):
            answers = [list(a['answers'].values()) for a in answers]
        else:
            answers = []

        docs = pd.DataFrame(answers, columns=questions).replace(
            r'^s*$', float('NaN'), regex=True)
        docs.dropna(axis=0, how='all', inplace=True)

        stream = io.StringIO()
        docs.to_csv(stream, index=False)
        response = StreamingResponse(
            iter([stream.getvalue()]), media_type='text/csv')
        response.headers["Content-Disposition"] = f"attachment; filename={dep}.csv"

        return response
