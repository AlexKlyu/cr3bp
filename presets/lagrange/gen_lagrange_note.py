"""
Генерация PDF-заметки: точки Лагранжа L1-L5 в системе Земля-Луна (CR3BP).
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

OUTPUT = 'lagrange_note.pdf'
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
    'Lagrange Points L1\u2013L5 in the Earth\u2013Moon CR3BP', styles['Title2']))
S.append(Paragraph('Technical Note \u2014 March 2026', styles['Subtitle']))
S.append(HRFlowable(width='100%', thickness=0.5, color=HexColor('#003366')))
S.append(Spacer(1, 4 * mm))

S.append(Paragraph('1. What Are Lagrange Points?', styles['H2']))
S.append(Paragraph(
    'In the Circular Restricted Three-Body Problem (CR3BP), the <i>Lagrange points</i> '
    '(also called <i>libration points</i>) are the five equilibrium solutions where a '
    'massless test particle remains stationary in the rotating frame. At these points, '
    'the gravitational attraction from both primary bodies and the centrifugal '
    'pseudo-force exactly cancel.',
    styles['Body']))
S.append(Paragraph(
    'First identified by Leonhard Euler (L1, L2, L3 in 1767) and Joseph-Louis Lagrange '
    '(L4, L5 in 1772), these points are fundamental structures of the three-body problem. '
    'In the Earth\u2013Moon system, they serve as natural "parking places" and gateways for '
    'space missions.',
    styles['Body']))
S.append(Paragraph(
    'At equilibrium, all accelerations vanish in the rotating frame:',
    styles['Body']))
S.append(Paragraph(
    f'a{sub("x")} = \u03c9\u00b2x + 2\u03c9v{sub("y")} '
    f'\u2212 K{sub("E")}(x + d{sub("E")}) \u2212 K{sub("M")}(x \u2212 d{sub("M")}) = 0',
    styles['Formula']))
S.append(Paragraph(
    f'a{sub("y")} = \u03c9\u00b2y \u2212 2\u03c9v{sub("x")} '
    f'\u2212 (K{sub("E")} + K{sub("M")})y = 0',
    styles['Formula']))
S.append(Paragraph(
    'with v = 0 at equilibrium. The collinear points (L1, L2, L3) lie on the x-axis '
    '(y = 0), while the triangular points (L4, L5) have y \u2260 0.',
    styles['Body']))

S.append(Paragraph('2. Computing the Collinear Points (L1, L2, L3)', styles['H2']))
S.append(Paragraph(
    'For the collinear points, setting y = 0 reduces the equilibrium condition to a '
    'single equation along the x-axis. After non-dimensionalization (using the '
    'Earth\u2013Moon distance D = 384,400 km as the length unit), the equilibrium '
    'condition becomes a quintic polynomial in x:',
    styles['Body']))
S.append(Paragraph(
    f'\u03c9\u00b2x \u2212 GM{sub("E")}(x + d{sub("E")})/r{sub("E")}\u00b3 '
    f'\u2212 GM{sub("M")}(x \u2212 d{sub("M")})/r{sub("M")}\u00b3 = 0',
    styles['Formula']))
S.append(Paragraph(
    'This quintic equation (known as the <i>Euler quintic</i>) has three real roots, '
    'one in each interval: between Earth and Moon (L1), beyond the Moon (L2), and '
    'behind Earth opposite to the Moon (L3). In our implementation, these roots are found '
    'numerically using the <b>bisection method</b> (see Section 7).',
    styles['Body']))

S.append(Paragraph('2.1 L1 \u2014 Between Earth and Moon', styles['H3']))
S.append(Paragraph(
    'L1 lies on the Earth\u2013Moon line between the two bodies, at the point where the '
    'gravitational pull of the Moon partially cancels that of the Earth (combined with '
    'the centrifugal effect). In the Earth\u2013Moon system:',
    styles['Body']))
S.append(Paragraph(
    '<b>L1:</b> x \u2248 323,696 km from the barycenter (about 58,500 km from the Moon)',
    styles['Formula']))

S.append(Paragraph('2.2 L2 \u2014 Beyond the Moon', styles['H3']))
S.append(Paragraph(
    'L2 lies on the far side of the Moon, where the combined gravitational pull of Earth '
    'and Moon (both pulling in the same direction) balances the centrifugal force:',
    styles['Body']))
S.append(Paragraph(
    '<b>L2:</b> x \u2248 446,531 km from the barycenter (about 63,700 km beyond the Moon)',
    styles['Formula']))

S.append(Paragraph('2.3 L3 \u2014 Opposite Earth from Moon', styles['H3']))
S.append(Paragraph(
    'L3 lies on the opposite side of the Earth from the Moon, where the weak lunar '
    'gravity adds to the centrifugal force to balance the dominant Earth gravity:',
    styles['Body']))
S.append(Paragraph(
    '<b>L3:</b> x \u2248 \u2212386,651 km from the barycenter',
    styles['Formula']))

S.append(Paragraph('3. The Triangular Points (L4, L5)', styles['H2']))
S.append(Paragraph(
    'L4 and L5 are Lagrange\u2019s remarkable discovery: they form equilateral triangles '
    'with Earth and Moon. Unlike the collinear points, which require solving a quintic '
    'equation, the triangular points have an elegant analytical solution. They are located '
    'at the vertices of equilateral triangles with the two primaries:',
    styles['Body']))
S.append(Paragraph(
    '<b>L4:</b> (x, y) \u2248 (188,080, +332,920) km &nbsp;&nbsp; '
    '<b>L5:</b> (x, y) \u2248 (188,080, \u2212332,920) km',
    styles['Formula']))
S.append(Paragraph(
    'At these points, both r{sub("E")} and r{sub("M")} equal the Earth\u2013Moon distance D. '
    'The gravitational forces from the two bodies and the centrifugal force form a '
    'closed triangle of forces, producing exact equilibrium.'.replace(
        '{sub("E")}', '<sub>E</sub>').replace('{sub("M")}', '<sub>M</sub>'),
    styles['Body']))

S.append(Paragraph('4. Positions Summary', styles['H2']))

pos_data = [
    ['Point', 'x (km)', 'y (km)', 'Description'],
    ['L1', '323,696', '0', 'Between Earth and Moon'],
    ['L2', '446,531', '0', 'Beyond the Moon'],
    ['L3', '\u2212386,651', '0', 'Opposite side of Earth'],
    ['L4', '188,080', '+332,920', 'Leading equilateral point'],
    ['L5', '188,080', '\u2212332,920', 'Trailing equilateral point'],
]
t1 = Table(pos_data, colWidths=[18 * mm, 28 * mm, 28 * mm, 42 * mm])
t1.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#003366')),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#FFFFFF')),
    ('FONTNAME', (0, 0), (-1, -1), FONT),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (1, 0), (2, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#999999')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#F5F5F5'), HexColor('#FFFFFF')]),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
]))
S.append(t1)
S.append(Spacer(1, 3 * mm))

S.append(Paragraph('5. Stability Analysis', styles['H2']))

S.append(Paragraph('5.1 Collinear Points: Unstable (Saddle Points)', styles['H3']))
S.append(Paragraph(
    'Linearizing the equations of motion around L1, L2, or L3, the characteristic '
    'equation yields eigenvalues with both real and imaginary parts. The real eigenvalues '
    'come in \u00b1 pairs, meaning there is always one exponentially growing mode. This '
    'makes all three collinear points <b>linearly unstable</b> \u2014 they are saddle points '
    'in the effective potential.',
    styles['Body']))
S.append(Paragraph(
    'A spacecraft placed at L1 or L2 with zero velocity will drift away exponentially, '
    'with a characteristic time of about 10\u201315 days in the Earth\u2013Moon system. '
    'Station-keeping requires regular small thruster firings (~1 m/s per year for '
    'Sun\u2013Earth L2).',
    styles['Body']))

S.append(Paragraph('5.2 Triangular Points: Linearly Stable (Conditionally)', styles['H3']))
S.append(Paragraph(
    'The triangular points L4 and L5 are remarkable: despite being maxima of the '
    'effective potential, they are <b>linearly stable</b> for sufficiently small mass '
    'ratios. The Coriolis force provides a stabilizing effect that overcomes the '
    'repulsive character of the potential maximum.',
    styles['Body']))
S.append(Paragraph(
    'The stability condition is:',
    styles['Body']))
S.append(Paragraph(
    f'\u03bc &lt; \u03bc{sub("crit")} = (1 \u2212 \u221a(23/27))/2 \u2248 0.03852...',
    styles['Formula']))
S.append(Paragraph(
    f'where \u03bc = M{sub("M")}/(M{sub("E")} + M{sub("M")}) is the mass ratio. For the '
    f'Earth\u2013Moon system, \u03bc \u2248 0.01215, which satisfies \u03bc &lt; \u03bc{sub("crit")}. '
    f'Therefore, L4 and L5 are linearly stable in the Earth\u2013Moon CR3BP.',
    styles['Body']))
S.append(Paragraph(
    'In practice, solar gravitational perturbations destabilize the Earth\u2013Moon L4/L5, '
    'but in the Sun\u2013Jupiter system, thousands of Trojan asteroids orbit stably around '
    'L4 and L5.',
    styles['Body']))

S.append(Paragraph('6. Practical Applications', styles['H2']))

S.append(Paragraph('<b>L1 Applications:</b>', styles['Body']))
S.append(Paragraph(
    '<b>Sun\u2013Earth L1:</b> SOHO solar observatory (1996\u2013present), continuous solar '
    'monitoring with uninterrupted view of the Sun.',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '<b>Earth\u2013Moon L1:</b> proposed as a gateway station for lunar missions, enabling '
    'low-energy transfers to the lunar surface and serving as a staging point.',
    styles['BulletItem'], bulletText='\u2022'))

S.append(Paragraph('<b>L2 Applications:</b>', styles['Body']))
S.append(Paragraph(
    '<b>Sun\u2013Earth L2:</b> James Webb Space Telescope (JWST, 2022), Planck, Gaia, '
    'Euclid \u2014 ideal for deep-space astronomy with stable thermal environment and '
    'Sun/Earth/Moon all behind the sunshield.',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '<b>Earth\u2013Moon L2:</b> Queqiao relay satellite (2018) for Chang\u2019e 4 '
    'far-side lunar mission \u2014 maintains line of sight to both Earth and the lunar '
    'far side.',
    styles['BulletItem'], bulletText='\u2022'))

S.append(Paragraph('<b>L4/L5 Applications:</b>', styles['Body']))
S.append(Paragraph(
    '<b>Jupiter Trojans:</b> over 12,000 known asteroids trapped around Sun\u2013Jupiter '
    'L4 and L5, confirming long-term stability for \u03bc \u226a \u03bc{sub("crit")}.'.replace(
        '{sub("crit")}', '<sub>crit</sub>'),
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '<b>NASA Lucy mission</b> (2021\u2013): first spacecraft to visit Jupiter Trojan '
    'asteroids at L4 and L5.',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '<b>Proposed space habitats:</b> Earth\u2013Moon L4/L5 suggested by Gerard O\u2019Neill '
    '(1974) as locations for large space colonies.',
    styles['BulletItem'], bulletText='\u2022'))

S.append(Paragraph('7. Numerical Algorithms in lagrange.py', styles['H2']))
S.append(Paragraph(
    'This section describes the algorithms actually implemented in <font face="Courier">lagrange.py</font> '
    'and visualized step-by-step in <font face="Courier">lagrange_streamlit.py</font>.',
    styles['Body']))

S.append(Paragraph('7.1 Bisection Method (L1, L2, L3)', styles['H3']))
S.append(Paragraph(
    'For the collinear points, the equilibrium condition reduces to finding the root of a '
    'scalar function f(x) = a<sub>x</sub>(x, 0) \u2014 the x-component of the acceleration '
    'in the rotating frame for a stationary particle on the x-axis:',
    styles['Body']))
S.append(Paragraph(
    f'f(x) = \u03c9\u00b2x \u2212 GM{sub("E")}(x + d{sub("E")})/|x + d{sub("E")}|\u00b3 '
    f'\u2212 GM{sub("M")}(x \u2212 d{sub("M")})/|x \u2212 d{sub("M")}|\u00b3',
    styles['Formula']))
S.append(Paragraph(
    'The bisection method is applied on intervals where f changes sign. Starting with an '
    'interval [a, b] such that f(a)\u00b7f(b) &lt; 0, we repeatedly halve the interval:',
    styles['Body']))
S.append(Paragraph(
    '1. Compute midpoint m = (a + b)/2 and evaluate f(m).',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '2. If f(a)\u00b7f(m) &lt; 0, set b = m (root is in [a, m]); otherwise set a = m.',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '3. Repeat for 200 iterations, guaranteeing convergence to ~60 significant digits '
    '(each iteration halves the interval, so after n iterations the error is |b\u2212a|/2\u207f).',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    'The search intervals are chosen to bracket exactly one root each:',
    styles['Body']))

bisect_data = [
    ['Point', 'Interval [a, b]', 'Rationale'],
    ['L1', '(\u2212d_E + \u03b5,  d_M \u2212 \u03b5)', 'Between Earth and Moon (excluding singularities)'],
    ['L2', '(d_M + \u03b5,  1.5\u00b7d_M)', 'Beyond the Moon'],
    ['L3', '(\u22121.5\u00b7d_M,  \u2212d_E \u2212 \u03b5)', 'Opposite side from Moon'],
]
t_bisect = Table(bisect_data, colWidths=[18 * mm, 42 * mm, 55 * mm])
t_bisect.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#003366')),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#FFFFFF')),
    ('FONTNAME', (0, 0), (-1, -1), FONT),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (0, 0), (0, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#999999')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#F5F5F5'), HexColor('#FFFFFF')]),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
]))
S.append(t_bisect)
S.append(Spacer(1, 3 * mm))
S.append(Paragraph(
    'where \u03b5 = 10\u00b3 m is a small offset to avoid the gravitational singularities at the '
    'positions of Earth and Moon.',
    styles['Body']))

S.append(Paragraph('7.2 Newton\u2019s Method in 2D (L4, L5)', styles['H3']))
S.append(Paragraph(
    'For the triangular points, both a<sub>x</sub> and a<sub>y</sub> must vanish simultaneously. '
    'We solve this 2D system using Newton\u2019s method with a numerically approximated Jacobian. '
    'Starting from the analytical guess (the equilateral triangle vertex):',
    styles['Body']))
S.append(Paragraph(
    f'(x{sub("0")}, y{sub("0")}) = (D/2 \u2212 d{sub("E")},  \u00b1D\u00b7sin(60\u00b0))',
    styles['Formula']))
S.append(Paragraph(
    'At each iteration, we:',
    styles['Body']))
S.append(Paragraph(
    '1. Evaluate the acceleration vector <b>F</b>(x, y) = (a<sub>x</sub>, a<sub>y</sub>) at the current point.',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '2. Approximate the 2\u00d72 Jacobian <b>J</b> via forward finite differences with step h = 1 m:',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    f'J = [ (\u2202a{sub("x")}/\u2202x, \u2202a{sub("x")}/\u2202y) ; '
    f'(\u2202a{sub("y")}/\u2202x, \u2202a{sub("y")}/\u2202y) ] '
    f'\u2248 [ (a{sub("x")}(x+h,y)\u2212a{sub("x")})/h, ... ]',
    styles['Formula']))
S.append(Paragraph(
    '3. Solve the linear system <b>J</b>\u00b7\u03b4 = \u2212<b>F</b> using Cramer\u2019s rule '
    '(explicit 2\u00d72 inverse via determinant).',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '4. Update: (x, y) \u2190 (x, y) + \u03b4. Repeat until |<b>F</b>| &lt; 10\u207b\u00b9\u2075 m/s\u00b2.',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    'Convergence is typically achieved within 5\u20138 iterations due to the excellent initial guess '
    'and quadratic convergence of Newton\u2019s method.',
    styles['Body']))

S.append(Paragraph('8. Halo Orbit Computation', styles['H2']))

S.append(Paragraph('8.1 Richardson 3rd-Order Approximation', styles['H3']))
S.append(Paragraph(
    'To compute initial conditions for halo orbits near L1 or L2, we use the '
    '<b>Richardson third-order analytical approximation</b> [6]. This method expands the '
    'equations of motion about the Lagrange point using Legendre polynomial coefficients '
    'and produces a closed-form estimate of the periodic orbit.',
    styles['Body']))
S.append(Paragraph('The algorithm proceeds as follows:', styles['Body']))
S.append(Paragraph(
    '1. <b>Compute \u03b3</b> \u2014 the normalized distance from the Lagrange point to the Moon: '
    '\u03b3 = |L \u2212 d<sub>M</sub>| / (d<sub>E</sub> + d<sub>M</sub>).',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '2. <b>Legendre coefficients</b> c<sub>2</sub>, c<sub>3</sub>, c<sub>4</sub> are computed '
    'from \u03b3 and the mass ratio \u03bc. The formulas differ for L1 and L2 due to the '
    'different geometry (L1 is between Earth and Moon; L2 is beyond the Moon).',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '3. <b>In-plane frequency \u03bb</b> is found from the characteristic equation: '
    '\u03bb\u2074 + (2\u2212c<sub>2</sub>)\u03bb\u00b2 + (1\u2212c<sub>2</sub>)(1+2c<sub>2</sub>) = 0.',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '4. <b>Series coefficients</b> (a<sub>21</sub>, a<sub>22</sub>, \u2026, b<sub>31</sub>, '
    'b<sub>32</sub>, d<sub>21</sub>, d<sub>31</sub>, d<sub>32</sub>) are computed from '
    'c<sub>2</sub>\u2013c<sub>4</sub> and \u03bb using Richardson\u2019s formulae.',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '5. <b>Amplitude constraint</b>: given the desired out-of-plane amplitude A<sub>z</sub>, '
    'the in-plane amplitude A<sub>x</sub> is determined by the condition '
    'l<sub>1</sub>A<sub>x</sub>\u00b2 + l<sub>2</sub>A<sub>z</sub>\u00b2 + \u0394 = 0, '
    'which ensures the orbit is periodic (halo condition).',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '6. <b>Initial conditions</b>: at \u03c4 = 0 (xz-plane crossing), the position (x<sub>0</sub>, 0, z<sub>0</sub>) '
    'and velocity (0, vy<sub>0</sub>, 0) are computed from the truncated Lindstedt\u2013Poincar\u00e9 series '
    'and converted to dimensional units.',
    styles['BulletItem'], bulletText='\u2022'))

S.append(Paragraph('8.2 Differential Correction', styles['H3']))
S.append(Paragraph(
    'The Richardson approximation provides an estimate accurate to ~1%, which is insufficient '
    'for numerical integration over many orbital periods. The function '
    '<font face="Courier">correct_halo_ic</font> refines the initial conditions using a '
    '<b>shooting method with differential correction</b>.',
    styles['Body']))
S.append(Paragraph('The procedure is:', styles['Body']))
S.append(Paragraph(
    '1. Start from the Richardson estimate: state = (x<sub>0</sub>, 0, z<sub>0</sub>, 0, vy<sub>0</sub>, 0).',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '2. <b>Integrate</b> the full CR3BP equations of motion (using scipy\u2019s '
    '<font face="Courier">solve_ivp</font> with RK45, rtol=10\u207b\u00b9\u00b2) '
    'until the trajectory crosses the y = 0 plane again with y decreasing (half-period crossing).',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '3. At the crossing, measure the <b>residual</b>: (v<sub>x,f</sub>, v<sub>z,f</sub>). '
    'A perfect periodic orbit has v<sub>x</sub> = v<sub>z</sub> = 0 at this symmetry plane.',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '4. <b>Compute the 2\u00d72 Jacobian</b> \u2202(v<sub>x,f</sub>, v<sub>z,f</sub>)/\u2202(x<sub>0</sub>, vy<sub>0</sub>) '
    'via finite differences (\u03b5<sub>x</sub> = 1 m, \u03b5<sub>vy</sub> = 0.1 mm/s), '
    'requiring two additional integrations per iteration.',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '5. <b>Newton update</b>: solve J\u00b7[\u03b4x<sub>0</sub>, \u03b4vy<sub>0</sub>]<sup>T</sup> = '
    '\u2212[v<sub>x,f</sub>, v<sub>z,f</sub>]<sup>T</sup> and update x<sub>0</sub>, vy<sub>0</sub>.',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '6. Repeat until |residual| &lt; 10\u207b\u00b9\u2070 m/s (typically 3\u20135 iterations).',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    'The corrected initial conditions yield a numerically periodic halo orbit suitable for '
    'long-duration simulation in the main trajectory simulator.',
    styles['Body']))

S.append(Paragraph('9. Interactive Convergence Visualization', styles['H2']))
S.append(Paragraph(
    'The Streamlit application <font face="Courier">lagrange_streamlit.py</font> provides '
    'an interactive step-by-step visualization of the algorithms described above. '
    'A slider controls the iteration number, and the display updates in real time:',
    styles['Body']))
S.append(Paragraph(
    '<b>For L1, L2, L3 (bisection):</b> the system map shows the current interval [a, b] '
    'shrinking around the root; a plot of f(x) highlights the active interval and current midpoint; '
    'and a convergence chart tracks the midpoint value across iterations.',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '<b>For L4, L5 (Newton):</b> the map shows the 2D iteration path converging to the '
    'equilibrium point; the acceleration magnitude |a| is plotted on a log scale showing '
    'quadratic convergence; and a zoomed view shows the iteration path with numbered steps.',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    'Both modes include a full iteration table with numerical values at each step.',
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
        'Foundational reference for the CR3BP, including derivation of all five '
        'Lagrange points, the Euler quintic, and stability analysis.'
    ),
    (
        'Koon, W.S., Lo, M.W., Marsden, J.E., Ross, S.D. (2011). '
        '<i>Dynamical Systems, the Three-Body Problem and Space Mission Design.</i> '
        'Marsden Books. ISBN 978-0-615-24095-4.'
        '<br/>'
        'Modern treatment of Lagrange point dynamics, invariant manifolds, halo orbits, '
        'and their applications to mission design.'
    ),
    (
        'Murray, C.D. and Dermott, S.F. (1999). '
        '<i>Solar System Dynamics.</i> '
        'Cambridge University Press. ISBN 978-0-521-57295-8.'
        '<br/>'
        'Detailed derivation of the stability criterion for L4/L5 and discussion '
        'of Trojan asteroids as natural examples.'
    ),
    (
        'Farquhar, R.W. (1967). '
        '"Lunar Communications with Libration-Point Satellites." '
        '<i>Journal of Spacecraft and Rockets</i>, 4(10), 1383\u20131384.'
        '<br/>'
        'Early proposal for using Earth\u2013Moon L2 halo orbits as relay stations '
        'for far-side lunar communication.'
    ),
    (
        'Euler, L. (1767). '
        '"De motu rectilineo trium corporum se mutuo attrahentium." '
        '<i>Novi Commentarii Academiae Scientiarum Petropolitanae</i>, 11, 144\u2013151.'
        '<br/>'
        'Original discovery of the three collinear equilibrium points (L1, L2, L3).'
    ),
    (
        'Richardson, D.L. (1980). '
        '"Analytic Construction of Periodic Orbits About the Collinear Points." '
        '<i>Celestial Mechanics</i>, 22(3), 241\u2013253.'
        '<br/>'
        'Third-order Lindstedt\u2013Poincar\u00e9 approximation for halo orbits near L1 and L2, '
        'used in our implementation for initial condition generation.'
    ),
]

for i, ref in enumerate(refs, 1):
    S.append(Paragraph(f'[{i}] {ref}', styles['Ref']))

doc.build(S)
print(f'PDF generated: {OUTPUT}')
