from fastapi import FastAPI

from api.service import router

app = FastAPI(
    title="Chicago's crimes map",
    description="""Map with locations of crimes commited in Chicago
                with possibility to filter them by date and type of crime.""",
    version="0.1.0",
)

app.include_router(router)
