
from PIL import Image, ImageDraw


EXPRESSIONS = {
    "Neutral", "Happy", "Blinking", "Surprised",
    "Angry", "Sad", "Confused", "Laughing",
    "Talking", "Sleepy",
}

ACTIONS = {"Idle", "Wave", "Dance", "Cry", "Talk"}


def create_avatar(
    expression="Neutral",
    style="Anime Girl",
    action="Idle",
    size=(400, 500),
):
    width, height = size
    girl = style == "Anime Girl"

    expression = expression if expression in EXPRESSIONS else "Neutral"
    action = action if action in ACTIONS else "Idle"

    image = Image.new("RGB", size, (25, 20, 43))
    draw = ImageDraw.Draw(image)

    skin = (255, 220, 194)
    outline = (65, 39, 57)
    hair = (74, 35, 93) if girl else (39, 45, 76)
    outfit = (157, 75, 190) if girl else (56, 117, 190)
    eye_color = (67, 112, 210)

    # Hair behind the face
    draw.ellipse((75, 40, 325, 340), fill=hair)

    if girl:
        # Long hair
        draw.rounded_rectangle(
            (80, 120, 125, 345), radius=22, fill=hair
        )
        draw.rounded_rectangle(
            (275, 120, 320, 345), radius=22, fill=hair
        )
    else:
        # Shorter side hair
        draw.ellipse((90, 55, 310, 225), fill=hair)

    # Neck and shoulders
    draw.rectangle((170, 290, 230, 365), fill=skin)

    draw.polygon(
        [(170, 330), (230, 330), (325, 480), (75, 480)],
        fill=outfit,
        outline=outline,
    )

    # Arms: actions change the arm pose
    if action == "Wave":
        draw.line(
            [(110, 360), (75, 300), (95, 230)],
            fill=skin, width=23
        )
        draw.line(
            [(290, 360), (325, 405)],
            fill=skin, width=23
        )
        draw.ellipse((80, 205, 110, 240), fill=skin)

    elif action == "Dance":
        draw.line(
            [(115, 360), (80, 300), (115, 245)],
            fill=skin, width=23
        )
        draw.line(
            [(285, 360), (320, 300), (285, 245)],
            fill=skin, width=23
        )
        draw.ellipse((100, 225, 130, 255), fill=skin)
        draw.ellipse((270, 225, 300, 255), fill=skin)

    else:
        draw.line(
            [(115, 365), (85, 435)],
            fill=skin, width=23
        )
        draw.line(
            [(285, 365), (315, 435)],
            fill=skin, width=23
        )

    # Face
    draw.ellipse(
        (105, 75, 295, 310),
        fill=skin,
        outline=outline,
        width=3,
    )

    # Fringe
    draw.pieslice(
        (95, 35, 305, 190),
        start=180,
        end=360,
        fill=hair,
    )

    if not girl:
        # Extra pointed fringe for the boy style
        draw.polygon(
            [(105, 120), (125, 65), (155, 112),
             (185, 48), (210, 112), (245, 62),
             (270, 120)],
            fill=hair,
        )

    # Eyebrows
    brow_y = 140

    if expression in ("Surprised", "Confused"):
        brow_y = 122

    if expression == "Angry":
        draw.line((130, 137, 172, 150), fill=outline, width=6)
        draw.line((228, 150, 270, 137), fill=outline, width=6)
    else:
        draw.line((132, brow_y, 173, brow_y), fill=outline, width=5)
        draw.line((227, brow_y, 268, brow_y), fill=outline, width=5)

    # Eyes
    if expression in ("Blinking", "Sleepy"):
        eye_y = 177 if expression == "Blinking" else 185
        draw.line((133, eye_y, 173, eye_y), fill=outline, width=5)
        draw.line((227, eye_y, 267, eye_y), fill=outline, width=5)
    else:
        eye_height = 43 if expression == "Surprised" else 35

        draw.ellipse(
            (132, 153, 174, 153 + eye_height),
            fill="white", outline=outline, width=2
        )
        draw.ellipse(
            (226, 153, 268, 153 + eye_height),
            fill="white", outline=outline, width=2
        )

        draw.ellipse((143, 160, 163, 190), fill=eye_color)
        draw.ellipse((237, 160, 257, 190), fill=eye_color)
        draw.ellipse((149, 164, 157, 174), fill="white")
        draw.ellipse((243, 164, 251, 174), fill="white")

    # Cheeks
    if expression in ("Happy", "Laughing"):
        draw.ellipse((115, 207, 145, 221), fill=(245, 145, 155))
        draw.ellipse((255, 207, 285, 221), fill=(245, 145, 155))

    # Mouth
    if expression in ("Happy", "Laughing"):
        draw.arc(
            (165, 215, 235, 265),
            start=0, end=180,
            fill=(150, 35, 55), width=5
        )
        if expression == "Laughing":
            draw.ellipse((180, 231, 220, 257), fill=(135, 35, 60))

    elif expression in ("Surprised", "Talking") or action == "Talk":
        draw.ellipse(
            (184, 225, 216, 260),
            fill=(120, 30, 48),
            outline=outline,
        )

    elif expression == "Sad" or action == "Cry":
        draw.arc(
            (170, 238, 230, 278),
            start=190, end=350,
            fill=(130, 45, 65), width=5
        )

    elif expression == "Angry":
        draw.line((177, 245, 223, 238), fill=(120, 35, 45), width=5)

    elif expression == "Confused":
        draw.line((180, 243, 218, 237), fill=(120, 45, 55), width=4)

    else:
        draw.line((180, 242, 220, 242), fill=(130, 55, 65), width=4)

    # Tears for Cry action
    if action == "Cry" or expression == "Sad":
        draw.ellipse((143, 193, 153, 215), fill=(90, 190, 255))
        draw.ellipse((247, 193, 257, 215), fill=(90, 190, 255))

    # Action label
    label = action.upper()
    draw.rounded_rectangle(
        (115, 450, 285, 485),
        radius=12,
        fill=(43, 33, 65),
    )
    draw.text((200, 467), label, fill="white", anchor="mm")

    return image