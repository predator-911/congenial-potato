def clamp_limit(value: int, default: int = 50, maximum: int = 200) -> int:
    return max(1, min(value or default, maximum))
