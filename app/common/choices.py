from model_utils import Choices

TYPE_USER = Choices((0,"admin", "admin"), (1, "customer", "customer"), (2, "manager", "manager"))
GENDER = Choices(("male", "Masculino"), ("female", "Feminino"),)