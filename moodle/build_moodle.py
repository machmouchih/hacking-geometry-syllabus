#!/usr/bin/env python3
"""Build a Moodle-safe HTML fragment of the DME2100 syllabus.

Moodle strips <script>, <style> and external stylesheets from Page resources,
so every rule here is an inline style attribute. No classes, no web fonts, no
JavaScript, single column so it survives Moodle's narrow, themed content area
on a phone.

Outputs:
  moodle/syllabus-moodle.html   fragment to paste into Moodle's source view
  moodle/preview.html           same fragment wrapped for local checking
"""
import pathlib

PAPER, CARD, INK = "#f5f3ef", "#ffffff", "#17171a"
GRAPHITE, MIST, RULE, ACCENT = "#4a4a52", "#8a8a94", "#d9d5cd", "#d24317"

DISPLAY = ("'Libre Franklin','Franklin Gothic Medium','Franklin Gothic',"
           "Roboto,Arial,Helvetica,sans-serif")
BODY = "Roboto,'Helvetica Neue',Arial,Helvetica,sans-serif"

LINKS = [
    ("Zoom Meeting", "Weekly session, Wednesdays at 4 PM EST.",
     "https://the-bac.zoom.us/j/2720645727?pwd=NlVrZzJmZjFPMmhkNTRPelhsWWlsdz09"),
    ("Studio Board", "FigJam board for pin-ups and critique.",
     "https://www.figma.com/board/IlY0PBye1Berdwzn8ED0Al/"),
    ("Geometry Almanac", "Concept reference and modeling guidance.",
     "https://geometryfieldguide.netlify.app/geometry-almanac.html"),
    ("Discord", "Announcements, questions, and technical support.",
     "https://discord.gg/D6KeB9xGjM"),
    ("Course Drive", "Main shared drive for the course.",
     "https://barch-my.sharepoint.com/:f:/g/personal/hamze_machmouchi_the-bac_edu/IgDFWbRZ6wd2T6SRhPZOTM9xAYAh_UzcC4HoC3C-aN-0HQ8?e=GGNudQ"),
    ("Class Folder", "Readings, resources, and project files.",
     "https://barch-my.sharepoint.com/:f:/g/personal/hamze_machmouchi_the-bac_edu/IgBJjKCC-_9XT4wo-IOO2HoFARcDYezBlWIZ8LgYmyXIKx0?e=VCG76d"),
    ("Software Tutorials", "Guides for Rhino, Maya, and related software.",
     "https://barch-my.sharepoint.com/:f:/g/personal/hamze_machmouchi_the-bac_edu/IgDuB-pwNIulSqfrln1g8aAwAbcXGu9AGbWDylg3BFIKW6A?e=Nm2Mr2"),
]

ROUTINES = [
    ("Weekly pin-up", None,
     "Each Sunday night, place one image of work in progress in your own frame on the studio "
     "board, along with one sentence describing the current difficulty. Work is not expected to "
     "be resolved or presentable at this stage. Each frame accumulates over the semester, so "
     "that by December it holds a complete visual record of the project."),
    ("Response partner", None,
     "Each week students are assigned one classmate by name and will respond to that classmate's "
     "work by Tuesday night. Responses are left as comments anchored to a specific point on the "
     "image, not as general remarks. Assignments rotate weekly, so that over the semester each "
     "student engages with every project in the class."),
    ("Crit partner", None,
     "Students are paired for the full semester. Crit partners review one another's material "
     "before each formal review and serve as a first point of contact for technical difficulties "
     "outside class hours."),
    ("Prompt log", "optional",
     "Students are encouraged, though not required, to keep a record of their exchanges with AI "
     "tools while developing their scripts, including unsuccessful attempts and revisions. It "
     "may be included at either review."),
    ("WIP", None,
     "Beyond the Sunday pin-up, students are encouraged to post work in progress at any point in "
     "the week, including scripts that do not yet run and models that came out wrong. Parameters "
     "driven past their useful range and errors that produced unexpected results are a legitimate "
     "source of formal material in this course."),
]

PHASES = [
    ("Physical Experiments",
     ["Students will conduct physical experiments to explore form-finding and geometric "
      "principles. The class is divided into three groups for the opening workshop. Each student "
      "concludes this phase with a written statement of the geometric rule observed in their "
      "material, expressed in plain language."],
     [("Group A &middot; The Developable Surface",
       "Folding, creasing, and ribboning. Cardboard, scoring tools, cutting mats, metal rulers."),
      ("Group B &middot; The Tensile Surface",
       "Soap film studies. Piano wire, wire in various gauges, pliers, soap solution with dish "
       "soap and glycerine, dipping container."),
      ("Group C &middot; The Solid Volume",
       "Carving, casting, or modeling with clay. Plaster of Paris blocks, modeling clay, carving "
       "tools such as rasps, files, and sandpaper.")]),
    ("Concept and Taxonomy",
     ["Students will research the history, architectural significance, and underlying geometric "
      "principles of their assigned concept, and create its geometric taxonomy. The taxonomy sets "
      "out the properties of the concept alongside the precedents in which it appears, and is "
      "presented to the class. Each taxonomy concludes with a list of the parameters that vary "
      "within the concept and those that remain fixed."], None),
    ("Parametric Tool",
     ["Students will translate the rule identified in Phase 1 into a working script that generates "
      "their geometry from a small set of inputs. Those inputs are then exposed as adjustable "
      "parameters, so that the script produces a range of related forms rather than a single "
      "result. AI tools are used as a coding assistant throughout this phase.",
      "Work takes place in the Python editor built into Rhino 8, which requires no additional "
      "software. Prior programming experience is not required.",
      "<b>Requirement.</b> Students must be able to explain the operation of their own tool, in "
      "their own words, at both reviews. A brief written explanation of each function is "
      "submitted alongside the script."], None),
    ("3D Modeling and Evolution",
     ["Students will create accurate and detailed freeform 3D models in Rhino 8 and Maya, "
      "demonstrating an understanding of the taxonomy studied in the first half of the semester. "
      "Each student is then assigned an Exploration Type and applies it to their system as an "
      "additional operation within the existing tool."], None),
    ("Site and Pavilion",
     ["Each student selects their own site and documents it: photographs, a location plan, and a "
      "short description of its conditions, including orientation, access, topography, and "
      "surroundings. The geometric system developed in the previous phases is then resolved into "
      "a pavilion on that site, at a scale a person can occupy and move through."], None),
    ("Visualization",
     ["Students will document their process and present their final project in a clear and "
      "compelling way. Submissions include rendered images produced in D5, Twinmotion, Rhino "
      "Render, Nano Banana, or GPT Image 2, diagrams illustrating the geometric properties of the "
      "concept, and a discussion of the architectural implications of the resulting form. At "
      "least one image must show the pavilion in its site context."], None),
]

CONCEPTS = [
    ("Minimal Surfaces", "Frei Otto, Munich Olympic Stadium"),
    ("Developable Surfaces", "Frank Gehry, Disney Concert Hall"),
    ("Platonic Solids and Geodesic Spheres", "Buckminster Fuller, Biosphere at Expo 67"),
    ("Translational Surfaces and Vaults", "Eero Saarinen, TWA Flight Center"),
    ("Ruled and HP Surfaces", "F&eacute;lix Candela, Los Manantiales"),
    ("Freeform Curves and NURBS", "Zaha Hadid, Heydar Aliyev Center"),
    ("Freeform and Subdivision Surfaces", "Peter Cook, Kunsthaus Graz"),
    ("Pipe Surfaces and Knots", "Piano and Rogers, Centre Pompidou"),
    ("Space-Filling Polyhedra", "Jean Renaudie, Ivry-sur-Seine"),
    ("Constant Mean Curvature Surfaces", "Grimshaw, Eden Project"),
]

EXPLORATIONS = [
    "Apply striation and pattern", "Deconstruct into a skeleton",
    "Introduce layering and stratification", "Carve sub-volumes",
    "Aggregate as clustered parts", "Define the boundary condition",
    "Develop spliced or interlocked joints", "Incorporate pleating",
    "Differentiate the intensity", "Create a nested loop",
]

# (date, title, note, body, kind) kind: normal | studio | closed | review | checkpoint
SCHEDULE = [
    ("August 26", "First Day of Classes", "Session 1",
     "Introduction to the course. Students are assigned their individual semester-long concepts, "
     "their initial group tasks, and their crit partners. The session closes with a demonstration "
     "in which a parametric script is written from scratch, including its errors and revisions.",
     "normal"),
    ("September 2", "Physical Experiments Workshop", "Studio, on Discord",
     "Groups carry out their form-finding experiments during the scheduled class time. There is "
     "no Zoom meeting for this session. The instructor is available on Discord throughout class "
     "hours. Photographs of at least three experiments, together with a written statement of the "
     "geometric rule observed, are due Sunday September 6.", "studio"),
    ("September 9", "Concept and Taxonomy", "Session 2",
     "Review of the physical experiments, followed by student presentations of research on the "
     "history and geometric principles of their concepts. Each presentation concludes with the "
     "student's parameter list.", "normal"),
    ("September 16", "Digital Translation and Topology", "Session 3",
     "A workshop on translating physical forms into digital models, including a session on clean "
     "mesh topology. The second half of the session is the first scripting lab.", "normal"),
    ("September 23", "Surface Analysis and Rationalization", "Session 4",
     "A lecture on understanding surface quality through synclastic and anticlastic curvature, "
     "using the Curvature Graph tool in Rhino, followed by a discussion of rationalization for "
     "fabrication.", "normal"),
    ("September 30", "Parametric Tool Development", "Session 5",
     "Moving from a script that produces a single instance to one that produces a family of "
     "forms. The second half of the session is an open debugging clinic.", "normal"),
    ("October 7", "Studio Session and Desk Crits", "Session 6",
     "An in-class studio session to develop parametric design rules with instructor support, "
     "combined with individual desk crits. The final working session before the midterm review.",
     "normal"),
    ("October 14", "Midterm Presentations", "Session 7",
     "Students present their full process to date: concept, physical experiments, and the "
     "resulting digital 3D models. Each student documents their taxonomy and demonstrates their "
     "parametric tool in operation. Submitted: rule statement, taxonomy, 3D models, working tool "
     "with written explanation.", "review"),
    ("October 21", "Studio Session", "Studio, on Discord",
     "Independent work on parametric tools and digital models during the scheduled class time. "
     "There is no Zoom meeting for this session. The instructor is available on Discord "
     "throughout class hours for questions and support.", "studio"),
    ("October 28", "Advanced Operations", "Session 8",
     "Students are assigned their Exploration Type, and the lecture covers methods for adding a "
     "second operation to an existing script without compromising the first. Site selection is "
     "introduced, and each student chooses and documents a site for their pavilion, due the "
     "following Sunday.", "normal"),
    ("November 4", "Desk Crits", "Session 9",
     "Individual reviews focused on the spatial and architectural qualities of the evolved "
     "digital forms, and on how each pavilion sits on its chosen site. The withdrawal deadline "
     "for this course is Friday November 6.", "normal"),
    ("November 11", "BAC Closed", "Veterans Day",
     "No class and no submissions due.", "closed"),
    ("November 18", "Visualization Workshop", "Session 10",
     "An introduction to advanced rendering techniques in D5, Twinmotion, Rhino Render, Nano "
     "Banana, and GPT Image 2, including methods for scripting repetitive output tasks. This is "
     "the final Zoom session before the final review.", "normal"),
    ("November 25", "BAC Closed", "Thanksgiving break",
     "No class and no submissions due.", "closed"),
    ("November 29", "Draft Boards Due", "Sunday night",
     "Students place draft final boards in their frame on the studio board. Response partners "
     "comment by Tuesday night, December 1.", "checkpoint"),
    ("December 2", "Final Presentations", "Session 11",
     "Students present their fully evolved final designs, covering concept, physical experiments, "
     "the parametric tool, and the resulting pavilion shown in its site, with final "
     "visualizations. Submitted: complete portfolio, final tool with written explanation.",
     "review"),
]

GRADING = [("Assignments", "25%"), ("Attendance and Participation", "25%"),
           ("Mid Review", "25%"), ("Final Review", "25%"), ("Total", "100%")]

CITE = ("https://www.chicagomanualofstyle.org/qanda/data/faq/topics/"
        "Documentation/faq0422.html")

out = []
W = out.append


def wrap(s):
    return " ".join(s.split())


def h2(text, num):
    W(f'<h2 style="font-family:{DISPLAY};font-size:22px;font-weight:800;color:{INK};'
      f'margin:34px 0 4px 0;padding:0;line-height:1.2;">'
      f'<span style="color:{ACCENT};font-size:12px;letter-spacing:1.6px;display:block;'
      f'margin-bottom:6px;">{num}</span>{text}</h2>')
    W(f'<div style="height:2px;background:{INK};margin:0 0 16px 0;"></div>')


def para(text, color=GRAPHITE, size=15, mb=12):
    W(f'<p style="font-family:{BODY};font-size:{size}px;line-height:1.6;color:{color};'
      f'margin:0 0 {mb}px 0;">{wrap(text)}</p>')


def card(inner, bg=CARD, border=RULE, pad=16, mb=10, accent=False):
    left = f'border-left:4px solid {ACCENT};' if accent else ''
    W(f'<div style="background:{bg};border:1px solid {border};{left}'
      f'padding:{pad}px;margin:0 0 {mb}px 0;">{inner}</div>')


# ---------------------------------------------------------------- header
W(f'<div style="background:{INK};padding:22px;margin:0 0 18px 0;">'
  f'<p style="font-family:{DISPLAY};font-size:11px;letter-spacing:1.6px;color:{ACCENT};'
  f'margin:0 0 8px 0;font-weight:700;">DME2100 &middot; BOSTON ARCHITECTURAL COLLEGE</p>'
  f'<h1 style="font-family:{DISPLAY};font-size:30px;font-weight:800;color:#ffffff;'
  f'margin:0 0 10px 0;line-height:1.1;">Hacking Geometry</h1>'
  f'<p style="font-family:{BODY};font-size:15px;line-height:1.6;color:#d8d4cc;margin:0;">'
  f'A course on the relationship between architectural geometry and 3D modeling, in which '
  f'students investigate form-finding through physical experiment, digital modeling, and the '
  f'construction of their own parametric tools, ending in a pavilion designed for a site of '
  f'their choosing.</p></div>')

facts = [("Term", "Fall 2026<br>August 26 to December 2"),
         ("Meeting Time", "Wednesday, 4 PM EST<br>Online via Zoom &middot; 3 credits"),
         ("Instructor", 'Hamze Machmouchi<br><a href="mailto:hamze.machmouchi@the-bac.edu" '
                        f'style="color:{ACCENT};">hamze.machmouchi@the-bac.edu</a>'),
         ("Office Hours", "4 PM to 6 PM EST<br>Wednesdays")]
rows = "".join(
    f'<div style="border-bottom:1px solid {RULE};padding:10px 0;">'
    f'<p style="font-family:{DISPLAY};font-size:10px;letter-spacing:1.4px;color:{ACCENT};'
    f'margin:0 0 4px 0;font-weight:700;">{k.upper()}</p>'
    f'<p style="font-family:{BODY};font-size:14px;color:{GRAPHITE};margin:0;line-height:1.5;">'
    f'{v}</p></div>' for k, v in facts)
card(rows, bg=PAPER, pad=14, mb=18)

# ---------------------------------------------------------------- links
h2("Quick Links", "01")
for name, desc, url in LINKS:
    W(f'<a href="{url}" target="_blank" rel="noopener" '
      f'style="display:block;background:{CARD};border:1px solid {RULE};padding:12px 14px;'
      f'margin:0 0 6px 0;text-decoration:none;">'
      f'<span style="font-family:{DISPLAY};font-size:15px;font-weight:700;color:{ACCENT};'
      f'display:block;">{name}</span>'
      f'<span style="font-family:{BODY};font-size:13px;color:{MIST};display:block;'
      f'margin-top:2px;">{desc}</span></a>')

# ---------------------------------------------------------------- course info
h2("Course Information", "02")
para("This course explores the relationship between architectural geometry and 3D modeling. "
     "Through a combination of hands-on physical experiments, theoretical readings, and digital "
     "modeling techniques, students will develop a strong understanding of form-finding and the "
     "geometric principles behind complex architectural forms. We will investigate topics such as "
     "NURBS, SUBD, and mesh modeling, and learn how to create 3D models with an awareness of "
     "architectural fabrication processes. Students should have basic skills in Rhino and be "
     "prepared to learn new software.")
para("This semester the course adds a further step. Students will identify the geometric rule "
     "governing their assigned concept and then encode that rule as a working script, using AI "
     "tools as a coding assistant. The result is not a single model but a parametric system "
     "capable of generating a family of related forms, which is then resolved into a pavilion on "
     "a site each student selects. No prior programming experience is required.")
goals = "".join(
    f'<li style="font-family:{BODY};font-size:14px;line-height:1.55;color:{GRAPHITE};'
    f'margin-bottom:6px;">{g}</li>' for g in [
        "Develop a strong understanding of architectural geometry principles.",
        "Gain proficiency in 3D modeling techniques using Rhino 8 and Maya.",
        "Apply theoretical knowledge to create informed and innovative 3D models.",
        "Bridge the gap between physical experimentation and digital design.",
        "Encode geometric rules as functioning parametric tools.",
        "Critically analyze and appreciate the role of geometry in architectural design."])
card(f'<p style="font-family:{DISPLAY};font-size:11px;letter-spacing:1.4px;color:{ACCENT};'
     f'margin:0 0 10px 0;font-weight:700;">LEARNING GOALS</p>'
     f'<ol style="margin:0;padding-left:20px;">{goals}</ol>', bg=PAPER)

# ---------------------------------------------------------------- expectations
h2("Course Expectations", "03")
para("Students are expected to be actively engaged throughout the course. Because the course "
     "meets online and only once per week, the following routines are used to maintain continuity "
     "between sessions. Each is brief. Except where noted as optional, each contributes to the "
     "participation portion of the final grade.")
for i, (name, tag, text) in enumerate(ROUTINES, 1):
    suffix = (f' <span style="font-family:{BODY};font-size:13px;color:{MIST};'
              f'font-weight:400;">({tag})</span>') if tag else ''
    card(f'<p style="font-family:{DISPLAY};font-size:10px;letter-spacing:1.4px;color:{ACCENT};'
         f'margin:0 0 6px 0;font-weight:700;">ROUTINE 0{i}</p>'
         f'<p style="font-family:{DISPLAY};font-size:16px;font-weight:700;color:{INK};'
         f'margin:0 0 8px 0;">{name}{suffix}</p>'
         f'<p style="font-family:{BODY};font-size:14px;line-height:1.6;color:{GRAPHITE};'
         f'margin:0;">{wrap(text)}</p>')

W(f'<p style="font-family:{DISPLAY};font-size:11px;letter-spacing:1.4px;color:{ACCENT};'
  f'margin:18px 0 8px 0;font-weight:700;">WHERE WORK IS POSTED</p>')
para("Work is posted on the studio board. Conversation happens on Discord. A single FigJam board "
     "runs for the whole semester, and each student has a named frame on it which functions as "
     "their wall in a physical studio. Weekly pin-ups, draft boards, and the midterm and final "
     "presentations all take place on this board. Critique is written as a comment anchored to a "
     "specific point on the work. Students should be signed in with their BAC accounts so that "
     "comments are attributed.")
para("Discord is used for everything that is not the work itself: announcements and weekly "
     "partner assignments, technical help with software and scripts, work in progress posted "
     "during the week, and a voice channel open during office hours and the two studio sessions.")
para("A shared drive dedicated to this class holds readings, resources, and materials. Students "
     "are expected and encouraged to upload their progress work to the drive throughout the "
     "semester.")

# ---------------------------------------------------------------- project
h2("Final Project", "04")
para("The final project challenges students to synthesize their knowledge of architectural "
     "geometry and 3D modeling skills to design and model a complex architectural form. Students "
     "retain the same assigned concept from August through December and develop it across six "
     "phases.")
card(f'<p style="font-family:{DISPLAY};font-size:10px;letter-spacing:1.4px;color:{ACCENT};'
     f'margin:0 0 8px 0;font-weight:700;">THE DELIVERABLE</p>'
     f'<p style="font-family:{BODY};font-size:15px;line-height:1.6;color:#d8d4cc;margin:0;">'
     f'The end product is a <b style="color:#ffffff;">pavilion-scale architectural exploration '
     f'on a site of the student\'s choosing</b>. Not an abstract object and not a building. A '
     f'freestanding, occupiable structure that a person can walk into, developed out of the '
     f'assigned geometric concept and resolved against the conditions of a real site the student '
     f'selects and documents. Scale, orientation, entry, structure, and materiality are all '
     f'answered in relation to that site.</p>', bg=INK, border=INK, pad=18, mb=14)

for i, (title, paras, extra) in enumerate(PHASES, 1):
    inner = (f'<p style="font-family:{DISPLAY};font-size:17px;font-weight:700;color:{INK};'
             f'margin:0 0 10px 0;">'
             f'<span style="color:{ACCENT};font-size:24px;font-weight:800;'
             f'margin-right:10px;">{i}</span>{title}</p>')
    for t in paras:
        inner += (f'<p style="font-family:{BODY};font-size:14px;line-height:1.6;'
                  f'color:{GRAPHITE};margin:0 0 10px 0;">{wrap(t)}</p>')
    if extra:
        for label, text in extra:
            inner += (f'<p style="font-family:{BODY};font-size:13px;line-height:1.55;'
                      f'color:{GRAPHITE};margin:0 0 6px 0;padding-left:12px;'
                      f'border-left:2px solid {RULE};"><b style="color:{INK};">{label}.</b> '
                      f'{wrap(text)}</p>')
    card(inner, accent=(i == 3))

W(f'<p style="font-family:{DISPLAY};font-size:11px;letter-spacing:1.4px;color:{ACCENT};'
  f'margin:18px 0 8px 0;font-weight:700;">ASSIGNED CONCEPTS</p>')
items = "".join(
    f'<li style="font-family:{BODY};font-size:14px;line-height:1.55;color:{GRAPHITE};'
    f'margin-bottom:5px;"><b style="color:{INK};">{n}</b> &middot; {p}</li>'
    for n, p in CONCEPTS)
W(f'<ul style="margin:0 0 14px 0;padding-left:20px;">{items}</ul>')

W(f'<p style="font-family:{DISPLAY};font-size:11px;letter-spacing:1.4px;color:{ACCENT};'
  f'margin:18px 0 8px 0;font-weight:700;">EXPLORATION TYPES</p>')
items = "".join(
    f'<li style="font-family:{BODY};font-size:14px;line-height:1.55;color:{GRAPHITE};'
    f'margin-bottom:4px;">{e}</li>' for e in EXPLORATIONS)
W(f'<ul style="margin:0 0 14px 0;padding-left:20px;">{items}</ul>')

# ---------------------------------------------------------------- schedule
h2("Course Structure", "05")
para("This course meets every Wednesday at 4 PM EST via Zoom, from August 26 through December 2, "
     "2026. The semester consists of thirteen sessions. Eleven meet on Zoom. Two are studio "
     "sessions held on Discord, where the instructor is available throughout the scheduled class "
     "time. Two further class dates fall on BAC closures.")

for date, title, note, body, kind in SCHEDULE:
    if kind == "review":
        bg, bd, dc, tc, bc, nc = ACCENT, ACCENT, "#ffffff", "#ffffff", "#ffeae3", "#ffd6c9"
    elif kind == "checkpoint":
        bg, bd, dc, tc, bc, nc = INK, INK, "#ffffff", "#ffffff", "#d8d4cc", ACCENT
    elif kind == "closed":
        bg, bd, dc, tc, bc, nc = PAPER, RULE, MIST, MIST, MIST, MIST
    elif kind == "studio":
        bg, bd, dc, tc, bc, nc = PAPER, RULE, INK, INK, GRAPHITE, ACCENT
    else:
        bg, bd, dc, tc, bc, nc = CARD, RULE, INK, INK, GRAPHITE, MIST
    W(f'<div style="background:{bg};border:1px solid {bd};padding:14px;margin:0 0 6px 0;">'
      f'<p style="font-family:{DISPLAY};font-size:15px;font-weight:800;color:{dc};margin:0;">'
      f'{date}</p>'
      f'<p style="font-family:{DISPLAY};font-size:10px;letter-spacing:1.3px;color:{nc};'
      f'margin:2px 0 8px 0;font-weight:700;">{note.upper()}</p>'
      f'<p style="font-family:{DISPLAY};font-size:15px;font-weight:700;color:{tc};'
      f'margin:0 0 6px 0;">{title}</p>'
      f'<p style="font-family:{BODY};font-size:14px;line-height:1.6;color:{bc};margin:0;">'
      f'{wrap(body)}</p></div>')

# ---------------------------------------------------------------- AI
h2("Use of Artificial Intelligence", "06")
card(f'<p style="font-family:{DISPLAY};font-size:15px;font-weight:700;color:{INK};'
     f'margin:0 0 8px 0;text-decoration:underline;">Use only with acknowledgment</p>'
     f'<p style="font-family:{BODY};font-size:14px;line-height:1.6;color:{GRAPHITE};'
     f'margin:0 0 10px 0;">Students are permitted to use artificial intelligence on assignments '
     f'in this course, except when specified otherwise by the instructor, and must always be '
     f'documented and credited with accurate citations.</p>'
     f'<p style="font-family:{BODY};font-size:14px;line-height:1.6;color:{GRAPHITE};'
     f'margin:0 0 10px 0;">For guidance on how to cite AI in your work see: '
     f'<a href="{CITE}" target="_blank" rel="noopener" style="color:{ACCENT};'
     f'word-break:break-all;">{CITE}</a></p>'
     f'<p style="font-family:{BODY};font-size:14px;line-height:1.6;color:{GRAPHITE};'
     f'margin:0;padding-top:10px;border-top:1px solid {RULE};">Different courses at the BAC could '
     f'implement different AI policies. It is the student&rsquo;s responsibility to be aware of '
     f'and comply with expectations for each course.</p>')
W(f'<p style="font-family:{BODY};font-size:11px;line-height:1.5;color:{MIST};margin:0 0 12px 0;">'
  f'<i>Language for our AI policy options draws from the University of Delaware, Duke '
  f'University, and Harvard College.</i></p>')

# ---------------------------------------------------------------- policies
h2("Evaluation and Policies", "07")
rows = ""
for label, pct in GRADING:
    bold = "700" if label == "Total" else "400"
    bg = PAPER if label == "Total" else CARD
    rows += (f'<tr><td style="font-family:{BODY};font-size:14px;color:{GRAPHITE};padding:9px 12px;'
             f'border-bottom:1px solid {RULE};background:{bg};font-weight:{bold};">{label}</td>'
             f'<td style="font-family:{DISPLAY};font-size:14px;color:{INK};padding:9px 12px;'
             f'border-bottom:1px solid {RULE};background:{bg};text-align:right;'
             f'font-weight:700;">{pct}</td></tr>')
W(f'<table style="width:100%;border-collapse:collapse;border:1px solid {RULE};'
  f'margin:0 0 14px 0;"><tbody>{rows}</tbody></table>')

for label, text in [
    ("ATTENDANCE",
     "Students are expected to be present during class. Absences accruing more than three times "
     "during the semester will result in a reduction of grades at the discretion of the "
     "instructor. If there are any extenuating circumstances, please reach out to the instructor "
     "to inform them of your situation and to schedule extensions if permitted. Lateness to class "
     "of more than 15 minutes will be counted as an absence unless otherwise communicated to the "
     "instructor in advance."),
    ("DEADLINES",
     "Students should complete assignments to the best of their ability and submit them on time. "
     "If circumstances require a late submission, the student should contact the instructor "
     "before the assignment is due. In the event of an emergency, the student should contact both "
     "the instructor and their student advisor as soon as possible."),
    ("ASSISTANCE",
     "Tutorials will be provided throughout the course in addition to technical support on "
     "Discord. For all hardware assistance, please contact the Help Desk at help@the-bac.edu or "
     "(617) 585-0191.")]:
    W(f'<p style="font-family:{DISPLAY};font-size:10px;letter-spacing:1.4px;color:{MIST};'
      f'margin:14px 0 4px 0;font-weight:700;">{label}</p>')
    para(text, size=14, mb=0)

W(f'<p style="font-family:{BODY};font-size:12px;line-height:1.5;color:{MIST};'
  f'margin:22px 0 0 0;padding-top:12px;border-top:1px solid {RULE};">This page summarizes the '
  f'course for reference. The complete syllabus, including BAC grade definitions, the '
  f'mid-semester warning policy, writing standards, and college policies on academic integrity '
  f'and plagiarism, is distributed separately and available in the class folder.</p>')

fragment = "\n".join(out)

d = pathlib.Path("moodle")
d.mkdir(exist_ok=True)
(d / "syllabus-moodle.html").write_text(fragment + "\n")
(d / "preview.html").write_text(
    '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>Moodle preview</title></head>'
    f'<body style="margin:0;background:#e9e7e2;">'
    f'<div style="max-width:760px;margin:0 auto;background:#fff;padding:24px;">{fragment}</div>'
    '</body></html>\n')

print(f"fragment: {len(fragment)//1024} KB, {fragment.count('<div')} divs, "
      f"{fragment.count('<script')} scripts, {fragment.count('<style')} style blocks")
