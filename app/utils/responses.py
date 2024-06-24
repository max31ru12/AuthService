from typing import Any

from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse


class Responses:


    @classmethod
    def get_responses(cls) -> dict[int | str, dict[str, Any]]:
        responses = {}
        for _, val in cls.__members__.items():  # noqa
            key = val.value[0]
            description = val.value[1]
            responses[key] = {
                                 "description": description,
                                 "content": {
                                     "application/json": {
                                         "example":
                                             {"detail:": description}
                                     }
                                 }
                             }
        return responses
