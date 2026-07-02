class EvaluatorAgent:
    def __init__(self):
        # In a real ADK, this agent would bind the MCP tools (OSM, Time)
        pass
        
    def execute(self, errands: list) -> dict:
        print("[EvaluatorAgent] Evaluating locations and hours via OSM MCP...")
        
        distance_matrix = {}
        for idx, errand in enumerate(errands):
            errand_id = errand.get("id", f"errand_{idx}")
            errand["id"] = errand_id
            distance_matrix[f"start_to_{errand_id}"] = {"duration_seconds": 600}
            distance_matrix[f"{errand_id}_to_end"] = {"duration_seconds": 600}
            
            for j, other in enumerate(errands):
                if idx != j:
                    other_id = other.get("id", f"errand_{j}")
                    distance_matrix[f"{errand_id}_to_{other_id}"] = {"duration_seconds": 300}
                    
        return distance_matrix
