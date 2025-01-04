class CPU:
    def __init__(self):
        # 初始化流水线寄存器
        self.IF_ID = {}
        self.ID_EX = {}
        self.EX_MEM = {}
        self.MEM_WB = {}

        # 初始化控制信号
        self.stall = False
        self.forwarding_signals = {
            "EX_to_ID": None,
            "MEM_to_ID": None,
            "EX_to_EX": None,
            "MEM_to_EX": None,
        }

    def detect_hazard(self):
        """
        检测数据冒险，并设置停顿或转发信号。
        """
        self.stall = False

        # 检测 LOAD-USE 冒险（MEM 阶段 -> EX 阶段的依赖）
        if self.ID_EX.get("opcode") == "LOAD":
            if self.ID_EX.get("destination") in [self.IF_ID.get("source1"), self.IF_ID.get("source2")]:
                self.stall = True

        # 设置转发信号
        self.forwarding_signals["EX_to_EX"] = self._check_forwarding(self.EX_MEM, self.ID_EX)
        self.forwarding_signals["MEM_to_EX"] = self._check_forwarding(self.MEM_WB, self.ID_EX)

    def _check_forwarding(self, producer_stage, consumer_stage):
        """
        检查两个流水线阶段之间是否可以进行数据转发。
        """
        if producer_stage.get("destination") and producer_stage.get("destination") in [
            consumer_stage.get("source1"),
            consumer_stage.get("source2"),
        ]:
            return producer_stage.get("destination")
        return None

    def execute_cycle(self):
        """
        模拟流水线的单个时钟周期，包括冒险检测和转发。
        """
        self.detect_hazard()

        if self.stall:
            print("由于数据冒险，流水线暂停。")
            # 在流水线中插入一个气泡
            self.ID_EX = {}
        else:
            # 如果需要，执行转发
            if self.forwarding_signals["EX_to_EX"]:
                print(f"从 EX 到 EX 的转发：{self.forwarding_signals['EX_to_EX']}")
            if self.forwarding_signals["MEM_to_EX"]:
                print(f"从 MEM 到 EX 的转发：{self.forwarding_signals['MEM_to_EX']}")

        # 更新流水线寄存器（为简化起见）
        self.MEM_WB = self.EX_MEM
        self.EX_MEM = self.ID_EX
        self.ID_EX = self.IF_ID
        self.IF_ID = self.fetch_next_instruction()

    def fetch_next_instruction(self):
        """
        获取下一条指令（模拟）。
        """
        return {}

# 测试案例
def test_forwarding_and_stalling():
    cpu = CPU()

    # 模拟具有依赖关系的指令
    cpu.IF_ID = {"opcode": "ADD", "source1": "R1", "source2": "R2", "destination": "R3"}
    cpu.ID_EX = {"opcode": "LOAD", "source1": "R4", "source2": None, "destination": "R1"}
    cpu.EX_MEM = {"opcode": "ADD", "source1": "R5", "source2": "R6", "destination": "R4"}
    cpu.MEM_WB = {"opcode": "SUB", "source1": "R7", "source2": "R8", "destination": "R9"}

    cpu.execute_cycle()

if __name__ == "__main__":
    test_forwarding_and_stalling()
