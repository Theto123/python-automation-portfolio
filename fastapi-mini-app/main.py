from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI(title="Advanced Math API", description="API providing mathematical operations with validation and logging", version="1.0")

class Numbers(BaseModel):
    a: float = Field(..., description="First number")
    b: Optional[float] = Field(None, description="Second number (optional)")

@app.get("/")
def home():
    """Home endpoint to check if API is running"""
    return {"message": "API running"}

@app.get("/square/{n}")
def square(n: int = Query(..., ge=0, le=10000, description="Number to square")):
    """Returns the square of a number (0-10000)"""
    logging.info(f"Calculating square of {n}")
    return {"input": n, "result": n**2}

@app.post("/add")
def add_numbers(numbers: Numbers):
    """Adds two numbers, second is optional (defaults to 0)"""
    b = numbers.b if numbers.b is not None else 0
    result = numbers.a + b
    logging.info(f"Adding {numbers.a} + {b} = {result}")
    return {"a": numbers.a, "b": b, "result": result}

@app.get("/factorial/{n}")
def factorial(n: int = Query(..., ge=0, le=100)):
    """Calculates factorial with error handling for large numbers"""
    logging.info(f"Calculating factorial of {n}")
    try:
        result = 1
        for i in range(2, n + 1):
            result *= i
        return {"number": n, "factorial": result}
    except OverflowError:
        raise HTTPException(status_code=400, detail="Number too large to compute factorial")

@app.get("/fibonacci")
def fibonacci(limit: int = Query(10, ge=1, le=100, description="Number of Fibonacci terms")):
    """Returns Fibonacci sequence up to 'limit' terms"""
    logging.info(f"Generating Fibonacci sequence with {limit} terms")
    seq = [0, 1]
    for _ in range(2, limit):
        seq.append(seq[-1] + seq[-2])
    return {"limit": limit, "sequence": seq[:limit]}
