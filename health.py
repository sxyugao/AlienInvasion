class Health:
    def __init__(self, max_health: float, current_health: float = None) -> None:
        self.max_health = max_health
        if current_health is None:
            self.current_health = max_health
        else:
            self.current_health = current_health

    def clamp(self, value: float, min_value: float, max_value: float) -> float:
        if min_value < value < max_value:
            return value
        if value < min_value:
            return max(value, min_value)
        if value > max_value:
            return min(value, max_value)

    def set_health(self, health: float):
        self.current_health = self.clamp(health, 0, self.max_health)

    def get_health_rate(self) -> float:
        return self.current_health / self.max_health

    def reduce(self, value: float) -> None:
        self.current_health -= value
        if self.current_health > self.max_health:
            self.current_health = self.max_health

    def alive(self) -> bool:
        return self.current_health > 0
