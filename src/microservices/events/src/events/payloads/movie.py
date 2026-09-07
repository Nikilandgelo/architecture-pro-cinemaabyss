from pydantic import BaseModel


class MoviePayload(BaseModel):
    movie_id: int
    title: str
    action: str
    user_id: int
