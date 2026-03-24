"""
Генерация PDF-заметки: подход к нахождению гало-орбиты у L2 (JWST).
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

OUTPUT = 'l2_halo_orbit_note.pdf'
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
    'Finding L2 Halo Orbits in the Earth\u2013Moon CR3BP', styles['Title2']))
S.append(Paragraph(
    'Technical Note \u2014 March 2026 | JWST-class orbit context', styles['Subtitle']))
S.append(HRFlowable(width='100%', thickness=0.5, color=HexColor('#003366')))
S.append(Spacer(1, 4 * mm))

S.append(Paragraph('1. Problem Statement', styles['H2']))
S.append(Paragraph(
    'The Earth\u2013Moon L2 point lies on the far side of the Moon, approximately 61,000 km '
    'beyond the lunar surface. This libration point is the translunar analogue of L1: '
    'both are collinear saddle points with unstable dynamics, but L2 is of particular '
    'interest because the Sun\u2013Earth L2 (a different system) hosts the James Webb Space '
    'Telescope (JWST). The Earth\u2013Moon L2 has been studied for lunar relay and far-side '
    'exploration missions.',
    styles['Body']))
S.append(Paragraph(
    f'Our goal is to find initial conditions (x{sub("0")}, 0, z{sub("0")}, 0, '
    f'vy{sub("0")}, 0) that produce a periodic halo orbit around the Earth\u2013Moon L2 '
    f'with a prescribed out-of-plane amplitude A{sub("z")} = 20,000 km.',
    styles['Body']))

S.append(Paragraph('2. L2 vs L1 \u2014 Key Differences', styles['H2']))
S.append(Paragraph(
    'While the Richardson method applies to both L1 and L2, the Legendre coefficients '
    f'c{sub("n")} differ because L2 is on the <i>opposite</i> side of the Moon from L1. '
    'This changes the gravitational expansion fundamentally.',
    styles['Body']))

S.append(Paragraph('2.1 Position and \u03b3', styles['H3']))
S.append(Paragraph(
    f'For L1, \u03b3{sub("1")} = (d{sub("M")} \u2212 x{sub("L1")}) / L \u2248 0.1526 '
    f'measures the L1\u2013Moon distance normalized by the Earth\u2013Moon separation. '
    f'For L2, \u03b3{sub("2")} = (x{sub("L2")} \u2212 d{sub("M")}) / L \u2248 0.1645 '
    '\u2014 L2 is about 8% farther from the Moon than L1.',
    styles['Body']))

S.append(Paragraph('2.2 Legendre Coefficients', styles['H3']))
S.append(Paragraph(
    f'The c{sub("n")} formula for L2 differs from L1 in two ways:',
    styles['Body']))
S.append(Paragraph(
    f'<b>L1:</b> &nbsp; c{sub("n")} = \u03b3{sup("\u22123")} '
    f'[ \u03bc + (\u22121){sup("n")} (1\u2212\u03bc) '
    f'\u03b3{sup("n+1")} / (1\u2212\u03b3){sup("n+1")} ]',
    styles['Formula']))
S.append(Paragraph(
    f'<b>L2:</b> &nbsp; c{sub("n")} = \u03b3{sup("\u22123")} '
    f'[ (\u22121){sup("n")} \u03bc + (1\u2212\u03bc) '
    f'\u03b3{sup("n+1")} / (1+\u03b3){sup("n+1")} ]',
    styles['Formula']))
S.append(Paragraph(
    f'The sign flip on \u03bc (via (\u22121){sup("n")}) and the change from '
    f'(1\u2212\u03b3) to (1+\u03b3) in the denominator have a dramatic effect: '
    f'for L2, c{sub("3")} \u2248 <b>\u22122.64</b> (negative!), '
    f'compared to c{sub("3")} \u2248 +3.13 for L1. '
    f'The other coefficients: c{sub("2")} \u2248 3.35, c{sub("4")} \u2248 2.74.',
    styles['Body']))

S.append(Paragraph('2.3 Eigenvalues', styles['H3']))
S.append(Paragraph(
    f'The smaller c{sub("2")} at L2 (3.35 vs 5.04 at L1) yields different eigenvalues: '
    f'<b>\u03bb \u2248 1.907</b> (vs 2.312 at L1) and '
    f'<b>\u03bd = \u221ac{sub("2")} \u2248 1.832</b> (vs 2.246 at L1). '
    'The ratio \u03bb/\u03bd is closer to 1, meaning less nonlinear frequency correction '
    'is needed for the halo resonance condition.',
    styles['Body']))

S.append(Paragraph(
    "3. Richardson's 3rd-Order Approximation for L2", styles['H2']))
S.append(Paragraph(
    f'The Richardson algebra is identical to L1 \u2014 only the c{sub("n")} values change. '
    'The same 2nd- and 3rd-order coefficients (a{sub}, b{sub}, d{sub} series), '
    'frequency corrections (s{sub("1")}, s{sub("2")}), and halo constraint '
    f'(l{sub("1")}A{sub("x")}{sup("2")} + l{sub("2")}A{sub("z")}{sup("2")} + \u0394 = 0) '
    'are computed from the new c{sub("n")} values.',
    styles['Body']))
S.append(Paragraph(
    f'The negative c{sub("3")} has a subtle but important effect: it flips the sign of '
    'many 2nd-order coefficients. In particular, the nonlinear coupling terms that shape '
    'the orbit have opposite curvature compared to L1. Despite this, the Richardson '
    'expansion remains valid and produces a reasonable starting guess.',
    styles['Body']))
S.append(Paragraph(
    f'For A{sub("z")} = 20,000 km, the method yields A{sub("x")} \u2248 8,810 km, '
    f'period T \u2248 350.0 h, and initial conditions '
    f'(x{sub("0")} = 434.27 \u00d7 10\u00b3 km, vy{sub("0")} = 0.138 km/s).',
    styles['Body']))

S.append(Paragraph(
    '4. Why the Analytical Approximation Alone Fails', styles['H2']))
S.append(Paragraph(
    f'As with L1, the 3rd-order Richardson guess for L2 does not produce a closed orbit '
    f'when propagated numerically. The trajectory departs from L2 and follows the '
    'unstable manifold, typically escaping toward (or away from) the Moon.',
    styles['Body']))
S.append(Paragraph(
    'The same two factors are responsible:',
    styles['Body']))
S.append(Paragraph(
    f'<b>Truncation error</b>: With A{sub("z")} = 20,000 km and '
    f'\u03b3{sub("2")}L \u2248 63,600 km, the ratio A{sub("z")}/(\u03b3L) \u2248 0.31 '
    'is not small. The 3rd-order expansion error is substantial, with '
    f'vy{sub("0")} off by ~65%.',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '<b>Dynamical instability</b>: L2, like L1, has a real (hyperbolic) eigenvalue. '
    'Any initial-condition error excites the unstable manifold and grows exponentially. '
    'The e-folding time at L2 is slightly longer than at L1 (~5 days vs ~4 days) due to '
    f'the weaker local gravity gradient (smaller c{sub("2")}), but the effect is still '
    'devastating over one orbital period (~14.5 days).',
    styles['BulletItem'], bulletText='\u2022'))

S.append(Paragraph(
    '5. Numerical Differential Correction', styles['H2']))
S.append(Paragraph(
    'The same shooting method used for L1 applies without modification. The full '
    'nonlinear CR3BP equations of motion are point-agnostic \u2014 they describe motion '
    'everywhere in the rotating frame. Only the initial conditions determine whether '
    'the trajectory orbits L1 or L2.',
    styles['Body']))
S.append(Paragraph(
    f'Starting from the Richardson guess for L2, we fix z{sub("0")} and iterate on '
    f'(x{sub("0")}, vy{sub("0")}) using Newton\u2019s method with the periodicity condition '
    f'vx{sub("f")} = vz{sub("f")} = 0 at the next y = 0 crossing.',
    styles['Body']))

S.append(Paragraph('5.1 Convergence', styles['H3']))
S.append(Paragraph(
    'The method converges in <b>10 iterations</b> to a residual of '
    f'1.2 \u00d7 10{sup("\u221211")} m/s. The corrections are again significant:',
    styles['Body']))

table_data = [
    ['Parameter', 'Richardson (Stage 1)', 'Corrected (Stage 2)', '\u0394'],
    ['x\u2080 (10\u00b3 km)', '434.270', '426.963', '\u22127.307'],
    ['vy\u2080 (km/s)', '0.1375', '0.2274', '+0.0899'],
    ['T (hours)', '350.0', '346.9', '\u22123.1'],
]
t = Table(table_data, colWidths=[30 * mm, 42 * mm, 42 * mm, 22 * mm])
t.setStyle(TableStyle([
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
S.append(t)
S.append(Spacer(1, 3 * mm))
S.append(Paragraph(
    f'The correction to vy{sub("0")} (+65%) confirms that the analytical approximation '
    'underpredicts the tangential velocity needed for the true periodic orbit, as was also '
    'the case for L1.',
    styles['Body']))

S.append(Paragraph('6. Final Result', styles['H2']))
S.append(Paragraph(
    f'The corrected initial conditions for an L2 halo orbit with A{sub("z")} = 20,000 km '
    f'in the Earth\u2013Moon rotating frame (barycenter at origin):', styles['Body']))

result_data = [
    ['x\u2080', '426.963 \u00d7 10\u00b3 km', '(~19,600 km beyond L2)'],
    ['y\u2080', '0', '(xz-plane crossing)'],
    ['z\u2080', '17.601 \u00d7 10\u00b3 km', '(out-of-plane amplitude)'],
    ['vx\u2080', '0', '(perpendicular crossing)'],
    ['vy\u2080', '0.22743 km/s', '(227.4 m/s in +y direction)'],
    ['vz\u2080', '0', '(perpendicular crossing)'],
    ['Period', '346.9 hours', '(14.5 days)'],
]
t2 = Table(result_data, colWidths=[16 * mm, 38 * mm, 55 * mm])
t2.setStyle(TableStyle([
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('FONTNAME', (0, 0), (-1, -1), FONT),
    ('TEXTCOLOR', (2, 0), (2, -1), HexColor('#666666')),
    ('GRID', (0, 0), (-1, -1), 0.3, HexColor('#CCCCCC')),
    ('TOPPADDING', (0, 0), (-1, -1), 2),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
]))
S.append(t2)
S.append(Spacer(1, 3 * mm))
S.append(Paragraph(
    'When propagated numerically for one full period (346.9 h), the trajectory forms a '
    'closed 3D loop around L2 \u2014 a halo orbit visible in the simulator as the '
    '"Орбита L2 (JWST)" preset.',
    styles['Body']))

S.append(Paragraph('7. JWST and L2 Halo Orbits', styles['H2']))
S.append(Paragraph(
    'The James Webb Space Telescope orbits the <i>Sun\u2013Earth</i> L2 point (1.5 million km '
    'from Earth), not the Earth\u2013Moon L2 computed here. However, the dynamics are '
    'analogous: both are collinear libration points requiring station-keeping due to '
    'inherent instability. The Earth\u2013Moon L2 halo orbit in this note has a similar '
    'shape and stability characteristics, making it a useful pedagogical model for '
    'understanding JWST-class missions.',
    styles['Body']))
S.append(Paragraph(
    'The Earth\u2013Moon L2 has practical applications too: China\u2019s Queqiao relay satellite '
    '(2018) used a halo orbit around this point to provide communications for the '
    'Chang\u2019e 4 far-side lander.',
    styles['Body']))

S.append(Paragraph('8. Key Takeaway', styles['H2']))
S.append(Paragraph(
    'The Richardson\u2013correction pipeline generalizes cleanly from L1 to L2: only the '
    f'Legendre coefficients c{sub("n")} change (notably c{sub("3")} flips sign), while '
    'the perturbation algebra and the differential corrector remain identical. The negative '
    f'c{sub("3")} at L2 does not cause any convergence issues \u2014 the corrector needs '
    'only 10 iterations. This confirms that the two-stage approach (analytical guess + '
    'numerical refinement) is robust across collinear libration points.',
    styles['Body']))

S.append(Paragraph('References', styles['H2']))

styles.add(ParagraphStyle(
    'Ref', parent=styles['Normal'], fontSize=9, leading=12,
    leftIndent=10 * mm, firstLineIndent=-10 * mm, spaceAfter=2 * mm,
    fontName=FONT,
))

refs = [
    (
        'Richardson, D.L. (1980). '
        '"Analytic Construction of Periodic Orbits about the Collinear Points." '
        '<i>Celestial Mechanics</i>, 22(3), 241\u2013253. '
        'doi:10.1007/BF01229511'
        '<br/>'
        'The original 3rd-order analytical approximation for halo orbits. '
        'Derives all Lindstedt\u2013Poincar\u00e9 coefficients; applies to L1, L2, and L3.'
    ),
    (
        'Howell, K.C. (1984). '
        '"Three-Dimensional, Periodic, \u2018Halo\u2019 Orbits." '
        '<i>Celestial Mechanics</i>, 32(1), 53\u201371. '
        'doi:10.1007/BF01358403'
        '<br/>'
        'Systematic numerical computation of halo orbit families using differential '
        'correction. Includes L2 orbit families and continuation methods.'
    ),
    (
        'Koon, W.S., Lo, M.W., Marsden, J.E., Ross, S.D. (2011). '
        '<i>Dynamical Systems, the Three-Body Problem and Space Mission Design.</i> '
        'Marsden Books. ISBN 978-0-615-24095-4.'
        '<br/>'
        'Comprehensive textbook covering CR3BP dynamics. Ch. 2\u20133 derive the '
        'Legendre coefficient formulas for both L1 and L2.'
    ),
    (
        'Farquhar, R.W. and Kamel, A.A. (1973). '
        '"Quasi-Periodic Orbits about the Translunar Libration Point." '
        '<i>Celestial Mechanics</i>, 7(4), 458\u2013473. '
        'doi:10.1007/BF01227511'
        '<br/>'
        'Pioneering study of orbits around the Earth\u2013Moon L2 point. '
        'Proposed relay satellite concepts later realized by Queqiao.'
    ),
    (
        'Gao, Y. et al. (2019). '
        '"Low-energy transfer to the Earth\u2013Moon L2 halo orbit: the Queqiao mission." '
        '<i>Acta Astronautica</i>, 164, 111\u2013120.'
        '<br/>'
        'Mission design for China\u2019s Queqiao relay satellite in an Earth\u2013Moon L2 '
        'halo orbit, demonstrating practical application of L2 halo orbit computation.'
    ),
]

for i, ref in enumerate(refs, 1):
    S.append(Paragraph(f'[{i}] {ref}', styles['Ref']))

doc.build(S)
print(f'PDF generated: {OUTPUT}')
