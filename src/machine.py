import tkinter as tk
from tkinter import font


class Reservoir:
    def __init__(self, capacity, volume, default_out_flow=5, name='', setting_delta=1):
        self.capacity = capacity  # total volume
        self.volume = volume  # current volume
        self.out_flow_set_value = default_out_flow
        self.out_flow = 0
        self.name = name
        self.setting_delta = setting_delta

    def update(self, previous_list, next_reservoir):
        # 流入後の液量の計算
        for prev in previous_list:
            self.volume += prev.out_flow

        # 流出量の計算
        # -> 自身の液量考慮
        if self.out_flow_set_value > self.volume:
            out_flow = self.volume
        else:
            out_flow = self.out_flow_set_value
        # -> 受け入れ側の液量考慮
        out_flow = next_reservoir.acceptable_volume(additional_volume=out_flow)

        # 流出後の液量
        self.volume -= out_flow
        self.out_flow = out_flow
        print(f'Reservoir({self.name}), Volume: {self.volume}, '
              f'SetFlow: {self.out_flow_set_value}, ActualFlow: {self.out_flow}')

    def acceptable_volume(self, additional_volume):
        if self.volume + additional_volume <= self.capacity:
            # 容量に余裕があれば、追加の容量はすべて受け入れ可能
            return additional_volume
        elif self.capacity == self.volume:
            # 容量が最大容量に到達していれば、受け入れ量は0
            return 0
        else:
            # 容量に余裕はないが、最大容量に達していない場合は最大までの量を返す
            return self.capacity - self.volume

    def set_flow_up(self, _):
        self.out_flow_set_value += self.setting_delta

    def set_flow_down(self, _):
        self.out_flow_set_value -= self.setting_delta


class ThreeStepsReservoir:
    def __init__(self):
        self.main_reservoir = Reservoir(1000, 800, default_out_flow=0, name='Main')
        self.reservoir1 = Reservoir(100, 70, default_out_flow=0, name='#1')
        self.reservoir2 = Reservoir(100, 50, default_out_flow=0, name='#2')
        self.reservoir3 = Reservoir(100, 30, default_out_flow=0, name='#3')

    def update(self):
        self.main_reservoir.update([], self.reservoir1)
        self.reservoir1.update([self.main_reservoir], self.reservoir2)
        self.reservoir2.update([self.reservoir1], self.reservoir3)
        self.reservoir3.update([self.reservoir2], self.main_reservoir)
        self.main_reservoir.volume += self.reservoir3.out_flow


class ReservoirViewer:
    def __init__(self, left, right, top, bottom):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

    def draw(self, can: tk.Canvas, reservoir: Reservoir):
        height = self.bottom - self.top
        water_top = self.top + height * (reservoir.capacity - reservoir.volume) / reservoir.capacity
        can.create_rectangle(self.left, self.top, self.right, self.bottom, fill='gray')
        can.create_rectangle(self.left, water_top, self.right, self.bottom, fill='blue')


class Meter:
    def __init__(self, x, y, width=5, height=1):
        self.left = x
        self.top = y
        self.width = width
        self.height = height

    def update(self, can: tk.Canvas, val):
        label = tk.Label(can, text=val, bg='black', fg='white', font=font.Font(size=20, weight='bold'),
                         width=self.width, height=self.height)
        label.place(x=self.left, y=self.top)


class ControlPanel:
    def __init__(self, can: tk.Canvas, x, y, name, width=90, height=170):
        self.name = name

        self.left = x
        self.right = x + width
        self.top = y
        self.left = y + height

        self.volume_meter = Meter(x + 20, y + 20)
        self.flow_meter = Meter(x + 20, y + 95)

        self.button_up = tk.Button(can, text='up')
        self.button_up.place(x=x+20, y=70, width=90, height=30)

        self.button_down = tk.Button(can, text='down')
        self.button_down.place(x=x+20, y=130, width=90, height=30)

    def update(self, can: tk.Canvas, reservoir: Reservoir):
        self.volume_meter.update(can, reservoir.volume)
        self.flow_meter.update(can, f'{reservoir.out_flow} / {reservoir.out_flow_set_value}')


class Application:
    def __init__(self):
        win = tk.Tk()
        win.title('Three steps reservoir')
        win.geometry('900x610')
        win.resizable(False, False)
        self.win = win

        # 三段水槽の初期化
        self.reservoir = ThreeStepsReservoir()

        # 液量描画用の画面の設定
        self.can_main = tk.Canvas(bg='white', width=470, height=400)
        self.can_main.place(x=10, y=10)

        # コントロールパネル用の画面の設定
        self.can_panel = tk.Canvas(bg='white', width=470, height=170)
        self.can_panel.place(x=10, y=420)

        # 水槽の様子を描画するクラスの設定
        self.rv0 = ReservoirViewer(20, 160, 20, 320)
        self.rv1 = ReservoirViewer(180, 250, 190, 340)
        self.rv2 = ReservoirViewer(270, 340, 210, 360)
        self.rv3 = ReservoirViewer(360, 430, 230, 380)

        # 水槽のパラメータを描画するコントロールパネルの設定
        self.main_panel = ControlPanel(self.can_panel, 30, 5, name='Main Reservoir')
        self.panel1 = ControlPanel(self.can_panel, 140, 5, name='Reservoir1')
        self.panel2 = ControlPanel(self.can_panel, 240, 5, name='Reservoir2')
        self.panel3 = ControlPanel(self.can_panel, 340, 5, name='Reservoir3')

        # ボタンの挙動の設定
        self.main_panel.button_up.bind('<Button-1>', self.reservoir.main_reservoir.set_flow_up)
        self.panel1.button_up.bind('<Button-1>', self.reservoir.reservoir1.set_flow_up)
        self.panel2.button_up.bind('<Button-1>', self.reservoir.reservoir2.set_flow_up)
        self.panel3.button_up.bind('<Button-1>', self.reservoir.reservoir3.set_flow_up)

        self.main_panel.button_down.bind('<Button-1>', self.reservoir.main_reservoir.set_flow_down)
        self.panel1.button_down.bind('<Button-1>', self.reservoir.reservoir1.set_flow_down)
        self.panel2.button_down.bind('<Button-1>', self.reservoir.reservoir2.set_flow_down)
        self.panel3.button_down.bind('<Button-1>', self.reservoir.reservoir3.set_flow_down)

    def loop(self):
        self.reservoir.update()

        self.rv0.draw(self.can_main, self.reservoir.main_reservoir)
        self.rv1.draw(self.can_main, self.reservoir.reservoir1)
        self.rv2.draw(self.can_main, self.reservoir.reservoir2)
        self.rv3.draw(self.can_main, self.reservoir.reservoir3)

        self.main_panel.update(self.can_panel, self.reservoir.main_reservoir)
        self.panel1.update(self.can_panel, self.reservoir.reservoir1)
        self.panel2.update(self.can_panel, self.reservoir.reservoir2)
        self.panel3.update(self.can_panel, self.reservoir.reservoir3)
        self.win.after(200, self.loop)

    def run(self):
        self.loop()
        self.win.mainloop()


if __name__ == '__main__':
    application = Application()
    application.run()
