import numpy as np

from camera import Camera
from light import Light
from material import Material


def calculate(camera, light, material, N_input, O_d_input=None):
    if not isinstance(camera, Camera):
        raise Exception('Camera is not ready.')
    if not isinstance(light, Light):
        raise Exception('Light is not ready.')
    if not isinstance(material, Material):
        raise Exception('Material is not ready.')
    if type(N_input) != np.ndarray or N_input.shape != (3,):
        raise Exception('There is a type error in parameter `N_input`.')
    if O_d_input is not None:
        if type(O_d_input) != list or len(O_d_input) != 3 \
                or (type(O_d_input[0]) != int and type(O_d_input[0]) != float) or O_d_input[0] < 0 or O_d_input[0] > 1 \
                or (type(O_d_input[1]) != int and type(O_d_input[1]) != float) or O_d_input[1] < 0 or O_d_input[1] > 1 \
                or (type(O_d_input[2]) != int and type(O_d_input[2]) != float) or O_d_input[2] < 0 or O_d_input[2] > 1:
            raise Exception('There is a type error in parameter `O_d_input`.')
    #
    I_a = light.I_a
    k_a = material.k_a
    O_d = material.O_d
    if O_d_input is not None:
        O_d = np.array(O_d_input)
    f_att = light.f_att
    I_p = light.I_p
    k_d = material.k_d
    N = N_input
    N = N / np.linalg.norm(N, 2)
    L = light.L  # `L` has been normalized.
    k_s = material.k_s
    O_s = light.O_s
    V = -camera.n  # `V` should point to camera, which has been normalized.
    n = light.n
    H = L + V
    H = H / np.linalg.norm(H, 2)
    #
    return I_a * k_a * O_d + f_att * I_p * (
            k_d * O_d * np.dot(N, L) + k_s * O_s * (np.dot(N, H) ** n)
    )
