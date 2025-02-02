import random
import re
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register

@register("dnd_dice", "Your Name", "一个 DnD 骰子插件，支持格式 xdY 和检定功能", "1.0.0")
class DicePlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
    
    # 注册指令 /roll  <次数>d<面数> <检定阈值> <是否单独检定>
    @filter.command("roll")
    async def roll_dice(self, event: AstrMessageEvent, dice: str = "1d6", threshold: int = 3, check_single_mode: bool = False):
        """
        掷骰子的逻辑，支持格式 xdy (默认 1d6) 和阈值。
        check_single_mode：如果为 True，分别计算每次投掷的检定成功与否。
        """
        # 解析 xdy 格式的骰子 默认值为 1d6
        roll_count, die_faces = map(int, dice.lower().split('d'))

        # 投掷骰子 默认值为 3
        rolls = [random.randint(1, die_faces) for _ in range(roll_count)]
        success_count = sum(1 for roll in rolls if roll >= threshold)
        total_sum = sum(rolls)

        # 根据 check_single_mode 参数判断检定方式
        if check_single_mode :
            # 使用单个骰子进行检定
            result_message = f"你投掷了 {roll_count} 次 {die_faces} 面骰子，结果: {', '.join(map(str, rolls))}。\n"
            result_message += f"检定成功的次数: {success_count}/{roll_count} 次\n"
            if success_count > 0:
                result_message += f"你有 {success_count} 次成功检定！"
            else:
                result_message += "很遗憾，你没有成功的检定。"
        else:
            # 使用总和进行检定
            success = total_sum >= threshold
            result_message = f"你投掷了 {roll_count} 次 {die_faces} 面骰子，结果: {', '.join(map(str, rolls))}。\n"
            result_message += f"所有骰子的总和为: {total_sum}。\n"
            result_message += f"检定结果: {'成功' if success else '失败'}\n"

        # 发送结果
        yield event.plain_result(result_message)
    
    # 注册指令 /dicehelp
    @filter.command("dicehelp")
        # 发送帮助信息
        yield event.plain_result(
            "输入/roll xdy <threshold> <check_single_mode>即可开始投掷，x代表投掷次数，y代表面数，threshold代表检定阈值, check_single_mode代表是否分别计算每次投掷的检定成功与否，False代表将所有投掷结果相加并进行总和检定，True代表分别计算每次投掷的检定。 默认值为 1d6 3 False，即/roll = /roll 1d6 3 False"
        )
