from rs.lina.vector import Vector2D

v1 = Vector2D(2, 3)
v2 = Vector2D(1, 1)

# Операции с векторами
print(v1 + v2)  # Vector2D(x=3, y=4)
print(v1 * v2)  # Vector2D(x=2, y=3)

# Операции со скалярами
print(v1 + 5)  # Vector2D(x=7, y=8)
print(v1 * 0.5)  # Vector2D(x=1.0, y=1.5)

# Неподдерживаемый тип
try:
    v1 + "abc"
except TypeError as e:
    print(e)  # Unsupported operand type
