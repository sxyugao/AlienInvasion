
class Exp:
    def __init__(self):
        self.level = 1
        self.current_exp = 0

    @staticmethod
    def exp_required_to_upgrade(current_level: int) -> int:
        """
        Calculate the experience points required to upgrade from current_level to (current_level + 1).
        :param current_level: current level
        :return: int
        """
        return current_level * 5

    def increase(self, exp) -> None:
        while exp > 0:
            exp_required = Exp.exp_required_to_upgrade(self.level)
            if self.current_exp + exp < exp_required:
                self.current_exp += exp
                return

            exp -= (exp_required - self.current_exp)
            self.level += 1
            self.current_exp = 0

    def __str__(self):
        return "level = " + str(self.level) + ", " + "exp = " + str(self.current_exp)
