import numpy as np

# --- CLASS HỖ TRỢ TRẢ KẾT QUẢ ---
# Tạo class này để kết quả trả về có thể gọi được `.t` và `.y` hoặc `.root` giống y hệt SciPy
class OdeResult:
    def __init__(self, t, y):
        self.t = t
        self.y = y

class OptimizeResult:
    def __init__(self, root):
        self.root = root

# --- 1. MODULE GIẢI PHƯƠNG TRÌNH VI PHÂN (Thay thế solve_ivp) ---
def solve_ivp_custom(fun, t_span, y0, t_eval=None, n_steps=100):
    """
    Giải hệ phương trình vi phân bằng phương pháp Runge-Kutta bậc 4 (RK4).
    """
    t0, tf = t_span
    
    # Thiết lập mảng thời gian t
    if t_eval is not None:
        t = np.array(t_eval)
        h = t[1] - t[0]  # Bước nhảy (giả sử t_eval chia đều)
        n_steps = len(t) - 1
    else:
        t = np.linspace(t0, tf, n_steps + 1)
        h = (tf - t0) / n_steps

    # Khởi tạo ma trận y: Số hàng = số biến (2), Số cột = số bước
    y = np.zeros((len(y0), len(t)))
    y[:, 0] = y0

    # Vòng lặp RK4
    for i in range(n_steps):
        ti = t[i]
        yi = y[:, i]
        
        # Tính 4 hệ số k
        k1 = np.array(fun(ti, yi))
        k2 = np.array(fun(ti + h/2.0, yi + (h/2.0) * k1))
        k3 = np.array(fun(ti + h/2.0, yi + (h/2.0) * k2))
        k4 = np.array(fun(ti + h, yi + h * k3))
        
        # Cập nhật trạng thái tiếp theo
        y[:, i+1] = yi + (h/6.0) * (k1 + 2*k2 + 2*k3 + k4)

    return OdeResult(t, y)

# --- 2. MODULE TÌM NGHIỆM (Thay thế root_scalar) ---
def root_scalar_secant(fun, x0, x1, tol=1e-6, max_iter=100):
    """
    Tìm nghiệm f(x) = 0 bằng phương pháp Cát tuyến (Secant Method).
    """
    f0 = fun(x0)
    f1 = fun(x1)
    
    for i in range(max_iter):
        # Tránh lỗi chia cho 0 nếu f1 và f0 quá gần nhau
        if abs(f1 - f0) < 1e-14:
            break
            
        # Công thức Secant: x_new = x1 - f1 * (x1 - x0) / (f1 - f0)
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        f2 = fun(x2)
        
        # Nếu sai số đã nhỏ hơn mức cho phép (tol) thì dừng
        if abs(f2) < tol:
            return OptimizeResult(x2)
            
        # Cập nhật các điểm cho vòng lặp tiếp theo
        x0, x1 = x1, x2
        f0, f1 = f1, f2
        
    # Trả về kết quả tốt nhất nếu hết max_iter mà chưa đạt sai số yêu cầu
    return OptimizeResult(x1)