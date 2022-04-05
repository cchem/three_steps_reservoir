import tkinter as tk


class Reservoir:
    def __init__(self, capacity, volume, default_out_flow=5, name=''):
        self.capacity = capacity  # total volume
        self.volume = volume  # current volume
        self.out_flow_set_value = default_out_flow
        self.out_flow = 0
        self.delta = 5
        self.name = name

    def update(self, previous_list, key_press_up, key_press_down, next_reservoir):
        # 流入後の液量の計算
        for prev in previous_list:
            self.volume += prev.out_flow

        # 設定流量の変更
        if key_press_up:
            self.out_flow_set_value += self.delta
        if key_press_down:
            self.out_flow_set_value -= self.delta

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
            # 容量に余裕はないが、最大容量に達してい無い場合は最大までの量を返す
            return self.capacity - self.volume


class ThreeStepsReservoir:
    def __init__(self):
        self.main_reservoir = Reservoir(1000, 800, default_out_flow=4, name='Main')
        self.reservoir1 = Reservoir(100, 70, default_out_flow=3, name='#1')
        self.reservoir2 = Reservoir(100, 50, default_out_flow=5, name='#2')
        self.reservoir3 = Reservoir(100, 30, default_out_flow=2, name='#3')

    def update(self, up0, down0, up1, down1, up2, down2, up3, down3):
        self.main_reservoir.update([], up0, down0, self.reservoir1)
        self.reservoir1.update([self.main_reservoir], up1, down1, self.reservoir2)
        self.reservoir2.update([self.reservoir1], up2, down2, self.reservoir3)
        self.reservoir3.update([self.reservoir2], up3, down3, self.main_reservoir)
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


class Application:
    def __init__(self):
        win = tk.Tk()
        win.title('Three steps reservoir')
        win.geometry('640x512')
        win.resizable(False, False)
        self.win = win

        can = tk.Canvas(bg='white', width=620, height=492)
        can.place(x=10, y=10)
        self.can = can

        self.reservoir = ThreeStepsReservoir()

        self.up0 = False
        self.down0 = False
        self.up1 = False
        self.down1 = False
        self.up2 = False
        self.down2 = False
        self.up3 = False
        self.down3 = False

        self.rv0 = ReservoirViewer(20, 160, 20, 320)
        self.rv1 = ReservoirViewer(180, 250, 190, 340)
        self.rv2 = ReservoirViewer(270, 340, 210, 360)
        self.rv3 = ReservoirViewer(360, 430, 230, 380)

    def loop(self):
        print('loop')
        self.reservoir.update(self.up0, self.down0, self.up1, self.down1, self.up2, self.down2, self.up3, self.down3)

        self.rv0.draw(self.can_main, self.reservoir.main_reservoir)
        self.rv1.draw(self.can_main, self.reservoir.reservoir1)
        self.rv2.draw(self.can_main, self.reservoir.reservoir2)
        self.rv3.draw(self.can_main, self.reservoir.reservoir3)
        self.win.after(200, self.loop)

    def run(self):
        self.loop()
        self.win.mainloop()


if __name__ == '__main__':
    application = Application()
    application.run()
