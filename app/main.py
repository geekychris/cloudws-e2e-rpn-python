"""FastAPI application exposing the RPN scientific calculator."""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.rpn import RPNError, evaluate

app = FastAPI(
    title="RPN Scientific Calculator",
    description="A REST API that evaluates scientific expressions in Reverse Polish Notation.",
    version="0.1.0",
)


class CalculateRequest(BaseModel):
    expression: str


class CalculateResponse(BaseModel):
    result: float


@app.post("/calculate", response_model=CalculateResponse)
def calculate(request: CalculateRequest):
    try:
        result = evaluate(request.expression)
    except RPNError as exc:
        return JSONResponse(status_code=400, content={"error": str(exc)})
    return {"result": result}
