import numpy as np

ftype = np.float64

def scifmt(x: ftype) -> str:
    return np.format_float_scientific(x, precision=4)

def make_table(table: list[list], headers: list):
    from tabulate import tabulate
    # Disable numerical parse to allow showing data in scientific notation.
    return tabulate(table, headers, tablefmt="grid", disable_numparse=True)

def run_study(f, df, x0: ftype):
    # Approximating derivative of f around x0
    D_true = df(x0)
    H = np.array([1e-1, 5e-2, 1e-2, 5e-3, 1e-3, 5e-4, 1e-4, 5e-5, 1e-5], dtype=ftype)

    # Aproximation values
    D_plus = (f(x0+H) - f(x0))/H
    D_minus = (f(x0) - f(x0-H))/H
    D_0 = (f(x0+H) - f(x0-H))/(2*H)
    D_3 = (2*f(x0+H) + 3*f(x0) - 6*f(x0-H) + f(x0-2*H))/(6*H)

    value_table = []
    error_table = []
    for i,h in enumerate(H):
        value_row = [scifmt(D) for D in [h, D_plus[i], D_minus[i], D_0[i], D_3[i]]]
        value_table.append(value_row)
        error_row = [scifmt(h)] + [scifmt(D_approx - D_true) for D_approx in [D_plus[i], D_minus[i], D_0[i], D_3[i]]]
        error_table.append(error_row)

    print("\n")
    print(f"True value: {scifmt(D_true)}")
    print(make_table(value_table, headers=["h","D+ u(x0)", "D- u(x0)", "D0 u(x0)", "D3 u(x0)"]))
    print(make_table(error_table, headers=["h","D+ u(x0)", "D- u(x0)", "D0 u(x0)", "D3 u(x0)"]))
    print("\n")

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

# Functions to study
def u_sin(x: ftype) -> ftype:
    return np.sin(x, dtype=ftype)
def du_sin(x: ftype) -> ftype:
    return np.cos(x, dtype=ftype)

def u_sin10(x: ftype) -> ftype:
    return np.sin(10.0*x, dtype=ftype)
def du_sin10(x: ftype) -> ftype:
    return 10.0*np.cos(10.0*x, dtype=ftype)

def u_poly(x: ftype) -> ftype:
    return 4*x**3 - 12*x**2 + 14*x - 4
def du_poly(x: ftype) -> ftype:
    return 12*x**2 - 24*x + 14

def u_mod(x: ftype) -> ftype:
    return np.power(np.abs(x-1.001), 3.0/2)
def du_mod(x: ftype) -> ftype:
    return 1# ..... compute 3.0/2 * np.power(np.abs(x-1.001), 3.0/2)

run_study(u_sin, du_sin, ftype(1))
run_study(u_sin10, du_sin10, ftype(1))
run_study(u_poly, du_poly, ftype(1))
