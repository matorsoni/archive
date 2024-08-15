import numpy as np

ftype = np.float64

def scifmt(x: ftype) -> str:
    return np.format_float_scientific(x, precision=4)

def make_table(table: list[list], headers: list):
    from tabulate import tabulate
    # Disable numerical parse to allow showing data in scientific notation.
    return tabulate(table, headers, tablefmt="grid", disable_numparse=True)

# Numerical approximations of first order (d1) and second order (d2) derivatives.
def d1_plus(f, x, h):
    return (f(x+h) - f(x))/h

def d1_minus(f, x, h):
    return (f(x) - f(x-h))/h

def d1_0(f, x, h):
    return (f(x+h) - f(x-h))/(2*h)

def d1_3(f, x, h):
    return (2*f(x+h) + 3*f(x) - 6*f(x-h) + f(x-2*h))/(6*h)

def d2_4(f, x, h):
    a = -1.0/12
    b =  4.0/3
    c = -5.0/2
    return (a*f(x+2*h) + b*f(x+h) + c*f(x) + b*f(x-h) + a*f(x-2*h))/(h*h)

# Create graphs and table of numerical errors related to
# derivative approximations
def run_study(f, df, x0: ftype, H: np.array = np.array([1e-1, 5e-2, 1e-2, 5e-3, 1e-3, 5e-4, 1e-4, 5e-5, 1e-5], dtype=ftype)):

    D_true = df(x0)
    D_plus = d1_plus(f, x0, H)
    D_minus = d1_minus(f, x0, H)
    D_0 = d1_0(f, x0, H)
    D_3 = d1_3(f, x0, H)

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

def run_study_2(f, true_val, x0: ftype, H = np.logspace(-1, -4, 13, dtype=ftype)):
    D_2 = d2_4(f, x0, H)
    D_2_true = true_val

    value_table = []
    error_table = []
    for i,h in enumerate(H):
        value_row = [scifmt(h), scifmt(D_2[i])]
        value_table.append(value_row)
        error_row = [scifmt(h), scifmt(D_2[i] - D_2_true)]
        error_table.append(error_row)

    print("\n")
    print(f"True value: {scifmt(D_2_true)}")
    print(make_table(value_table, headers=["h","D2_4 u(x0)"]))
    print(make_table(error_table, headers=["h","D2_4 u(x0)"]))
    print("\n")

    # Error values for log-log plot
    D_2_error = np.abs(D_2 - D_2_true)

    # Generate plot
    import matplotlib.pyplot as plt
    t = np.arange(0., 5., 0.2)
    plt.plot(H, D_2_error, 'ro-')
    plt.xlabel('h')
    plt.ylabel('Aproximation error')
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(False)
    plt.legend(["D2_4"], loc="lower right")
    plt.show()

f = lambda x: np.sin(2.0*x, dtype=ftype)
d2f = -4.0 * f(1)
run_study_2(f, d2f, ftype(1))
