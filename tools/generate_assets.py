"""Generate Tidekeeper's original pixel-inspired PNG artwork once."""

from pathlib import Path
import math
import random
import sys

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1] / "assets"
INK = (17, 43, 57, 255)


def save(image: Image.Image, category: str, name: str) -> None:
    path = ROOT / category / f"{name}.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True)
    print(f"Created {path.relative_to(ROOT.parent)} ({image.width}x{image.height})")


def outlined_fish(
    name: str,
    body: tuple[int, int, int],
    light: tuple[int, int, int],
    accent: tuple[int, int, int],
    species: str,
) -> None:
    image = Image.new("RGBA", (104, 72))
    draw = ImageDraw.Draw(image)
    tail = [(21, 35), (5, 19), (9, 35), (5, 53)]
    silhouette = [(18, 35), (29, 19), (48, 13), (68, 19), (84, 31), (94, 35), (83, 40), (67, 54), (45, 58), (28, 51)]
    draw.polygon(tail, fill=INK)
    draw.polygon([(x + 2, y) for x, y in tail], fill=accent)
    draw.polygon(silhouette, fill=INK)
    draw.polygon([(x + 3, y + 3) for x, y in silhouette], fill=body)
    draw.polygon([(34, 23), (47, 17), (63, 21), (75, 28), (57, 29), (41, 28)], fill=light)
    draw.polygon([(49, 16), (57, 5), (69, 20)], fill=INK)
    draw.polygon([(53, 17), (58, 10), (65, 20)], fill=accent)
    draw.polygon([(48, 52), (58, 66), (68, 52)], fill=INK)
    draw.polygon([(53, 52), (58, 60), (64, 52)], fill=accent)
    draw.polygon([(51, 34), (62, 45), (42, 43)], fill=INK)
    draw.polygon([(53, 35), (59, 42), (47, 41)], fill=light)
    if species == "snapper":
        draw.line((36, 25, 35, 47), fill=(255, 187, 125, 255), width=3)
        draw.line((45, 20, 44, 51), fill=(255, 187, 125, 255), width=2)
        draw.line((66, 24, 64, 48), fill=(255, 187, 125, 255), width=2)
        draw.ellipse((76, 29, 81, 34), fill=(255, 214, 145, 255))
    elif species == "tang":
        draw.polygon([(77, 23), (88, 33), (84, 39), (76, 47)], fill=(249, 215, 84, 255))
        draw.ellipse((73, 28, 78, 33), fill=(250, 245, 205, 255))
        draw.ellipse((75, 29, 77, 31), fill=INK)
        draw.line((35, 24, 34, 49), fill=(39, 100, 195, 255), width=3)
    else:
        for x in (37, 47, 58, 69):
            draw.line((x, 21, x - 3, 50), fill=(255, 205, 83, 255), width=4)
        draw.polygon([(35, 19), (47, 12), (55, 20)], fill=(253, 221, 113, 255))
        draw.ellipse((77, 29, 82, 34), fill=(255, 236, 162, 255))
    draw.ellipse((79, 29, 82, 32), fill=INK)
    draw.line((84, 37, 89, 37), fill=(255, 239, 205, 255), width=2)
    draw.ellipse((24, 29, 28, 33), fill=light)
    save(image, "fish", name)


def make_diver() -> None:
    image = Image.new("RGBA", (128, 88))
    draw = ImageDraw.Draw(image)
    # Fins and legs
    draw.polygon([(32, 46), (22, 53), (11, 49), (3, 54), (15, 64), (39, 59), (49, 51)], fill=INK)
    draw.polygon([(31, 48), (22, 54), (12, 51), (7, 55), (17, 60), (39, 56)], fill=(247, 116, 98, 255))
    draw.polygon([(42, 51), (30, 63), (17, 62), (10, 68), (25, 73), (51, 61), (56, 52)], fill=INK)
    draw.polygon([(42, 53), (31, 64), (19, 64), (15, 68), (26, 70), (50, 59)], fill=(255, 155, 105, 255))
    # Tank and harness
    draw.rounded_rectangle((42, 20, 64, 60), radius=8, fill=INK)
    draw.rounded_rectangle((46, 21, 61, 56), radius=6, fill=(152, 208, 204, 255))
    draw.rectangle((50, 25, 53, 51), fill=(205, 244, 226, 255))
    draw.rectangle((46, 31, 61, 35), fill=(102, 166, 172, 255))
    draw.line((63, 28, 68, 35, 67, 45), fill=(39, 71, 85, 255), width=3)
    # Suit body, arms, gloves
    draw.polygon([(52, 31), (62, 25), (79, 28), (91, 37), (87, 46), (72, 48), (63, 56), (49, 50)], fill=INK)
    draw.polygon([(56, 32), (64, 29), (78, 31), (87, 37), (83, 42), (70, 44), (62, 52), (53, 48)], fill=(244, 149, 90, 255))
    draw.line((67, 36, 84, 31, 101, 33), fill=INK, width=11)
    draw.line((68, 36, 84, 32, 101, 34), fill=(244, 149, 90, 255), width=6)
    draw.ellipse((98, 28, 109, 39), fill=INK)
    draw.ellipse((100, 30, 108, 37), fill=(215, 226, 199, 255))
    draw.line((61, 45, 76, 51, 92, 50), fill=INK, width=9)
    draw.line((62, 45, 76, 50, 92, 49), fill=(214, 128, 84, 255), width=5)
    draw.ellipse((88, 45, 98, 54), fill=(215, 226, 199, 255))
    # Hood, mask, visor highlights, and regulator
    draw.ellipse((77, 17, 111, 48), fill=INK)
    draw.ellipse((80, 19, 108, 45), fill=(244, 149, 90, 255))
    draw.rounded_rectangle((88, 23, 110, 38), radius=6, fill=(14, 45, 67, 255))
    draw.rounded_rectangle((91, 25, 107, 35), radius=4, fill=(82, 207, 218, 255))
    draw.line((94, 27, 102, 27), fill=(213, 252, 235, 255), width=2)
    draw.ellipse((85, 38, 91, 44), fill=(231, 231, 190, 255))
    draw.line((86, 42, 78, 47, 72, 46), fill=(232, 215, 167, 255), width=2)
    # Small control panel and suit seams
    draw.rounded_rectangle((59, 39, 69, 47), radius=2, fill=(21, 79, 99, 255))
    draw.rectangle((62, 41, 65, 44), fill=(113, 239, 197, 255))
    draw.line((56, 48, 62, 52), fill=(255, 210, 139, 255), width=2)
    save(image, "player", "diver")


def make_dolphin() -> None:
    image = Image.new("RGBA", (136, 82))
    draw = ImageDraw.Draw(image)
    body = [(15, 43), (27, 27), (52, 19), (77, 20), (101, 29), (119, 35), (132, 38), (120, 44), (105, 51), (78, 58), (48, 57), (27, 52)]
    draw.polygon([(x, y + 8) for x, y in body], fill=INK)
    draw.polygon(body, fill=(85, 157, 178, 255))
    draw.polygon([(31, 43), (50, 47), (75, 49), (103, 42), (112, 43), (95, 53), (70, 57), (45, 54)], fill=(196, 224, 213, 255))
    draw.polygon([(66, 24), (79, 4), (88, 25)], fill=INK)
    draw.polygon([(70, 23), (79, 10), (84, 24)], fill=(73, 127, 151, 255))
    draw.polygon([(64, 53), (54, 74), (82, 60)], fill=INK)
    draw.polygon([(66, 54), (59, 68), (77, 59)], fill=(89, 149, 162, 255))
    draw.polygon([(113, 35), (134, 28), (127, 41), (134, 47), (114, 44)], fill=INK)
    draw.ellipse((105, 33, 110, 38), fill=(243, 229, 193, 255))
    draw.ellipse((107, 34, 109, 36), fill=INK)
    draw.line((119, 41, 130, 40), fill=(38, 72, 88, 255), width=2)
    draw.line((41, 29, 70, 25), fill=(152, 204, 208, 255), width=2)
    save(image, "animals", "bottlenose_dolphin")


def make_turtle() -> None:
    image = Image.new("RGBA", (112, 100))
    draw = ImageDraw.Draw(image)
    # Four paddle-like flippers and a small head.
    for points in (
        [(40, 43), (22, 24), (13, 29), (21, 51), (35, 58)],
        [(69, 42), (84, 21), (95, 27), (88, 50), (75, 58)],
        [(39, 58), (20, 73), (26, 86), (47, 71)],
        [(69, 59), (87, 75), (81, 88), (62, 72)],
    ):
        draw.polygon(points, fill=INK)
        draw.polygon([(x, y - 2) for x, y in points], fill=(90, 164, 127, 255))
        draw.line(points[:3], fill=(155, 203, 147, 255), width=2)
    draw.ellipse((79, 42, 108, 67), fill=INK)
    draw.ellipse((82, 44, 104, 64), fill=(129, 184, 125, 255))
    draw.ellipse((98, 49, 102, 53), fill=INK)
    draw.ellipse((34, 34, 79, 74), fill=INK)
    draw.ellipse((38, 36, 75, 69), fill=(51, 115, 91, 255))
    draw.ellipse((42, 39, 71, 66), fill=(100, 150, 96, 255))
    for points in (
        [(56, 39), (48, 47), (52, 57), (61, 63), (69, 55), (66, 45), (56, 39)],
        [(42, 43), (49, 47), (48, 57), (42, 62)],
        [(70, 43), (65, 48), (67, 57), (72, 62)],
    ):
        draw.line(points, fill=(36, 86, 76, 255), width=2, joint="curve")
    draw.ellipse((46, 43, 50, 47), fill=(172, 191, 118, 255))
    draw.ellipse((61, 57, 65, 61), fill=(172, 191, 118, 255))
    save(image, "animals", "green_sea_turtle")


def make_shark() -> None:
    image = Image.new("RGBA", (136, 82))
    draw = ImageDraw.Draw(image)
    body = [(12, 43), (28, 30), (54, 24), (82, 29), (104, 36), (130, 40), (112, 47), (92, 55), (61, 58), (34, 54)]
    draw.polygon([(x, y + 7) for x, y in body], fill=INK)
    draw.polygon(body, fill=(91, 130, 148, 255))
    draw.polygon([(51, 28), (66, 5), (82, 30)], fill=INK)
    draw.polygon([(57, 27), (67, 11), (76, 29)], fill=(66, 103, 124, 255))
    draw.polygon([(58, 53), (73, 74), (80, 53)], fill=INK)
    draw.polygon([(63, 53), (73, 67), (76, 53)], fill=(72, 113, 130, 255))
    draw.polygon([(29, 46), (17, 63), (47, 54)], fill=INK)
    draw.polygon([(100, 35), (132, 28), (122, 42), (133, 51), (101, 47)], fill=INK)
    draw.polygon([(30, 47), (56, 49), (86, 45), (107, 44), (91, 55), (58, 59), (36, 54)], fill=(205, 218, 208, 255))
    draw.line((93, 46, 101, 47), fill=(44, 68, 78, 255), width=2)
    draw.ellipse((101, 36, 106, 41), fill=(239, 230, 194, 255))
    draw.ellipse((103, 37, 105, 39), fill=INK)
    for x in (91, 97, 103):
        draw.line((x, 49, x + 3, 52), fill=(61, 84, 93, 255), width=1)
    save(image, "animals", "bull_shark")


def make_whale() -> None:
    image = Image.new("RGBA", (160, 92))
    draw = ImageDraw.Draw(image)
    body = [(14, 48), (25, 31), (47, 22), (80, 20), (110, 29), (129, 40), (143, 45), (132, 49), (127, 57), (110, 61), (78, 65), (47, 60), (26, 56)]
    draw.polygon([(x, y + 7) for x, y in body], fill=INK)
    draw.polygon(body, fill=(87, 119, 140, 255))
    draw.polygon([(30, 48), (60, 50), (91, 48), (123, 47), (112, 58), (81, 63), (51, 59), (34, 55)], fill=(204, 215, 211, 255))
    draw.polygon([(67, 25), (79, 9), (92, 25)], fill=INK)
    draw.polygon([(70, 24), (79, 13), (88, 24)], fill=(70, 102, 124, 255))
    draw.polygon([(63, 59), (52, 78), (83, 64)], fill=INK)
    draw.polygon([(67, 59), (58, 72), (78, 63)], fill=(94, 132, 149, 255))
    draw.polygon([(125, 39), (156, 31), (147, 45), (157, 54), (125, 51)], fill=INK)
    draw.ellipse((115, 40, 120, 45), fill=(243, 226, 188, 255))
    draw.ellipse((117, 41, 119, 43), fill=INK)
    draw.arc((111, 10, 133, 32), 205, 340, fill=(164, 222, 220, 255), width=3)
    draw.ellipse((113, 8, 117, 12), fill=(209, 244, 228, 200))
    save(image, "animals", "sperm_whale")


def make_jellyfish() -> None:
    image = Image.new("RGBA", (72, 76))
    draw = ImageDraw.Draw(image)
    draw.ellipse((10, 9, 62, 47), fill=INK)
    draw.ellipse((14, 10, 58, 43), fill=(239, 140, 190, 255))
    draw.ellipse((19, 13, 52, 31), fill=(255, 194, 219, 255))
    draw.arc((17, 12, 54, 39), 195, 345, fill=(255, 228, 238, 255), width=3)
    draw.rectangle((14, 33, 58, 45), fill=(205, 99, 163, 255))
    draw.line((17, 36, 54, 36), fill=(255, 172, 207, 255), width=2)
    for points in (
        [(20, 43), (17, 53), (22, 61), (18, 73)],
        [(30, 43), (34, 52), (29, 61), (33, 72)],
        [(41, 43), (39, 54), (45, 62), (41, 73)],
        [(52, 43), (56, 52), (51, 62), (55, 71)],
    ):
        draw.line(points, fill=INK, width=5, joint="curve")
        draw.line([(x - 1, y) for x, y in points], fill=(247, 157, 203, 255), width=2, joint="curve")
    draw.ellipse((27, 29, 31, 33), fill=(62, 60, 96, 255))
    draw.ellipse((42, 29, 46, 33), fill=(62, 60, 96, 255))
    save(image, "animals", "moon_jellyfish")


def make_coral_branch() -> None:
    image = Image.new("RGBA", (176, 148))
    draw = ImageDraw.Draw(image)
    paths = [
        [(86, 139), (86, 104), (79, 79), (64, 58), (60, 39), (49, 25)],
        [(79, 82), (97, 62), (103, 43), (119, 26)],
        [(84, 105), (108, 90), (121, 72), (139, 61)],
        [(72, 69), (55, 58), (43, 43)],
        [(89, 88), (74, 69), (75, 46), (86, 32)],
        [(86, 118), (64, 105), (51, 86), (36, 78)],
    ]
    for points in paths:
        draw.line(points, fill=INK, width=17, joint="curve")
        draw.line([(x - 2, y) for x, y in points], fill=(222, 112, 125, 255), width=11, joint="curve")
        draw.line([(x - 4, y) for x, y in points], fill=(255, 171, 156, 255), width=4, joint="curve")
    for x, y in ((49, 25), (119, 26), (139, 61), (43, 43), (86, 32), (36, 78)):
        draw.ellipse((x - 6, y - 6, x + 6, y + 6), fill=(255, 191, 160, 255))
    draw.ellipse((29, 127, 151, 148), fill=(35, 72, 79, 255))
    draw.ellipse((35, 127, 144, 143), fill=(90, 111, 96, 255))
    save(image, "coral", "branching_coral")


def make_coral_brain() -> None:
    image = Image.new("RGBA", (160, 112))
    draw = ImageDraw.Draw(image)
    outline = [(15, 83), (15, 65), (25, 53), (25, 41), (38, 34), (49, 21), (67, 27), (82, 16), (99, 25), (116, 23), (129, 35), (145, 39), (145, 59), (153, 71), (143, 92), (25, 96)]
    draw.polygon(outline, fill=INK)
    inner = [(21, 80), (21, 65), (31, 54), (31, 45), (42, 39), (52, 28), (68, 33), (82, 23), (98, 31), (115, 29), (125, 40), (139, 44), (139, 60), (147, 72), (139, 86), (27, 89)]
    draw.polygon(inner, fill=(227, 154, 105, 255))
    draw.polygon([(28, 65), (44, 44), (67, 38), (55, 57), (39, 68), (30, 81)], fill=(248, 191, 132, 255))
    for points in (
        [(31, 53), (42, 51), (48, 60), (43, 70), (51, 78), (46, 87)],
        [(57, 32), (58, 43), (70, 49), (67, 62), (77, 70), (73, 87)],
        [(86, 28), (84, 39), (97, 47), (91, 58), (101, 66), (97, 88)],
        [(117, 34), (111, 44), (122, 53), (116, 64), (128, 74), (124, 87)],
    ):
        draw.line(points, fill=(151, 81, 78, 255), width=4, joint="curve")
        draw.line([(x - 1, y - 1) for x, y in points], fill=(255, 207, 143, 255), width=1, joint="curve")
    save(image, "coral", "brain_coral")


def make_coral_fan() -> None:
    image = Image.new("RGBA", (160, 150))
    draw = ImageDraw.Draw(image)
    fan = [(80, 134), (31, 98), (28, 76), (34, 56), (48, 39), (68, 30), (80, 18), (94, 30), (114, 38), (129, 58), (134, 79), (126, 101)]
    draw.line(fan + [fan[0]], fill=INK, width=11, joint="curve")
    draw.line(fan + [fan[0]], fill=(113, 182, 171, 255), width=6, joint="curve")
    for end in ((31, 98), (28, 76), (34, 56), (48, 39), (68, 30), (80, 18), (94, 30), (114, 38), (129, 58), (134, 79), (126, 101)):
        draw.line((80, 132, *end), fill=(INK), width=4)
        draw.line((80, 131, *end), fill=(195, 224, 185, 255), width=2)
    for y in (61, 77, 94):
        draw.arc((40, y - 17, 120, y + 23), 190, 350, fill=(182, 214, 183, 255), width=2)
    draw.line((80, 130, 81, 148), fill=INK, width=8)
    draw.line((80, 130, 81, 146), fill=(99, 151, 130, 255), width=4)
    save(image, "coral", "sea_fan")


def make_seagrass() -> None:
    image = Image.new("RGBA", (136, 150))
    draw = ImageDraw.Draw(image)
    draw.ellipse((30, 129, 110, 149), fill=(31, 71, 72, 255))
    paths = [
        [(68, 137), (57, 105), (46, 75), (39, 32)],
        [(68, 139), (75, 104), (83, 69), (97, 25)],
        [(66, 137), (61, 97), (64, 62), (62, 11)],
        [(71, 138), (89, 113), (105, 88), (116, 50)],
        [(63, 138), (48, 115), (30, 91), (20, 57)],
        [(70, 136), (74, 100), (70, 67), (77, 35)],
    ]
    for index, points in enumerate(paths):
        shade = (38, 123 + index % 3 * 12, 98 + index % 2 * 12, 255)
        draw.line(points, fill=(21, 73, 69, 255), width=10, joint="curve")
        draw.line([(x - 2, y) for x, y in points], fill=shade, width=6, joint="curve")
        draw.line([(x - 3, y) for x, y in points], fill=(112, 194, 129, 255), width=2, joint="curve")
    save(image, "plants", "seagrass")


def make_sargassum() -> None:
    image = Image.new("RGBA", (144, 152))
    draw = ImageDraw.Draw(image)
    draw.ellipse((35, 134, 113, 150), fill=(35, 66, 66, 255))
    draw.line((75, 141, 75, 37, 70, 14), fill=INK, width=10)
    draw.line((73, 140, 73, 38, 69, 17), fill=(128, 145, 63, 255), width=5)
    for x, y, side in ((56, 112, -1), (96, 99, 1), (54, 84, -1), (96, 66, 1), (60, 47, -1), (83, 32, 1)):
        leaf = [(75, y + 8), (x + side * 11, y + 2), (x, y - 7), (x - side * 8, y + 3)]
        draw.polygon(leaf, fill=INK)
        draw.polygon([(point[0], point[1] + 2) for point in leaf], fill=(172, 156, 73, 255))
        draw.line((x - 3, y + 1, x + 2, y), fill=(220, 191, 99, 255), width=2)
        draw.ellipse((x + side * 2 - 4, y - 2, x + side * 2 + 4, y + 6), fill=(210, 183, 95, 255))
    save(image, "plants", "sargassum")


def make_rock(name: str, seed: int, cool: bool) -> None:
    image = Image.new("RGBA", (180, 116))
    draw = ImageDraw.Draw(image)
    randomizer = random.Random(seed)
    points = [(12, 89), (21, 60), (38, 48), (52, 23), (76, 34), (93, 16), (119, 35), (139, 31), (162, 59), (169, 92), (151, 104), (28, 105)]
    base = (62, 92, 105, 255) if cool else (104, 105, 91, 255)
    highlight = (103, 139, 147, 255) if cool else (155, 143, 112, 255)
    draw.polygon(points, fill=INK)
    draw.polygon([(x + 5, y + 5) for x, y in points], fill=base)
    draw.polygon([(28, 68), (51, 32), (74, 42), (90, 25), (113, 43), (82, 51), (66, 65), (44, 62)], fill=highlight)
    draw.polygon([(100, 49), (122, 39), (148, 61), (138, 72), (115, 66)], fill=(77, 111, 119, 255))
    for _ in range(40):
        x = randomizer.randint(25, 155)
        y = randomizer.randint(55, 96)
        color = randomizer.choice((highlight, (40, 70, 82, 255), (132, 142, 127, 255)))
        draw.rectangle((x, y, x + randomizer.choice((1, 2, 3)), y + 1), fill=color)
    draw.ellipse((52, 83, 75, 93), fill=(46, 96, 84, 255))
    draw.ellipse((117, 73, 131, 81), fill=(43, 99, 86, 255))
    save(image, "terrain", name)


def make_floor_tile() -> None:
    image = Image.new("RGBA", (256, 96))
    draw = ImageDraw.Draw(image)
    randomizer = random.Random(81)
    for y in range(image.height):
        shade = round(14 * y / image.height)
        draw.line((0, y, image.width, y), fill=(119 + shade, 123 + shade, 103 + shade, 255))
    for _ in range(300):
        x = randomizer.randrange(image.width)
        y = randomizer.randrange(image.height)
        radius = randomizer.choice((1, 1, 2, 3))
        color = randomizer.choice(((94, 106, 99, 255), (148, 143, 116, 255), (171, 159, 127, 255), (81, 103, 101, 255)))
        draw.ellipse((x, y, x + radius * 2, y + radius), fill=color)
    for x, y in ((29, 43), (148, 68), (219, 29)):
        draw.ellipse((x, y, x + 17, y + 7), fill=(61, 88, 89, 255))
        draw.arc((x, y - 3, x + 17, y + 8), 185, 350, fill=(169, 156, 121, 255), width=2)
    save(image, "terrain", "sandy_floor_tile")


def make_backdrop() -> None:
    width, height = 1600, 700
    image = Image.new("RGBA", (width, height))
    rays = Image.new("RGBA", (width, height))
    ray_draw = ImageDraw.Draw(rays)
    for x in range(90, width, 300):
        ray_draw.polygon(((x, 0), (x + 30, 0), (x + 190, 450), (x + 40, 385)), fill=(186, 248, 222, 25))
    image.alpha_composite(rays.filter(ImageFilter.GaussianBlur(24)))
    draw = ImageDraw.Draw(image, "RGBA")
    ridge_far = [(0, 464), (120, 419), (270, 452), (430, 393), (610, 453), (790, 414), (990, 456), (1180, 400), (1370, 448), (1515, 413), (1600, 438), (1600, 700), (0, 700)]
    draw.polygon(ridge_far, fill=(32, 91, 119, 65))
    ridge_near = [(0, 547), (140, 495), (280, 531), (440, 469), (605, 535), (770, 492), (945, 546), (1100, 480), (1275, 530), (1440, 482), (1600, 536), (1600, 700), (0, 700)]
    draw.polygon(ridge_near, fill=(17, 66, 93, 80))
    for x, y, scale in ((170, 555, 0.7), (420, 540, 0.55), (700, 558, 0.8), (1120, 545, 0.65), (1450, 560, 0.75)):
        draw.ellipse((x, y, x + 72 * scale, y + 21 * scale), fill=(20, 65, 87, 90))
        draw.polygon(((x + 24 * scale, y + 3), (x + 35 * scale, y - 13 * scale), (x + 43 * scale, y + 4)), fill=(20, 65, 87, 90))
    for x, y in ((310, 350), (900, 313), (1290, 380)):
        draw.ellipse((x, y, x + 22, y + 8), fill=(188, 226, 213, 75))
        draw.polygon(((x + 3, y + 4), (x - 4, y + 10), (x + 4, y + 7)), fill=(188, 226, 213, 75))
        draw.polygon(((x + 19, y + 4), (x + 27, y + 10), (x + 18, y + 7)), fill=(188, 226, 213, 75))
    save(image, "backgrounds", "gulf_backdrop")


def make_mediterranean_fish(
    name: str,
    body: tuple[int, int, int],
    highlight: tuple[int, int, int],
    accent: tuple[int, int, int],
    pattern: str,
) -> None:
    image = Image.new("RGBA", (120, 78))
    draw = ImageDraw.Draw(image)
    if pattern == "sardine":
        body_shape = [(17, 40), (31, 28), (55, 25), (82, 30), (99, 37), (112, 40), (98, 44), (78, 51), (52, 53), (30, 48)]
        tail = [(22, 40), (7, 27), (11, 40), (7, 53)]
    else:
        body_shape = [(16, 40), (27, 23), (48, 15), (70, 17), (91, 28), (105, 39), (92, 47), (73, 59), (49, 62), (28, 54)]
        tail = [(25, 40), (8, 22), (12, 40), (8, 58)]
    draw.polygon(tail, fill=INK)
    draw.polygon([(x + 2, y) for x, y in tail], fill=accent)
    draw.polygon(body_shape, fill=INK)
    draw.polygon([(x + 3, y + 3) for x, y in body_shape], fill=body)
    draw.polygon([(34, 30), (53, 22), (76, 26), (92, 35), (73, 37), (49, 35)], fill=highlight)
    draw.polygon([(51, 20), (62, 5), (74, 22)], fill=INK)
    draw.polygon([(55, 20), (62, 10), (70, 22)], fill=accent)
    draw.polygon([(53, 56), (64, 70), (75, 56)], fill=INK)
    draw.polygon([(57, 56), (64, 65), (70, 56)], fill=accent)
    draw.polygon([(52, 39), (67, 49), (45, 48)], fill=INK)
    draw.polygon([(55, 40), (64, 47), (49, 46)], fill=highlight)
    if pattern == "bream":
        draw.line((35, 30, 34, 51), fill=accent, width=3)
        draw.line((42, 27, 41, 54), fill=(247, 226, 175, 255), width=2)
        draw.line((79, 29, 77, 52), fill=(242, 222, 165, 255), width=2)
    elif pattern == "grouper":
        for x, y, radius in ((40, 35, 3), (53, 29, 3), (69, 34, 4), (81, 42, 3), (59, 49, 3), (38, 46, 2)):
            draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=accent)
    else:
        draw.line((31, 39, 91, 39), fill=(217, 237, 224, 255), width=3)
        draw.line((29, 35, 86, 32), fill=(120, 161, 174, 255), width=1)
    draw.ellipse((91, 33, 97, 39), fill=(255, 237, 199, 255))
    draw.ellipse((93, 34, 96, 37), fill=INK)
    draw.line((101, 42, 106, 42), fill=(250, 236, 207, 255), width=2)
    save(image, "fish", name)


def make_mediterranean_octopus() -> None:
    image = Image.new("RGBA", (144, 128))
    draw = ImageDraw.Draw(image)
    mantle = [(55, 51), (52, 35), (60, 17), (77, 8), (96, 14), (108, 32), (105, 51), (91, 61), (69, 61)]
    draw.polygon([(x + 3, y + 3) for x, y in mantle], fill=INK)
    draw.polygon(mantle, fill=(194, 111, 111, 255))
    draw.ellipse((62, 19, 100, 54), fill=(218, 137, 128, 255))
    draw.ellipse((68, 28, 73, 34), fill=(244, 218, 191, 255))
    draw.ellipse((88, 27, 94, 33), fill=(244, 218, 191, 255))
    draw.ellipse((70, 30, 73, 33), fill=INK)
    draw.ellipse((89, 29, 92, 32), fill=INK)
    arms = (
        [(64, 51), (51, 69), (31, 68), (22, 82), (26, 96)],
        [(70, 54), (63, 76), (45, 83), (42, 101), (48, 113)],
        [(77, 55), (77, 78), (66, 94), (70, 111), (78, 118)],
        [(84, 54), (91, 75), (87, 91), (99, 101), (111, 99)],
        [(92, 51), (108, 67), (123, 67), (130, 81), (126, 94)],
    )
    for points in arms:
        draw.line(points, fill=INK, width=10, joint="curve")
        draw.line(points, fill=(177, 91, 100, 255), width=6, joint="curve")
        for x, y in points[1:-1]:
            draw.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(243, 194, 165, 255))
    save(image, "animals", "common_octopus")


def make_loggerhead_turtle() -> None:
    image = Image.new("RGBA", (112, 100))
    draw = ImageDraw.Draw(image)
    for points in (
        [(39, 44), (20, 26), (12, 31), (20, 54), (36, 60)],
        [(71, 43), (87, 23), (99, 29), (90, 52), (76, 59)],
        [(39, 60), (19, 76), (27, 90), (48, 72)],
        [(70, 60), (88, 77), (80, 91), (62, 72)],
    ):
        draw.polygon(points, fill=INK)
        draw.polygon([(x, y - 2) for x, y in points], fill=(190, 132, 91, 255))
        draw.line(points[:3], fill=(229, 184, 128, 255), width=2)
    draw.ellipse((79, 43, 109, 68), fill=INK)
    draw.ellipse((82, 45, 105, 65), fill=(207, 153, 105, 255))
    draw.ellipse((99, 50, 103, 54), fill=INK)
    draw.ellipse((31, 31, 81, 74), fill=INK)
    draw.ellipse((35, 34, 77, 70), fill=(118, 77, 60, 255))
    draw.ellipse((40, 38, 72, 66), fill=(166, 112, 76, 255))
    for points in (
        [(55, 38), (47, 46), (51, 57), (61, 63), (70, 55), (67, 45), (55, 38)],
        [(39, 42), (47, 46), (46, 57), (40, 63)],
        [(73, 42), (66, 47), (68, 57), (74, 63)],
    ):
        draw.line(points, fill=(103, 67, 54, 255), width=2, joint="curve")
    draw.ellipse((44, 43, 49, 48), fill=(215, 168, 112, 255))
    draw.ellipse((63, 56, 68, 61), fill=(215, 168, 112, 255))
    save(image, "animals", "loggerhead_turtle")


def make_mediterranean_diver() -> None:
    image = Image.new("RGBA", (128, 88))
    draw = ImageDraw.Draw(image)
    draw.polygon([(29, 47), (18, 55), (7, 52), (2, 59), (15, 66), (39, 60), (51, 51)], fill=INK)
    draw.polygon([(30, 49), (19, 57), (9, 54), (7, 59), (17, 62), (39, 57)], fill=(203, 89, 91, 255))
    draw.polygon([(42, 52), (28, 65), (15, 66), (11, 72), (26, 76), (53, 62), (57, 52)], fill=INK)
    draw.polygon([(43, 55), (30, 66), (18, 68), (16, 72), (27, 73), (51, 60)], fill=(230, 124, 95, 255))
    draw.rounded_rectangle((40, 19, 64, 61), radius=8, fill=INK)
    draw.rounded_rectangle((44, 21, 61, 57), radius=6, fill=(182, 159, 127, 255))
    draw.rectangle((49, 26, 53, 51), fill=(235, 216, 180, 255))
    draw.rectangle((45, 33, 61, 37), fill=(129, 111, 99, 255))
    draw.line((63, 29, 69, 36, 68, 45), fill=(61, 58, 64, 255), width=3)
    draw.polygon([(52, 32), (62, 25), (79, 28), (92, 37), (88, 47), (73, 49), (63, 56), (49, 51)], fill=INK)
    draw.polygon([(56, 34), (65, 29), (78, 31), (87, 38), (83, 43), (70, 45), (62, 52), (53, 49)], fill=(201, 93, 92, 255))
    draw.line((68, 37, 84, 32, 101, 34), fill=INK, width=11)
    draw.line((69, 37, 84, 33, 101, 35), fill=(201, 93, 92, 255), width=6)
    draw.ellipse((98, 29, 110, 40), fill=INK)
    draw.ellipse((100, 31, 108, 38), fill=(229, 218, 190, 255))
    draw.ellipse((77, 16, 112, 49), fill=INK)
    draw.ellipse((80, 18, 109, 46), fill=(216, 170, 133, 255))
    draw.rounded_rectangle((88, 23, 111, 39), radius=6, fill=(70, 51, 60, 255))
    draw.rounded_rectangle((91, 25, 108, 36), radius=4, fill=(154, 211, 207, 255))
    draw.line((94, 27, 103, 27), fill=(248, 230, 204, 255), width=2)
    draw.ellipse((85, 39, 92, 45), fill=(240, 212, 176, 255))
    save(image, "player", "mediterranean_diver")


def make_mediterranean_jellyfish() -> None:
    image = Image.new("RGBA", (84, 96))
    draw = ImageDraw.Draw(image)
    draw.pieslice((12, 8, 72, 64), 180, 360, fill=INK)
    draw.pieslice((16, 11, 68, 60), 180, 360, fill=(177, 101, 131, 255))
    draw.arc((23, 17, 61, 52), 205, 335, fill=(237, 170, 175, 255), width=3)
    draw.rectangle((15, 33, 69, 41), fill=INK)
    draw.rectangle((19, 34, 65, 39), fill=(177, 101, 131, 255))
    draw.line((22, 35, 62, 35), fill=(237, 170, 175, 255), width=2)
    for x in (26, 38, 50, 61):
        draw.line((x, 39, x - 4, 55, x + 2, 72, x - 1, 91), fill=INK, width=4)
        draw.line((x, 40, x - 3, 55, x + 2, 72, x, 90), fill=(224, 151, 162, 255), width=2)
    draw.ellipse((31, 31, 36, 36), fill=(250, 215, 196, 255))
    draw.ellipse((47, 31, 52, 36), fill=(250, 215, 196, 255))
    save(image, "animals", "mediterranean_moon_jellyfish")


def make_mediterranean_barracuda() -> None:
    image = Image.new("RGBA", (154, 76))
    draw = ImageDraw.Draw(image)
    body = [(15, 40), (34, 29), (63, 25), (94, 28), (119, 34), (143, 38), (122, 43), (95, 49), (65, 53), (37, 49)]
    tail = [(22, 40), (5, 22), (11, 40), (5, 58)]
    draw.polygon(tail, fill=INK)
    draw.polygon([(x + 3, y) for x, y in tail], fill=(131, 143, 139, 255))
    draw.polygon(body, fill=INK)
    draw.polygon([(x + 3, y + 3) for x, y in body], fill=(158, 166, 154, 255))
    draw.polygon([(44, 33), (76, 29), (112, 34), (129, 39), (92, 39), (54, 39)], fill=(209, 208, 186, 255))
    draw.polygon([(74, 28), (91, 8), (101, 30)], fill=INK)
    draw.polygon([(79, 28), (91, 14), (97, 29)], fill=(115, 132, 127, 255))
    draw.polygon([(68, 51), (80, 66), (94, 50)], fill=INK)
    draw.polygon([(73, 51), (81, 61), (89, 50)], fill=(119, 137, 130, 255))
    for x in (57, 72, 87, 102):
        draw.line((x, 32, x - 2, 49), fill=(116, 131, 128, 255), width=2)
    draw.polygon([(133, 35), (153, 29), (144, 39), (153, 45), (133, 43)], fill=INK)
    draw.ellipse((121, 33, 126, 38), fill=(241, 225, 197, 255))
    draw.ellipse((123, 34, 126, 37), fill=INK)
    draw.line((131, 42, 145, 41), fill=(49, 56, 56, 255), width=2)
    save(image, "animals", "mediterranean_barracuda")


def make_mediterranean_bubble() -> None:
    image = Image.new("RGBA", (30, 30))
    draw = ImageDraw.Draw(image)
    draw.ellipse((3, 3, 26, 26), fill=(196, 140, 173, 90), outline=(250, 220, 218, 205), width=2)
    draw.arc((5, 4, 24, 25), 195, 295, fill=(255, 238, 220, 235), width=2)
    draw.ellipse((8, 7, 12, 11), fill=(255, 239, 232, 225))
    save(image, "effects", "mediterranean_bubble")


def make_mediterranean_debris() -> None:
    bottle = Image.new("RGBA", (42, 54))
    draw = ImageDraw.Draw(bottle)
    draw.rounded_rectangle((13, 3, 28, 12), radius=3, fill=INK)
    draw.rounded_rectangle((15, 5, 26, 12), radius=2, fill=(191, 145, 116, 255))
    draw.polygon(((14, 12), (29, 12), (32, 19), (30, 45), (25, 50), (15, 47), (11, 20)), fill=INK)
    draw.polygon(((16, 15), (27, 15), (29, 21), (27, 43), (24, 46), (17, 44), (14, 21)), fill=(174, 122, 99, 255))
    draw.line((16, 20, 27, 20), fill=(224, 180, 151, 255), width=2)
    save(bottle, "pollution", "mediterranean_bottle")

    can = Image.new("RGBA", (44, 48))
    draw = ImageDraw.Draw(can)
    draw.rounded_rectangle((8, 6, 36, 42), radius=6, fill=INK)
    draw.rounded_rectangle((11, 8, 33, 39), radius=4, fill=(151, 131, 116, 255))
    draw.ellipse((11, 6, 33, 12), fill=(194, 181, 160, 255), outline=INK, width=2)
    draw.ellipse((11, 36, 33, 42), fill=(108, 101, 96, 255), outline=INK, width=2)
    draw.line((15, 17, 29, 17), fill=(217, 201, 180, 255), width=2)
    draw.line((16, 28, 28, 28), fill=(117, 99, 93, 255), width=2)
    save(can, "pollution", "mediterranean_can")

    net = Image.new("RGBA", (54, 46))
    draw = ImageDraw.Draw(net)
    draw.line(((4, 8), (45, 5), (50, 35), (12, 40), (4, 8)), fill=INK, width=5, joint="curve")
    for points in (
        ((7, 10), (15, 38)),
        ((17, 8), (23, 38)),
        ((28, 7), (32, 37)),
        ((40, 7), (42, 36)),
        ((5, 18), (48, 15)),
        ((8, 28), (49, 25)),
        ((11, 37), (50, 34)),
    ):
        draw.line(points, fill=(139, 122, 91, 255), width=2)
    draw.line(((4, 8), (45, 5), (50, 35), (12, 40), (4, 8)), fill=(187, 166, 129, 255), width=2)
    save(net, "pollution", "mediterranean_net")


def make_posidonia() -> None:
    image = Image.new("RGBA", (150, 174))
    draw = ImageDraw.Draw(image)
    draw.ellipse((31, 153, 119, 170), fill=(67, 90, 73, 255))
    blades = (
        ((70, 157), (49, 112), (34, 60), (40, 12)),
        ((74, 158), (66, 113), (62, 66), (69, 7)),
        ((77, 158), (89, 115), (105, 75), (111, 23)),
        ((72, 160), (51, 127), (24, 94), (13, 49)),
        ((80, 160), (99, 130), (127, 101), (137, 61)),
        ((76, 158), (77, 121), (84, 81), (90, 35)),
    )
    for index, blade in enumerate(blades):
        shade = (31, 97 + index % 3 * 10, 91 + index % 2 * 14, 255)
        draw.line(blade, fill=(26, 66, 66, 255), width=12, joint="curve")
        draw.line(blade, fill=shade, width=8, joint="curve")
        draw.line([(x - 2, y) for x, y in blade], fill=(135, 183, 139, 255), width=2, joint="curve")
    save(image, "plants", "posidonia")


def make_mediterranean_rock(name: str) -> None:
    image = Image.new("RGBA", (180, 116))
    draw = ImageDraw.Draw(image)
    points = [(10, 91), (18, 67), (37, 53), (48, 33), (69, 37), (91, 17), (115, 33), (140, 29), (166, 57), (174, 91), (151, 105), (26, 106)]
    draw.polygon(points, fill=INK)
    draw.polygon([(x + 4, y + 4) for x, y in points], fill=(145, 139, 119, 255))
    draw.polygon([(27, 71), (49, 40), (73, 45), (91, 27), (113, 44), (84, 57), (64, 70), (42, 65)], fill=(192, 180, 151, 255))
    draw.polygon([(98, 55), (124, 40), (150, 60), (139, 76), (113, 71)], fill=(115, 123, 112, 255))
    randomizer = random.Random(812)
    for _ in range(50):
        x = randomizer.randint(23, 155)
        y = randomizer.randint(57, 96)
        draw.ellipse((x, y, x + 2, y + 2), fill=randomizer.choice(((86, 111, 103, 255), (218, 203, 169, 255), (110, 99, 84, 255))))
    save(image, "terrain", name)


def make_rock_arch() -> None:
    image = Image.new("RGBA", (420, 290))
    draw = ImageDraw.Draw(image)
    outer = [(12, 282), (25, 194), (58, 134), (90, 83), (130, 48), (178, 35), (225, 43), (266, 68), (300, 103), (334, 151), (369, 201), (407, 282)]
    draw.polygon(outer, fill=INK)
    inner = [(78, 282), (87, 212), (107, 164), (131, 127), (158, 105), (187, 96), (215, 101), (241, 122), (265, 155), (286, 199), (303, 282)]
    draw.polygon([(x + 6, y + 5) for x, y in outer], fill=(135, 137, 120, 255))
    draw.polygon(inner, fill=(0, 0, 0, 0))
    draw.line(((57, 157), (94, 108), (133, 70), (175, 56), (218, 60), (260, 82), (293, 120)), fill=(203, 189, 153, 255), width=8, joint="curve")
    for x, y in ((55, 224), (111, 193), (322, 221), (351, 242), (146, 84), (271, 102)):
        draw.ellipse((x, y, x + 9, y + 6), fill=(78, 115, 98, 255))
    save(image, "terrain", "mediterranean_rock_arch")


def make_amphora() -> None:
    image = Image.new("RGBA", (116, 142))
    draw = ImageDraw.Draw(image)
    draw.ellipse((39, 8, 77, 21), fill=INK)
    draw.ellipse((43, 11, 73, 17), fill=(183, 126, 82, 255))
    body = [(42, 19), (33, 29), (30, 42), (36, 56), (36, 88), (28, 103), (31, 122), (43, 133), (73, 133), (85, 122), (88, 103), (80, 88), (80, 56), (86, 42), (83, 29), (74, 19)]
    draw.polygon(body, fill=INK)
    draw.polygon([(x + 4, y + 3) for x, y in body], fill=(170, 111, 73, 255))
    draw.arc((21, 26, 45, 58), 80, 280, fill=INK, width=6)
    draw.arc((71, 26, 95, 58), 260, 100, fill=INK, width=6)
    draw.arc((24, 30, 43, 55), 80, 280, fill=(196, 142, 95, 255), width=3)
    draw.arc((73, 30, 92, 55), 260, 100, fill=(196, 142, 95, 255), width=3)
    for y in (39, 92, 111):
        draw.line((39, y, 77, y), fill=(110, 76, 62, 255), width=3)
    draw.ellipse((48, 59, 70, 79), outline=(214, 170, 119, 255), width=3)
    save(image, "landmarks", "amphora")


def make_mediterranean_backdrop() -> None:
    width, height = 1600, 700
    image = Image.new("RGBA", (width, height))
    haze = Image.new("RGBA", (width, height))
    haze_draw = ImageDraw.Draw(haze)
    for x in range(80, width, 340):
        haze_draw.polygon(((x, 0), (x + 34, 0), (x + 220, 455), (x + 30, 425)), fill=(220, 248, 230, 29))
    image.alpha_composite(haze.filter(ImageFilter.GaussianBlur(26)))
    draw = ImageDraw.Draw(image, "RGBA")
    far = [(0, 459), (123, 411), (252, 431), (375, 361), (504, 390), (653, 324), (800, 391), (967, 363), (1118, 406), (1283, 347), (1443, 382), (1600, 331), (1600, 700), (0, 700)]
    near = [(0, 529), (143, 472), (277, 500), (432, 423), (587, 463), (728, 415), (876, 475), (1043, 439), (1196, 489), (1334, 431), (1490, 467), (1600, 424), (1600, 700), (0, 700)]
    draw.polygon(far, fill=(50, 114, 139, 75))
    draw.polygon(near, fill=(28, 81, 108, 89))
    for x, y, scale in ((70, 515, 1.0), (311, 474, 0.75), (612, 503, 0.88), (934, 470, 0.8), (1260, 506, 0.92), (1464, 450, 0.72)):
        draw.polygon(((x, y + 35 * scale), (x + 24 * scale, y), (x + 56 * scale, y - 17 * scale), (x + 92 * scale, y + 7 * scale), (x + 124 * scale, y + 39 * scale)), fill=(34, 87, 108, 95))
    for x, y in ((185, 350), (533, 328), (1067, 346), (1398, 312)):
        draw.ellipse((x, y, x + 24, y + 8), fill=(220, 241, 224, 72))
        draw.polygon(((x + 4, y + 4), (x - 4, y + 11), (x + 5, y + 7)), fill=(220, 241, 224, 72))
        draw.polygon(((x + 21, y + 4), (x + 29, y + 11), (x + 20, y + 7)), fill=(220, 241, 224, 72))
    save(image, "backgrounds", "mediterranean_backdrop")


def make_mediterranean_floor() -> None:
    image = Image.new("RGBA", (256, 96))
    draw = ImageDraw.Draw(image)
    randomizer = random.Random(122)
    for y in range(image.height):
        shade = round(12 * y / image.height)
        draw.line((0, y, image.width, y), fill=(174 + shade, 164 + shade, 136 + shade, 255))
    for _ in range(300):
        x = randomizer.randrange(image.width)
        y = randomizer.randrange(image.height)
        radius = randomizer.choice((1, 1, 2, 3))
        color = randomizer.choice(((142, 137, 119, 255), (201, 185, 151, 255), (214, 199, 163, 255), (113, 128, 120, 255)))
        draw.ellipse((x, y, x + radius * 2, y + radius), fill=color)
    for x, y in ((29, 43), (148, 68), (219, 29)):
        draw.ellipse((x, y, x + 17, y + 7), fill=(85, 108, 105, 255))
        draw.arc((x, y - 3, x + 17, y + 8), 185, 350, fill=(210, 190, 151, 255), width=2)
    save(image, "terrain", "mediterranean_sandy_floor")


REGIONAL_PALETTES = {
    "arctic": ((113, 165, 184), (190, 225, 231), (235, 249, 246), (51, 94, 121)),
    "great_lakes": ((72, 153, 148), (151, 197, 167), (229, 213, 164), (39, 89, 105)),
    "amazon": ((184, 116, 83), (224, 160, 115), (236, 201, 145), (81, 70, 67)),
}


def make_regional_backdrop(region: str) -> None:
    image = Image.new("RGBA", (1600, 760))
    top, middle, light, deep = REGIONAL_PALETTES[region]
    pixels = image.load()
    for y in range(image.height):
        amount = y / image.height
        color = tuple(round(top[i] * (1 - amount) + deep[i] * amount) for i in range(3))
        for x in range(image.width):
            pixels[x, y] = (*color, 255)
    haze = Image.new("RGBA", image.size)
    haze_draw = ImageDraw.Draw(haze)
    for x in range(60, 1600, 310):
        haze_draw.polygon(
            ((x, 0), (x + 30, 0), (x + 205, 500), (x + 8, 470)),
            fill=(*light, 34),
        )
    image.alpha_composite(haze.filter(ImageFilter.GaussianBlur(25)))
    draw = ImageDraw.Draw(image, "RGBA")
    draw.polygon(
        ((0, 490), (170, 415), (330, 445), (510, 358), (670, 422),
         (820, 370), (1010, 440), (1180, 360), (1390, 421), (1600, 342),
         (1600, 760), (0, 760)),
        fill=(*deep, 112),
    )
    draw.polygon(
        ((0, 560), (160, 490), (350, 515), (510, 455), (735, 510),
         (890, 450), (1080, 525), (1290, 455), (1480, 500), (1600, 440),
         (1600, 760), (0, 760)),
        fill=(*middle, 77),
    )
    if region == "arctic":
        draw.polygon(((0, 0), (410, 0), (365, 55), (0, 34)), fill=(231, 248, 249, 220))
        draw.polygon(((920, 0), (1600, 0), (1600, 45), (1010, 60)), fill=(231, 248, 249, 210))
        for x in range(150, 1550, 230):
            draw.ellipse((x, 300 + (x % 120), x + 11, 306 + (x % 120)), fill=(228, 249, 249, 95))
    elif region == "great_lakes":
        for x, y in ((175, 375), (520, 339), (980, 354), (1380, 319)):
            draw.polygon(((x, y), (x + 42, y - 13), (x + 89, y + 2), (x + 38, y + 7)), fill=(207, 232, 197, 92))
        draw.ellipse((1190, 275, 1206, 280), fill=(231, 246, 212, 120))
    else:
        for x in range(-20, 1620, 180):
            draw.line((x, 0, x + 34, 175), fill=(61, 79, 61, 95), width=8)
            draw.ellipse((x - 38, 84, x + 82, 184), fill=(72, 105, 74, 98))
    randomizer = random.Random(180 + len(region))
    for _ in range(85):
        x = randomizer.randrange(image.width)
        y = randomizer.randrange(150, 690)
        radius = randomizer.choice((1, 2, 3))
        draw.ellipse((x, y, x + radius, y + radius), fill=(*light, randomizer.randint(28, 75)))
    save(image, f"regions/{region}/backgrounds", "backdrop")


def make_regional_floor_and_rock(region: str) -> None:
    top, middle, light, deep = REGIONAL_PALETTES[region]
    floor = Image.new("RGBA", (320, 104))
    draw = ImageDraw.Draw(floor)
    randomizer = random.Random(302 + len(region))
    for y in range(floor.height):
        amount = y / floor.height
        color = tuple(round(middle[i] * (1 - amount * 0.2) + deep[i] * amount * 0.2) for i in range(3))
        draw.line((0, y, floor.width, y), fill=(*color, 255))
    for _ in range(360):
        x, y = randomizer.randrange(320), randomizer.randrange(104)
        color = randomizer.choice(((*light, 255), (*deep, 255), (*middle, 255)))
        radius = randomizer.choice((1, 1, 2, 3))
        draw.ellipse((x, y, x + radius * 2, y + radius), fill=color)
    save(floor, f"regions/{region}/terrain", "floor")

    rock = Image.new("RGBA", (190, 126))
    draw = ImageDraw.Draw(rock)
    outline = [(8, 111), (15, 83), (35, 68), (42, 39), (67, 34), (86, 14),
               (111, 28), (140, 22), (170, 49), (181, 82), (176, 112), (22, 119)]
    draw.polygon(outline, fill=INK)
    draw.polygon([(x + 5, y + 4) for x, y in outline], fill=(*middle, 255))
    draw.polygon([(24, 80), (47, 45), (69, 42), (87, 24), (107, 39), (92, 63), (61, 78)], fill=(*light, 255))
    draw.polygon([(105, 64), (135, 40), (162, 62), (150, 85), (120, 82)], fill=(*top, 255))
    for index in range(7):
        y = 76 + index * 5
        draw.line((36 + index * 2, y, 150 - index * 4, y + 2), fill=(*deep, 105), width=2)
    save(rock, f"regions/{region}/terrain", "rock")


def make_regional_fish(region: str, name: str) -> None:
    image = Image.new("RGBA", (144, 86))
    draw = ImageDraw.Draw(image)
    top, middle, light, deep = REGIONAL_PALETTES[region]
    tail = [(27, 42), (7, 22), (12, 43), (7, 64)]
    body = [(20, 43), (34, 24), (59, 17), (87, 21), (112, 33), (132, 42),
            (112, 52), (87, 65), (58, 68), (34, 58)]
    draw.polygon(tail, fill=INK)
    draw.polygon([(x + 3, y) for x, y in tail], fill=(*top, 255))
    draw.polygon(body, fill=INK)
    draw.polygon([(x + 4, y + 3) for x, y in body], fill=(*middle, 255))
    draw.polygon([(42, 32), (63, 22), (88, 26), (105, 35), (79, 39), (52, 39)], fill=(*light, 255))
    draw.polygon([(55, 24), (68, 7), (79, 25)], fill=INK)
    draw.polygon([(60, 23), (69, 13), (76, 24)], fill=(*top, 255))
    draw.polygon([(66, 62), (75, 79), (88, 62)], fill=INK)
    draw.polygon([(70, 62), (75, 73), (83, 62)], fill=(*top, 255))
    if name in ("yellow_perch", "piranha"):
        for x in (47, 61, 75, 89):
            draw.line((x, 28, x - 4, 57), fill=(*light, 255), width=4)
    elif name in ("lake_sturgeon", "arapaima", "tambaqui"):
        for x in (51, 68, 86, 101):
            draw.line((x, 25, x + 3, 60), fill=(*deep, 255), width=3)
        if name == "lake_sturgeon":
            for x in (38, 47, 56):
                draw.line((x, 57, x - 3, 68), fill=(*light, 255), width=2)
    elif name in ("arctic_cod", "polar_cod", "arctic_char", "lake_trout"):
        draw.line((47, 29, 46, 59), fill=(*light, 255), width=2)
        draw.line((95, 29, 94, 59), fill=(*light, 255), width=2)
    else:
        draw.polygon([(115, 37), (133, 41), (121, 47)], fill=(*light, 255))
    draw.ellipse((111, 36, 116, 41), fill=(255, 245, 221, 255))
    draw.ellipse((113, 37, 115, 39), fill=INK)
    draw.line((126, 47, 133, 46), fill=(*deep, 255), width=2)
    save(image, f"regions/{region}/fish", name)


def make_regional_animal(region: str, name: str) -> None:
    image = Image.new("RGBA", (220, 136))
    draw = ImageDraw.Draw(image)
    top, middle, light, deep = REGIONAL_PALETTES[region]
    if name == "ringed_seal":
        draw.ellipse((30, 55, 177, 111), fill=INK)
        draw.ellipse((37, 59, 171, 104), fill=(*middle, 255))
        draw.ellipse((144, 49, 196, 91), fill=INK)
        draw.ellipse((150, 52, 190, 85), fill=(*light, 255))
        draw.polygon(((59, 95), (34, 127), (81, 103)), fill=INK)
        draw.polygon(((62, 96), (44, 119), (78, 102)), fill=(*top, 255))
        draw.polygon(((119, 94), (155, 124), (145, 96)), fill=INK)
        draw.polygon(((122, 95), (148, 117), (142, 97)), fill=(*top, 255))
        draw.ellipse((178, 62, 183, 67), fill=INK)
        for x, y in ((69, 70), (93, 83), (119, 69), (145, 88)):
            draw.ellipse((x, y, x + 9, y + 8), outline=(*light, 210), width=2)
    elif name in ("narwhal", "boto", "greenland_shark", "muskellunge", "black_caiman"):
        body_color = (*middle, 255)
        body = [(20, 77), (41, 48), (89, 39), (139, 47), (173, 63), (204, 70), (184, 81), (157, 98), (105, 108), (56, 98), (31, 89)]
        draw.polygon([(x, y + 8) for x, y in body], fill=INK)
        draw.polygon(body, fill=body_color)
        draw.polygon([(44, 79), (79, 83), (127, 82), (169, 74), (176, 82), (146, 94), (96, 101), (58, 93)], fill=(*light, 255))
        draw.polygon([(113, 47), (128, 20), (144, 50)], fill=INK)
        draw.polygon([(119, 46), (129, 28), (139, 48)], fill=(*top, 255))
        draw.polygon([(77, 98), (60, 124), (102, 103)], fill=INK)
        draw.polygon([(80, 99), (66, 116), (96, 102)], fill=(*top, 255))
        draw.polygon([(181, 66), (214, 52), (201, 73), (214, 91), (181, 82)], fill=INK)
        if name == "narwhal":
            draw.line((183, 69, 218, 51), fill=INK, width=7)
            draw.line((184, 68, 216, 52), fill=(*light, 255), width=3)
            for offset in range(0, 27, 7):
                draw.line((189 + offset, 64 - offset // 2, 192 + offset, 68 - offset // 2), fill=(*top, 255), width=2)
        elif name == "boto":
            draw.ellipse((182, 69, 218, 81), fill=(*top, 255), outline=INK, width=3)
            draw.ellipse((184, 63, 190, 69), fill=(*light, 255))
        elif name == "muskellunge":
            for x in range(65, 155, 18):
                draw.line((x, 51, x - 4, 91), fill=(*deep, 240), width=4)
        elif name == "greenland_shark":
            for x in (78, 87, 96, 105):
                draw.line((x, 62, x - 4, 80), fill=(*deep, 255), width=2)
        if name == "black_caiman":
            for x in range(62, 171, 13):
                draw.polygon(((x, 51), (x + 7, 43), (x + 13, 53)), fill=(*light, 255))
            draw.ellipse((178, 67, 182, 71), fill=INK)
        else:
            draw.ellipse((177, 66, 183, 72), fill=(255, 246, 220, 255))
            draw.ellipse((179, 67, 182, 70), fill=INK)
    elif name == "lions_mane":
        draw.ellipse((61, 17, 158, 82), fill=INK)
        draw.ellipse((67, 21, 152, 77), fill=(*middle, 245))
        draw.arc((77, 28, 142, 70), 180, 360, fill=(*light, 255), width=5)
        for x in (70, 84, 99, 114, 130, 145):
            draw.line((x, 74, x - 9, 129), fill=(*top, 255), width=4)
            draw.line((x + 4, 75, x + 13, 130), fill=(*light, 220), width=2)
    elif name == "stingray":
        draw.polygon(((67, 58), (21, 92), (75, 79), (110, 96), (150, 79), (204, 93), (151, 55), (111, 45)), fill=INK)
        draw.polygon(((73, 59), (36, 87), (78, 74), (110, 89), (147, 74), (190, 87), (147, 59), (111, 50)), fill=(*middle, 255))
        draw.line((113, 88, 171, 124), fill=(*deep, 255), width=3)
        draw.ellipse((99, 66, 104, 70), fill=INK)
        draw.ellipse((119, 66, 124, 70), fill=INK)
    elif name in ("mussels", "zebra_mussels"):
        for x, y in ((38, 73), (78, 50), (113, 77), (151, 51), (174, 83)):
            draw.ellipse((x - 23, y - 26, x + 23, y + 25), fill=INK)
            draw.ellipse((x - 18, y - 22, x + 18, y + 20), fill=(*middle, 255))
            for offset in range(-10, 11, 6):
                color = (*light, 255) if name == "mussels" or offset % 2 else (*deep, 255)
                draw.arc((x - 15 + offset, y - 18, x + 13 + offset, y + 18), 280, 85, fill=color, width=2)
    elif name == "river_turtle":
        draw.ellipse((48, 35, 163, 106), fill=INK)
        draw.ellipse((54, 40, 157, 100), fill=(*middle, 255))
        draw.ellipse((165, 51, 209, 82), fill=INK)
        draw.ellipse((169, 54, 204, 78), fill=(*light, 255))
        draw.ellipse((197, 60, 201, 64), fill=INK)
        for x, y in ((62, 34), (132, 33), (61, 94), (132, 97)):
            draw.ellipse((x, y, x + 31, y + 24), fill=(*top, 255), outline=INK, width=4)
        draw.polygon(((87, 44), (111, 52), (102, 69), (80, 63)), outline=INK)
        draw.polygon(((112, 73), (131, 78), (119, 93), (99, 84)), outline=INK)
    elif name == "sea_lamprey":
        draw.arc((19, 25, 201, 115), 185, 350, fill=INK, width=23)
        draw.arc((22, 29, 198, 111), 185, 350, fill=(*middle, 255), width=15)
        draw.ellipse((18, 67, 43, 90), fill=(186, 95, 96, 255), outline=INK, width=3)
        for angle in range(0, 360, 45):
            x = 30 + round(7 * math.cos(angle))
            y = 78 + round(7 * math.sin(angle))
            draw.ellipse((x, y, x + 3, y + 3), fill=(*light, 255))
    save(image, f"regions/{region}/animals", name)


def make_regional_plant(region: str, name: str) -> None:
    image = Image.new("RGBA", (210, 135) if name == "water_lily" else (190, 220))
    draw = ImageDraw.Draw(image)
    top, middle, light, deep = REGIONAL_PALETTES[region]
    if name == "kelp":
        draw.ellipse((46, 195, 146, 212), fill=(*deep, 255))
        for index, x in enumerate((57, 75, 94, 114, 132)):
            points = [(x, 201), (x - 15 + index * 2, 151), (x + 10, 100), (x + 2, 48 - index * 3)]
            draw.line(points, fill=INK, width=13)
            draw.line(points, fill=(*middle, 255), width=8)
            draw.line([(px - 2, py) for px, py in points], fill=(*light, 255), width=2)
            draw.ellipse((x - 11, 140 - index * 9, x + 8, 158 - index * 9), fill=(*top, 255))
    elif name == "wild_rice":
        draw.ellipse((35, 198, 159, 214), fill=(*deep, 255))
        for index, x in enumerate((54, 78, 103, 129, 149)):
            top_y = 24 + index % 2 * 20
            draw.line((x, 202, x + (index - 2) * 4, top_y + 25), fill=INK, width=7)
            draw.line((x, 200, x + (index - 2) * 4, top_y + 25), fill=(*middle, 255), width=4)
            for seed in range(5):
                sy = top_y + 24 + seed * 8
                draw.ellipse((x - 2 + seed % 2 * 6, sy, x + 4 + seed % 2 * 6, sy + 9), fill=(*light, 255))
            for side in (-1, 1):
                draw.line((x, 160 - index * 3, x + side * 24, 142 - index * 3), fill=(*top, 255), width=4)
    else:
        for x, y, radius in ((48, 82, 42), (105, 92, 48), (165, 79, 37)):
            draw.ellipse((x - radius, y - radius // 2, x + radius, y + radius // 2), fill=INK)
            draw.ellipse((x - radius + 4, y - radius // 2 + 4, x + radius - 4, y + radius // 2 - 4), fill=(*middle, 255))
            draw.line((x, y, x + 4, y - radius // 2 + 10), fill=(*light, 255), width=3)
            draw.line((x, y, x - 8, y + 7), fill=(*top, 255), width=2)
        draw.ellipse((91, 13, 124, 46), fill=(*light, 255), outline=INK, width=4)
        for angle in range(0, 360, 45):
            radians = math.radians(angle)
            px = 107 + round(17 * math.cos(radians))
            py = 29 + round(17 * math.sin(radians))
            draw.ellipse((px - 3, py - 3, px + 3, py + 3), fill=(*top, 255))
    save(image, f"regions/{region}/plants", name)


def make_regional_landmark(region: str, name: str) -> None:
    top, middle, light, deep = REGIONAL_PALETTES[region]
    dimensions = {
        "ice_shelf": (520, 220),
        "shipwreck": (420, 250),
        "flooded_forest": (380, 280),
        "forest_roots": (300, 240),
    }
    image = Image.new("RGBA", dimensions[name])
    draw = ImageDraw.Draw(image)
    if name == "ice_shelf":
        draw.polygon(((0, 30), (82, 19), (166, 28), (240, 12), (330, 22), (411, 8), (520, 20), (520, 80), (0, 86)), fill=(*light, 255))
        draw.polygon(((0, 77), (82, 89), (152, 78), (230, 96), (330, 82), (405, 97), (520, 80), (520, 220), (0, 220)), fill=(*middle, 245))
        draw.polygon(((45, 85), (116, 91), (152, 220), (74, 220)), fill=(*top, 175))
        draw.polygon(((320, 87), (399, 92), (438, 220), (363, 220)), fill=(*top, 175))
        draw.line((0, 100, 520, 100), fill=(*light, 180), width=3)
    elif name == "shipwreck":
        draw.polygon(((22, 158), (91, 165), (135, 190), (344, 189), (398, 155), (373, 216), (78, 221)), fill=INK)
        draw.polygon(((36, 161), (101, 170), (144, 193), (337, 191), (380, 160), (358, 204), (81, 208)), fill=(*middle, 255))
        draw.polygon(((150, 155), (154, 56), (162, 56), (169, 156)), fill=INK)
        draw.polygon(((158, 61), (220, 128), (165, 127)), fill=(*light, 255))
        draw.line((160, 66, 160, 163), fill=(*deep, 255), width=5)
        draw.line((255, 168, 255, 94), fill=INK, width=8)
        draw.polygon(((247, 96), (260, 89), (270, 98), (263, 105)), fill=(*top, 255))
        for x in (112, 299, 344):
            draw.line((x, 176, x + 18, 183), fill=(*light, 255), width=3)
    elif name == "flooded_forest":
        draw.rectangle((0, 0, 380, 76), fill=(*deep, 175))
        for x in (26, 90, 166, 244, 331):
            draw.line((x, 0, x + 5, 142), fill=INK, width=24)
            draw.line((x + 2, 2, x + 7, 138), fill=(*deep, 255), width=16)
            draw.ellipse((x - 28, 0, x + 34, 61), fill=(*middle, 220))
            for root in range(3):
                draw.line((x + 5, 117, x - 22 + root * 19, 277), fill=INK, width=8)
                draw.line((x + 5, 119, x - 22 + root * 19, 274), fill=(*top, 255), width=4)
        draw.line((0, 190, 380, 190), fill=(*light, 170), width=4)
    else:
        for x in (34, 102, 165, 237, 282):
            draw.line((x, 0, x - 4, 118), fill=INK, width=19)
            draw.line((x - 3, 12, x - 38, 92), fill=(*middle, 255), width=12)
            draw.line((x - 4, 58, x + 39, 142), fill=(*top, 255), width=10)
            draw.line((x - 4, 106, x - 26, 230), fill=(*deep, 255), width=8)
        draw.polygon(((0, 185), (300, 178), (300, 240), (0, 240)), fill=(*deep, 120))
    save(image, f"regions/{region}/landmarks", name)


def make_regional_pollution(region: str, name: str) -> None:
    image = Image.new("RGBA", (100, 88))
    draw = ImageDraw.Draw(image)
    accent = (226, 184, 112, 255)
    top = REGIONAL_PALETTES[region][0]
    middle = REGIONAL_PALETTES[region][1]
    light = REGIONAL_PALETTES[region][2]
    if name in ("plastic", "canister", "can", "drum"):
        size = (29, 53) if name in ("plastic", "canister") else (41, 49) if name == "can" else (51, 60)
        x0, y0 = (35, 18) if size[0] < 40 else (25, 19)
        x1, y1 = x0 + size[0], y0 + size[1]
        draw.rounded_rectangle((x0 - 4, y0 - 5, x1 + 4, y1 + 3), radius=8, fill=INK)
        color = (114, 183, 189, 255) if name == "plastic" else (178, 160, 108, 255)
        draw.rounded_rectangle((x0, y0, x1, y1), radius=7, fill=color)
        draw.ellipse((x0, y0 - 5, x1, y0 + 5), fill=(*light, 255), outline=INK, width=2)
        draw.line((x0 + 5, y0 + 14, x1 - 5, y0 + 14), fill=accent, width=3)
    elif name in ("net", "line"):
        draw.polygon(((12, 18), (87, 27), (78, 70), (20, 65)), fill=(*middle, 65), outline=INK)
        for x in range(18, 86, 12):
            draw.line((x, 20, x - 3, 66), fill=accent, width=2)
        for y in range(27, 70, 10):
            draw.line((15, y, 82, y + 3), fill=accent, width=2)
        if name == "line":
            draw.line((7, 9, 89, 80), fill=(*light, 255), width=3)
            draw.line((89, 11, 13, 80), fill=(*top, 255), width=2)
    save(image, f"regions/{region}/pollution", name)


def make_regional_diver_and_bubble(region: str) -> None:
    top, middle, light, deep = REGIONAL_PALETTES[region]
    image = Image.new("RGBA", (128, 88))
    draw = ImageDraw.Draw(image)
    suit = {"arctic": (210, 230, 232, 255), "great_lakes": (225, 173, 99, 255), "amazon": (226, 123, 92, 255)}[region]
    draw.polygon(((19, 50), (4, 60), (20, 69), (49, 57)), fill=INK)
    draw.polygon(((22, 51), (11, 60), (22, 65), (48, 56)), fill=(*top, 255))
    draw.polygon(((41, 51), (25, 68), (12, 72), (24, 79), (54, 62)), fill=INK)
    draw.polygon(((43, 53), (29, 67), (19, 71), (28, 75), (51, 60)), fill=suit)
    draw.rounded_rectangle((43, 19, 65, 59), radius=7, fill=INK)
    draw.rounded_rectangle((47, 22, 61, 55), radius=5, fill=(*middle, 255))
    draw.line((55, 28, 55, 48), fill=(*light, 255), width=3)
    draw.polygon(((54, 32), (67, 25), (83, 29), (93, 39), (87, 49), (67, 48), (54, 56)), fill=INK)
    draw.polygon(((58, 34), (68, 29), (81, 32), (88, 39), (83, 45), (66, 45), (56, 52)), fill=suit)
    draw.line((68, 36, 86, 30, 104, 32), fill=INK, width=10)
    draw.line((70, 36, 86, 32, 102, 34), fill=suit, width=5)
    draw.ellipse((100, 28, 111, 39), fill=INK)
    draw.ellipse((102, 30, 109, 37), fill=(*light, 255))
    draw.ellipse((79, 16, 111, 47), fill=INK)
    draw.ellipse((82, 18, 108, 43), fill=suit)
    draw.rounded_rectangle((90, 24, 110, 37), radius=5, fill=(*deep, 255))
    draw.rounded_rectangle((93, 26, 107, 35), radius=4, fill=(*top, 255))
    draw.line((95, 28, 102, 28), fill=(*light, 255), width=2)
    save(image, f"regions/{region}/player", "diver")
    bubble = Image.new("RGBA", (28, 28))
    bd = ImageDraw.Draw(bubble)
    bd.ellipse((3, 3, 24, 24), fill=(*top, 75), outline=(*light, 210), width=2)
    bd.arc((5, 4, 23, 23), 200, 300, fill=(255, 255, 255, 235), width=2)
    bd.ellipse((8, 6, 11, 9), fill=(255, 255, 255, 240))
    save(bubble, f"regions/{region}/effects", "bubble")


def generate_new_regions() -> None:
    regional_assets = {
        "arctic": {
            "fish": ("arctic_cod", "polar_cod", "arctic_char"),
            "animals": ("narwhal", "ringed_seal", "lions_mane", "greenland_shark"),
            "plants": ("kelp",),
            "landmarks": ("ice_shelf",),
            "pollution": ("plastic", "net", "canister"),
        },
        "great_lakes": {
            "fish": ("lake_sturgeon", "lake_trout", "yellow_perch"),
            "animals": ("muskellunge", "sea_lamprey", "mussels", "zebra_mussels"),
            "plants": ("wild_rice",),
            "landmarks": ("shipwreck",),
            "pollution": ("plastic", "line", "can"),
        },
        "amazon": {
            "fish": ("arapaima", "piranha", "tambaqui"),
            "animals": ("boto", "river_turtle", "black_caiman", "stingray"),
            "plants": ("water_lily",),
            "landmarks": ("flooded_forest", "forest_roots"),
            "pollution": ("plastic", "net", "drum"),
        },
    }
    for region, categories in regional_assets.items():
        make_regional_backdrop(region)
        make_regional_floor_and_rock(region)
        make_regional_diver_and_bubble(region)
        for name in categories["fish"]:
            make_regional_fish(region, name)
        for name in categories["animals"]:
            make_regional_animal(region, name)
        for name in categories["plants"]:
            make_regional_plant(region, name)
        for name in categories["landmarks"]:
            make_regional_landmark(region, name)
        for name in categories["pollution"]:
            make_regional_pollution(region, name)


def make_bubble() -> None:
    image = Image.new("RGBA", (28, 28))
    draw = ImageDraw.Draw(image)
    draw.ellipse((3, 3, 24, 24), fill=(118, 216, 227, 95), outline=(207, 250, 245, 190), width=2)
    draw.arc((5, 4, 23, 23), 200, 300, fill=(255, 255, 244, 230), width=2)
    draw.ellipse((8, 6, 11, 9), fill=(255, 255, 255, 230))
    save(image, "effects", "bubble")


def main() -> None:
    make_diver()
    make_dolphin()
    make_turtle()
    make_shark()
    make_whale()
    make_jellyfish()
    outlined_fish("red_snapper", (203, 84, 71), (240, 139, 100), (247, 154, 103), "snapper")
    outlined_fish("blue_tang", (45, 130, 211), (100, 190, 235), (248, 211, 72), "tang")
    outlined_fish("queen_angelfish", (43, 132, 168), (88, 185, 195), (250, 196, 76), "angel")
    make_coral_branch()
    make_coral_brain()
    make_coral_fan()
    make_seagrass()
    make_sargassum()
    make_rock("limestone_reef", 14, True)
    make_rock("sandstone_reef", 43, False)
    make_floor_tile()
    make_backdrop()
    make_mediterranean_fish("european_sardine", (112, 151, 165), (190, 207, 197), (98, 137, 157), "sardine")
    make_mediterranean_fish("white_seabream", (177, 164, 133), (223, 205, 161), (111, 91, 72), "bream")
    make_mediterranean_fish("dusky_grouper", (117, 126, 91), (167, 165, 116), (67, 79, 62), "grouper")
    make_mediterranean_octopus()
    make_loggerhead_turtle()
    make_mediterranean_diver()
    make_mediterranean_jellyfish()
    make_mediterranean_barracuda()
    make_mediterranean_bubble()
    make_mediterranean_debris()
    make_posidonia()
    make_mediterranean_rock("mediterranean_rock")
    make_rock_arch()
    make_amphora()
    make_mediterranean_backdrop()
    make_mediterranean_floor()
    make_bubble()
    generate_new_regions()


if __name__ == "__main__":
    if "--new-regions" in sys.argv:
        generate_new_regions()
    else:
        main()
