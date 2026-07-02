from typing import List, Dict, Any
import itertools

class RouteOptimizationSkill:
    """
    Skill for optimizing the sequence of errands based on distance and closing times.
    This operates as a Traveling Salesperson Problem (TSP) with Time Windows solver.
    """
    
    def __init__(self):
        pass
        
    def optimize(self, start_loc: Dict, end_loc: Dict, errands: List[Dict], distance_matrix: Dict) -> List[Dict]:
        """
        Calculates the most optimal route visiting all errands.
        
        Args:
            start_loc: {"lat": float, "lon": float, "name": str}
            end_loc: {"lat": float, "lon": float, "name": str}
            errands: List of {"id": str, "lat": float, "lon": float, "closing_time": str}
            distance_matrix: Pre-computed distances and times between all points
                             e.g., distance_matrix["start_to_errand1"]["duration_seconds"]
                             
        Returns:
            A list representing the optimal ordered sequence of errands.
        """
        if not errands:
            return {}
            
        # Ensure errands have an 'id'
        for idx, e in enumerate(errands):
            if "id" not in e:
                e["id"] = f"errand_{idx}"
                
        # Brute force optimization for a small number of errands (typical daily use case)
        # For N errands, there are N! permutations. (e.g., 5 errands = 120 paths)
        best_route = None
        min_duration = float('inf')
        
        errand_ids = [e["id"] for e in errands]
        print(f"[RouteOptimizer] IDs: {errand_ids}")
        print(f"[RouteOptimizer] Matrix: {distance_matrix}")
        
        for permutation in itertools.permutations(errand_ids):
            current_duration = 0
            is_valid = True
            
            # Calculate time from start to first errand
            first_errand = permutation[0]
            current_duration += distance_matrix.get(f"start_to_{first_errand}", {}).get("duration_seconds", float('inf'))
            
            # Add times between errands
            for i in range(len(permutation) - 1):
                from_id = permutation[i]
                to_id = permutation[i+1]
                leg_duration = distance_matrix.get(f"{from_id}_to_{to_id}", {}).get("duration_seconds", float('inf'))
                current_duration += leg_duration
                
                # TODO: Add logic to check if arrival time exceeds closing_time for `to_id`
                # If so, is_valid = False; break
                
            # Add time from last errand to end
            last_errand = permutation[-1]
            current_duration += distance_matrix.get(f"{last_errand}_to_end", {}).get("duration_seconds", float('inf'))
            
            if is_valid and current_duration < min_duration:
                min_duration = current_duration
                best_route = permutation
                
        # Map the best route IDs back to the actual errand objects
        ordered_errands = []
        if best_route:
            id_to_errand = {e["id"]: e for e in errands}
            ordered_errands = [id_to_errand[eid] for eid in best_route]
            
        return {
            "ordered_sequence": ordered_errands,
            "total_estimated_seconds": min_duration
        }
