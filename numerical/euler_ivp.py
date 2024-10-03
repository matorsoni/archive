import numpy as np
from tqdm import tqdm

flt = np.float64

def g(t):
    t2 = t*t
    t3 = t*t2
    t4 = t*t3
    return (t4 - 6*t3 + 12*t2 - 14*t + 9)/(1 + 2*t + t2)

# Initial value problem:
# y' = f(t, y) = y^2 - g(t) ; y(0) = 2
def f(t, y):
    return y*y - g(t)

# Analytical solution
def ytrue(t):
    return (1 - t)*(2 - t)/(1 + t)

def forward_euler(ti, tf, N):
    h = (tf - ti) / (N-1)
    T = np.linspace(ti, tf, N, dtype=flt)
    Y = np.zeros(shape=(N,), dtype=flt)
    Y[0] = 2.0
    for i in tqdm(range(1, N)):
        t_ = T[i-1]
        y_ = Y[i-1]
        Y[i] = y_ + h * f(t_, y_)
    return T, Y

def backward_euler(ti, tf, N):

    def zero_by_newton(y_init, y_prev, t, h):
        def G(y, y_, t, h): return y - h*f(t, y) - y_
        def dG(y, y_, t, h): return 1 - h*2*y
        tol = 1e-6
        max_iter = 200
        y = y_init
        for _ in range(max_iter):
            update = G(y, y_prev, t, h)/dG(y, y_prev, t, h)
            y = y - update
            if np.abs(update) < tol:
                break
        return y

    h = (tf - ti) / (N-1)
    T = np.linspace(ti, tf, N, dtype=flt)
    Y = np.zeros(shape=(N,), dtype=flt)
    Y[0] = 2.0
    for i in tqdm(range(1, N)):
        t_ = T[i]
        y_ = Y[i-1]
        Y[i] = zero_by_newton(y_, y_, t_, h)
    return T, Y

def runge_kutta_4(ti, tf, N):
    h = (tf - ti) / (N-1)
    half_h = 0.5 * h
    T = np.linspace(ti, tf, N, dtype=flt)
    Y = np.zeros(shape=(N,), dtype=flt)
    Y[0] = 2.0
    for i in tqdm(range(1, N)):
        t_ = T[i-1]
        y_ = Y[i-1]
        y1 = y_
        y2 = y_ + half_h*f(t_, y1)
        y3 = y_ + half_h*f(t_ + half_h, y2)
        y4 = y_ + h*f(t_ + half_h, y3)
        k1 = f(t_, y1)
        k2 = f(t_ + half_h, y2)
        k3 = f(t_ + half_h, y3)
        k4 = f(t_ + h, y4)
        Y[i] = y_ + (k1 + 2*k2 + 2*k3 + k4) * h / 6
    return T, Y

def adams_moulton_4(ti, tf, N):
    h = (tf - ti) / (N-1)
    T = np.linspace(ti, tf, N, dtype=flt)
    Y = np.zeros(shape=(N,), dtype=flt)
    Y[0] = 2.0
    Y[1] = Y[0] + f(T[0], Y[0])*h
    Y[2] = Y[1] + (-f(T[0], Y[0]) + 3*f(T[1], Y[1]))*h/2
    Y[3] = Y[2] + (5*f(T[0], Y[0]) - 16*f(T[1], Y[1]) + 23*f(T[2], Y[2]))*h/12
    for i in tqdm(range(4, N)):
        Y[i] = Y[i-1] + (-9*f(T[i-4], Y[i-4]) + 37*f(T[i-3], Y[i-3]) - 59*f(T[i-2], Y[i-2]) + 55*f(T[i-1], Y[i-1]))*h/24
    return T, Y

def generate_plot(T, Y, Y_true, title):
    import matplotlib.pyplot as plt
    pad = 0.1
    mint = min(T) - pad
    maxt = max(T) + pad
    miny = min(Y_true) - pad
    maxy = max(Y_true) + pad
    plt.plot(T, Y, 'r-')
    plt.plot(T, Y_true, 'b-')
    plt.xlabel('T')
    plt.ylabel('Y')
    plt.title(title)
    plt.xlim(mint, maxt)
    plt.ylim(miny, maxy)
    plt.grid(True)
    plt.legend(["Numerical", "Analytical"], loc="upper right")
    plt.show()

h = 0.01
ti = 0.0
tf = 4.6
N = int((tf-ti) / h)

T, Y = forward_euler(ti, tf, N)
Y_true = ytrue(T)
generate_plot(T, Y, Y_true, "Forward Euler (explicit)")

T, Y = backward_euler(ti, tf, N)
Y_true = ytrue(T)
generate_plot(T, Y, Y_true, "Forward Euler (implicit)")

T, Y = runge_kutta_4(ti, tf, N)
Y_true = ytrue(T)
generate_plot(T, Y, Y_true, "Runge-Kutta 4")

T, Y = adams_moulton_4(ti, tf, N)
Y_true = ytrue(T)
generate_plot(T, Y, Y_true, "Adams-Moulton 4")
