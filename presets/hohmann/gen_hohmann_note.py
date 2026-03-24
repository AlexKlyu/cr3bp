"""
Генерация PDF-заметки: прямой (Hohmann-подобный) баллистический перелёт к Луне.
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

OUTPUT = 'hohmann_note.pdf'
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
    'Direct Ballistic Transfer to the Moon (Hohmann-like)', styles['Title2']))
S.append(Paragraph('Technical Note \u2014 March 2026', styles['Subtitle']))
S.append(HRFlowable(width='100%', thickness=0.5, color=HexColor('#003366')))
S.append(Spacer(1, 4 * mm))

S.append(Paragraph('1. Concept', styles['H2']))
S.append(Paragraph(
    'A direct ballistic transfer to the Moon is the simplest class of Earth\u2013Moon '
    'trajectories: the spacecraft departs from low Earth orbit at near-escape velocity '
    'and follows a direct arc to the Moon with no intermediate maneuvers. Unlike a '
    'free-return trajectory, this path is optimized solely for <i>arrival</i> at the Moon, '
    'not for a safe return to Earth.',
    styles['Body']))
S.append(Paragraph(
    'The name "Hohmann-like" reflects the conceptual similarity to Walter Hohmann\u2019s '
    'classical two-impulse coplanar transfer (1925): one burn at departure, one at arrival. '
    'However, in the CR3BP the trajectory is not a simple ellipse due to the Moon\u2019s '
    'gravitational influence throughout the flight and the Coriolis/centrifugal effects '
    'of the rotating frame.',
    styles['Body']))

S.append(Paragraph('2. Initial Conditions', styles['H2']))
S.append(Paragraph(
    'The preset initial conditions in the CR3BP rotating frame are:',
    styles['Body']))

ic_data = [
    ['Parameter', 'Value', 'Notes'],
    ['x\u2080', '\u22129.463 \u00d7 10\u00b3 km', 'LEO departure point'],
    ['y\u2080', '\u22124.782 \u00d7 10\u00b3 km', '(launch angle in 3rd quadrant)'],
    ['z\u2080', '0', 'Planar trajectory'],
    ['vx\u2080', '7.626 km/s', 'TLI velocity components'],
    ['vy\u2080', '\u22127.643 km/s', '(prograde direction)'],
    ['vz\u2080', '0', 'Planar trajectory'],
    ['|v\u2080|', '10.80 km/s', 'Near escape velocity'],
    ['t\u2082\u2099\u2084', '58 h', 'Integration time'],
]
t1 = Table(ic_data, colWidths=[24 * mm, 38 * mm, 48 * mm])
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

S.append(Paragraph('3. Numerical Search Method', styles['H2']))
S.append(Paragraph(
    'The search methodology follows the same two-phase approach as the free-return '
    'trajectory finder, but with a different optimization objective:',
    styles['Body']))

S.append(Paragraph('3.1 Phase 1 \u2014 Angular Scan', styles['H3']))
S.append(Paragraph(
    'The spacecraft departs from the LEO circle (~6,771 km from Earth\u2019s center) with '
    'TLI velocity directed tangentially (prograde). The launch angle \u03b8 is scanned '
    'from 180\u00b0 to 270\u00b0 in 5\u00b0 steps. For each angle, the CR3BP equations '
    'are integrated and the minimum Moon distance is recorded.',
    styles['Body']))

S.append(Paragraph('3.2 Phase 2 \u2014 Nelder-Mead Optimization', styles['H3']))
S.append(Paragraph(
    'Starting from the best angle found in Phase 1, the Nelder-Mead simplex method '
    f'optimizes (\u03b8, v{sub("TLI")}) to minimize the closest approach to the Moon:',
    styles['Body']))
S.append(Paragraph(
    f'f(\u03b8, v) = d{sub("Moon flyby")}',
    styles['Formula']))
S.append(Paragraph(
    'This is simpler than the free-return objective (which also included an Earth return '
    'term) because only arrival at the Moon matters. The optimization converges quickly '
    'since close lunar approaches are easier to achieve than the delicate balance needed '
    'for a free-return.',
    styles['Body']))

S.append(Paragraph('4. Trajectory Properties', styles['H2']))

props_data = [
    ['Property', 'Value'],
    ['Flight time', '~58 hours (2.4 days)'],
    ['Min Moon distance', '~1,765 km (1.0 Moon radii above surface)'],
    ['Min Moon distance (Verlet)', '1,765 km'],
    ['Trajectory shape', 'Direct arc, single pass'],
    ['Total \u0394v', '0 after TLI (ballistic coast)'],
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
    'The trajectory forms a nearly direct arc from Earth to Moon in the rotating frame. '
    'The flight time of ~58 hours is shorter than the free-return trip (~162 hours) '
    'because there is no return leg. The close lunar approach of 1,765 km '
    '(~1.0 Moon radii above the surface) demonstrates successful targeting.',
    styles['Body']))

S.append(Paragraph('5. Comparison with Apollo-13 Free-Return', styles['H2']))

comp_data = [
    ['Property', 'Direct Transfer', 'Free-Return (Apollo-13)'],
    ['Departure area', '3rd quadrant', '3rd quadrant'],
    ['|v\u2080|', '10.80 km/s', '10.78 km/s'],
    ['Flight time', '58 h (one-way)', '162 h (round-trip)'],
    ['Min Moon dist.', '1,765 km', '3,117 km'],
    ['Earth return', 'No return', '6,681 km'],
    ['Optimization target', 'Min Moon distance', 'Min Earth return + Moon flyby'],
    ['Safety', 'No abort option', 'Inherent abort trajectory'],
]
t3 = Table(comp_data, colWidths=[30 * mm, 35 * mm, 45 * mm])
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
    'Both trajectories depart from the same general region (3rd quadrant of the rotating '
    'frame) with nearly identical TLI velocities (~10.8 km/s). The key difference is in '
    'the objective: the direct transfer achieves a closer lunar approach (1,765 km vs. '
    '3,117 km) by not needing to thread the needle for a return path. The free-return '
    'sacrifices close approach distance for the safety of an automatic Earth return.',
    styles['Body']))

S.append(Paragraph('6. Comparison with Classical Hohmann Transfer', styles['H2']))
S.append(Paragraph(
    'The classical Hohmann transfer (1925) is the minimum-energy two-impulse coplanar '
    'transfer between two circular orbits in a two-body problem:',
    styles['Body']))
S.append(Paragraph(
    f'\u0394v{sub("1")} at departure: accelerate from circular orbit onto elliptical '
    f'transfer orbit',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    f'\u0394v{sub("2")} at arrival: circularize into the target orbit',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Spacer(1, 2 * mm))
S.append(Paragraph(
    'For Earth\u2013Moon transfer in the two-body approximation:',
    styles['Body']))
S.append(Paragraph(
    f'\u0394v{sub("1")} \u2248 3.13 km/s (TLI from 400 km LEO), &nbsp; '
    f'\u0394v{sub("2")} \u2248 0.82 km/s (lunar orbit insertion at 100 km)',
    styles['Formula']))
S.append(Paragraph(
    'The CR3BP direct transfer in our simulation is a "half-Hohmann": only the departure '
    'burn is applied. Without the arrival burn, the spacecraft performs a flyby rather '
    'than orbit insertion. In a real mission, an orbit insertion burn at perilune would '
    'capture the spacecraft into lunar orbit, completing the Hohmann-like transfer.',
    styles['Body']))
S.append(Paragraph(
    'The advantage of modeling in the CR3BP rather than the two-body problem is that '
    'lunar gravity is included throughout the trajectory, not just at arrival. This '
    'produces a more realistic flyby geometry and allows the trajectory to be sensitive '
    'to the Moon\u2019s gravitational focusing effect.',
    styles['Body']))

S.append(Paragraph('References', styles['H2']))

styles.add(ParagraphStyle(
    'Ref', parent=styles['Normal'], fontSize=9, leading=12,
    leftIndent=10 * mm, firstLineIndent=-10 * mm, spaceAfter=2 * mm,
    fontName=FONT,
))

refs = [
    (
        'Hohmann, W. (1925). '
        '<i>Die Erreichbarkeit der Himmelsk\u00f6rper.</i> '
        'R. Oldenbourg, Munich.'
        '<br/>'
        'Original work proposing the minimum-energy two-impulse transfer between '
        'coplanar circular orbits.'
    ),
    (
        'Szebehely, V. (1967). '
        '<i>Theory of Orbits: The Restricted Problem of Three Bodies.</i> '
        'Academic Press. ISBN 978-0-12-680650-9.'
        '<br/>'
        'CR3BP formulation and equations of motion used for the trajectory integration.'
    ),
    (
        'Koon, W.S., Lo, M.W., Marsden, J.E., Ross, S.D. (2011). '
        '<i>Dynamical Systems, the Three-Body Problem and Space Mission Design.</i> '
        'Marsden Books. ISBN 978-0-615-24095-4.'
        '<br/>'
        'Modern trajectory design techniques in the CR3BP, including direct transfers '
        'and their relationship to invariant manifolds.'
    ),
    (
        'Battin, R.H. (1999). '
        '<i>An Introduction to the Mathematics and Methods of Astrodynamics.</i> '
        'Revised edition. AIAA Education Series. ISBN 978-1-56347-342-5.'
        '<br/>'
        'Detailed derivation of Hohmann transfers, Lambert\u2019s problem, and '
        'the transition from two-body to three-body trajectory design.'
    ),
    (
        'Bate, R.R., Mueller, D.D., White, J.E. (1971). '
        '<i>Fundamentals of Astrodynamics.</i> '
        'Dover Publications. ISBN 978-0-486-60061-1.'
        '<br/>'
        'Standard reference for orbital mechanics including Hohmann transfers, '
        'patched conics, and lunar trajectory design.'
    ),
]

for i, ref in enumerate(refs, 1):
    S.append(Paragraph(f'[{i}] {ref}', styles['Ref']))

doc.build(S)
print(f'PDF generated: {OUTPUT}')
