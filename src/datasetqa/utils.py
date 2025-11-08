def map_det_type(code: str) -> str:
    mapping = {"BB": "broken_bone", "NB": "non_broken", "EX": "excluded"}
    return mapping.get(code, "unknown")
