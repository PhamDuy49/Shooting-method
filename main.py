import numpy as np
import matplotlib.pyplot as plt

# BƯỚC MỚI: Import module tự viết (thay thế hoàn toàn Scipy)
from my_solvers import solve_ivp_custom, root_scalar_secant

# 1. Định nghĩa hệ phương trình bậc 1: y1' = y2, y2' = -y1
def system(x, Y):
    y1, y2 = Y
    return [y2, -y1]

# 2. Hàm mục tiêu tính sai số tại biên b
def objective(z):
    # Dùng hàm custom thay vì solve_ivp
    sol = solve_ivp_custom(system, [0, np.pi/2], [1, z])
    y_end = sol.y[0, -1] # Giá trị y tại x = pi/2
    return y_end - 0     # Sai số so với điều kiện biên y(pi/2) = 0

# 3. Tìm góc bắn tối ưu (nghiệm z của hàm objective)
# Dùng hàm custom thay vì root_scalar
res = root_scalar_secant(objective, x0=-0.5, x1=0.5)
z_opt = res.root
print(f"Góc bắn tối ưu y'(0) = {z_opt:.6f}")

# 4. Giải lại hệ với góc bắn tối ưu để lấy kết quả
sol_opt = solve_ivp_custom(system, [0, np.pi/2], [1, z_opt], t_eval=np.linspace(0, np.pi/2, 50))

# Vẽ đồ thị
plt.plot(sol_opt.t, sol_opt.y[0], 'o-', label='Phương pháp bắn (RK4)')
plt.plot(sol_opt.t, np.cos(sol_opt.t), 'k--', label='Nghiệm chính xác (cos(x))')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.title('Phương pháp Bắn với RK4 và Secant Method')
plt.grid(True)
plt.show()