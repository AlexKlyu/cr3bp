"""
Генерация PDF-заметки: свободно-возвратная траектория (Apollo-13).
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable,
)

pdfmetrics.registerFont(TTFont('ArialUni', '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'))

OUTPUT = 'free_return_note.pdf'
FONT = 'ArialUni'

doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    leftMargin=25 * mm, rightMargin=25 * mm,
    topMargin=20 * mm, bottomMargin=20 * mm,
)

styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    'Title2', parent=styles['Title'], fontSize=18, spaceAfter=4 * mm,
    textColor=HexColor('#003366'), fontName=FONT,
))
styles.add(ParagraphStyle(
    'Subtitle', parent=styles['Normal'], fontSize=11, alignment=TA_CENTER,
    textColor=HexColor('#666666'), spaceAfter=8 * mm, fontName=FONT,
))
styles.add(ParagraphStyle(
    'H2', parent=styles['Heading2'], fontSize=13,
    textColor=HexColor('#003366'), spaceBefore=6 * mm, spaceAfter=3 * mm,
    fontName=FONT,
))
styles.add(ParagraphStyle(
    'H3', parent=styles['Heading3'], fontSize=11,
    textColor=HexColor('#336699'), spaceBefore=4 * mm, spaceAfter=2 * mm,
    fontName=FONT,
))
styles.add(ParagraphStyle(
    'Body', parent=styles['Normal'], fontSize=10, leading=14,
    alignment=TA_JUSTIFY, spaceAfter=2 * mm, fontName=FONT,
))
styles.add(ParagraphStyle(
    'Formula', parent=styles['Normal'], fontSize=10, leading=14,
    alignment=TA_CENTER, spaceAfter=2 * mm, spaceBefore=2 * mm,
    fontName=FONT,
))
styles.add(ParagraphStyle(
    'BulletItem', parent=styles['Normal'], fontSize=10, leading=14,
    leftIndent=12 * mm, bulletIndent=6 * mm, spaceAfter=1 * mm,
    fontName=FONT,
))


def sub(text):
    return f'<sub>{text}</sub>'


def sup(text):
    return f'<sup>{text}</sup>'


S = []

S.append(Paragraph(
    'Free-Return Trajectory in the Earth\u2013Moon CR3BP', styles['Title2']))
S.append(Paragraph('Technical Note \u2014 March 2026', styles['Subtitle']))
S.append(HRFlowable(width='100%', thickness=0.5, color=HexColor('#003366')))
S.append(Spacer(1, 4 * mm))

S.append(Paragraph('1. Problem Statement', styles['H2']))
S.append(Paragraph(
    'A <i>free-return trajectory</i> is a circumlunar flight path that, after '
    'trans-lunar injection (TLI), requires no further propulsion to return to Earth. '
    'The spacecraft departs from low Earth orbit, swings around the Moon using lunar '
    'gravity, and returns to Earth vicinity \u2014 all ballistically.',
    styles['Body']))
S.append(Paragraph(
    'This trajectory type became famous during Apollo 13 (April 1970), when an oxygen '
    'tank explosion disabled the Service Module. The crew used a free-return trajectory '
    'to safely return to Earth without the main engine.',
    styles['Body']))
S.append(Paragraph(
    'The goal is to find initial conditions in the CR3BP rotating frame that produce a '
    'trajectory departing from LEO altitude, performing a close lunar flyby, and returning '
    'to Earth vicinity \u2014 with zero thrust throughout.',
    styles['Body']))

S.append(Paragraph('2. CR3BP Rotating Frame', styles['H2']))
S.append(Paragraph(
    'We work in the Circular Restricted Three-Body Problem (CR3BP) rotating frame with '
    'the Earth\u2013Moon barycenter at the origin. In this frame, both bodies are stationary:',
    styles['Body']))
S.append(Paragraph(
    f'<b>Earth</b> at x = \u22124.67 \u00d7 10\u00b3 km, '
    f'<b>Moon</b> at x = +382.80 \u00d7 10\u00b3 km.',
    styles['Formula']))
S.append(Paragraph(
    'The equations of motion include gravitational attraction from both bodies plus '
    'Coriolis and centrifugal pseudo-forces from the rotating frame:',
    styles['Body']))
S.append(Paragraph(
    f'a{sub("x")} = \u03c9\u00b2x + 2\u03c9v{sub("y")} '
    f'\u2212 K{sub("E")}(x + d{sub("E")}) \u2212 K{sub("M")}(x \u2212 d{sub("M")})',
    styles['Formula']))
S.append(Paragraph(
    f'a{sub("y")} = \u03c9\u00b2y \u2212 2\u03c9v{sub("x")} '
    f'\u2212 (K{sub("E")} + K{sub("M")})y',
    styles['Formula']))
S.append(Paragraph(
    f'where K{sub("i")} = GM{sub("i")}/r{sub("i")}\u00b3 and '
    f'\u03c9 = 2.662 \u00d7 10{sup("\u22126")} rad/s is the angular velocity of the '
    'rotating frame.',
    styles['Body']))

S.append(Paragraph('3. Physics of the Free-Return Trajectory', styles['H2']))

S.append(Paragraph('3.1 LEO Departure and TLI', styles['H3']))
S.append(Paragraph(
    f'The spacecraft starts in a 400 km altitude low Earth orbit (LEO), at radius '
    f'r{sub("LEO")} = 6,771 km from Earth\u2019s center. The circular orbital velocity '
    f'at this altitude is v{sub("circ")} \u2248 7.67 km/s.',
    styles['Body']))
S.append(Paragraph(
    f'Trans-Lunar Injection (TLI) adds approximately 3.1 km/s of \u0394v prograde, '
    f'bringing the total velocity to ~10.8 km/s \u2014 just below Earth escape velocity '
    f'(v{sub("esc")} = \u221a(2GM{sub("E")}/r{sub("LEO")}) \u2248 10.85 km/s). '
    f'This places the spacecraft on a highly eccentric, near-parabolic orbit that '
    f'reaches the Moon\u2019s distance (~384,400 km).',
    styles['Body']))

S.append(Paragraph('3.2 Lunar Gravity Assist', styles['H3']))
S.append(Paragraph(
    'As the spacecraft approaches the Moon, lunar gravity bends its trajectory. '
    'The key parameter is the <i>perilune distance</i> \u2014 the closest approach to the '
    'Moon\u2019s center. A closer flyby produces a stronger deflection. For a free-return, '
    'the deflection must be precisely tuned so the outbound trajectory curves back toward '
    'Earth.',
    styles['Body']))
S.append(Paragraph(
    'In the CR3BP rotating frame, this appears as the spacecraft passing behind the Moon '
    '(in the +x direction) and being deflected back by the combined effect of lunar '
    'gravity and Coriolis forces.',
    styles['Body']))

S.append(Paragraph('3.3 Energy and the Jacobi Integral', styles['H3']))
S.append(Paragraph(
    'The CR3BP has one integral of motion \u2014 the Jacobi constant:',
    styles['Body']))
S.append(Paragraph(
    f'C{sub("J")} = \u03c9\u00b2(x\u00b2 + y\u00b2) + '
    f'2GM{sub("E")}/r{sub("E")} + 2GM{sub("M")}/r{sub("M")} '
    f'\u2212 (v{sub("x")}\u00b2 + v{sub("y")}\u00b2 + v{sub("z")}\u00b2)',
    styles['Formula']))
S.append(Paragraph(
    f'A free-return trajectory must have a Jacobi constant that allows passage near the '
    f'Moon (through the "neck" around the L1 point) while also permitting return to '
    f'Earth. This constrains the energy window: too much energy and the spacecraft '
    f'escapes; too little and it cannot reach the Moon.',
    styles['Body']))

S.append(Paragraph('4. Numerical Search Methodology', styles['H2']))
S.append(Paragraph(
    'Unlike Lagrange points or halo orbits, no analytical formula exists for free-return '
    'initial conditions. The CR3BP is chaotic near the Moon, making the trajectory '
    'exquisitely sensitive to initial conditions. We use a two-phase numerical approach:',
    styles['Body']))

S.append(Paragraph('4.1 Phase 1 \u2014 Angular Scan', styles['H3']))
S.append(Paragraph(
    'The spacecraft departs from a point on the LEO circle around Earth, with TLI '
    'velocity directed tangentially (prograde). The launch <i>angle</i> \u03b8 determines '
    'which point on the LEO circle is the departure point (0\u00b0 = Earth\u2013Moon line, '
    'counterclockwise). We scan \u03b8 from 180\u00b0 to 270\u00b0 in 5\u00b0 steps at '
    'a fixed TLI velocity near escape speed.',
    styles['Body']))
S.append(Paragraph(
    'For each angle, we integrate the CR3BP equations for 400 hours using '
    f'scipy\u2019s RK45 integrator and record: (a) minimum distance to Moon, '
    f'(b) minimum distance to Earth after the Moon flyby.',
    styles['Body']))

S.append(Paragraph('4.2 Phase 2 \u2014 Nelder-Mead Optimization', styles['H3']))
S.append(Paragraph(
    'Starting from the best angle found in Phase 1, we optimize two parameters '
    '(\u03b8, v{sub("TLI")}) using the Nelder-Mead simplex method. The objective function '
    'minimizes the Earth return distance (with a penalty for Moon collision), subject to '
    'the constraint that the trajectory must pass within a reasonable distance of both '
    'the Moon and Earth:'.replace('{sub("TLI")}', '<sub>TLI</sub>'),
    styles['Body']))
S.append(Paragraph(
    f'f(\u03b8, v) = d{sub("Earth return")} + 0.5 \u00d7 d{sub("Moon flyby")}',
    styles['Formula']))
S.append(Paragraph(
    'The optimization converges in ~80 iterations, each requiring a full trajectory '
    'integration (600 hours). Total computation time: ~2\u20133 minutes.',
    styles['Body']))

S.append(Paragraph('4.3 Return Detection', styles['H3']))
S.append(Paragraph(
    'A naive approach checks the Earth distance in the "second half" of the trajectory, '
    'but this fails because the return time is unpredictable. Instead, we find the Moon '
    'flyby time (global minimum of Moon distance), then search for the first local '
    'minimum of Earth distance <i>after</i> the flyby using scipy\u2019s '
    '<font face="Courier">argrelmin</font> function.',
    styles['Body']))

S.append(Paragraph('5. Results', styles['H2']))
S.append(Paragraph(
    'The optimization yields a free-return trajectory with the following initial '
    'conditions in the CR3BP rotating frame:',
    styles['Body']))

result_data = [
    ['Parameter', 'Value', 'Notes'],
    ['x\u2080', '\u22129.331 \u00d7 10\u00b3 km', 'LEO departure point'],
    ['y\u2080', '\u22124.912 \u00d7 10\u00b3 km', '(launch angle \u2248 226.5\u00b0)'],
    ['z\u2080', '0', 'Planar trajectory'],
    ['vx\u2080', '7.819 km/s', 'Tangential TLI velocity'],
    ['vy\u2080', '\u22127.420 km/s', '(prograde direction)'],
    ['vz\u2080', '0', 'Planar trajectory'],
    ['|v\u2080|', '10.78 km/s', 'Near escape velocity (10.85)'],
    ['t\u2080 \u2192 flyby', '~64 hours', '2.7 days to Moon'],
    ['t\u2080 \u2192 return', '~162 hours', '6.7 days total trip'],
]
t1 = Table(result_data, colWidths=[24 * mm, 38 * mm, 48 * mm])
t1.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#003366')),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#FFFFFF')),
    ('FONTNAME', (0, 0), (-1, -1), FONT),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (1, 0), (1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#999999')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#F5F5F5'), HexColor('#FFFFFF')]),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
]))
S.append(t1)
S.append(Spacer(1, 3 * mm))

S.append(Paragraph('Trajectory Properties:', styles['H3']))

props_data = [
    ['Property', 'Value'],
    ['Perilune (min Moon distance)', '3,117 km (~1.8 Moon radii)'],
    ['Earth return distance', '6,681 km (~1.05 Earth radii above surface)'],
    ['x range', '[\u2212341, +386] \u00d7 10\u00b3 km'],
    ['y range', '[\u2212381, +406] \u00d7 10\u00b3 km'],
    ['Total \u0394v required', '0 (ballistic after TLI)'],
]
t2 = Table(props_data, colWidths=[42 * mm, 68 * mm])
t2.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#003366')),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#FFFFFF')),
    ('FONTNAME', (0, 0), (-1, -1), FONT),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#999999')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#F5F5F5'), HexColor('#FFFFFF')]),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
]))
S.append(t2)
S.append(Spacer(1, 3 * mm))

S.append(Paragraph(
    'The trajectory forms a large loop in the rotating frame: departing Earth in the '
    '\u22123rd quadrant (x &lt; 0, y &lt; 0), swinging around the Moon at perilune of '
    '~3,100 km (comparable to Apollo missions), and returning to Earth vicinity at a '
    'distance of ~6,700 km \u2014 just 310 km above LEO altitude.',
    styles['Body']))

S.append(Paragraph('6. Comparison with Apollo Missions', styles['H2']))

apollo_data = [
    ['Parameter', 'Our CR3BP Result', 'Apollo 13 (actual)'],
    ['Perilune distance', '3,117 km', '254 km'],
    ['Total flight time', '6.7 days', '5.9 days'],
    ['TLI velocity', '10.78 km/s', '10.83 km/s'],
    ['Model', 'CR3BP (2 bodies + rotation)', 'Full ephemeris (n-body)'],
    ['Mid-course corrections', 'None (ballistic)', '2 small burns'],
]
t3 = Table(apollo_data, colWidths=[32 * mm, 38 * mm, 40 * mm])
t3.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#003366')),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#FFFFFF')),
    ('FONTNAME', (0, 0), (-1, -1), FONT),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#999999')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#F5F5F5'), HexColor('#FFFFFF')]),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
]))
S.append(t3)
S.append(Spacer(1, 3 * mm))

S.append(Paragraph(
    'Our perilune is larger than Apollo 13\u2019s because the CR3BP model lacks the '
    'eccentricity of the real Moon\u2019s orbit and solar perturbations. In the simplified '
    'model, closer approaches tend to result in Moon collision or escape, requiring '
    'the optimization to find a delicate balance.',
    styles['Body']))

S.append(Paragraph('7. Apollo 13: Historical Context', styles['H2']))
S.append(Paragraph(
    'On April 13, 1970, an oxygen tank exploded in the Apollo 13 Service Module, '
    'crippling the spacecraft 321,860 km from Earth. The crew \u2014 Jim Lovell, Jack '
    'Swigert, and Fred Haise \u2014 moved into the Lunar Module as a "lifeboat" and '
    'faced a critical decision: attempt a direct abort (fire the SPS engine to turn '
    'around) or continue to the Moon on a free-return trajectory.',
    styles['Body']))
S.append(Paragraph(
    'Mission Control chose the free-return option because:',
    styles['Body']))
S.append(Paragraph(
    '<b>Safety</b>: The SPS engine\u2019s health was unknown after the explosion. '
    'A free-return required no main engine firing.',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '<b>Physics</b>: The Moon\u2019s gravity provided the trajectory deflection for free, '
    'acting as a natural "slingshot."',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '<b>Margin</b>: Two small LM descent-engine burns were used to refine the trajectory '
    'and speed up the return, but the basic path was ballistic.',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Spacer(1, 2 * mm))
S.append(Paragraph(
    'The crew rounded the Moon at a perilune of 254 km, endured freezing temperatures '
    'and power rationing, and splashed down safely on April 17 \u2014 142 hours after '
    'the explosion. The mission is often called NASA\u2019s "successful failure."',
    styles['Body']))
S.append(Paragraph(
    'Free-return trajectories remain relevant today: China\u2019s Queqiao-2 relay '
    'satellite (2024) used a lunar free-return flyby, and the concept underpins abort '
    'options for Artemis missions to the Moon.',
    styles['Body']))

S.append(Paragraph('References', styles['H2']))

styles.add(ParagraphStyle(
    'Ref', parent=styles['Normal'], fontSize=9, leading=12,
    leftIndent=10 * mm, firstLineIndent=-10 * mm, spaceAfter=2 * mm,
    fontName=FONT,
))

refs = [
    (
        'Szebehely, V. (1967). '
        '<i>Theory of Orbits: The Restricted Problem of Three Bodies.</i> '
        'Academic Press. ISBN 978-0-12-680650-9.'
        '<br/>'
        'Classical reference for the CR3BP formulation, Jacobi integral, rotating-frame '
        'equations of motion, and stability analysis.'
    ),
    (
        'Koon, W.S., Lo, M.W., Marsden, J.E., Ross, S.D. (2011). '
        '<i>Dynamical Systems, the Three-Body Problem and Space Mission Design.</i> '
        'Marsden Books. ISBN 978-0-615-24095-4.'
        '<br/>'
        'Comprehensive treatment of CR3BP dynamics, invariant manifolds, and trajectory '
        'design including free-return and low-energy transfers.'
    ),
    (
        'NASA. (1970). '
        '"Apollo 13 Mission Report." MSC-02680. NASA Manned Spacecraft Center, Houston.'
        '<br/>'
        'Official post-flight report covering the accident, trajectory decisions, '
        'free-return implementation, and crew return.'
    ),
    (
        'Lovell, J. and Kluger, J. (1994). '
        '<i>Lost Moon: The Perilous Voyage of Apollo 13.</i> '
        'Houghton Mifflin. ISBN 978-0-395-67029-7.'
        '<br/>'
        'First-person account of the Apollo 13 mission by Commander Jim Lovell, '
        'including the decision to use the free-return trajectory.'
    ),
    (
        'Schwaniger, A.J. (1963). '
        '"Trajectories in the Earth-Moon Space with Symmetrical Free Return Properties." '
        '<i>NASA TN D-1833.</i>'
        '<br/>'
        'Early analytical study of free-return trajectories in the Earth\u2013Moon system, '
        'establishing the mathematical framework for Apollo mission planning.'
    ),
]

for i, ref in enumerate(refs, 1):
    S.append(Paragraph(f'[{i}] {ref}', styles['Ref']))

doc.build(S)
print(f'PDF generated: {OUTPUT}')
