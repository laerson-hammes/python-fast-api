from http import HTTPStatus

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse

from api_requests.exceptions import (
    FalhaDeComunicacaoError,
    PedidoNaoEncontradoError,
)
from api_requests.magalu_api import recuperar_itens_por_pedido
from api_requests.schema import HealthCheckResponse, Item, ErrorResponse

app = FastAPI()


@app.exception_handler(FalhaDeComunicacaoError)
async def tratar_erro_falha_de_comunicacao(
    request: Request, exc: FalhaDeComunicacaoError
):
    return JSONResponse(
        status_code=HTTPStatus.BAD_GATEWAY,
        content={"message": "Falha de comunicação com o servidor remoto"},
    )


@app.exception_handler(PedidoNaoEncontradoError)
async def tratar_erro_pedido_nao_encontrado(
    request: Request, exc: PedidoNaoEncontradoError
):
    return JSONResponse(
        status_code=HTTPStatus.NOT_FOUND,
        content={"message": "Pedido não encontrado"},
    )


@app.get(
    "/healthcheck",
    tags=["healthcheck"],
    summary="Integridade do sistema",
    description="Checa se o servidor está online",
    response_model=HealthCheckResponse,
)
@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}


# ...
@app.get(
    "/orders/{identificacao_do_pedido}/items",
    responses={
        HTTPStatus.NOT_FOUND.value: {
            "description": "Pedido não encontrado",
            "model": ErrorResponse,
        },
        HTTPStatus.BAD_GATEWAY.value: {
            "description": "Falha de comunicação com o servidor remoto",
            "model": ErrorResponse,
        },
    },
    summary="Itens de um pedido",
    tags=["pedidos"],
    description="Retorna todos os itens de um determinado pedido",
    response_model=list[Item],
)
@app.get("/orders/{identificacao_do_pedido}/items")
async def listar_itens(itens: list[Item] = Depends(recuperar_itens_por_pedido)):
    return itens