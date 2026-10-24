"""Generate Tidekeeper's original pixel-inspired PNG artwork once."""

from pathlib import Path
import random

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
    make_bubble()


if __name__ == "__main__":
    main()
