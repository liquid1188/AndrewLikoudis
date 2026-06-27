#!/usr/bin/env python3
# Assembles interior pages for the v2 site with a shared shell.
import os
OUT = os.path.dirname(os.path.abspath(__file__))
IMG = "https://andrewlikoudis.com"

def head(title, desc):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{IMG}/og-banner.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="{IMG}/favicon.png">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<script>document.documentElement.classList.add("js")</script>
<link rel="stylesheet" href="styles.css">
</head>
<body>'''

def nav(active):
    def a(href,label):
        cur=' aria-current="page"' if active==href else ''
        return f'<li><a href="{href}"{cur}>{label}</a></li>'
    def m(href,label,cls=''):
        c=f' class="{cls}"' if cls else ''
        return f'<a href="{href}"{c}>{label}</a>'
    return f'''
<nav id="nav">
  <div class="nav-wrap">
    <a href="index.html" class="nav-logo"><span class="mono">AL</span> Andrew Likoudis</a>
    <ul class="nav-links">
      {a("about.html","About")}
      {a("faith-in-crisis.html","Faith in Crisis")}
      {a("writing.html","Writing")}
      {a("speaking.html","Speaking")}
      {a("gallery.html","Gallery")}
    </ul>
    <a href="work-with-me.html" class="nav-cta">Work With Me</a>
    <button class="hamburger" id="burger" aria-label="Menu"><span></span><span></span><span></span></button>
  </div>
</nav>
<div class="mobile-menu" id="mobileMenu">
  {m("about.html","About")}{m("faith-in-crisis.html","Faith in Crisis")}{m("writing.html","Writing")}{m("speaking.html","Speaking")}{m("gallery.html","Gallery")}{m("work-with-me.html","Work With Me →","cta")}
</div>'''

FOOTER = f'''
<footer>
  <div class="ornament"><span>✦</span></div>
  <p class="footer-quote">“In the evening of life, we will be judged on love alone.” — St. John of the Cross</p>
  <div class="footer-links">
    <a href="about.html">About</a><a href="faith-in-crisis.html">Faith in Crisis</a>
    <a href="writing.html">Writing</a><a href="speaking.html">Speaking</a>
    <a href="work-with-me.html">Work With Me</a><a href="gallery.html">Gallery</a>
  </div>
  <div class="footer-social">
    <a href="https://traditionandrenewal.substack.com" target="_blank" rel="noopener">Substack</a>
    <a href="https://linkedin.com/in/andrewlikoudis" target="_blank" rel="noopener">LinkedIn</a>
    <a href="https://instagram.com/likoudislegacy" target="_blank" rel="noopener">Instagram</a>
    <a href="https://x.com/A_lickity_split" target="_blank" rel="noopener">X</a>
  </div>
  <p class="footer-copy">
    Affiliated with the <a href="https://likoudislegacy.com" target="_blank" rel="noopener">Likoudis Legacy Foundation</a>.<br>
    Entrusted to St. Maximilian Kolbe, patron of journalists and media communications.<br>
    © 2026 Andrew Likoudis. All rights reserved. · Designed &amp; built by Andrew Likoudis.
  </p>
</footer>
<script>
const nav=document.getElementById('nav');
addEventListener('scroll',()=>nav.classList.toggle('scrolled',scrollY>20));
const burger=document.getElementById('burger'),mm=document.getElementById('mobileMenu');
burger.addEventListener('click',()=>{{burger.classList.toggle('open');mm.classList.toggle('open');}});
mm.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{{burger.classList.remove('open');mm.classList.remove('open');}}));
const io=new IntersectionObserver((es)=>es.forEach(e=>{{if(e.isIntersecting){{e.target.classList.add('in');io.unobserve(e.target);}}}}),{{threshold:.1}});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
</script>
</body></html>'''

def page(fname, title, desc, body):
    html = head(title, desc) + nav(fname) + body + FOOTER
    with open(os.path.join(OUT, fname), 'w') as f:
        f.write(html)
    print("wrote", fname, len(html), "bytes")

# ---------------- ABOUT ----------------
about_body = f'''
<section class="page-hero">
  <span class="eyebrow">Strategy · Editorial · Research · Communications</span>
  <h1>Andrew Robert Likoudis</h1>
  <span class="greek" style="display:block;margin-top:.5rem">Ανδρέας Ροβέρτος Λυκούδης</span>
  <p>Catholic scholar, editor, and consultant working at the intersection of tradition and reform in the contemporary Church.</p>
</section>
<section>
  <div class="narrow prose reveal">
    <p><strong>Andrew Likoudis</strong> is a Catholic scholar, editor, and consultant whose interdisciplinary work spans ecclesiology, ecumenism, institutional strategy, and Catholic public life. He serves as Digital Editor of <em>Where Peter Is</em>. His research and writing address the intersection of tradition and reform in the contemporary Church.</p>
    <p>His major scholarly project is <em>Faith in Crisis: Critical Dialogues in Catholic Traditionalism, Church Authority, and Reform</em> — a 40-chapter volume he organized and edited, coordinating 30+ contributors across three continents. The work features chapters by <strong>Robert Cardinal Sarah</strong>, Mike Aquilina, Jimmy Akin, Timothy O'Malley, Rafael Luciani, and other leading theologians, with endorsements from Odilo Cardinal Scherer of São Paulo and Rodrigo Guerra, Secretary of the Pontifical Commission for Latin America. It carries an <strong>imprimatur from Archbishop William E. Lori</strong>.</p>
    <p>He has authored, edited, or compiled twelve volumes on Catholic ecclesiology and the papacy. His recent editorial work includes the fiftieth-anniversary edition of Yves Congar's <em>Challenge to the Church: The Case of Archbishop Lefebvre</em> (En Route Books, 2026), the first English edition of Congar's answer to the Lefèbvre crisis; and the third edition of James Likoudis's <em>Ending the Byzantine Greek Schism</em> (Emmaus Road / St. Paul Center, 2026), with a foreword by Scott Hahn.</p>
    <p>As founder and chairman of the Likoudis Legacy Foundation, he built a 501(c)(3) research institute from the ground up — establishing governance structures, recruiting a distinguished advisory council, launching a fellows program, founding <em>The Kydones Review</em>, a peer-reviewed journal of which he is editor-in-chief, and establishing the LLF Reading Circle. With the Orientale Lumen Foundation, he is co-founding the Orientale Lumen Institute and co-sponsoring the <em>Orientale Lumen Conference</em> in Washington, DC, July 13–15, 2026.</p>
    <p>His institutional experience includes three years on the Archdiocesan Lay Pastoral Council of Baltimore — the young adult representative on a 14-member council — as well as support for a $5 million capital campaign at the Cathedral of Mary Our Queen, completion of McKinsey &amp; Co.'s Forward program, a Goldman Sachs 10,000 Small Businesses fellowship, and a Johns Hopkins University fellowship on a Bloomberg Philanthropies–backed workforce initiative.</p>
    <p>His communications work includes 50+ published articles in major Catholic outlets: the <em>National Catholic Register</em>, <em>Where Peter Is</em>, <em>Philosophy Now</em>, and EWTN News. He has conducted exclusive interviews with Archbishop Salvatore Cordileone and provided coverage of the USCCB General Assembly, and has begun assisting the Benedict XVI Institute in its work for liturgical renewal.</p>
    <p>Andrew is a dedicated parishioner at the Basilica of the National Shrine of the Assumption — America's First Cathedral. Beyond the academy, he draws on a decade of hospitality experience as an Airbnb Superhost. He enjoys kayaking, bachata, and chess.</p>
    <div class="btn-row" style="margin-top:1.6rem">
      <a href="{IMG}/Andrew-Likoudis-Resume.pdf" target="_blank" class="btn btn-outline">Download Résumé</a>
      <a href="{IMG}/Andrew-Likoudis-CV.pdf" target="_blank" class="btn btn-outline">Download Full CV</a>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Career</span><h2 class="section-title">Professional background</h2></div>
    <div class="narrow prose reveal">
      <div class="pull"><strong>Digital Editor</strong> · Where Peter Is · 2026–present<br><span style="font-size:.9rem;color:var(--text-light)">Oversees digital editorial operations for one of the leading independent voices in Catholic commentary.</span></div>
      <div class="pull"><strong>Founder &amp; Chairman</strong> · Likoudis Legacy Foundation (501c3) · 2023–present<br><span style="font-size:.9rem;color:var(--text-light)">Built a research institute from scratch — board, nine-person advisory council, academic journal, fellows program, and Reading Circle.</span></div>
      <div class="pull"><strong>Summer Intern, News &amp; Analysis</strong> · EWTN / National Catholic Register · 2025<br><span style="font-size:.9rem;color:var(--text-light)">Produced 17 published articles covering policy, governance, ethics, and emerging technology.</span></div>
      <div class="pull"><strong>Young Adult Representative</strong> · Archdiocesan Lay Pastoral Council, Archdiocese of Baltimore · 2022–2025</div>
      <div class="pull"><strong>Development Administrative Assistant</strong> · Cathedral of Mary Our Queen · 2023 · Supported a $5M capital campaign.</div>
      <div class="pull"><strong>Fellow</strong> · Goldman Sachs 10,000 Small Businesses (2022) · Johns Hopkins University / Bloomberg Philanthropies (2022)</div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">A legacy of faith</span><h2 class="section-title">Building on three generations</h2></div>
    <div class="offers reveal" style="grid-template-columns:1fr 1fr">
      <div class="offer">
        <h3>James Likoudis (1928–2024)</h3>
        <p class="outcome">Grandfather</p>
        <p style="font-size:.92rem;color:var(--text-light)">President Emeritus of Catholics United for the Faith. A convert from Greek Orthodoxy who became a leading voice for Catholic–Orthodox reunion, honored with a Doctorate of Divinity from Sacred Heart Major Seminary.</p>
      </div>
      <div class="offer">
        <h3>Paul Likoudis (1954–2016)</h3>
        <p class="outcome">Uncle &amp; Godfather</p>
        <p style="font-size:.92rem;color:var(--text-light)">Longtime editor of <em>The Wanderer</em>, America's oldest national Catholic newspaper. For decades he uncovered and documented clerical abuse — years before the Boston Globe exposé.</p>
      </div>
    </div>
  </div>
</section>
'''
page("about.html", "About — Andrew Likoudis", "Andrew Likoudis is a Catholic scholar, editor, and consultant. Founder of the Likoudis Legacy Foundation and editor of Faith in Crisis.", about_body)

# ---------------- WORK WITH ME ----------------
wwm_body = f'''
<section class="page-hero">
  <span class="eyebrow">Work With Me</span>
  <h1>Execute at a higher level</h1>
  <p>I bring institutional experience and editorial precision to Catholic publishers, nonprofits, and institutions. Whether you're publishing a multi-author volume, launching an apostolate, or developing a communications strategy, I can help.</p>
</section>
<section>
  <div class="wrap offers reveal">
    <div class="offer">
      <span class="eyebrow">01 — Publishing &amp; Editorial</span>
      <h3>Publish a volume the Church can endorse</h3>
      <p class="outcome">From manuscript to imprimatur, brought to completion with theological accuracy and cohesion.</p>
      <ul><li>Manuscript development &amp; theological review</li><li>Editorial review for magisterial alignment</li><li>Multi-author volume management</li><li>Publication strategy &amp; endorsements</li></ul>
      <p style="font-size:.78rem;color:var(--text-faint);margin-top:1rem"><strong>Credentials:</strong> Author or editor of 12 volumes; managed the imprimatur process for <em>Faith in Crisis</em> with Archbishop Lori.</p>
    </div>
    <div class="offer">
      <span class="eyebrow">02 — Nonprofit Strategy</span>
      <h3>Build an apostolate that lasts</h3>
      <p class="outcome">Governance, strategy, and fundraising from someone who built a 501(c)(3) from scratch.</p>
      <ul><li>Organizational development &amp; governance</li><li>Strategic planning &amp; mission alignment</li><li>Fundraising &amp; donor engagement</li><li>501(c)(3) formation guidance</li></ul>
      <p style="font-size:.78rem;color:var(--text-faint);margin-top:1rem"><strong>Credentials:</strong> Founder, Likoudis Legacy Foundation; Co-Founder, Orientale Lumen Institute; McKinsey Forward Alum; Goldman Sachs 10KSB &amp; Johns Hopkins Fellow.</p>
    </div>
    <div class="offer">
      <span class="eyebrow">03 — Research &amp; Communications</span>
      <h3>Say it clearly, and say it right</h3>
      <p class="outcome">Analysis and thought leadership grounded in primary sources and magisterial fidelity.</p>
      <ul><li>Long-form analysis on Church policy</li><li>Policy memos &amp; white papers</li><li>Media coverage &amp; editorial strategy</li><li>Ghostwriting &amp; thought leadership</li></ul>
      <p style="font-size:.78rem;color:var(--text-faint);margin-top:1rem"><strong>Credentials:</strong> 50+ published articles across NCR, EWTN, Philosophy Now; M.A., Franciscan University.</p>
    </div>
    <div class="offer">
      <span class="eyebrow">04 — Speaking</span>
      <h3>Bring the conversation to your audience</h3>
      <p class="outcome">Talks for parishes, conferences, and universities — original research, primary sources.</p>
      <ul><li>Traditionalism &amp; Church authority</li><li>The liturgical reform: Vatican II &amp; beyond</li><li>Ecumenism &amp; Catholic–Orthodox relations</li><li>Young adult engagement</li></ul>
      <p style="font-size:.78rem;color:var(--text-faint);margin-top:1rem"><strong>Credentials:</strong> 12 podcast appearances; keynotes at Florida Atlantic, Goldman Sachs 10KSB, Maryland Collegiate Honors Council.</p>
    </div>
  </div>
</section>

<section class="alt">
  <div class="narrow">
    <div class="section-head reveal"><span class="eyebrow">Start a conversation</span><h2 class="section-title">Tell me about your project</h2><p class="lead" style="margin-top:.8rem">I review all submissions personally and respond within 3–5 business days if there's a potential fit.</p></div>
    <div class="reveal" style="background:#fff;padding:2rem;border-radius:8px;box-shadow:var(--shadow)">
      <div class="form-row" style="display:grid;grid-template-columns:1fr 1fr;gap:1rem">
        <div><label class="fld">Your Name *</label><input id="f_name" type="text"></div>
        <div><label class="fld">Email *</label><input id="f_email" type="email"></div>
      </div>
      <div style="margin-top:1rem"><label class="fld">Organization / Institution</label><input id="f_org" type="text"></div>
      <div style="margin-top:1rem"><label class="fld">Type of Engagement *</label>
        <select id="f_type"><option>Editorial / Manuscript Development</option><option>Research Memo / White Paper</option><option>Media Coverage / News Analysis</option><option>Ghostwriting / Thought Leadership</option><option>Multi-Author Volume Management</option><option>Nonprofit Strategy &amp; Governance</option><option>Speaking / Keynote</option><option>Other / Not Sure Yet</option></select>
      </div>
      <div style="margin-top:1rem"><label class="fld">Project Description *</label><textarea id="f_desc"></textarea></div>
      <button class="btn btn-primary" style="margin-top:1.2rem;border:none" id="f_submit">Submit Project Inquiry →</button>
      <p style="font-size:.75rem;color:var(--text-faint);margin-top:1rem">Prefer to reach out directly? <a href="mailto:alikoudis@likoudislegacy.com" style="color:var(--burgundy)">alikoudis@likoudislegacy.com</a> · <a href="https://linkedin.com/in/andrewlikoudis" style="color:var(--burgundy)" target="_blank" rel="noopener">LinkedIn</a></p>
    </div>
  </div>
</section>
<style>
.fld{{display:block;font-family:'Lato',sans-serif;font-size:.65rem;letter-spacing:.1em;text-transform:uppercase;color:var(--text-light);margin-bottom:.35rem}}
.narrow input,.narrow textarea,.narrow select{{width:100%;padding:.7rem .9rem;font-family:'Libre Baskerville',serif;font-size:.88rem;border:1px solid rgba(0,0,0,.12);border-radius:4px;background:var(--ivory)}}
.narrow input:focus,.narrow textarea:focus,.narrow select:focus{{outline:none;border-color:var(--gold);box-shadow:0 0 0 2px rgba(201,169,98,.12)}}
.narrow textarea{{min-height:120px;resize:vertical}}
</style>
<script>
document.getElementById('f_submit').addEventListener('click',function(){{
  var n=f_name.value,e=f_email.value,o=f_org.value,t=f_type.value,d=f_desc.value;
  var body=encodeURIComponent("Name: "+n+"\\nEmail: "+e+"\\nOrganization: "+o+"\\nType: "+t+"\\n\\n"+d);
  window.location.href="mailto:alikoudis@likoudislegacy.com?subject="+encodeURIComponent("Project Inquiry — "+(n||"Website"))+"&body="+body;
}});
</script>
'''
page("work-with-me.html", "Work With Me — Andrew Likoudis", "Editorial, nonprofit strategy, research, and speaking services for Catholic publishers, nonprofits, and institutions.", wwm_body)

# ---------------- SPEAKING ----------------
talks = [
  ("Tradition, Authority &amp; the Crisis of Trust","Why do so many faithful Catholics distrust the Church they love? Andrew addresses the roots of the traditionalist movement, the theology of magisterial authority, and the path from suspicion to communion.",
   ["Faith, Authority, and Functionality: The Three Crises Behind the Traditionalist Turn","When Formation Fails: How a Century of Catechetical Deficit Produced a Generation of Dissent"]),
  ("The Liturgical Reform: What Happened and What It Means","A historically grounded, non-polemical account of the post-conciliar liturgical reform, its theological foundations, and the ongoing questions it raises for worship and formation.",
   ["One Rite, One Church: The Reform from Sacrosanctum Concilium to Traditionis Custodes","Formed in the Paschal Mystery: The Next Stage of Liturgical Renewal"]),
  ("Catholic–Orthodox Unity: The Unfinished Conversation","Drawing on three generations of ecumenical scholarship, Andrew explores the doctrinal differences, where common ground exists, and what the approaching millennium of the 1054 schism demands of both Churches.",
   ["The Road to 2054: Primacy, Synodality, and the Unfinished Work of Reunion","From Leo XIII to Leo XIV: Two Centuries of Catholic Ecumenical Commitment"]),
  ("The Unmoored Generation: Faith, Purpose &amp; the Crisis of Meaning","Why are young adults leaving the Church, and what does Catholic anthropology have to say about the broader crisis of meaning, identity, and belonging in a post-Christian society?",
   ["Ultrasupernaturalism, Spiritual Abuse, and the Closed Loop","The Sacramental Vision Against the Culture War"]),
]
talk_cards = ""
for i,(t,d,ex) in enumerate(talks,1):
    exli="".join(f"<li>{x}</li>" for x in ex)
    talk_cards += f'''<div class="offer reveal"><span class="eyebrow">Talk {i:02d}</span><h3>{t}</h3><p class="outcome">{d}</p><p style="font-size:.7rem;letter-spacing:.12em;text-transform:uppercase;color:var(--gold-dark);margin-bottom:.4rem">Example talks</p><ul>{exli}</ul></div>'''
speaking_body = f'''
<section class="page-hero">
  <span class="eyebrow">Speaking</span>
  <h1>Tradition &amp; reform, brought to your audience</h1>
  <p>Andrew speaks at parishes, conferences, and universities. Each talk draws on original research, primary sources, and the arguments of <em>Faith in Crisis</em>.</p>
  <div class="btn-row" style="justify-content:center;margin-top:1.6rem"><a href="work-with-me.html" class="btn btn-primary">Request a talk</a></div>
</section>
<section><div class="wrap offers reveal">{talk_cards}</div>
<p style="text-align:center;font-size:.8rem;color:var(--text-faint);max-width:680px;margin:2rem auto 0"><strong>Credentials:</strong> 12 podcast appearances; keynote speaker at Florida Atlantic University, Goldman Sachs 10KSB, and the Maryland Collegiate Honors Council; Archdiocesan Lay Pastoral Council, Archdiocese of Baltimore (2022–2025).</p>
</section>
'''
page("speaking.html", "Speaking — Andrew Likoudis", "Andrew Likoudis speaks at parishes, conferences, and universities on tradition, authority, liturgy, and Catholic–Orthodox unity.", speaking_body)

# ---------------- WRITING ----------------
def wlist(items):
    rows=""
    for pub,title,url,date in items:
        rows+=f'<a class="writing-item" href="{url}" target="_blank" rel="noopener"><span class="pub">{pub}</span><span class="t">{title}</span><span class="d">{date}</span></a>'
    return f'<div class="writing-list">{rows}</div>'
ncr=[("NCR","Ethicists Warn About the Dangers of Linking Assisted Suicide to Organ Donation","https://www.ncregister.com/news/organ-donation-assisted-suicide-ethics-medical-malpractice","01/2026"),
("NCR","A Vocation in Beauty: How Music Is Restoring the Sacred","https://www.ncregister.com/features/sacred-music-apostolates","10/2025"),
("NCR","'Neuralink' vs. Imago Dei: Catholic Anthropology and AI","https://www.ncregister.com/news/neuralink-vs-imago-dei","09/2025"),
("NCR","Patron Saint of Fashion? Pier Giorgio Frassati Dressed for God","https://www.ncregister.com/features/frassati-tailored-for-holiness","09/2025"),
("NCR","Smart Glasses Offer a Glimpse of the Future — But the Church Sees More Clearly","https://www.ncregister.com/news/smart-glasses-offer-a-glimpse-of-the-future-but-the-church-sees-more-clearly","08/2025")]
wpi=[("WPI","Leo XIV Issues First Encyclical, Calling AI a 'Change of Epoch' for the Human Person","https://wherepeteris.com/leo-xiv-issues-first-encyclical-calling-ai-a-change-of-epoch-for-the-human-person/","05/2026"),
("WPI","The Case for Standing to Receive Communion","https://wherepeteris.com/the-case-for-standing-to-receive-communion/","02/2026"),
("WPI","In the Footsteps of Francis: Ten Lines of Continuity in Leo XIV's Church","https://wherepeteris.com/in-the-footsteps-of-francis-ten-lines-of-continuity-in-leo-xivs-church/","02/2026"),
("WPI","After Traditionis Custodes: Archbishop Cordileone and Liturgical Renewal (Exclusive Interview)","https://wherepeteris.com/after-traditionis-custodes-archbishop-cordileone-and-liturgical-renewal/","11/2025"),
("WPI","Bugnini, the Protestant Myth, and the Making of the New Mass","https://wherepeteris.com/bugnini-the-protestant-myth-and-the-making-of-the-new-mass/","09/2025")]
other=[("PN","A Critique of Pure Atheism — Philosophy Now","https://philosophynow.org/issues/165/A_Critique_of_Pure_Atheism","12/2024"),
("CR","Pope Francis: A Reflection of Christ's Tenderness — Catholic Review","https://catholicreview.org/pope-francis-a-reflection-of-christs-tenderness-merch/","05/2025"),
("PA","Nature and Grace — Patheos (ongoing column)","https://www.patheos.com/blogs/natureandgrace/","—")]
writing_body = f'''
<section class="page-hero">
  <span class="eyebrow">Portfolio</span>
  <h1>Writing &amp; Publications</h1>
  <div class="stats reveal" style="margin-top:2rem">
    <div class="stat"><div class="n">50+</div><div class="l">Articles</div></div>
    <div class="stat"><div class="n">12</div><div class="l">Books</div></div>
    <div class="stat"><div class="n">12</div><div class="l">Podcasts</div></div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="logos reveal">
      <img src="{IMG}/logo-ncr.png" alt="NCR"><img src="{IMG}/logo-wpi.png" alt="WPI"><img src="{IMG}/logo-philosophynow.png" alt="Philosophy Now"><img src="{IMG}/logo-ewtn.png" alt="EWTN"><img src="{IMG}/logo-catholic-world-report.png" alt="Catholic World Report"><img src="{IMG}/logo-new-oxford-review.png" alt="New Oxford Review"><img src="{IMG}/logo-patheos.png" alt="Patheos"><img src="{IMG}/logo-catholic-review.png" alt="Catholic Review">
    </div>
  </div>
</section>
<section class="alt"><div class="wrap"><div class="section-head reveal"><span class="eyebrow">National Catholic Register</span></div><div class="reveal">{wlist(ncr)}</div><div style="text-align:center;margin-top:1.4rem"><a href="https://www.ncregister.com/author/andrew-likoudis" target="_blank" rel="noopener" class="btn btn-outline">View all at NCRegister.com</a></div></div></section>
<section><div class="wrap"><div class="section-head reveal"><span class="eyebrow">Where Peter Is</span></div><div class="reveal">{wlist(wpi)}</div><div style="text-align:center;margin-top:1.4rem"><a href="https://wherepeteris.com/author/andrew-likoudis/" target="_blank" rel="noopener" class="btn btn-outline">View all at WherePeterIs.com</a></div></div></section>
<section class="alt"><div class="wrap"><div class="section-head reveal"><span class="eyebrow">Other publications</span></div><div class="reveal">{wlist(other)}</div></div></section>
<section class="newsletter"><div class="wrap reveal"><span class="eyebrow" style="color:var(--gold)">Tradition &amp; Renewal</span><h2>Essays on faith, culture, and the Church</h2><p>Delivered to your inbox.</p><div class="form"><input type="email" placeholder="you@example.com" aria-label="Email"><a href="https://traditionandrenewal.substack.com/subscribe" target="_blank" rel="noopener" class="btn btn-gold">Subscribe</a></div></div></section>
'''
page("writing.html", "Writing — Andrew Likoudis", "50+ articles across the National Catholic Register, Where Peter Is, EWTN, and Philosophy Now.", writing_body)

# ---------------- FAITH IN CRISIS ----------------
toc_parts = {
 "Part One — Traditionalism":[
  "1. Functionality over Faith: A Modern Crisis — Andrew Mioni","2. Lessons from St. Hilary, the 'Athanasius of the West' — Mike Aquilina",
  "3. Rigorism in the Early Church: The First 'Fundamentalists' — James L. Papandrea","4. Fundamentalism &amp; Americanism — William Masur",
  "5. Reframing Orthodoxy: Beyond Conservative &amp; Liberal — Fr. Matthew Mary Bartow","6. Faithfulness, or Rigidity? — Pedro Gabriel",
  "7. What is Heresy? — Jimmy Akin","8. Diagnosing the Malaise of Modernism within Traditionalism — Pedro Gabriel",
  "9. Private Revelation &amp; Apparition Subculture — Andrew Likoudis","10. Clericalism &amp; Spiritual Abuse within Traditionalism — Andrew Likoudis",
  "11. Trad-adjacent: Radical Catholic Reactionaryism — Dave Armstrong"],
 "Part Two — Church Authority":[
  "12. Lessons from St. Peter's Papacy — Suan Sonna","13. Collegiality: A Traditional Doctrine — Richard G. DeClue, Jr.",
  "14. How Doctrinal Development Happens — Jimmy Akin","15. Finding Catholic Orthodoxy — Mike Lewis",
  "16. Thinking with the Mind of the Church — Henry Matthew Alt","17. Catholic Clickbait: Digital Media &amp; Outrage Culture — Andrew Likoudis",
  "18. The Ordinary Magisterium &amp; the Question of Dissent — Robert Fastiggi","19. The Antidote of Trust — Laura Vander Vos",
  "20. The Spirit of Obedience — Fr. Bernard Mulcahy, OP","21. Doctrinal Safety of the Ordinary Magisterium — Emmett O'Regan",
  "22. Heresy in the Pope's Non-definitive Acts? — Michael Lofton"],
 "Part Three — Reform":[
  "23. Vatican II &amp; Theological Paradigms — Michel Therrien","24. Conversion and Reform in the Light of Synodality — Rafael Luciani",
  "25. Veritatis Splendor Magistra et Amoris Laetitia Matris — Pedro Gabriel","26. The Death Penalty and Doctrinal Development — Robert Fastiggi",
  "27. Between Pessimism and Presumption — Adam Rasmussen","28. The Church is One: The Irrevocable Commitment to Christian Unity — Andrew J. Boyd",
  "29. Religious Liberty and its Foundation — R. Michael Dunnigan","30. Interreligious Dialogue &amp; the Incarnation — Fr. Francis J. Tiso",
  "31. Eastern Philosophy &amp; a Christology of Religions — Tyler McNabb","32. Catholic Teaching on the Jewish People — Gavin D'Costa",
  "33. Do Catholics &amp; Muslims Worship the Same God? — Robert Fastiggi","34. Inculturation &amp; the 'Pachamama' Ordeal — Luis Dizon",
  "35. Missiology &amp; Material Culture — Steven Schloeder","36. The Liturgical Reform in Retrospect — James Likoudis",
  "37. Challenges in Liturgy: Authority, Continuity &amp; Sectarian Concern — Andrew Likoudis","38. A Reader's Guide to Pope Francis' Vision of Liturgical Formation — Timothy O'Malley",
  "39. The Road Ahead: A Call for True Ecclesial Unity — Robert Cardinal Sarah","40. Taking the Virtuous Path: An Open Letter to Confused Young Catholics — Gregory Downs"],
}
toc_html=""
for part,chs in toc_parts.items():
    items="".join(f"<li>{c}</li>" for c in chs)
    toc_html+=f'<div class="reveal" style="margin-bottom:1.6rem"><h3 style="font-family:\'Cormorant Garamond\',serif;color:var(--burgundy);font-size:1.4rem;margin-bottom:.6rem">{part}</h3><ul style="list-style:none;columns:2;column-gap:2.5rem;font-size:.86rem;line-height:1.5">{items}</ul></div>'

fic_endorse = [
 ("endorser-cardinal-scherer.jpg","† Odilo Pedro Cardinal Scherer","Archbishop of São Paulo, Brazil","I welcome initiatives such as this volume, which seeks to reaffirm ecclesial communion and the authentic meaning of the liturgy. There is only one 'Mass of the Ages': the one regulated by the Church's living Magisterium."),
 ("endorser-rocco-buttiglione.jpg","Rocco Buttiglione","Leading interpreter of Pope St. John Paul II — From the Foreword","Faith in Crisis takes the objections of traditionalists against Pope Francis seriously and answers them from the true and great Tradition of the Church… a model of the hermeneutics of reform in continuity recommended by Benedict XVI."),
 ("endorser-david-bentley-hart.jpg","David Bentley Hart","University of Notre Dame","This is a splendid collection… a call to remember that the deepest and most essential resource of Catholic tradition is the law of love, given by him who laid down his life for his brothers and sisters."),
 ("endorser-rodrigo-guerra.jpg","Rodrigo Guerra","Secretary, Pontifical Commission for Latin America","Faith in Crisis allows us to appreciate, through different voices, how much we need to overcome pharisaical attitudes and rediscover the most elementary thing: Christianity is not a set of values, but a living Person encountered in the Church."),
 ("endorser-tim-staples.jpg","Tim Staples","Senior Apologist, Catholic Answers","Faith in Crisis is a godsend for our times. Andrew Likoudis has done the Church a great service by presenting the teaching of the living Magisterium."),
]
fic_cards=""
for img,name,role,quote in fic_endorse:
    fic_cards+=f'<div class="offer reveal"><img src="{IMG}/{img}" alt="{name}" style="width:60px;height:60px;border-radius:50%;object-fit:cover;border:2px solid var(--gold);margin-bottom:.8rem"><p class="outcome" style="margin-bottom:.6rem">“{quote}”</p><div class="who" style="font-family:\'Lato\',sans-serif;font-size:.82rem;color:var(--burgundy);font-weight:600">{name}</div><div style="font-family:\'Lato\',sans-serif;font-size:.72rem;color:var(--text-light)">{role}</div></div>'

fic_body = f'''
<section class="page-hero">
  <span class="eyebrow">The flagship</span>
  <h1>Faith in Crisis</h1>
  <p>Critical Dialogues in Catholic Traditionalism, Church Authority, and Reform</p>
</section>
<section>
  <div class="wrap book-feature">
    <img class="cover reveal" src="{IMG}/book-faith-in-crisis.jpg" alt="Faith in Crisis">
    <div class="reveal">
      <div class="book-meta"><span class="badge gold">✝ Imprimatur — Abp. Lori</span><span class="badge">40 Chapters</span><span class="badge">30+ Contributors</span></div>
      <p>Bringing together 30+ Catholic voices including <strong>Robert Cardinal Sarah</strong>, Mike Aquilina, Jimmy Akin, Timothy O'Malley, and Dave Armstrong — with a foreword by <strong>Rocco Buttiglione</strong> and an imprimatur from Archbishop William E. Lori. En Route Books &amp; Media, 2025.</p>
      <div class="retailers"><a href="https://amzn.to/3KY25Ng" target="_blank" rel="noopener">Order on Amazon →</a><a href="https://enroutebooksandmedia.com/faithincrisis/" target="_blank" rel="noopener">En Route Books →</a></div>
    </div>
  </div>
</section>
<section class="alt">
  <div class="narrow prose">
    <div class="section-head reveal"><span class="eyebrow">The story behind the book</span></div>
    <p class="reveal">A profound crisis of faith has gripped many in the Church today, leaving the faithful “like passengers in a storm-tossed boat — disoriented, unmoored, and struggling to trust in the Church's teaching, her mission, and the very foundations of a faith that once felt immovable.”</p>
    <p class="reveal">The project began in August 2023. I had no publisher, no budget, and no institutional backing. What I had was a table of contents taking shape in my head, a certainty that the questions deserved more rigorous answers than they were getting, and a willingness to cold-email professors, writers, theologians, and church officials across three continents to ask if they agreed. Within days, what I had imagined as a modest ten-chapter volume began to expand to forty.</p>
    <p class="reveal">The book serves simultaneously as a cultural analysis of the phenomenon of traditionalism and as a response to the questions that kept arising — above all about magisterial authority and reform. It is non-polemic in tone; it does not engage in point-by-point refutation, but takes the questions seriously enough to answer them on their own theological merits. As Fr. Carter Griffin wrote in his endorsement: “I don't agree with everything in this anthology. And I think that's the point.”</p>
    <div class="pull reveal">The imprimatur from Archbishop William E. Lori of Baltimore was the final confirmation that the volume had achieved what I set out to do: not a polemic, but a work the Church herself could endorse.</div>
  </div>
</section>
<section>
  <div class="wrap"><div class="section-head reveal"><span class="eyebrow">In their words</span><h2 class="section-title">Endorsements</h2></div>
  <div class="offers reveal" style="grid-template-columns:1fr 1fr">{fic_cards}</div></div>
</section>
<section class="alt">
  <div class="wrap"><div class="section-head reveal"><span class="eyebrow">Forty chapters, three continents</span><h2 class="section-title">Table of Contents</h2></div>{toc_html}
  <div style="text-align:center;margin-top:1.4rem"><a href="https://amzn.to/3KY25Ng" target="_blank" rel="noopener" class="btn btn-primary">Get your copy</a></div></div>
</section>
'''
page("faith-in-crisis.html", "Faith in Crisis — Andrew Likoudis", "A 40-chapter response to Catholic traditionalism, Church authority, and reform, featuring Robert Cardinal Sarah, with an imprimatur from Archbishop Lori.", fic_body)

# ---------------- GALLERY ----------------
gallery = [
 ("gallery-cardinal-pierre.jpg","Cardinal Christophe Pierre","Apostolic Nuncio to the United States"),
 ("gallery-cardinal-sarah.jpg","Cardinal Robert Sarah","Prefect Emeritus, Dicastery for Divine Worship"),
 ("gallery-imprimatur.jpg","Official Imprimatur","Archbishop William E. Lori · July 2025"),
 ("gallery-cardinal-roche.jpg","Cardinal Arthur Roche","Prefect, Dicastery for Divine Worship — Baltimore Basilica"),
 ("gallery-jack-figel.jpg","Jack Figel","Orientale Lumen Foundation · USCCB"),
 ("gallery-jason-shanks.jpg","Jason Shanks","President, National Eucharistic Congress"),
 ("gallery-mike-lewis-usccb.jpg","Reporting with Mike Lewis","USCCB Fall Assembly"),
 ("gallery-pierre-dinner.jpg","Mike Lewis &amp; Cardinal Pierre","Private dinner, Maryland"),
 ("gallery-press-club.jpg","National Press Club","EWTN"),
 ("gallery-ewtn.jpg","EWTN Office","Washington, DC"),
 ("gallery-michael-knowles.jpg","Michael Knowles","Catholic University of America"),
 ("gallery-ted-cruz.jpg","Senator Ted Cruz","Catholic University of America"),
 ("gallery-goldman-sachs.jpg","Goldman Sachs 10KSB Summit","Washington, DC"),
 ("gallery-larry-chapp.jpg","Theologian Larry Chapp","Baltimore Basilica"),
 ("gallery-barron-2022a.jpg","Bishop Robert Barron","2022"),
 ("gallery-barron-2023.jpg","Bishop Robert Barron","2023"),
 ("gallery-barron-2022b.jpg","Bishop Robert Barron","2024"),
 ("gallery-sister-imelda.jpg","Sister Imelda Joy",""),
 ("gallery-alice-hildebrand.jpg","Alice von Hildebrand","New Rochelle, NY, 2021"),
 ("gallery-james-likoudis.jpg","James Likoudis","With The Divine Primacy"),
 ("gallery-ruth-funeral.jpg","Tom Nash, Dr. Robert Fastiggi &amp; James Likoudis","Ruth Likoudis Funeral"),
 ("gallery-likoudis-jpii-teresa.jpg","James &amp; Ruth Likoudis","With Pope John Paul II &amp; Mother Teresa"),
 ("gallery-james-mother-angelica.jpg","James Likoudis","Mother Angelica Live · EWTN"),
 ("gallery-byzantine-schism-title.jpg","Ending the Byzantine Greek Schism","Edited by Andrew Likoudis · Foreword by Scott Hahn"),
 ("gallery-mike-ordination.jpg","Fr. Michael Likoudis","Ordination Day"),
 ("gallery-fic-flyer.jpg","Faith in Crisis","Book Launch Flyer"),
 ("gallery-isabel-brown.jpg","Isabel Brown","March for Life, 2023"),
 ("gallery-thomas-mckenna.jpg","Thomas McKenna","La Tavola, Baltimore"),
 ("gallery-basilica-christmas.jpg","Baltimore Basilica","Christmas Eve Mass"),
 ("gallery-usccb-coakley.jpg","Archbishop Paul Coakley","USCCB President"),
 ("gallery-guadalupe-radio.jpg","Guadalupe Radio","EWTN Affiliate Studio, Washington, DC"),
 ("gallery-white-house-interns.jpg","White House Interns","With Toby Capion &amp; Fr. John Paul Mary, EWTN"),
 ("gallery-white-house-podium.jpg","White House Press Briefing Room","Washington, DC"),
 ("gallery-bull-run-winery.jpg","DC Social Collective","Bull Run Winery, Virginia"),
 ("gallery-andrew-klavan.jpg","Andrew Klavan","Daily Wire — National Press Club, DC"),
 ("gallery-college-fix-gala.jpg","The College Fix Gala","Keynote: Bret Baier — National Press Club, DC"),
 ("gallery-chess.jpg","Chess","A favorite pastime"),
 ("gallery-reading.jpg","Reading with scotch",""),
 ("gallery-gracian-reading.jpg","The Art of Worldly Wisdom","Baltasar Gracián"),
]
tiles=""
for img,cap,sub in gallery:
    subhtml=f'<span>{sub}</span>' if sub else ''
    tiles+=f'<figure class="gallery-item" data-src="{IMG}/{img}" data-cap="{cap}" data-sub="{sub}"><img src="{IMG}/{img}" alt="{cap}" loading="lazy"><figcaption class="gallery-cap"><b>{cap}</b>{subhtml}</figcaption></figure>'
gallery_body = f'''
<section class="page-hero">
  <span class="eyebrow">Gallery</span>
  <h1>Encounters &amp; archives</h1>
  <p>Three generations of one family's work in the Church — and the people met along the way. Tap any photo to enlarge.</p>
</section>
<section>
  <div class="gallery-grid">{tiles}</div>
</section>
<div class="lightbox" id="lightbox">
  <button class="lb-close" id="lbClose" aria-label="Close">&times;</button>
  <img id="lbImg" src="" alt="">
  <div class="lb-cap" id="lbCap"></div>
</div>
<script>
(function(){{
  var lb=document.getElementById('lightbox'),img=document.getElementById('lbImg'),cap=document.getElementById('lbCap');
  document.querySelectorAll('.gallery-item').forEach(function(el){{
    el.addEventListener('click',function(){{
      img.src=el.dataset.src;img.alt=el.dataset.cap;
      cap.innerHTML='<b>'+el.dataset.cap+'</b>'+(el.dataset.sub?'<span>'+el.dataset.sub+'</span>':'');
      lb.classList.add('open');
    }});
  }});
  function close(){{lb.classList.remove('open');img.src='';}}
  lb.addEventListener('click',function(e){{if(e.target!==img)close();}});
  document.getElementById('lbClose').addEventListener('click',close);
  document.addEventListener('keydown',function(e){{if(e.key==='Escape')close();}});
}})();
</script>
'''
page("gallery.html", "Gallery — Andrew Likoudis", "Photographs from Andrew Likoudis's work in the Church — encounters with cardinals, bishops, and scholars, and the Likoudis family archive.", gallery_body)

print("done")
