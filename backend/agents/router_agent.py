class RouterAgent:
    def __init__(self, router_skill):
        self.router_skill = router_skill
        
    def execute(self, start_loc, end_loc, errands, distance_matrix) -> dict:
        print("[RouterAgent] Running route optimization skill...")
        return self.router_skill.optimize(start_loc, end_loc, errands, distance_matrix)
