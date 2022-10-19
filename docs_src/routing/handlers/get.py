from esmerald import Esmerald, Gateway, Request, UJSONResponse, get


@get()
async def example(request: Request) -> UJSONResponse:
    return UJSONResponse({"message": "Welcome home!"})


@get(path="/another")
def another() -> str:
    return "Another welcome!"


@get(path="/")
def another_read(name: str) -> str:
    return f"Another welcome, {name}!"


app = Esmerald(
    routes=[
        Gateway(handler=example),
        Gateway(handler=another),
        Gateway(path="/last/{name:str}", handler=another_read),
    ]
)
