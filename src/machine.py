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
