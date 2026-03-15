from fastapi import FastAPI, HTTPException
from core.orchestrator import InferenceOrchestrator, InferenceRequest, NodeStatus
import uvicorn
import uuid

app = FastAPI(title="ScaleAI Inference Orchestrator")
orchestrator = InferenceOrchestrator()

@app.on_event("startup")
def startup_event():
    # Pre-register default worker nodes
    orchestrator.register_worker_node(NodeStatus(node_id="primary-gpu-0", current_latency_ms=12.5, gpu_utilization=0.2))
    orchestrator.register_worker_node(NodeStatus(node_id="secondary-gpu-1", current_latency_ms=18.2, gpu_utilization=0.4))

@app.post("/v1/inference")
async def process_inference(request: InferenceRequest):
    result = orchestrator.simulate_inference(request)
    if result["status"] == "error":
        raise HTTPException(status_code=503, detail=result["message"])
    return result

@app.get("/health")
def health_check():
    return {"status": "online", "platform": orchestrator.platform_name}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)