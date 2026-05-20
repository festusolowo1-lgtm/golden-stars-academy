from pathlib import Path

INDEX = Path("templates/index.html")
html = INDEX.read_text(encoding="utf-8")

# ── STEP 1: Remove the wrongly injected Bootstrap carousel from top of body ──
import re
bad = re.compile(
    r'<div id="heroCarousel".*?</div>\s*</div>\s*</div>\s*<button class="carousel-control-prev".*?</button>\s*<button class="carousel-control-next".*?</button>\s*</div>',
    re.DOTALL
)
html = bad.sub("", html, count=1)
print("Step 1: Removed Bootstrap carousel from top of body")

# ── STEP 2: Replace original carousel-wrap with enhanced illustrated version ──
OLD_CAROUSEL = '''  <div class="carousel-wrap">
    <button class="carousel-nav prev" onclick="moveCarousel(-1)">&#10249;</button>
    <button class="carousel-nav next" onclick="moveCarousel(1)">&#10250;</button>
    <div class="carousel-slide active"><div class="carousel-content"><div class="carousel-quote">"Education is the <em>most powerful weapon</em> you can use to change the world."</div><div class="carousel-author">&#8212; Nelson Mandela &middot; Inspiring Excellence at Golden Stars Academy</div></div></div>
    <div class="carousel-slide"><div class="carousel-content"><div class="carousel-quote">"The <em>function of education</em> is to teach one to think intensively and to think critically."</div><div class="carousel-author">&#8212; Martin Luther King Jr. &middot; Our Guiding Philosophy</div></div></div>
    <div class="carousel-slide"><div class="carousel-content"><div class="carousel-quote">"Tell me and I forget. Teach me and I remember. <em>Involve me and I learn.</em>"</div><div class="carousel-author">&#8212; Benjamin Franklin &middot; Active Learning at Golden Stars</div></div></div>
    <div class="carousel-slide"><div class="carousel-content"><div class="carousel-quote">"Children must be taught <em>how to think</em>, not what to think."</div><div class="carousel-author">&#8212; Margaret Mead &middot; Critical Thinking at the Core</div></div></div>
    <div class="carousel-slide"><div class="carousel-content"><div class="carousel-quote">"<em>God is Able</em> &#8212; our faith anchors our pursuit of excellence, character, and service."</div><div class="carousel-author">&#8212; The Golden Stars Academy Motto &middot; Est. 2011, GRA Gbessa, Abuja</div></div></div>
    <div class="carousel-dots" id="carouselDots"></div>
  </div>'''

NEW_CAROUSEL = '''  <div class="carousel-wrap" style="height:520px;">
    <button class="carousel-nav prev" onclick="moveCarousel(-1)">&#10249;</button>
    <button class="carousel-nav next" onclick="moveCarousel(1)">&#10250;</button>

    <!-- SLIDE 1: Nelson Mandela — Education as a weapon for change -->
    <div class="carousel-slide active" style="background:linear-gradient(160deg,#0f2d5a 0%,#1a3a6b 60%,#1a5c3a 100%);">
      <svg style="position:absolute;inset:0;width:100%;height:100%;opacity:.13" viewBox="0 0 1200 520" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice">
        <!-- Globe representing changing the world -->
        <circle cx="900" cy="260" r="200" fill="none" stroke="#c9a84c" stroke-width="2"/>
        <ellipse cx="900" cy="260" rx="80" ry="200" fill="none" stroke="#c9a84c" stroke-width="1.5"/>
        <ellipse cx="900" cy="260" rx="200" ry="80" fill="none" stroke="#c9a84c" stroke-width="1.5"/>
        <line x1="700" y1="260" x2="1100" y2="260" stroke="#c9a84c" stroke-width="1"/>
        <line x1="900" y1="60" x2="900" y2="460" stroke="#c9a84c" stroke-width="1"/>
        <!-- Torch / weapon of knowledge -->
        <rect x="180" y="280" width="20" height="120" rx="4" fill="#c9a84c" opacity=".6"/>
        <ellipse cx="190" cy="270" rx="22" ry="30" fill="#f59e0b" opacity=".7"/>
        <ellipse cx="190" cy="255" rx="14" ry="22" fill="#fff" opacity=".5"/>
        <ellipse cx="190" cy="245" rx="8" ry="14" fill="#f59e0b" opacity=".9"/>
        <!-- Rays from torch -->
        <line x1="190" y1="240" x2="140" y2="190" stroke="#f59e0b" stroke-width="2" opacity=".4"/>
        <line x1="190" y1="240" x2="240" y2="190" stroke="#f59e0b" stroke-width="2" opacity=".4"/>
        <line x1="190" y1="240" x2="190" y2="180" stroke="#f59e0b" stroke-width="2" opacity=".4"/>
        <line x1="190" y1="240" x2="120" y2="230" stroke="#f59e0b" stroke-width="2" opacity=".3"/>
        <line x1="190" y1="240" x2="260" y2="230" stroke="#f59e0b" stroke-width="2" opacity=".3"/>
        <!-- Stars scattered -->
        <circle cx="400" cy="100" r="3" fill="#c9a84c" opacity=".5"/>
        <circle cx="600" cy="80" r="2" fill="#fff" opacity=".4"/>
        <circle cx="300" cy="400" r="2.5" fill="#c9a84c" opacity=".4"/>
        <circle cx="700" cy="450" r="2" fill="#fff" opacity=".3"/>
      </svg>
      <div class="carousel-content">
        <div class="carousel-quote">"Education is the <em>most powerful weapon</em> you can use to change the world."</div>
        <div class="carousel-author">&#8212; Nelson Mandela &middot; Inspiring Excellence at Golden Stars Academy</div>
        <div style="margin-top:22px;display:flex;justify-content:center;gap:12px;flex-wrap:wrap;">
          <a href="#" onclick="showPage('admissions');return false;" style="background:#c9a84c;color:#fff;padding:.65rem 1.8rem;border-radius:30px;text-decoration:none;font-weight:700;font-size:.9rem;">Enrol Now</a>
          <a href="#" onclick="showPage('who-we-are');return false;" style="border:2px solid rgba(255,255,255,.5);color:#fff;padding:.6rem 1.6rem;border-radius:30px;text-decoration:none;font-weight:600;font-size:.9rem;">About Us</a>
        </div>
      </div>
    </div>

    <!-- SLIDE 2: Martin Luther King Jr. — Think intensively & critically -->
    <div class="carousel-slide" style="background:linear-gradient(160deg,#1a0f4a 0%,#2d1a6b 60%,#0f3a5a 100%);">
      <svg style="position:absolute;inset:0;width:100%;height:100%;opacity:.13" viewBox="0 0 1200 520" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice">
        <!-- Brain / thinking illustration -->
        <ellipse cx="900" cy="220" rx="140" ry="120" fill="none" stroke="#c9a84c" stroke-width="2.5"/>
        <path d="M800 220 Q830 160 870 200 Q900 160 930 200 Q970 160 1000 220" fill="none" stroke="#c9a84c" stroke-width="2" opacity=".7"/>
        <path d="M790 240 Q820 300 870 270 Q900 310 930 270 Q980 300 1010 240" fill="none" stroke="#c9a84c" stroke-width="2" opacity=".7"/>
        <line x1="900" y1="100" x2="900" y2="80" stroke="#f59e0b" stroke-width="3"/>
        <circle cx="900" cy="70" r="14" fill="#f59e0b" opacity=".6"/>
        <!-- Lightbulb rays -->
        <line x1="900" y1="56" x2="900" y2="40" stroke="#f59e0b" stroke-width="2" opacity=".5"/>
        <line x1="912" y1="58" x2="922" y2="44" stroke="#f59e0b" stroke-width="2" opacity=".5"/>
        <line x1="888" y1="58" x2="878" y2="44" stroke="#f59e0b" stroke-width="2" opacity=".5"/>
        <line x1="920" y1="65" x2="936" y2="56" stroke="#f59e0b" stroke-width="2" opacity=".4"/>
        <line x1="880" y1="65" x2="864" y2="56" stroke="#f59e0b" stroke-width="2" opacity=".4"/>
        <!-- Books stack left -->
        <rect x="150" y="300" width="160" height="22" rx="4" fill="#c9a84c" opacity=".5"/>
        <rect x="155" y="278" width="150" height="22" rx="4" fill="#fff" opacity=".2"/>
        <rect x="160" y="256" width="140" height="22" rx="4" fill="#c9a84c" opacity=".4"/>
        <rect x="165" y="234" width="130" height="22" rx="4" fill="#fff" opacity=".15"/>
        <rect x="170" y="212" width="120" height="22" rx="4" fill="#c9a84c" opacity=".35"/>
        <!-- Connecting dots -->
        <circle cx="400" cy="150" r="5" fill="#c9a84c" opacity=".4"/>
        <circle cx="500" cy="200" r="4" fill="#c9a84c" opacity=".3"/>
        <circle cx="600" cy="160" r="5" fill="#c9a84c" opacity=".4"/>
        <line x1="400" y1="150" x2="500" y2="200" stroke="#c9a84c" stroke-width="1" opacity=".3"/>
        <line x1="500" y1="200" x2="600" y2="160" stroke="#c9a84c" stroke-width="1" opacity=".3"/>
      </svg>
      <div class="carousel-content">
        <div class="carousel-quote">"The <em>function of education</em> is to teach one to think intensively and to think critically."</div>
        <div class="carousel-author">&#8212; Martin Luther King Jr. &middot; Our Guiding Philosophy</div>
        <div style="margin-top:22px;display:flex;justify-content:center;gap:12px;flex-wrap:wrap;">
          <a href="#" onclick="showPage('curriculum');return false;" style="background:#c9a84c;color:#fff;padding:.65rem 1.8rem;border-radius:30px;text-decoration:none;font-weight:700;font-size:.9rem;">Our Curriculum</a>
          <a href="#" onclick="showPage('admissions');return false;" style="border:2px solid rgba(255,255,255,.5);color:#fff;padding:.6rem 1.6rem;border-radius:30px;text-decoration:none;font-weight:600;font-size:.9rem;">Apply Now</a>
        </div>
      </div>
    </div>

    <!-- SLIDE 3: Benjamin Franklin — Involve me and I learn -->
    <div class="carousel-slide" style="background:linear-gradient(160deg,#1a3a0f 0%,#2d5a1a 60%,#5a3a0f 100%);">
      <svg style="position:absolute;inset:0;width:100%;height:100%;opacity:.13" viewBox="0 0 1200 520" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice">
        <!-- Three figures: tell / teach / involve -->
        <!-- Figure 1: Teacher telling -->
        <circle cx="250" cy="180" r="30" fill="#c9a84c" opacity=".5"/>
        <line x1="250" y1="210" x2="250" y2="340" stroke="#c9a84c" stroke-width="6" stroke-linecap="round" opacity=".5"/>
        <line x1="250" y1="250" x2="200" y2="300" stroke="#c9a84c" stroke-width="5" stroke-linecap="round" opacity=".5"/>
        <line x1="250" y1="250" x2="300" y2="300" stroke="#c9a84c" stroke-width="5" stroke-linecap="round" opacity=".5"/>
        <line x1="250" y1="340" x2="220" y2="420" stroke="#c9a84c" stroke-width="5" stroke-linecap="round" opacity=".5"/>
        <line x1="250" y1="340" x2="280" y2="420" stroke="#c9a84c" stroke-width="5" stroke-linecap="round" opacity=".5"/>
        <!-- Speech bubble -->
        <rect x="290" y="140" width="80" height="45" rx="10" fill="#fff" opacity=".15"/>
        <line x1="295" y1="185" x2="280" y2="200" stroke="#fff" stroke-width="1" opacity=".15"/>
        <!-- Figure 2: Teacher teaching at board -->
        <circle cx="600" cy="160" r="30" fill="#f59e0b" opacity=".5"/>
        <line x1="600" y1="190" x2="600" y2="320" stroke="#f59e0b" stroke-width="6" stroke-linecap="round" opacity=".5"/>
        <line x1="600" y1="230" x2="550" y2="280" stroke="#f59e0b" stroke-width="5" stroke-linecap="round" opacity=".5"/>
        <line x1="600" y1="230" x2="650" y2="210" stroke="#f59e0b" stroke-width="5" stroke-linecap="round" opacity=".5"/>
        <!-- Blackboard -->
        <rect x="660" y="130" width="120" height="90" rx="6" fill="#1a3a6b" stroke="#c9a84c" stroke-width="2" opacity=".6"/>
        <line x1="675" y1="155" x2="765" y2="155" stroke="#fff" stroke-width="2" opacity=".4"/>
        <line x1="675" y1="170" x2="750" y2="170" stroke="#fff" stroke-width="2" opacity=".3"/>
        <line x1="675" y1="185" x2="740" y2="185" stroke="#c9a84c" stroke-width="2" opacity=".5"/>
        <!-- Figure 3: Students involved in activity -->
        <circle cx="950" cy="170" r="28" fill="#c9a84c" opacity=".5"/>
        <circle cx="1010" cy="185" r="28" fill="#fff" opacity=".2"/>
        <circle cx="1070" cy="170" r="28" fill="#c9a84c" opacity=".4"/>
        <line x1="950" y1="198" x2="950" y2="320" stroke="#c9a84c" stroke-width="6" stroke-linecap="round" opacity=".5"/>
        <line x1="1010" y1="213" x2="1010" y2="330" stroke="#fff" stroke-width="6" stroke-linecap="round" opacity=".2"/>
        <line x1="1070" y1="198" x2="1070" y2="320" stroke="#c9a84c" stroke-width="6" stroke-linecap="round" opacity=".4"/>
        <!-- Connecting hands -->
        <line x1="978" y1="260" x2="1040" y2="260" stroke="#f59e0b" stroke-width="4" stroke-linecap="round" opacity=".5"/>
        <circle cx="978" cy="260" r="6" fill="#f59e0b" opacity=".5"/>
        <circle cx="1040" cy="260" r="6" fill="#f59e0b" opacity=".5"/>
        <!-- Arrow progression -->
        <line x1="360" y1="280" x2="480" y2="280" stroke="#c9a84c" stroke-width="3" opacity=".4" stroke-dasharray="8,6"/>
        <polygon points="480,273 495,280 480,287" fill="#c9a84c" opacity=".4"/>
        <line x1="760" y1="280" x2="880" y2="280" stroke="#c9a84c" stroke-width="3" opacity=".4" stroke-dasharray="8,6"/>
        <polygon points="880,273 895,280 880,287" fill="#c9a84c" opacity=".4"/>
      </svg>
      <div class="carousel-content">
        <div class="carousel-quote">"Tell me and I forget. Teach me and I remember. <em>Involve me and I learn.</em>"</div>
        <div class="carousel-author">&#8212; Benjamin Franklin &middot; Active Learning at Golden Stars</div>
        <div style="margin-top:22px;display:flex;justify-content:center;gap:12px;flex-wrap:wrap;">
          <a href="#" onclick="showPage('curriculum');return false;" style="background:#c9a84c;color:#fff;padding:.65rem 1.8rem;border-radius:30px;text-decoration:none;font-weight:700;font-size:.9rem;">Our Approach</a>
          <a href="#" onclick="showPage('tour');return false;" style="border:2px solid rgba(255,255,255,.5);color:#fff;padding:.6rem 1.6rem;border-radius:30px;text-decoration:none;font-weight:600;font-size:.9rem;">Take a Tour</a>
        </div>
      </div>
    </div>

    <!-- SLIDE 4: Margaret Mead — How to think, not what to think -->
    <div class="carousel-slide" style="background:linear-gradient(160deg,#3a0f2d 0%,#5a1a3a 60%,#1a0f4a 100%);">
      <svg style="position:absolute;inset:0;width:100%;height:100%;opacity:.13" viewBox="0 0 1200 520" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice">
        <!-- Child figure thinking independently -->
        <circle cx="600" cy="160" r="45" fill="#c9a84c" opacity=".4"/>
        <line x1="600" y1="205" x2="600" y2="370" stroke="#c9a84c" stroke-width="8" stroke-linecap="round" opacity=".4"/>
        <line x1="600" y1="270" x2="520" y2="340" stroke="#c9a84c" stroke-width="7" stroke-linecap="round" opacity=".4"/>
        <line x1="600" y1="270" x2="680" y2="340" stroke="#c9a84c" stroke-width="7" stroke-linecap="round" opacity=".4"/>
        <line x1="600" y1="370" x2="560" y2="460" stroke="#c9a84c" stroke-width="7" stroke-linecap="round" opacity=".4"/>
        <line x1="600" y1="370" x2="640" y2="460" stroke="#c9a84c" stroke-width="7" stroke-linecap="round" opacity=".4"/>
        <!-- Thought bubble with multiple question marks and ideas -->
        <circle cx="700" cy="100" r="40" fill="none" stroke="#c9a84c" stroke-width="2" opacity=".5"/>
        <circle cx="760" cy="80" r="30" fill="none" stroke="#c9a84c" stroke-width="2" opacity=".4"/>
        <circle cx="820" cy="70" r="20" fill="none" stroke="#c9a84c" stroke-width="1.5" opacity=".3"/>
        <text x="700" y="108" text-anchor="middle" font-size="32" fill="#c9a84c" opacity=".5">?</text>
        <text x="760" y="86" text-anchor="middle" font-size="24" fill="#f59e0b" opacity=".5">!</text>
        <!-- Diverging paths / arrows showing multiple ways of thinking -->
        <line x1="350" y1="260" x2="250" y2="160" stroke="#c9a84c" stroke-width="2" opacity=".3" stroke-dasharray="10,6"/>
        <line x1="350" y1="260" x2="200" y2="280" stroke="#c9a84c" stroke-width="2" opacity=".3" stroke-dasharray="10,6"/>
        <line x1="350" y1="260" x2="240" y2="380" stroke="#c9a84c" stroke-width="2" opacity=".3" stroke-dasharray="10,6"/>
        <circle cx="350" cy="260" r="8" fill="#c9a84c" opacity=".4"/>
        <!-- Right side: multiple paths -->
        <line x1="850" y1="260" x2="950" y2="160" stroke="#c9a84c" stroke-width="2" opacity=".3" stroke-dasharray="10,6"/>
        <line x1="850" y1="260" x2="1000" y2="280" stroke="#c9a84c" stroke-width="2" opacity=".3" stroke-dasharray="10,6"/>
        <line x1="850" y1="260" x2="960" y2="380" stroke="#c9a84c" stroke-width="2" opacity=".3" stroke-dasharray="10,6"/>
        <circle cx="850" cy="260" r="8" fill="#c9a84c" opacity=".4"/>
        <!-- Horizon line -->
        <line x1="0" y1="430" x2="1200" y2="430" stroke="#c9a84c" stroke-width="1" opacity=".2"/>
      </svg>
      <div class="carousel-content">
        <div class="carousel-quote">"Children must be taught <em>how to think</em>, not what to think."</div>
        <div class="carousel-author">&#8212; Margaret Mead &middot; Critical Thinking at the Core</div>
        <div style="margin-top:22px;display:flex;justify-content:center;gap:12px;flex-wrap:wrap;">
          <a href="#" onclick="showPage('core-values');return false;" style="background:#c9a84c;color:#fff;padding:.65rem 1.8rem;border-radius:30px;text-decoration:none;font-weight:700;font-size:.9rem;">Our Values</a>
          <a href="#" onclick="showPage('admissions');return false;" style="border:2px solid rgba(255,255,255,.5);color:#fff;padding:.6rem 1.6rem;border-radius:30px;text-decoration:none;font-weight:600;font-size:.9rem;">Apply Now</a>
        </div>
      </div>
    </div>

    <!-- SLIDE 5: God is Able — Golden Stars Academy Motto -->
    <div class="carousel-slide" style="background:linear-gradient(160deg,#1a3a0f 0%,#c9840a 40%,#1a2d6b 100%);">
      <svg style="position:absolute;inset:0;width:100%;height:100%;opacity:.15" viewBox="0 0 1200 520" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice">
        <!-- Large golden star centre -->
        <polygon points="600,80 625,155 705,155 643,200 667,275 600,230 533,275 557,200 495,155 575,155" fill="#c9a84c" opacity=".6"/>
        <!-- Radiating light beams from star -->
        <line x1="600" y1="60" x2="600" y2="10" stroke="#f59e0b" stroke-width="4" opacity=".4"/>
        <line x1="640" y1="70" x2="670" y2="30" stroke="#f59e0b" stroke-width="3" opacity=".3"/>
        <line x1="560" y1="70" x2="530" y2="30" stroke="#f59e0b" stroke-width="3" opacity=".3"/>
        <line x1="670" y1="100" x2="720" y2="70" stroke="#f59e0b" stroke-width="2" opacity=".25"/>
        <line x1="530" y1="100" x2="480" y2="70" stroke="#f59e0b" stroke-width="2" opacity=".25"/>
        <!-- Shield / crest below star -->
        <path d="M480 310 L480 420 Q480 460 600 490 Q720 460 720 420 L720 310 Z" fill="none" stroke="#c9a84c" stroke-width="3" opacity=".5"/>
        <path d="M500 320 L500 415 Q500 448 600 472 Q700 448 700 415 L700 320 Z" fill="#c9a84c" opacity=".08"/>
        <!-- Cross inside shield -->
        <line x1="600" y1="335" x2="600" y2="460" stroke="#c9a84c" stroke-width="3" opacity=".4"/>
        <line x1="535" y1="385" x2="665" y2="385" stroke="#c9a84c" stroke-width="3" opacity=".4"/>
        <!-- Smaller stars around main star -->
        <polygon points="200,120 208,145 235,145 213,160 221,185 200,170 179,185 187,160 165,145 192,145" fill="#c9a84c" opacity=".35"/>
        <polygon points="1000,100 1007,122 1030,122 1011,135 1018,158 1000,145 982,158 989,135 970,122 993,122" fill="#c9a84c" opacity=".3"/>
        <polygon points="150,350 155,368 174,368 159,378 164,396 150,386 136,396 141,378 126,368 145,368" fill="#c9a84c" opacity=".25"/>
        <polygon points="1050,360 1055,378 1074,378 1059,388 1064,406 1050,396 1036,406 1041,388 1026,378 1045,378" fill="#c9a84c" opacity=".25"/>
        <!-- School building silhouette at bottom -->
        <rect x="300" y="430" width="600" height="80" fill="#1a2d6b" opacity=".3"/>
        <rect x="400" y="390" width="400" height="40" fill="#1a2d6b" opacity=".25"/>
        <rect x="520" y="360" width="160" height="30" fill="#1a2d6b" opacity=".2"/>
        <!-- Flag on top -->
        <line x1="600" y1="300" x2="600" y2="360" stroke="#c9a84c" stroke-width="2" opacity=".4"/>
        <polygon points="600,300 640,318 600,336" fill="#c9a84c" opacity=".4"/>
      </svg>
      <div class="carousel-content">
        <div class="carousel-quote">"<em>God is Able</em> &#8212; our faith anchors our pursuit of excellence, character, and service."</div>
        <div class="carousel-author">&#8212; The Golden Stars Academy Motto &middot; Est. 2011, GRA Gbessa, Abuja</div>
        <div style="margin-top:22px;display:flex;justify-content:center;gap:12px;flex-wrap:wrap;">
          <a href="#" onclick="showPage('admissions');return false;" style="background:#c9a84c;color:#fff;padding:.65rem 1.8rem;border-radius:30px;text-decoration:none;font-weight:700;font-size:.9rem;">Join Our Family</a>
          <a href="#" onclick="showPage('contact');return false;" style="border:2px solid rgba(255,255,255,.5);color:#fff;padding:.6rem 1.6rem;border-radius:30px;text-decoration:none;font-weight:600;font-size:.9rem;">Contact Us</a>
        </div>
      </div>
    </div>

    <div class="carousel-dots" id="carouselDots"></div>
  </div>'''

if OLD_CAROUSEL in html:
    html = html.replace(OLD_CAROUSEL, NEW_CAROUSEL)
    print("Step 2: Carousel replaced with illustrated version")
else:
    # Try flexible match
    pattern = re.compile(r'<div class="carousel-wrap">.*?</div>\s*</div>', re.DOTALL)
    if pattern.search(html):
        html = pattern.sub(NEW_CAROUSEL.strip(), html, count=1)
        print("Step 2: Carousel replaced via pattern match")
    else:
        print("WARNING: Could not find original carousel - check manually")

# ── STEP 3: Fix admin sidebar — add portals for ICT role ──────────────────
BASE = Path("templates/admin/base.html")
base = BASE.read_text(encoding="utf-8")

OLD_SIDEBAR = """    {% if current_user.role == 'superadmin' %}
    <div class="sb-sec">Portals</div>
    <a href="/admin/staff"   class="sb-a {% if '/admin/staff'   in request.url.path %}on{% endif %}"><i class="ti ti-users"></i> Staff Accounts</a>
    <a href="/admin/parents" class="sb-a {% if '/admin/parents' in request.url.path %}on{% endif %}"><i class="ti ti-heart"></i> Parent Accounts</a>
    {% endif %}"""

NEW_SIDEBAR = """    {% if current_user.role in ['superadmin','ict'] %}
    <div class="sb-sec">Portals</div>
    <a href="/admin/staff"   class="sb-a {% if '/admin/staff'   in request.url.path %}on{% endif %}"><i class="ti ti-users"></i> Staff Accounts</a>
    <a href="/admin/parents" class="sb-a {% if '/admin/parents' in request.url.path %}on{% endif %}"><i class="ti ti-heart"></i> Parent Accounts</a>
    {% endif %}"""

if OLD_SIDEBAR in base:
    base = base.replace(OLD_SIDEBAR, NEW_SIDEBAR)
    BASE.write_text(base, encoding="utf-8")
    print("Step 3: Admin sidebar updated — ICT can now see Portals")
elif NEW_SIDEBAR in base:
    print("Step 3: Sidebar already updated for ICT role")
else:
    print("Step 3: WARNING — sidebar pattern not found, check admin/base.html manually")

# ── STEP 4: Also update carousel height CSS ───────────────────────────────
html = html.replace(
    ".carousel-wrap{position:relative;overflow:hidden;height:480px;",
    ".carousel-wrap{position:relative;overflow:hidden;height:520px;"
)

INDEX.write_text(html, encoding="utf-8")
print("\nAll done! Now run:")
print("  git add .")
print('  git commit -m "illustrated carousel + sidebar fix"')
print("  git push")