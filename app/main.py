from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from app.config import settings
from app.database import check_db_connection, redis_client
from app.logger import logger

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)


class OperationItem(BaseModel):
    task_name: str = Field(..., min_length=3, max_length=50)
    operator: str = Field(..., min_length=2, max_length=30)
    priority: str = Field(default="MEDIUM", pattern="^(LOW|MEDIUM|HIGH|CRITICAL)$")


@app.on_event("startup")
def on_startup():
    logger.info(f"Initialized {settings.APP_NAME} version {settings.APP_VERSION}")


@app.get("/health", status_code=status.HTTP_200_OK)
def health():
    return {
        "status": "UP",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }


@app.get("/ready", status_code=status.HTTP_200_OK)
def ready():
    is_ready = check_db_connection()
    if not is_ready:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Storage dependency not ready"
        )
    return {"status": "READY", "dependency": "CONNECTED"}


@app.post("/api/v1/operations", status_code=status.HTTP_201_CREATED)
def create_operation(item: OperationItem):
    try:
        new_id = redis_client.incr("operations_counter")
        redis_client.hset(f"operation:{new_id}", mapping=item.model_dump())
        logger.info(f"Operation record created with ID {new_id}")
        return {"id": new_id, **item.model_dump()}
    except Exception as e:
        logger.error(f"Failed to record operation: {str(e)}")
        raise HTTPException(status_code=500, detail="Database write failure")


@app.get("/api/v1/operations", status_code=status.HTTP_200_OK)
def list_operations():
    try:
        keys = redis_client.keys("operation:*")
        records = [redis_client.hgetall(k) for k in keys]
        return {"total": len(records), "data": records}
    except Exception as e:
        logger.error(f"Failed to fetch operations: {str(e)}")
        return {"total": 0, "data": []}


@app.get("/api/v1/simulate-error")
def simulate_error():
    logger.error("Intentional failure triggered for log inspection and incident triage demo")
    raise HTTPException(status_code=500, detail="Simulated 500 error for incident response")