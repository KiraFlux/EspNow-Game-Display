def get_text_color(bg_color: str) -> str:
    """Определение цвета текста на основе фона"""
    r = int(bg_color[1:3], 16)
    g = int(bg_color[3:5], 16)
    b = int(bg_color[5:7], 16)
    brightness = (r * 299 + g * 587 + b * 114) / 1000
    return "#000000" if brightness > 128 else "#FFFFFF"


def adjust_color(color: str, amount: int) -> str:
    """Осветление или затемнение цвета"""
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)

    r = min(255, max(0, r + amount))
    g = min(255, max(0, g + amount))
    b = min(255, max(0, b + amount))

    return f"#{r:02x}{g:02x}{b:02x}"


def get_team_color(team: int) -> str:
    colors = {
        1: "#FF6B6B",
        2: "#4ECDC4",
        3: "#45B7D1",
        4: "#FFBE0B",
        5: "#FB5607",
        6: "#8338EC",
        7: "#3A86FF",
        8: "#06D6A0",
        9: "#118AB2",
        10: "#073B4C",
        11: "#EF476F",
        12: "#FFD166",
        13: "#8AC926",
        14: "#7209B7",
        15: "#F15BB5",
        16: "#9B5DE5",
        17: "#00BBF9",
        18: "#00F5D4",
        19: "#FEE440",
        20: "#9B2226",
    }

    return colors.get(team)
