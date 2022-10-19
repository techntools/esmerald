from esmerald import Esmerald, Gateway, Include, UJSONResponse, patch


@patch(path="/partial/{item_id:int}")
def update(item_id: int) -> int:
    return item_id


@patch(path="/")
def another_update(item_id: int) -> UJSONResponse:
    return UJSONResponse({"Success", {item_id}})


app = Esmerald(
    routes=[
        Include(
            "/update",
            routes=[
                Gateway("/update", handler=update),
                Gateway(path="/last/{item_id:int}", handler=another_update),
            ],
        )
    ]
)
