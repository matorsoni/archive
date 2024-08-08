import numpy as np
from tabulate import tabulate

datatype = np.float64

def u(x: datatype) -> datatype:
    return np.sin(x, dtype=datatype)

def du(x: datatype) -> datatype:
    return np.cos(x, dtype=datatype)

def scifmt(x: datatype) -> str:
    return np.format_float_scientific(x, precision=4)

def make_table(table: list[list], headers: list):
    # Disable numerical parse to allow showing data in scientific notation.
    return tabulate(table, headers, tablefmt="grid", disable_numparse=True)

# Approximating derivative of u around x=1
x = datatype(1)
H = np.array([1e-1, 5e-2, 1e-2, 5e-3, 1e-3], dtype=datatype)
D_plus = (u(x+H) - u(x))/H
D_minus = (u(x) - u(x-H))/H
D_0 = (u(x+H) - u(x-H))/(2*H)
D_3 = (2*u(x+H) + 3*u(x) - 6*u(x-H) + u(x-2*H))/(6*H)
D_true = du(x)

value_table = []
error_table = []
for i,h in enumerate(H):
    value_row = [scifmt(x) for x in [h, D_plus[i], D_minus[i], D_0[i], D_3[i]]]
    value_table.append(value_row)
    error_row = [scifmt(h)] + [scifmt(np.abs(D_true - x)) for x in [D_plus[i], D_minus[i], D_0[i], D_3[i]]]
    error_table.append(error_row)


print(f"True value: {scifmt(D_true)}")
print(make_table(value_table, headers=["h","D+ u(1)", "D- u(1)", "D0 u(1)", "D3 u(1)"]))
print(make_table(error_table, headers=["h","D+ u(1)", "D- u(1)", "D0 u(1)", "D3 u(1)"]))
