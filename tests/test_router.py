from router_logic import decide_route

def test_routing_rag():
    assert decide_route("explain embeddings") == "rag"

def test_routing_code():
    assert decide_route("create file") == "code"

def test_routing_default():
    assert decide_route("hello") == "rag"
