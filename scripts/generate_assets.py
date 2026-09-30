#!/usr/bin/env python3
"""Generates all animated SVG cards for the profile README into ./assets"""
import os, sys, textwrap
from xml.sax.saxutils import escape as esc

OUT = sys.argv[1] if len(sys.argv) > 1 else "assets"
os.makedirs(OUT, exist_ok=True)

BG, CARD, BORDER, TXT, MUTED = "#0d1117", "#161b22", "#30363d", "#e6edf3", "#8b949e"
BLUE, PURPLE, CYAN, GREEN = "#58a6ff", "#a371f7", "#39c5cf", "#3fb950"
MONO = "'JetBrains Mono','SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"
SANS = "-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"

STYLE = """
.m{font-family:__MONO__}.s{font-family:__SANS__}
@keyframes fu{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
.fu{animation:fu .7s ease backwards}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}
.pulse{animation:pulse 2s ease-in-out infinite}
@keyframes dash{to{stroke-dashoffset:-20}}
.dash{stroke-dasharray:5 5;animation:dash 1.2s linear infinite}
@keyframes act{0%,14%{opacity:1}18%,100%{opacity:0}}
""".replace("__MONO__", MONO).replace("__SANS__", SANS)


def doc(w, h, body, title, defs="", style=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(title)}">
<title>{esc(title)}</title>
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{BLUE}"/><stop offset=".55" stop-color="{PURPLE}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
<marker id="ar" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="{MUTED}"/></marker>{defs}</defs>
<style>{STYLE}{style}</style>
{body}
</svg>'''


def save(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)


def tx(x, y, text, size=13, fill=TXT, cls="s", weight=400, anchor="start", ls=None, extra=""):
    l = f' letter-spacing="{ls}"' if ls else ""
    return (f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}"{l} {extra}>{esc(text)}</text>')


def fu(inner, delay=0):
    return f'<g class="fu" style="animation-delay:{delay}s">{inner}</g>'


def chip(x, y, text, kind, color, fs=11):
    w = round(len(text) * fs * 0.6 + 18, 1)
    if kind == "accent":
        fill, fo, st, so, tc = color, ".13", color, ".55", color
    else:
        fill, fo, st, so, tc = "#21262d", "1", BORDER, "1", "#c9d1d9"
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="22" rx="6" fill="{fill}" fill-opacity="{fo}" stroke="{st}" stroke-opacity="{so}"/>'
         f'<text x="{round(x + w / 2, 1)}" y="{y + 15}" class="m" font-size="{fs}" fill="{tc}" text-anchor="middle">{esc(text)}</text>')
    return s, w


def chips_flow(items, maxw, y0, x0=20, gap=6):
    x, y, out = x0, y0, []
    for text, kind, color in items:
        _, w = chip(0, 0, text, kind, color)
        if x + w > x0 + maxw and x > x0:
            x, y = x0, y + 28
        s, w = chip(x, y, text, kind, color)
        out.append(s)
        x += w + gap
    return "".join(out), y + 22


def card(x, y, w, h, label, color, inner="", delay=0):
    return (f'<g transform="translate({x},{y})">' + fu(
        f'<rect width="{w}" height="{h}" rx="12" fill="{CARD}" stroke="{BORDER}"/>'
        f'<path d="M14 .5 H{w - 14}" stroke="{color}" stroke-width="2" opacity=".85"/>'
        f'<circle cx="20" cy="26" r="3.5" fill="{color}"/>'
        + tx(32, 30, label, 11, MUTED, "m", 600, ls=1.5) + inner, delay) + '</g>')


def list_card(x, y, w, h, label, color, items, delay=0):
    inner = "".join(
        f'<text x="20" y="{62 + 22 * i}" class="s" font-size="13.5" fill="#c9d1d9"><tspan fill="{color}">›  </tspan>{esc(it)}</text>'
        for i, it in enumerate(items))
    return card(x, y, w, h, label, color, inner, delay)


# ------------------------------------------------------------------ section headers
def section(fn, idx, title, sub):
    body = fu(
        tx(0, 36, idx, 13, BLUE, "m", 600) + tx(34, 40, title, 26, TXT, "s", 700)
        + tx(800, 38, sub, 11, MUTED, "m", anchor="end")
        + f'<rect x="0" y="54" width="800" height="1" fill="{BORDER}"/>'
        + f'<rect x="0" y="53" width="140" height="3" rx="1.5" fill="url(#g)"><animate attributeName="x" values="0;660;0" dur="7s" repeatCount="indefinite"/></rect>')
    save(fn, doc(800, 64, body, title))


SECTIONS = [
    ("sec-profile.svg", "01", "Profile", "// identity.config"),
    ("sec-analytics.svg", "02", "GitHub Analytics", "// live data"),
    ("sec-activity.svg", "03", "Contribution Activity", "// commits · PRs · issues"),
    ("sec-building.svg", "04", "Currently Building", "// in progress"),
    ("sec-projects.svg", "05", "Featured Projects", "// concepts and builds"),
    ("sec-stack.svg", "06", "Languages & Tools", "// working stack"),
    ("sec-interests.svg", "07", "Technical Interests", "// focus areas"),
    ("sec-philosophy.svg", "08", "Engineering Philosophy", "// the loop"),
    ("sec-ai.svg", "09", "AI × Development", "// workflow"),
    ("sec-roadmap.svg", "10", "Learning Roadmap", "// now · next · later"),
    ("sec-trophies.svg", "11", "GitHub Trophies", "// achievements"),
    ("sec-connect.svg", "12", "Connect With Me", "// links"),
]
for s in SECTIONS:
    section(*s)


# ------------------------------------------------------------------ hero
def hero():
    W, H = 900, 280
    defs = f'''
<linearGradient id="gn" x1="0" y1="0" x2="0.6" y2="0" spreadMethod="reflect"><stop offset="0" stop-color="{BLUE}"/><stop offset=".5" stop-color="{PURPLE}"/><stop offset="1" stop-color="{CYAN}"/><animateTransform attributeName="gradientTransform" type="translate" values="0 0;0.6 0;0 0" dur="8s" repeatCount="indefinite"/></linearGradient>
<radialGradient id="rad"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/></radialGradient>
<mask id="fade"><rect width="{W}" height="{H}" fill="url(#rad)"/></mask>
<pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" fill="none" stroke="#262c36" stroke-width="1"/></pattern>
<radialGradient id="b1"><stop offset="0" stop-color="{BLUE}" stop-opacity=".28"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>
<radialGradient id="b2"><stop offset="0" stop-color="{PURPLE}" stop-opacity=".26"/><stop offset="1" stop-color="{PURPLE}" stop-opacity="0"/></radialGradient>
<clipPath id="cl"><rect width="{W}" height="{H}" rx="16"/></clipPath>'''
    cyc = """
@keyframes cyc{0%{opacity:0}4%,30%{opacity:1}34%,100%{opacity:0}}
.c{opacity:0;animation:cyc 9s infinite}
.c1{opacity:1;animation-delay:0s}.c2{animation-delay:3s}.c3{animation-delay:6s}
@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}
"""
    lines = ["Building software, experimenting with products, and turning real-world problems into systems.",
             "Builder mindset over tutorial mindset.",
             "Designing systems. Building products. Learning by shipping."]
    cyc_txt = "".join(
        f'<text x="450" y="224" class="m c c{i + 1}" font-size="14" fill="{TXT}" text-anchor="middle"><tspan fill="{BLUE}">› </tspan>{esc(l)}</text>'
        for i, l in enumerate(lines))
    particles = "".join(
        f'<circle cx="{x}" cy="{y}" r="1.6" fill="{BLUE}"><animate attributeName="opacity" values=".08;.9;.08" dur="{d}s" begin="{b}s" repeatCount="indefinite"/></circle>'
        for x, y, d, b in [(90, 90, 3, 0), (240, 200, 4, 1), (380, 70, 3.5, .5), (560, 210, 4, 2), (700, 80, 3, 1.4), (820, 150, 4.5, .8), (150, 160, 3.2, 2.2), (760, 230, 3.8, .3)])
    body = f'''<g clip-path="url(#cl)">
<rect width="{W}" height="{H}" rx="16" fill="{BG}"/>
<rect width="{W}" height="{H}" fill="url(#grid)" mask="url(#fade)"/>
<circle cx="220" cy="130" r="230" fill="url(#b1)"><animateTransform attributeName="transform" type="translate" values="0 0;70 20;0 0" dur="14s" repeatCount="indefinite"/></circle>
<circle cx="700" cy="150" r="230" fill="url(#b2)"><animateTransform attributeName="transform" type="translate" values="0 0;-70 -20;0 0" dur="16s" repeatCount="indefinite"/></circle>
{particles}
<rect x="0" y="38" width="{W}" height="2" fill="url(#g)" opacity=".4"><animateTransform attributeName="transform" type="translate" values="0 0;0 236;0 0" dur="9s" repeatCount="indefinite"/></rect>
<rect width="{W}" height="38" fill="#0d1117" opacity=".7"/>
<line x1="0" y1="38" x2="{W}" y2="38" stroke="{BORDER}"/>
<circle cx="24" cy="19" r="5" fill="#ff5f56" opacity=".85"/><circle cx="42" cy="19" r="5" fill="#ffbd2e" opacity=".85"/><circle cx="60" cy="19" r="5" fill="#27c93f" opacity=".85"/>
{tx(84, 23, "praful@builder:~/RajputPraful", 12, MUTED, "m")}
{tx(W - 24, 23, "main", 12, MUTED, "m", anchor="end")}
{fu(tx(450, 128, "PRAFUL SINGH", 60, "url(#gn)", "s", 800, "middle", 2))}
{fu(tx(450, 168, "COMPUTER SCIENCE ENGINEER  •  DEVELOPER  •  BUILDER", 14, MUTED, "m", 500, "middle", 3), .3)}
{cyc_txt}
<line x1="24" y1="246" x2="{W - 24}" y2="246" stroke="{BORDER}" opacity=".7"/>
<circle cx="30" cy="265" r="3.5" fill="{GREEN}" class="pulse"/>
{tx(42, 269, "building: private bus mobility platform", 11, MUTED, "m")}
{tx(W - 24, 269, "Amrita University · Kerala, India · Nepal", 11, MUTED, "m", anchor="end")}
</g>
<rect width="{W}" height="{H}" rx="16" fill="none" stroke="{BORDER}"/>'''
    save("hero.svg", doc(W, H, body, "Praful Singh - Computer Science Engineer, Developer, Builder", defs, cyc))


hero()


# ------------------------------------------------------------------ profile dashboard
def profile():
    cw, ch = 388, 136
    xs = [0, 412]
    ys = [0, 152, 304]
    cards = []

    def kv(k, v, y):
        return tx(20, y, k, 10, MUTED, "m", 600, ls=1) + tx(110, y, v, 14, TXT, "s", 500)

    c1 = (tx(20, 66, "Praful Singh", 22, TXT, "s", 700) + tx(20, 88, "Computer Science Engineer", 13, MUTED)
          + tx(20, 106, "Developer · Builder", 13, MUTED) + tx(20, 124, "@RajputPraful", 12, BLUE, "m"))
    c2 = (tx(20, 66, "B.Tech · Computer Science Engineering", 15, TXT, "s", 600)
          + tx(20, 92, "Amrita University, Amritapuri", 13, MUTED) + tx(20, 112, "Kerala, India", 13, MUTED))
    c3 = kv("BASED IN", "Kerala, India", 66) + kv("ORIGIN", "Nepal", 90) + kv("HOMETOWN", "Rajbiraj, Saptari, Nepal", 114)
    ch4, _ = chips_flow([(t, "accent", GREEN) for t in ["Software Engineering", "Full Stack", "Backend", "Database Systems", "System Design", "DSA", "Product Development"]], 348, 46)
    c5 = (tx(20, 66, "Private Bus Mobility Platform", 16, TXT, "s", 700) + tx(20, 88, "Booking · Operators · GPS · Admin", 12, MUTED, "m")
          + f'<circle cx="24" cy="112" r="3.5" fill="{GREEN}" class="pulse"/>' + tx(36, 116, "In design & development", 11, GREEN, "m"))
    ch6, _ = chips_flow([(t, "accent", PURPLE) for t in ["Backend Architecture", "Scalable Systems", "AI-assisted Development", "Product Engineering", "Startup Engineering"]], 348, 46)
    data = [("PROFILE", BLUE, c1), ("EDUCATION", PURPLE, c2), ("LOCATION", CYAN, c3),
            ("CURRENT FOCUS", GREEN, ch4), ("BUILDING", BLUE, c5), ("INTERESTS", PURPLE, ch6)]
    for i, (lab, col, inner) in enumerate(data):
        cards.append(card(xs[i % 2], ys[i // 2], cw, ch, lab, col, inner, round(i * .12, 2)))
    qy = 456
    quote = fu(f'<g transform="translate(0,{qy})"><rect width="800" height="70" rx="12" fill="{CARD}" stroke="{BORDER}"/>'
               f'<rect width="5" height="70" rx="2.5" fill="url(#g)"/>'
               + tx(28, 32, "“Builder mindset over tutorial mindset.”", 20, TXT, "s", 700)
               + tx(28, 54, "I build systems, experiment with products, solve real-world problems and learn by shipping.", 12, MUTED, "m")
               + '</g>', .8)
    save("profile.svg", doc(800, qy + 70, "".join(cards) + quote, "Profile dashboard"))


profile()


# ------------------------------------------------------------------ currently building
def building():
    b = []
    # header
    hdr = (f'<circle cx="24" cy="26" r="4" fill="{GREEN}" class="pulse"/>' + tx(36, 30, "IN DESIGN & DEVELOPMENT", 11, GREEN, "m", 600, ls=1.5)
           + tx(20, 70, "PRIVATE BUS MOBILITY PLATFORM", 27, "url(#g)", "s", 800)
           + tx(20, 96, "A digital bus booking and operator management platform designed to solve problems", 13, MUTED)
           + tx(20, 114, "in traditional private bus booking systems.", 13, MUTED))
    b.append(f'<g>' + fu(f'<rect width="800" height="132" rx="12" fill="{CARD}" stroke="{BORDER}"/><rect width="800" height="132" rx="12" fill="url(#g)" opacity=".05"/>' + hdr) + '</g>')
    # architecture
    ay = 148
    nodes = [("Passenger", BLUE), ("Booking Engine", BLUE), ("Operator Dashboard", PURPLE), ("Admin Control Center", CYAN)]
    nw, gap = 150, (760 - 4 * 150) / 3
    inner = ""
    for i, (n, c) in enumerate(nodes):
        x = round(20 + i * (nw + gap), 1)
        inner += (f'<rect x="{x}" y="46" width="{nw}" height="44" rx="8" fill="{BG}" stroke="{c}" stroke-opacity=".7"/>'
                  + tx(round(x + nw / 2, 1), 73, n, 11.5, TXT, "m", 500, "middle"))
        if i < 3:
            x1, x2 = round(x + nw + 4, 1), round(x + nw + gap - 4, 1)
            inner += (f'<line x1="{x1}" y1="68" x2="{x2}" y2="68" stroke="{MUTED}" class="dash" marker-end="url(#ar)"/>'
                      f'<circle r="3" fill="{c}"><animateMotion dur="2.4s" begin="{i * .8}s" repeatCount="indefinite" path="M{x1},68 L{x2},68"/></circle>')
    b.append(f'<g transform="translate(0,{ay})">' + fu(f'<rect width="800" height="110" rx="12" fill="{CARD}" stroke="{BORDER}"/>'
             f'<circle cx="20" cy="26" r="3.5" fill="{BLUE}"/>' + tx(32, 30, "PLANNED ARCHITECTURE", 11, MUTED, "m", 600, ls=1.5)
             + f'<g transform="translate(0,0)">{inner}</g>'.replace('x="', 'x="', 1), .15) + '</g>')
    # feature grid
    feats = [
        ("DISCOVERY", BLUE, ["Bus search", "Route search", "From / To selection", "Seat availability"]),
        ("BOOKING", PURPLE, ["Seat booking", "Pricing", "Passenger management", "Booking management", "Refund workflow"]),
        ("OPERATORS", CYAN, ["Operator dashboard", "Bus registration", "Operator management"]),
        ("REAL-TIME", GREEN, ["Live bus location", "GPS tracking using phone"]),
        ("CONTROL CENTER", BLUE, ["Central admin control", "Operator oversight", "Refund handling"]),
        ("PLATFORM", PURPLE, ["Commission system", "Scalable backend architecture"]),
    ]
    gy = 274
    for i, (lab, col, items) in enumerate(feats):
        b.append(list_card((i % 3) * 272, gy + (0 if i < 3 else 182), 256, 166 if i < 3 else 116, lab, col, items, .3 + i * .1))
    # commission
    my = gy + 182 + 116 + 16
    bar = (f'<rect x="300" y="52" width="440" height="10" rx="5" fill="#21262d"/>'
           f'<rect x="300" y="52" width="22" height="10" rx="5" fill="url(#g)" class="pulse"/>')
    b.append(f'<g transform="translate(0,{my})">' + fu(
        f'<rect width="800" height="100" rx="12" fill="{CARD}" stroke="{BORDER}"/><circle cx="20" cy="26" r="3.5" fill="{CYAN}"/>'
        + tx(32, 30, "BUSINESS MODEL · COMMISSION", 11, MUTED, "m", 600, ls=1.5)
        + tx(20, 78, "5%", 38, "url(#g)", "s", 800) + tx(84, 62, "per booking", 14, TXT, "s", 600) + tx(84, 80, "target commission concept", 11, MUTED, "m")
        + bar + tx(300, 82, "revenue model: commission from bookings", 11, MUTED, "m"), 1.0) + '</g>')
    save("building.svg", doc(800, my + 100, "".join(b), "Private Bus Mobility Platform - currently building"))


building()


# ------------------------------------------------------------------ projects
def project_content(w, color, title, desc, stack, focus, status=None):
    inner = ""
    if status:
        t, c = status
        sw = round(len(t) * 6 + 16, 1)
        inner += (f'<rect x="{round(w - 16 - sw, 1)}" y="15" width="{sw}" height="20" rx="5" fill="{c}" fill-opacity=".14" stroke="{c}" stroke-opacity=".6"/>'
                  + tx(round(w - 16 - sw / 2, 1), 29, t, 10, c, "m", 600, "middle"))
    inner += tx(20, 62, title, 19, TXT, "s", 700)
    wrapped = textwrap.wrap(desc, int((w - 40) / 6.4))
    for i, l in enumerate(wrapped):
        inner += tx(20, 84 + 17 * i, l, 12.5, MUTED)
    y0 = 84 + 17 * len(wrapped) + 4
    items = [(s, "accent", color) for s in stack] + [(f, "plain", color) for f in focus]
    ch, end = chips_flow(items, w - 40, y0)
    return inner + ch, end + 20


def projects():
    P = [
        ("01 · MOBILITY", BLUE, "Bus Mobility Platform", "Digital bus booking and operator management for private bus systems.",
         [], ["Booking", "Seat Management", "Operators", "GPS", "Admin", "Scalability"], ("IN DESIGN / DEV", GREEN)),
        ("02 · E-COMMERCE", PURPLE, "SWADIKA", "A food / spice product and e-commerce concept.",
         ["HTML", "CSS", "JavaScript", "Flask", "REST API", "MySQL"],
         ["E-commerce", "Product Management", "Inventory", "Orders", "Backend APIs", "Admin Systems"], ("CONCEPT", PURPLE)),
        ("03 · SYSTEMS", CYAN, "Hotel Management System", "Database-driven hotel management system.",
         ["Flask", "PostgreSQL", "REST API", "JavaScript", "SQL"],
         ["Customers", "Rooms", "Reservations", "Staff", "Services", "Service Requests", "Bills", "Housekeeping"], None),
        ("04 · DATA / GEO", GREEN, "Tourism Intelligence", "Tourism data and location intelligence.",
         ["Node.js", "PostgreSQL", "PostGIS", "Prisma", "Vite"],
         ["Tourism Data", "Location Intelligence", "Price Anomaly Detection", "Receipt OCR", "Sentiment Analysis", "Tourism Insights"], None),
        ("05 · AI / PLANNING", BLUE, "AI Expedition Planner / Polar-X", "AI-assisted expedition planning system.",
         [], ["AI Planning", "Route Planning", "Environmental Considerations", "Risk Awareness", "Decision Support"], ("CONCEPT", PURPLE)),
    ]
    cw = 388
    out, y, d = [], 0, 0
    for r in range(3):
        row = P[r * 2:r * 2 + 2] if r < 2 else P[4:]
        w = cw if r < 2 else 800
        built = [project_content(w, p[1], p[2], p[3], p[4], p[5], p[6]) for p in row]
        H = max(h for _, h in built)
        for i, (p, (inner, _)) in enumerate(zip(row, built)):
            out.append(card(i * 412, y, w, H, p[0], p[1], inner, d))
            d += .15
        y += H + 16
    save("projects.svg", doc(800, y - 16, "".join(out), "Featured projects"))


projects()


# ------------------------------------------------------------------ interests
def interests():
    groups = [("ENGINEERING", BLUE, ["Software Engineering", "Full Stack Development", "Backend Engineering", "Product Engineering"]),
              ("SYSTEMS", PURPLE, ["Database Architecture", "System Design", "REST APIs", "Scalable Systems"]),
              ("DIRECTION", CYAN, ["Data Structures & Algorithms", "AI-assisted Development", "Startup Engineering"])]
    body = "".join(list_card(i * 272, 0, 256, 150, l, c, it, i * .15) for i, (l, c, it) in enumerate(groups))
    save("interests.svg", doc(800, 150, body, "Technical interests"))


interests()


# ------------------------------------------------------------------ flows
def node_flow(labels, colors, w_node, y, h, gap, step, cycle, x0=16):
    out, cxs = "", []
    for i, (lab, col) in enumerate(zip(labels, colors)):
        x = round(x0 + i * (w_node + gap), 1)
        cx = round(x + w_node / 2, 1)
        cxs.append(cx)
        out += f'<rect x="{x}" y="{y}" width="{w_node}" height="{h}" rx="10" fill="{CARD}" stroke="{BORDER}"/>'
        out += (f'<rect x="{x}" y="{y}" width="{w_node}" height="{h}" rx="10" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-width="1.5" '
                f'style="opacity:0;animation:act {cycle}s linear infinite;animation-delay:{i * step}s"/>')
        parts = lab if isinstance(lab, tuple) else (lab,)
        for j, p in enumerate(parts):
            yy = y + h / 2 + 4 + (j - (len(parts) - 1) / 2) * 15
            out += tx(cx, round(yy, 1), p, 11, TXT, "m", 700, "middle", 0.5)
        if i < len(labels) - 1:
            out += f'<line x1="{round(x + w_node + 3, 1)}" y1="{y + h / 2}" x2="{round(x + w_node + gap - 3, 1)}" y2="{y + h / 2}" stroke="{MUTED}" marker-end="url(#ar)"/>'
    return out, cxs


def philosophy():
    labels = ["BUILD", "BREAK", "DEBUG", "LEARN", "SHIP", "ITERATE"]
    cols = [BLUE, BLUE, PURPLE, PURPLE, CYAN, CYAN]
    nw = 104
    gap = (768 - 6 * nw) / 5
    nodes, cx = node_flow(labels, cols, nw, 36, 56, gap, 2, 12)
    nums = "".join(tx(c, 28, f"0{i + 1}", 10, MUTED, "m", 600, "middle", 1) for i, c in enumerate(cx))
    ret = (f'<path d="M{cx[-1]},{92 + 3} V120 H{cx[0]} V{92 + 6}" fill="none" stroke="{CYAN}" stroke-opacity=".7" class="dash" marker-end="url(#ar)"/>'
           + f'<circle r="3.5" fill="{CYAN}"><animateMotion dur="5s" repeatCount="indefinite" path="M{cx[-1]},95 V120 H{cx[0]} V98"/></circle>'
           + f'<rect x="352" y="112" width="96" height="16" fill="{BG}"/>' + tx(400, 124, "REPEAT", 10, MUTED, "m", 600, "middle", 2))
    cap = tx(400, 152, "Understand the system first. Then build it, break it and ship it again.", 12, MUTED, "m", anchor="middle")
    body = f'<rect width="800" height="164" rx="12" fill="{BG}"/>' + fu(nums + nodes + ret + cap)
    save("flow-build.svg", doc(800, 164, body, "Build, break, debug, learn, ship, iterate"))


philosophy()


def ai_flow():
    labels = ["PROTOTYPE", "EXPLORE", "ACCELERATE", ("HUMAN", "VERIFICATION"), "TESTING", "ARCHITECTURE", "SHIP"]
    cols = [BLUE] * 3 + [PURPLE] * 3 + [CYAN]
    nw = 94
    gap = (768 - 7 * nw) / 6
    nodes, cx = node_flow(labels, cols, nw, 66, 64, gap, 2, 14)
    x = lambda i: round(16 + i * (nw + gap), 1)

    def bracket(a, b, col, txt):
        l, r = x(a), round(x(b) + nw, 1)
        return (f'<path d="M{l},58 V50 H{r} V58" fill="none" stroke="{col}" stroke-opacity=".7"/>'
                + tx(round((l + r) / 2, 1), 40, txt, 10, col, "m", 600, "middle", 2))
    br = bracket(0, 2, BLUE, "AI-ASSISTED") + bracket(3, 5, PURPLE, "HUMAN-LED") + bracket(6, 6, CYAN, "OUTPUT")
    dot = (f'<line x1="16" y1="150" x2="784" y2="150" stroke="{BORDER}"/><line x1="16" y1="150" x2="784" y2="150" stroke="{BLUE}" class="dash" opacity=".6"/>'
           f'<circle r="4" fill="#fff" opacity=".9"><animateMotion dur="9s" repeatCount="indefinite" path="M16,150 H784"/></circle>')
    cap = tx(400, 180, "AI accelerates the work. Verification, testing, architecture and security stay human.", 12, MUTED, "m", anchor="middle")
    body = f'<rect width="800" height="196" rx="12" fill="{BG}"/>' + fu(br + nodes + dot + cap)
    save("flow-ai.svg", doc(800, 196, body, "AI x Development workflow"))


ai_flow()


# ------------------------------------------------------------------ roadmap
def roadmap():
    cols = [
        ("CURRENT", GREEN, ["Java", "DSA", "DBMS", "SQL", "Full Stack Development", "Backend Development", "Git / GitHub", "REST APIs"], True),
        ("NEXT", PURPLE, ["Advanced Backend", "System Design", "Cloud", "DevOps", "Distributed Systems", "AI Integration", "Scalable Architecture"], False),
        ("LONG TERM", CYAN, ["Production Systems", "Product Engineering", "Startup Engineering", "Large-Scale Systems", "Technical Leadership"], False),
    ]
    centers = [128, 400, 672]
    tl = (f'<line x1="128" y1="20" x2="672" y2="20" stroke="{BORDER}"/>'
          f'<line x1="128" y1="20" x2="672" y2="20" stroke="{BLUE}" class="dash" opacity=".7"/>'
          f'<circle r="4" fill="#fff"><animateMotion dur="6s" repeatCount="indefinite" path="M128,20 H672"/></circle>')
    for c, (_, col, _, filled) in zip(centers, cols):
        tl += f'<circle cx="{c}" cy="20" r="7" fill="{BG}" stroke="{col}" stroke-width="2"/>' + (f'<circle cx="{c}" cy="20" r="3" fill="{col}" class="pulse"/>' if filled else "")
    out = [fu(tl)]
    for i, (lab, col, items, filled) in enumerate(cols):
        inner = ""
        for j, it in enumerate(items):
            y = 66 + j * 26
            inner += (f'<circle cx="24" cy="{y - 4}" r="3.5" fill="{col if filled else "none"}" stroke="{col}" stroke-opacity="{1 if filled else .6}"/>'
                      + tx(38, y, it, 13.5, "#c9d1d9" if filled else "#adbac7"))
        out.append(card(i * 272, 48, 256, 48 + len(items) * 26 + 6 if False else 276, lab, col, inner, .2 + i * .15))
    save("roadmap.svg", doc(800, 48 + 276, "".join(out), "Learning roadmap"))


roadmap()


# ------------------------------------------------------------------ footer
def footer():
    words = ["BUILD", "BREAK", "DEBUG", "LEARN", "SHIP", "ITERATE"]
    st = "".join(f".w{i}{{fill:{MUTED};animation:hl 9s infinite;animation-delay:{i * 1.5}s}}" for i in range(6))
    st = "@keyframes hl{0%,12%{fill:#58a6ff}17%,100%{fill:#8b949e}}" + st
    spans = '<tspan fill="#484f58"> → </tspan>'.join(f'<tspan class="w{i}">{w}</tspan>' for i, w in enumerate(words))
    body = (f'<rect x="0" y="10" width="800" height="1" fill="{BORDER}"/>'
            f'<rect x="0" y="9" width="160" height="3" rx="1.5" fill="url(#g)"><animate attributeName="x" values="0;640;0" dur="7s" repeatCount="indefinite"/></rect>'
            + fu(tx(400, 56, "Designing systems. Building products. Learning by shipping.", 18, TXT, "s", 600, "middle")
                 + f'<text x="400" y="88" class="m" font-size="13" font-weight="700" text-anchor="middle" letter-spacing="2">{spans}</text>'
                 + tx(400, 116, "Praful Singh · @RajputPraful", 10, MUTED, "m", anchor="middle", ls=1)))
    save("footer.svg", doc(800, 128, body, "Footer", "", st))


footer()
print("done ->", OUT, sorted(os.listdir(OUT)))
