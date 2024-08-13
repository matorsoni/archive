import numpy as np

ftype = np.float64

def u(x: ftype) -> ftype:
    return np.sin(x, dtype=ftype)

def du(x: ftype) -> ftype:
    return np.cos(x, dtype=ftype)

def scifmt(x: ftype) -> str:
    return np.format_float_scientific(x, precision=4)

def make_table(table: list[list], headers: list):
    from tabulate import tabulate
    # Disable numerical parse to allow showing data in scientific notation.
    return tabulate(table, headers, tablefmt="grid", disable_numparse=True)

# Approximating derivative of u around x=1
x = ftype(1)
D_true = du(x)
H = np.array([1e-1, 5e-2, 1e-2, 5e-3, 1e-3], dtype=ftype)

# Aproximation values
D_plus = (u(x+H) - u(x))/H
D_minus = (u(x) - u(x-H))/H
D_0 = (u(x+H) - u(x-H))/(2*H)
D_3 = (2*u(x+H) + 3*u(x) - 6*u(x-H) + u(x-2*H))/(6*H)

value_table = []
error_table = []
for i,h in enumerate(H):
    value_row = [scifmt(x) for x in [h, D_plus[i], D_minus[i], D_0[i], D_3[i]]]
    value_table.append(value_row)
    error_row = [scifmt(h)] + [scifmt(D_approx - D_true) for D_approx in [D_plus[i], D_minus[i], D_0[i], D_3[i]]]
    error_table.append(error_row)


print(f"True value: {scifmt(D_true)}")
print(make_table(value_table, headers=["h","D+ u(1)", "D- u(1)", "D0 u(1)", "D3 u(1)"]))
print(make_table(error_table, headers=["h","D+ u(1)", "D- u(1)", "D0 u(1)", "D3 u(1)"]))


# Error values for log-log plot
D_plus_error = np.abs(D_plus - D_true)
D_minus_error = np.abs(D_minus - D_true)
D_0_error = np.abs(D_0 - D_true)
D_3_error = np.abs(D_3 - D_true)

# Generate plot
import matplotlib.pyplot as plt
t = np.arange(0., 5., 0.2)
plt.plot(H, D_plus_error, 'ro-')
plt.plot(H, D_0_error, 'bs-')
plt.plot(H, D_3_error, 'g^-')
plt.xlabel('h')
plt.ylabel('Aproximation error')
plt.xscale('log')
plt.yscale('log')
plt.grid(False)
plt.legend(["D+", "D0", "D3"], loc="lower right")
plt.show()
