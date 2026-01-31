from fastapi import FastAPI
from models import OrderRequest, DecisionResponse
from agent import build_agent

app = FastAPI(title="Decision-Centric MSME AI")

agent = build_agent()


@app.post("/order", response_model=DecisionResponse)
def process_order(order: OrderRequest):
    result = agent.invoke({"order": order})

    return DecisionResponse(
        decision=result["decision"],
        reason=result["reason"],
        customer_name=order.customer_name,
        customer_email=order.customer_email,
        assigned_staff=result.get("assigned_staff"),
        explanation=result.get("explanation")
    )


@app.get("/bottleneck")
def get_bottleneck():
    result = agent.invoke({"order": None})
    return {"bottlenecks": result.get("bottlenecks", [])}
