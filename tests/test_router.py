from router import tester_router

def test_max_iterations_stops_graph():
    mock_state = {
        "is_approved": False,
        "iteration_count": 3
    }
    
    result = tester_router(mock_state)
    
    assert result == "human_mediation"