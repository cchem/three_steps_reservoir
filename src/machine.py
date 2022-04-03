import tkinter as tk


class Reservoir:
    def __init__(self, volume):
        # self.capacity = capacity  # total volume
        self.volume = volume  # current volume
        self.out_flow_set_value = 0
        self.out_flow = 0
        self.delta = 5

    def update(self, previous_list, key_press_u, key_press_d):
        # 流入後の液量の計算
        for prev in previous_list:
            self.volume += prev.out_flow

        # 設定流量の変更
        if key_press_u:
            self.out_flow_set_value += self.delta
        if key_press_d:
            self.out_flow_set_value -= self.delta

        # 流出量の計算
        if self.out_flow_set_value < self.volume:
            out_flow = self.volume
        else:
            out_flow = self.out_flow_set_value

        # 流出後の液量
        self.volume -= out_flow
        self.out_flow = out_flow


class ThreeStepsReservoir:
    def __init__(self):
        self.main_reservoir = Reservoir(1000)
        self.reservoir1 = Reservoir(100)
        self.reservoir2 = Reservoir(100)
        self.reservoir3 = Reservoir(100)

    def update(self, up0, down0, up1, down1, up2, down2, up3, down3):
        self.main_reservoir.update([], up0, down0)
        self.reservoir1.update([self.main_reservoir], up1, down1)
        self.reservoir2.update([self.reservoir1], up2, down2)
        self.reservoir3.update([self.reservoir2], up3, down3)
        self.main_reservoir.volume += self.reservoir3.out_flow


class Application:
    def __init__(self):
        win = tk.Tk()
        win.title('Three steps reservoir')
        win.geometry('640x512')
        win.resizable(False, False)
        self.win = win

        self.key_binding()

        self.q_key = False
        self.a_key = False
        self.w_key = False
        self.s_key = False
        self.e_key = False
        self.d_key = False
        self.r_key = False
        self.f_key = False

    def key_binding(self):
        self.win.bind('<KeyPress-Q', self.q_key_pressed)
        self.win.bind('<KeyPress-A', self.a_key_pressed)
        self.win.bind('<KeyPress-W', self.w_key_pressed)
        self.win.bind('<KeyPress-S', self.s_key_pressed)
        self.win.bind('<KeyPress-E', self.e_key_pressed)
        self.win.bind('<KeyPress-D', self.d_key_pressed)
        self.win.bind('<KeyPress-R', self.r_key_pressed)
        self.win.bind('<KeyPress-F', self.f_key_pressed)

        self.win.bind('<KeyRelease-Q', self.q_key_released)
        self.win.bind('<KeyRelease-A', self.a_key_released)
        self.win.bind('<KeyRelease-W', self.w_key_released)
        self.win.bind('<KeyRelease-S', self.s_key_released)
        self.win.bind('<KeyRelease-E', self.e_key_released)
        self.win.bind('<KeyRelease-D', self.d_key_released)
        self.win.bind('<KeyRelease-R', self.r_key_released)
        self.win.bind('<KeyRelease-F', self.f_key_released)

    def q_key_pressed(self, _):
        self.q_key = True

    def a_key_pressed(self, _):
        self.a_key = True

    def w_key_pressed(self, _):
        self.w_key = True

    def s_key_pressed(self, _):
        self.s_key = True

    def e_key_pressed(self, _):
        self.e_key = True

    def d_key_pressed(self, _):
        self.d_key = True

    def r_key_pressed(self, _):
        self.r_key = True

    def f_key_pressed(self, _):
        self.f_key = True

    def q_key_released(self, _):
        self.q_key = False

    def a_key_released(self, _):
        self.a_key = False

    def w_key_released(self, _):
        self.w_key = False

    def s_key_released(self, _):
        self.s_key = False

    def e_key_released(self, _):
        self.e_key = False

    def d_key_released(self, _):
        self.d_key = False

    def r_key_released(self, _):
        self.r_key = False

    def f_key_released(self, _):
        self.f_key = False
