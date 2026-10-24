
def analyze_expressions(blendshapes: dict) -> dict:
    """
    Convert MediaPipe face blendshape scores into
    simple expression signals for EMOTUNE.
    Scores generally range from 0.0 to 1.0.
    """

    def score(name):
        return float(blendshapes.get(name, 0.0))

    left_blink = score("eyeBlinkLeft")
    right_blink = score("eyeBlinkRight")

    blink = (left_blink + right_blink) / 2

    smile = (
        score("mouthSmileLeft")
        + score("mouthSmileRight")
    ) / 2

    mouth_open = (
        score("jawOpen")
        + score("mouthOpen")
    ) / 2

    brow_raise = (
        score("browInnerUp")
        + score("browOuterUpLeft")
        + score("browOuterUpRight")
    ) / 3

    if blink > 0.55:
        expression = "Blinking"
    elif smile > 0.55:
        expression = "Happy"
    elif mouth_open > 0.55:
        expression = "Surprised"
    elif brow_raise > 0.55:
        expression = "Curious"
    else:
        expression = "Neutral"

    return {
        "expression": expression,
        "blink": round(blink, 3),
        "smile": round(smile, 3),
        "mouth_open": round(mouth_open, 3),
        "brow_raise": round(brow_raise, 3),
    }