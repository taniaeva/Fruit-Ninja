import pygame
import random
import math

pygame.init()

BASE_W, BASE_H = 1080, 640
screen = pygame.display.set_mode((BASE_W, BASE_H))
pygame.display.set_caption("Fruit Slice Classic - Week 1")
clock = pygame.time.Clock()
FPS = 60

# ---------- Colors ----------
WHITE = (255, 255, 255)
BLACK = (14, 12, 10)
WOOD_BASE = (96, 56, 28)
WOOD_PLANK_ALT = (88, 50, 24)
WOOD_SEAM = (54, 29, 13)
WOOD_GRAIN = (74, 41, 19)
WOOD_HIGHLIGHT = (116, 70, 36)
GOLD = (255, 212, 52)
GOLD_SHADOW = (140, 82, 10)
CREAM = (255, 246, 214)
BLADE_CORE = WHITE
BLADE_GLOW = (160, 215, 255)


# ---------- Fonts ----------
def get_clean_font(size, bold=True):
    for name in ["Futura", "Impact", "Helvetica Neue", "Arial", "Helvetica", "Menlo"]:
        matched = pygame.font.match_font(name, bold=bold)
        if matched:
            return pygame.font.Font(matched, size)
    return pygame.font.Font(None, int(size * 1.15))


font_score = get_clean_font(42)
font_med = get_clean_font(22)
font_small = get_clean_font(16)


# ---------- Wooden board background ----------
def create_wooden_board():
    surf = pygame.Surface((BASE_W, BASE_H)).convert()
    rng = random.Random(108)
    plank_w = 72
    for idx, x in enumerate(range(0, BASE_W, plank_w)):
        base = WOOD_BASE if idx % 2 == 0 else WOOD_PLANK_ALT
        d = rng.randint(-4, 4)
        col = tuple(max(0, min(255, c + d)) for c in base)
        pygame.draw.rect(surf, col, (x, 0, plank_w, BASE_H))
        pygame.draw.line(surf, WOOD_HIGHLIGHT, (x + 2, 0), (x + 2, BASE_H), 2)
        pygame.draw.line(surf, WOOD_SEAM, (x + plank_w - 2, 0), (x + plank_w - 2, BASE_H), 3)
        for _ in range(4):
            gx = x + rng.randint(10, plank_w - 12)
            pygame.draw.line(surf, WOOD_GRAIN, (gx, rng.randint(20, 180)),
                             (gx, BASE_H - rng.randint(20, 180)), 1)
    return surf


board_bg = create_wooden_board()

# ---------- Fruit types ----------
FRUIT_TYPES = {
    "watermelon": {"rind": (38, 155, 52), "stripe": (16, 78, 24), "flesh": (238, 45, 65), "hi": (140, 235, 145), "radius": 46, "points": 1},
    "pineapple":  {"rind": (222, 148, 28), "stripe": (145, 82, 14), "flesh": (255, 224, 65), "hi": (255, 220, 120), "radius": 42, "points": 1},
    "orange":     {"rind": (248, 128, 18), "stripe": (200, 88, 8), "flesh": (255, 175, 45), "hi": (255, 210, 130), "radius": 36, "points": 1},
    "apple":      {"rind": (215, 28, 36), "stripe": (135, 14, 20), "flesh": (252, 244, 198), "hi": (255, 145, 150), "radius": 37, "points": 1},
    "strawberry": {"rind": (225, 22, 55), "stripe": (150, 10, 32), "flesh": (255, 125, 145), "hi": (255, 150, 165), "radius": 31, "points": 2},
    "banana":     {"rind": (250, 214, 32), "stripe": (195, 152, 12), "flesh": (255, 248, 205), "hi": (255, 250, 165), "radius": 42, "points": 1},
}


# ---------- Drawing helpers (original code theke hubohu) ----------
def rot_pt(px, py, cx, cy, angle_deg):
    rad = math.radians(-angle_deg)
    dx, dy = px - cx, py - cy
    rx = cx + dx * math.cos(rad) - dy * math.sin(rad)
    ry = cy + dx * math.sin(rad) + dy * math.cos(rad)
    return (rx, ry)

def draw_realistic_banana_direct(surface, cx, cy, r, angle, main_col, shadow_col, hi_col, half=0):
    outer_pts = []
    inner_pts = []
    steps = 16
    for i in range(steps + 1):
        t = i / steps
        ang = math.radians(200 - t * 140)
        ox = cx + math.cos(ang) * (r * 1.15)
        oy = cy - r * 0.25 + math.sin(ang) * (r * 0.85)
        outer_pts.append(rot_pt(ox, oy, cx, cy, angle))

        thickness = math.sin(t * math.pi) * (r * 0.44) + 3
        ix = cx + math.cos(ang) * (r * 1.15 - thickness * 0.6)
        iy = cy - r * 0.25 + math.sin(ang) * (r * 0.85 - thickness)
        inner_pts.append(rot_pt(ix, iy, cx, cy, angle))

    full_poly = outer_pts + list(reversed(inner_pts))
    if half == 1:
        full_poly = [p for p in full_poly if p[1] <= cy + 2]
    elif half == 2:
        full_poly = [p for p in full_poly if p[1] >= cy - 2]

    if len(full_poly) >= 3:
        pygame.draw.polygon(surface, main_col, full_poly)

    mid_pts = [((o[0] + i[0]) / 2, (o[1] + i[1]) / 2) for o, i in zip(outer_pts[2:-2], inner_pts[2:-2])]
    if half == 1:
        mid_pts = [p for p in mid_pts if p[1] <= cy + 2]
    elif half == 2:
        mid_pts = [p for p in mid_pts if p[1] >= cy - 2]
    if len(mid_pts) > 1:
        pygame.draw.lines(surface, shadow_col, False, mid_pts, 2)

    hi_pts = [((o[0] * 0.35 + i[0] * 0.65), (o[1] * 0.35 + i[1] * 0.65)) for o, i in zip(outer_pts[3:-3], inner_pts[3:-3])]
    if half == 1:
        hi_pts = [p for p in hi_pts if p[1] <= cy + 2]
    elif half == 2:
        hi_pts = [p for p in hi_pts if p[1] >= cy - 2]
    if len(hi_pts) > 1:
        pygame.draw.lines(surface, hi_col, False, hi_pts, 3)

    p_start = outer_pts[0]
    p_end = outer_pts[-1]
    if half == 0 or (half == 1 and p_start[1] <= cy) or (half == 2 and p_start[1] >= cy):
        pygame.draw.circle(surface, (65, 42, 16), (int(p_start[0]), int(p_start[1])), max(3, r // 11))
    if half == 0 or (half == 1 and p_end[1] <= cy) or (half == 2 and p_end[1] >= cy):
        tip = rot_pt(cx + math.cos(math.radians(60)) * (r * 1.15) + 6, cy - r * 0.25 + math.sin(math.radians(60)) * (r * 0.85) - 6, cx, cy, angle)
        pygame.draw.line(surface, (85, 62, 22), p_end, tip, max(4, r // 9))
        pygame.draw.circle(surface, (55, 38, 14), (int(tip[0]), int(tip[1])), max(3, r // 11))

def draw_fruit_sprite(surface, ftype, x, y, radius, angle=0, half=0, scale=1.0):
    data = FRUIT_TYPES[ftype]
    r = max(10, int(radius * scale))
    cx, cy = int(x), int(y)

    if ftype in ("banana", "freeze", "frenzy", "double"):
        draw_realistic_banana_direct(surface, cx, cy, r, angle, data["rind"], data["stripe"], data["hi"], half)
        return

    clip_prev = surface.get_clip()
    if half == 1:
        surface.set_clip(pygame.Rect(cx - r * 2, cy - r * 2, r * 4, r * 2))
    elif half == 2:
        surface.set_clip(pygame.Rect(cx - r * 2, cy, r * 4, r * 2))

    if ftype == "watermelon":
        pygame.draw.circle(surface, data["stripe"], (cx, cy + 2), r)
        pygame.draw.circle(surface, data["rind"], (cx, cy), r)
        for dx in (-r // 2, 0, r // 2):
            p_s = rot_pt(cx + dx, cy, cx, cy, angle)
            pygame.draw.circle(surface, data["stripe"], (int(p_s[0]), int(p_s[1])), max(4, r // 6))
        hi_p = rot_pt(cx - r // 3, cy - r // 3, cx, cy, angle)
        pygame.draw.circle(surface, data["hi"], (int(hi_p[0]), int(hi_p[1])), max(4, r // 6))

        if half != 0:
            pygame.draw.circle(surface, (235, 248, 225), (cx, cy), max(5, r - 4))
            pygame.draw.circle(surface, data["flesh"], (cx, cy), max(4, r - 8))
            for deg in range(0, 360, 40):
                sx = cx + int(math.cos(math.radians(deg)) * (r * 0.48))
                sy = cy + int(math.sin(math.radians(deg)) * (r * 0.48))
                pygame.draw.circle(surface, (28, 16, 12), (sx, sy), max(2, r // 14))

    elif ftype == "pineapple":
        l1 = [rot_pt(cx - 18, cy - r + 8, cx, cy, angle), rot_pt(cx - 12, cy - r - 20, cx, cy, angle), rot_pt(cx - 2, cy - r + 5, cx, cy, angle)]
        l2 = [rot_pt(cx + 18, cy - r + 8, cx, cy, angle), rot_pt(cx + 12, cy - r - 20, cx, cy, angle), rot_pt(cx + 2, cy - r + 5, cx, cy, angle)]
        l3 = [rot_pt(cx - 10, cy - r + 6, cx, cy, angle), rot_pt(cx, cy - r - 26, cx, cy, angle), rot_pt(cx + 10, cy - r + 6, cx, cy, angle)]
        pygame.draw.polygon(surface, (28, 135, 45), l1)
        pygame.draw.polygon(surface, (28, 135, 45), l2)
        pygame.draw.polygon(surface, (54, 202, 74), l3)
        pygame.draw.circle(surface, data["stripe"], (cx, cy + 3), r - 2)
        pygame.draw.circle(surface, data["rind"], (cx, cy), r - 2)
        for gx in range(cx - r + 10, cx + r - 8, 12):
            p_a = rot_pt(gx, cy - r + 10, cx, cy, angle)
            p_b = rot_pt(gx + 10, cy + r - 10, cx, cy, angle)
            pygame.draw.line(surface, data["stripe"], p_a, p_b, 2)
        hi_p = rot_pt(cx - r // 3, cy - r // 3, cx, cy, angle)
        pygame.draw.circle(surface, data["hi"], (int(hi_p[0]), int(hi_p[1])), max(4, r // 6))

    elif ftype == "strawberry":
        pts = [
            rot_pt(cx - r + 3, cy - 8, cx, cy, angle),
            rot_pt(cx + r - 3, cy - 8, cx, cy, angle),
            rot_pt(cx, cy + r + 2, cx, cy, angle),
        ]
        pygame.draw.polygon(surface, data["rind"], pts)
        c_l = rot_pt(cx - 9, cy - 9, cx, cy, angle)
        c_r = rot_pt(cx + 9, cy - 9, cx, cy, angle)
        pygame.draw.circle(surface, data["rind"], (int(c_l[0]), int(c_l[1])), max(8, r // 2))
        pygame.draw.circle(surface, data["rind"], (int(c_r[0]), int(c_r[1])), max(8, r // 2))
        for sx, sy in [(-8, -2), (8, -2), (0, 6), (-5, 13), (5, 13), (0, -7)]:
            sp = rot_pt(cx + sx, cy + sy, cx, cy, angle)
            pygame.draw.circle(surface, (255, 225, 95), (int(sp[0]), int(sp[1])), 2)
        leaf = [
            rot_pt(cx - 16, cy - 20, cx, cy, angle),
            rot_pt(cx + 16, cy - 20, cx, cy, angle),
            rot_pt(cx, cy - 10, cx, cy, angle),
        ]
        pygame.draw.polygon(surface, (34, 168, 52), leaf)
        hi_p = rot_pt(cx - 10, cy - 9, cx, cy, angle)
        pygame.draw.circle(surface, data["hi"], (int(hi_p[0]), int(hi_p[1])), 4)

    elif ftype == "orange":
        pygame.draw.circle(surface, data["stripe"], (cx, cy + 2), r)
        pygame.draw.circle(surface, data["rind"], (cx, cy), r)
        for px, py in [(-10, 8), (12, 5), (-4, 15), (8, -10), (-14, -6)]:
            pp = rot_pt(cx + px, cy + py, cx, cy, angle)
            pygame.draw.circle(surface, data["stripe"], (int(pp[0]), int(pp[1])), 2)
        hi_p = rot_pt(cx - r // 3, cy - r // 3, cx, cy, angle)
        pygame.draw.circle(surface, data["hi"], (int(hi_p[0]), int(hi_p[1])), max(4, r // 6))
        st_p = rot_pt(cx, cy - r + 4, cx, cy, angle)
        pygame.draw.circle(surface, (45, 145, 45), (int(st_p[0]), int(st_p[1])), 4)

    else:
        pygame.draw.circle(surface, data["stripe"], (cx, cy + 2), r)
        pygame.draw.circle(surface, data["rind"], (cx, cy), r)
        hi_p = rot_pt(cx - r // 3, cy - r // 3, cx, cy, angle)
        pygame.draw.circle(surface, data["hi"], (int(hi_p[0]), int(hi_p[1])), max(4, r // 6))
        s1 = rot_pt(cx, cy - r + 5, cx, cy, angle)
        s2 = rot_pt(cx + 4, cy - r - 10, cx, cy, angle)
        pygame.draw.line(surface, (72, 40, 14), s1, s2, 4)
        lf_p = rot_pt(cx + 10, cy - r - 8, cx, cy, angle)
        pygame.draw.circle(surface, (46, 175, 62), (int(lf_p[0]), int(lf_p[1])), 6)

    if half != 0:
        surface.set_clip(clip_prev)


# ---------- Effects ----------
class Particle:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        ang = random.uniform(0, 2 * math.pi)
        spd = random.uniform(2, 9.5)
        self.vx, self.vy = math.cos(ang) * spd, math.sin(ang) * spd
        self.color = color
        self.radius = random.randint(4, 9)
        self.life = 1.0

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.26
        self.life -= 0.028

    def draw(self, surf):
        if self.life > 0:
            pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), max(1, int(self.radius * self.life)))


class JuiceSplatter:
    def __init__(self, x, y, color):
        self.x, self.y, self.color = x, y, color
        self.life = 120
        self.blobs = [(random.randint(-30, 30), random.randint(-30, 30), random.randint(5, 16)) for _ in range(7)]

    def update(self):
        self.life -= 1

    def draw(self, surf):
        scale = min(1.0, self.life / 40.0)
        for bx, by, br in self.blobs:
            pygame.draw.circle(surf, self.color, (int(self.x + bx), int(self.y + by)), max(1, int(br * scale)))


# ---------- Entities ----------
class FruitEntity:
    def __init__(self, ftype):
        self.ftype = ftype
        self.radius = FRUIT_TYPES[ftype]["radius"]
        self.x = random.randint(150, BASE_W - 150)
        self.y = BASE_H + 45
        target_x = BASE_W // 2 + random.randint(-260, 260)
        self.vx = (target_x - self.x) * random.uniform(0.012, 0.022)
        self.vy = random.uniform(-17.4, -13.8)
        self.gravity = 0.34
        self.angle = random.uniform(0, 360)
        self.rot_speed = random.uniform(-4.5, 4.5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.angle += self.rot_speed

    def draw(self, surf):
        draw_fruit_sprite(surf, self.ftype, self.x, self.y, self.radius, self.angle)


class SlicedHalf:
    def __init__(self, ftype, x, y, angle, side):
        self.ftype, self.x, self.y, self.angle, self.side = ftype, x, y, angle, side
        self.vx = random.uniform(-5.5, -1.5) if side == 1 else random.uniform(1.5, 5.5)
        self.vy = random.uniform(-4.5, 1.0)
        self.rot_speed = -5.5 if side == 1 else 5.5

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.42
        self.angle += self.rot_speed

    def draw(self, surf):
        draw_fruit_sprite(surf, self.ftype, self.x, self.y, FRUIT_TYPES[self.ftype]["radius"], self.angle, self.side)


def check_slash_hit(p1, p2, cx, cy, r):
    """Line segment (p1->p2) er sathe circle (cx, cy, r) er collision check."""
    x1, y1 = p1
    x2, y2 = p2
    dx, dy = x2 - x1, y2 - y1
    if dx == 0 and dy == 0:
        return math.hypot(cx - x1, cy - y1) <= r
    t = max(0, min(1, ((cx - x1) * dx + (cy - y1) * dy) / (dx * dx + dy * dy)))
    nx, ny = x1 + t * dx, y1 + t * dy
    return math.hypot(cx - nx, cy - ny) <= r


# ---------- Game ----------
class Game:
    def __init__(self):
        self.score = 0
        self.fruits, self.halves = [], []
        self.particles, self.splatters = [], []
        self.blade_trail = []
        self.spawn_timer = 30

    def spawn_wave(self):
        for _ in range(random.randint(2, 4)):
            self.fruits.append(FruitEntity(random.choice(list(FRUIT_TYPES.keys()))))

    def process_slash(self, p1, p2):
        for fruit in self.fruits[:]:
            if check_slash_hit(p1, p2, fruit.x, fruit.y, fruit.radius + 10):
                self.fruits.remove(fruit)
                fdata = FRUIT_TYPES[fruit.ftype]
                self.halves.append(SlicedHalf(fruit.ftype, fruit.x, fruit.y, fruit.angle, 1))
                self.halves.append(SlicedHalf(fruit.ftype, fruit.x, fruit.y, fruit.angle, 2))
                self.splatters.append(JuiceSplatter(fruit.x, fruit.y, fdata["flesh"]))
                for _ in range(18):
                    self.particles.append(Particle(fruit.x, fruit.y, fdata["flesh"]))
                self.score += fdata["points"]

    def update(self):
        now = pygame.time.get_ticks()
        self.blade_trail = [pt for pt in self.blade_trail if now - pt[2] < 140]

        for lst, dead in ((self.particles, lambda p: p.life <= 0),
                          (self.splatters, lambda s: s.life <= 0),
                          (self.halves, lambda h: h.y > BASE_H + 80)):
            for obj in lst[:]:
                obj.update()
                if dead(obj):
                    lst.remove(obj)

        self.spawn_timer -= 1
        if self.spawn_timer <= 0:
            self.spawn_wave()
            self.spawn_timer = 110

        for fruit in self.fruits[:]:
            fruit.update()
            if fruit.y > BASE_H + 70 and fruit.vy > 0:
                self.fruits.remove(fruit)  # Week 1: miss korle kono penalty nai

    def draw(self, surf):
        surf.blit(board_bg, (0, 0))
        for s in self.splatters:
            s.draw(surf)
        for f in self.fruits:
            f.draw(surf)
        for h in self.halves:
            h.draw(surf)
        for p in self.particles:
            p.draw(surf)

        # Score HUD
        draw_fruit_sprite(surf, "watermelon", 54, 52, 28, 0, 1)
        sc_shd = font_score.render(str(self.score), True, GOLD_SHADOW)
        sc_lbl = font_score.render(str(self.score), True, GOLD)
        surf.blit(sc_shd, (96, 28))
        surf.blit(sc_lbl, (94, 26))
        hint = font_small.render("Swipe the mouse to slice fruits  •  ESC to quit", True, CREAM)
        surf.blit(hint, (96, 76))

        # Blade trail
        n = len(self.blade_trail)
        for i in range(1, n):
            p1 = self.blade_trail[i - 1][:2]
            p2 = self.blade_trail[i][:2]
            w = max(2, int((i / n) * 12))
            pygame.draw.line(surf, BLADE_GLOW, p1, p2, w + 6)
            pygame.draw.line(surf, BLADE_CORE, p1, p2, w)


def main():
    game = Game()
    last_pos = None
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                curr = event.pos
                if last_pos is not None and math.hypot(curr[0] - last_pos[0], curr[1] - last_pos[1]) > 4:
                    game.blade_trail.append((curr[0], curr[1], pygame.time.get_ticks()))
                    game.process_slash(last_pos, curr)
                last_pos = curr

        game.update()
        game.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
