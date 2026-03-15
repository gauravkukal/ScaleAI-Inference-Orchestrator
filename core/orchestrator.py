import time
import random
from typing import List, Dict, Optional
from loguru import logger
from pydantic import BaseModel

class InferenceRequest(BaseModel):
    request_id: str
    model_id: str
    payload: Dict[str, str]
    priority: int = 1

class NodeStatus(BaseModel):
    node_id: str
    current_latency_ms: float
    gpu_utilization: float
    is_healthy: bool = True

class InferenceOrchestrator:
    \"\"\"
    The core engine responsible for routing and optimizing AI inference requests.
    Designed for high-scale, low-latency environments.
    \"\"\"
    def __init__(self, platform_name: str = "Adobe-Express-Foundations"):
        self.platform_name = platform_name
        self.nodes: Dict[str, NodeStatus] = {}
        logger.info(f"Initialized ScaleAI Orchestrator on: {platform_name}")

    def register_worker_node(self, node: NodeStatus):
        self.nodes[node.node_id] = node
        logger.debug(f"Registered worker node: {node.node_id}")

    def get_optimal_node(self, request: InferenceRequest) -> Optional[str]:
        \"\"\"
        Routing Strategy: Latency-aware least utilization.
        Balances between the fastest response and lowest compute load.
        \"\"\"
        healthy_nodes = [n for n in self.nodes.values() if n.is_healthy]
        
        if not healthy_nodes:
            logger.error("Critical: No healthy worker nodes available for inference!")
            return None

        # Sort by utilization then latency
        best_node = sorted(healthy_nodes, key=lambda x: (x.gpu_utilization, x.current_latency_ms))[0]
        logger.info(f"Routing Request [{request.request_id}] to Node [{best_node.node_id}]")
        return best_node.node_id

    def simulate_inference(self, request: InferenceRequest):
        \"\"\"
        Simulates the end-to-end inference lifecycle.
        \"\"\"
        start_time = time.time()
        node_id = self.get_optimal_node(request)
        
        if node_id:
            # Simulate processing delay
            processing_time = random.uniform(0.05, 0.2)
            time.sleep(processing_time)
            
            end_time = time.time()
            total_latency = (end_time - start_time) * 1000
            logger.success(f"Inference complete for {request.request_id} in {total_latency:.2f}ms")
            return {"status": "success", "latency_ms": total_latency, "worker": node_id}
        
        return {"status": "error", "message": "No available workers"}

if __name__ == "__main__":
    orchestrator = InferenceOrchestrator()
    
    # Simulate high-scale node registration
    for i in range(5):
        orchestrator.register_worker_node(NodeStatus(
            node_id=f"gpu-worker-{i}",
            current_latency_ms=random.uniform(10, 50),
            gpu_utilization=random.uniform(0.1, 0.8)
        ))

    # Simulate incoming GenAI request
    sample_req = InferenceRequest(
        request_id="REQ-GENAI-001",
        model_id="sensei-gen-v2",
        payload={"prompt": "Generate a creative layout for digital marketing."}
    )
    
    orchestrator.simulate_inference(sample_req)