from PIL import Image, ImageDraw, ImageFilter
import math


def create_avatar(
    expression="Neutral",
    style="Anime Girl",
    action="Idle",
    size=(400, 500),
):
    W, H = 400, 500

    girl = style == "Anime Girl"

    # ---------- BACKGROUND ----------
    img = Image.new("RGB", (W, H))
    pixels = img.load()

    top = (30, 24, 65) if girl else (20, 38, 75)
    bottom = (111, 66, 128) if girl else (42, 115, 145)

    for y in range(H):
        t = y / H
        color = tuple(
            int(top[i] * (1 - t) + bottom[i] * t)
            for i in range(3)
        )
        for x in range(W):
            pixels[x, y] = color

    draw = ImageDraw.Draw(img)

    # Background decoration
    for x, y, r in [
        (42, 80, 3), (350, 65, 4), (335, 180, 2),
        (55, 225, 3), (320, 300, 3), (75, 330, 2),
        (275, 90, 2), (95, 145, 2)
    ]:
        draw.ellipse((x-r, y-r, x+r, y+r), fill="#F7DFFF")

    # ---------- COLORS ----------
    hair = "#40203D" if girl else "#18243F"
    hair_light = "#75446C" if girl else "#354D78"
    skin = "#F5C9AC"
    skin_shadow = "#DFA88F"
    eye_color = "#7549B5" if girl else "#398BC5"
    outfit = "#D85D9B" if girl else "#397FC2"
    outfit_dark = "#863B79" if girl else "#214D86"
    white = "#FFF8FF"

    # ---------- SOFT SHADOW ----------
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse((85, 440, 315, 475), fill=(12, 8, 30, 75))
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))
    img = Image.alpha_composite(img.convert("RGBA"), shadow)
    draw = ImageDraw.Draw(img)

    # ---------- ACTION POSES ----------
    if action == "Wave":
        draw.line(
            [(235, 365), (282, 325), (300, 260)],
            fill=skin, width=25
        )
        draw.ellipse((286, 230, 315, 266), fill=skin)
        draw.line(
            [(298, 242), (288, 215)],
            fill=skin, width=8
        )
        draw.line(
            [(302, 240), (307, 213)],
            fill=skin, width=8
        )
        draw.line(
            [(307, 243), (325, 225)],
            fill=skin, width=8
        )

    elif action == "Dance":
        draw.line(
            [(150, 365), (95, 325), (70, 285)],
            fill=skin, width=25
        )
        draw.ellipse((58, 270, 82, 294), fill=skin)
        draw.line(
            [(245, 365), (300, 325), (330, 300)],
            fill=skin, width=25
        )
        draw.ellipse((319, 286, 342, 309), fill=skin)

    else:
        draw.line(
            [(155, 365), (110, 405)],
            fill=skin, width=25
        )
        draw.line(
            [(245, 365), (290, 405)],
            fill=skin, width=25
        )

    # ---------- BODY / OUTFIT ----------
    draw.ellipse((105, 345, 295, 555), fill=outfit_dark)
    draw.polygon(
        [(160, 340), (240, 340), (300, 500), (100, 500)],
        fill=outfit
    )

    # Outfit details
    draw.polygon(
        [(170, 350), (200, 390), (230, 350)],
        fill=white
    )
    draw.line((200, 390, 200, 480), fill=outfit_dark, width=3)

    if girl:
        draw.polygon(
            [(125, 440), (275, 440), (310, 500), (90, 500)],
            fill="#F08ABA"
        )
        for x in [135, 165, 195, 225, 255]:
            draw.line((x, 450, x-8, 495), fill="#FFD5EC", width=2)

    # Neck
    draw.rectangle((174, 315, 226, 375), fill=skin)
    draw.ellipse((174, 342, 226, 375), fill=skin_shadow)

    # ---------- HAIR BACK LAYER ----------
    if girl:
        draw.ellipse((95, 65, 305, 335), fill=hair)
        draw.polygon(
            [(105, 170), (100, 320), (135, 390),
             (165, 340), (150, 205)],
            fill=hair
        )
        draw.polygon(
            [(270, 170), (300, 315), (270, 385),
             (235, 335), (250, 205)],
            fill=hair
        )
    else:
        draw.ellipse((105, 65, 295, 290), fill=hair)
        draw.polygon(
            [(110, 145), (95, 235), (135, 285), (150, 175)],
            fill=hair
        )
        draw.polygon(
            [(280, 140), (300, 220), (270, 280), (250, 170)],
            fill=hair
        )

    # Hair shine
    draw.arc(
        (112, 80, 285, 260),
        start=195, end=290, fill=hair_light, width=8
    )

    # ---------- FACE ----------
    draw.ellipse((123, 100, 277, 315), fill=skin)

    # Ears
    draw.ellipse((112, 190, 137, 235), fill=skin)
    draw.ellipse((263, 190, 288, 235), fill=skin)

    # Face shading
    draw.ellipse((135, 270, 265, 317), fill=skin_shadow)
    draw.ellipse((137, 263, 263, 309), fill=skin)

    # ---------- EYES ----------
    eye_y = 202

    if expression == "Blinking" or expression == "Sleepy":
        draw.arc(
            (143, eye_y-5, 183, eye_y+14),
            start=0, end=180, fill="#44283A", width=4
        )
        draw.arc(
            (217, eye_y-5, 257, eye_y+14),
            start=0, end=180, fill="#44283A", width=4
        )
    else:
        eye_height = 31 if expression == "Surprised" else 25

        for cx in [163, 237]:
            draw.ellipse(
                (cx-21, eye_y-eye_height, cx+21, eye_y+eye_height),
                fill=white
            )
            draw.ellipse(
                (cx-14, eye_y-18, cx+14, eye_y+22),
                fill=eye_color
            )
            draw.ellipse(
                (cx-9, eye_y-13, cx+9, eye_y+15),
                fill="#211A42"
            )
            draw.ellipse(
                (cx-8, eye_y-15, cx-1, eye_y-7),
                fill="white"
            )
            draw.ellipse(
                (cx+4, eye_y+6, cx+9, eye_y+12),
                fill="#D7F6FF"
            )

            draw.arc(
                (cx-23, eye_y-eye_height-4,
                 cx+23, eye_y+eye_height+4),
                start=180, end=350,
                fill="#38223C", width=4
            )

    # Eyebrows
    if expression in ["Surprised", "Curious"]:
        brow_y = 155
    elif expression in ["Sad", "Confused"]:
        brow_y = 170
    else:
        brow_y = 178

    draw.line(
        (143, brow_y, 180, brow_y-4),
        fill=hair, width=5
    )
    draw.line(
        (220, brow_y-4, 257, brow_y),
        fill=hair, width=5
    )

    # ---------- BLUSH ----------
    blush = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(blush)
    bd.ellipse((137, 235, 166, 248), fill=(255, 105, 145, 100))
    bd.ellipse((234, 235, 263, 248), fill=(255, 105, 145, 100))
    blush = blush.filter(ImageFilter.GaussianBlur(4))
    img = Image.alpha_composite(img, blush)
    draw = ImageDraw.Draw(img)

    # ---------- NOSE ----------
    draw.line((199, 224, 195, 233), fill=skin_shadow, width=2)

    # ---------- MOUTH / EXPRESSION ----------
    if expression in ["Happy", "Laughing"]:
        draw.arc(
            (177, 235, 223, 270),
            start=0, end=180, fill="#8D354D", width=4
        )
        if expression == "Laughing":
            draw.ellipse((184, 247, 216, 266), fill="#7D253F")
            draw.arc(
                (185, 246, 215, 262),
                start=0, end=180, fill=white, width=3
            )

    elif expression in ["Surprised", "Talking"]:
        mouth_box = (186, 239, 214, 265)
        draw.ellipse(
            mouth_box,
            fill="#7D253F" if expression == "Talking" else "#8D354D"
        )
        if expression == "Talking":
            draw.arc(
                (190, 242, 210, 254),
                start=0, end=180, fill="#F6A3B5", width=3
            )

    elif expression in ["Sad", "Crying"]:
        draw.arc(
            (180, 251, 220, 276),
            start=180, end=350, fill="#8D354D", width=4
        )
        draw.ellipse((150, 218, 158, 239), fill="#7DDFFF")
        draw.ellipse((244, 218, 252, 239), fill="#7DDFFF")

    elif expression == "Angry":
        draw.line((183, 254, 217, 254), fill="#8D354D", width=4)

    elif expression == "Confused":
        draw.arc(
            (183, 245, 218, 270),
            start=190, end=330, fill="#8D354D", width=4
        )

    else:
        draw.line((187, 254, 213, 254), fill="#8D354D", width=3)

    # ---------- HAIR FRINGE ----------
    if girl:
        draw.pieslice(
            (112, 70, 288, 235),
            start=180, end=360, fill=hair
        )
        draw.polygon(
            [(115, 150), (145, 105), (170, 178),
             (190, 115), (220, 177), (250, 108),
             (285, 160), (272, 185), (240, 166),
             (218, 200), (190, 171), (163, 201),
             (140, 166), (121, 190)],
            fill=hair
        )
        draw.line((140, 115, 160, 155), fill=hair_light, width=5)
        draw.line((225, 112, 238, 151), fill=hair_light, width=5)
    else:
        draw.pieslice(
            (112, 65, 288, 220),
            start=180, end=360, fill=hair
        )
        draw.polygon(
            [(115, 145), (132, 85), (165, 125),
             (183, 65), (210, 112), (245, 75),
             (281, 145), (250, 160), (228, 145),
             (205, 173), (180, 145), (151, 170)],
            fill=hair
        )
        draw.line((147, 103, 163, 132), fill=hair_light, width=5)
        draw.line((222, 99, 239, 128), fill=hair_light, width=5)

    # Girl hair accessory
    if girl:
        draw.ellipse((248, 112, 280, 145), fill="#FF8BC4")
        draw.ellipse((258, 118, 272, 137), fill="#FFD9ED")
        draw.ellipse((258, 124, 270, 136), fill="#FFB5DA")

    # ---------- FINAL RENDER ----------
    img = img.convert("RGB")
    img = img.resize(size, Image.Resampling.LANCZOS)

    return img
