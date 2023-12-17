
def solve_quadratic_equation(a, b, c) -> float or tuple:
	d = b ** 2 - 4 * a * c
	if d < 0:
		return None
	elif d == 0:
		return -b / (2 * a)
	else:
		return (-b - d ** 0.5) / (2 * a), (-b + d ** 0.5) / (2 * a)
