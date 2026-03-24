"""
Генерация PDF-заметки: подход к нахождению гало-орбиты у L1.
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

OUTPUT = 'halo_orbit_note.pdf'
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
    'Finding L1 Halo Orbits in the Earth\u2013Moon CR3BP', styles['Title2']))
S.append(Paragraph('Technical Note \u2014 March 2026', styles['Subtitle']))
S.append(HRFlowable(width='100%', thickness=0.5, color=HexColor('#003366')))
S.append(Spacer(1, 4 * mm))

S.append(Paragraph('1. Problem Statement', styles['H2']))
S.append(Paragraph(
    'A <i>halo orbit</i> is a three-dimensional periodic orbit in the vicinity of a '
    'collinear Lagrange point (L1, L2, or L3) in the Circular Restricted Three-Body '
    'Problem (CR3BP). Unlike planar Lyapunov orbits, halo orbits have a significant '
    'out-of-plane (z) component, which arises from a 1:1 resonance between the in-plane '
    'and out-of-plane oscillation frequencies enabled by nonlinear dynamics.',
    styles['Body']))
S.append(Paragraph(
    f'The goal is to find initial conditions (x{sub("0")}, 0, z{sub("0")}, 0, '
    f'vy{sub("0")}, 0) \u2014 a state at the xz-plane crossing \u2014 that produce a '
    f'periodic orbit around the Earth\u2013Moon L1 point with a prescribed out-of-plane '
    f'amplitude A{sub("z")}.',
    styles['Body']))

S.append(Paragraph('2. Two-Stage Approach', styles['H2']))
S.append(Paragraph(
    'Finding exact halo orbit initial conditions is done in two stages:',
    styles['Body']))
S.append(Paragraph(
    "<b>Stage 1</b> \u2014 Richardson's 3rd-order analytical approximation provides an "
    'initial guess.', styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '<b>Stage 2</b> \u2014 Numerical differential correction refines the guess to machine '
    'precision.', styles['BulletItem'], bulletText='\u2022'))
S.append(Spacer(1, 2 * mm))
S.append(Paragraph(
    'Stage 1 alone is insufficient because halo orbits are <i>unstable</i>: the L1 '
    'equilibrium has a hyperbolic (real) eigenvalue, so even small errors in the initial '
    f'conditions grow exponentially. A 3rd-order approximation error of order '
    f'O(A{sup("4")}) causes the trajectory to depart from periodicity within one '
    'orbital period (~12 days).', styles['Body']))

S.append(Paragraph(
    "3. Stage 1 \u2014 Richardson's 3rd-Order Approximation", styles['H2']))

S.append(Paragraph('3.1 Setup and Notation', styles['H3']))
S.append(Paragraph(
    'We work in the CR3BP rotating frame with the barycenter at the origin. '
    f'The mass parameter is \u03bc = M{sub("Moon")} / (M{sub("Earth")} + M{sub("Moon")}) '
    f'\u2248 0.01215. '
    f'The Earth\u2013Moon distance L = d{sub("E")} + d{sub("M")} \u2248 3.875 \u00d7 '
    f'10{sup("8")} m serves as the characteristic length scale.',
    styles['Body']))
S.append(Paragraph(
    'The L1 point lies on the x-axis between Earth and Moon. Its distance from the Moon, '
    f'normalized by L, is \u03b3{sub("1")} \u2248 0.1525. This is found by bisection on '
    'the quintic equilibrium equation.',
    styles['Body']))

S.append(Paragraph('3.2 Legendre Coefficients', styles['H3']))
S.append(Paragraph(
    'The gravitational potential is expanded about L1 using Legendre polynomials. '
    f'The coefficients c{sub("n")} capture the local gravity gradient:',
    styles['Body']))
S.append(Paragraph(
    f'c{sub("n")} = \u03b3{sub("1")}{sup("\u22123")} \u00b7 '
    f'[ \u03bc + (\u22121){sup("n")} (1\u2212\u03bc) \u00b7 '
    f'\u03b3{sub("1")}{sup("n+1")} / (1\u2212\u03b3{sub("1")}){sup("n+1")} ]',
    styles['Formula']))
S.append(Paragraph(
    f'For the Earth\u2013Moon system: c{sub("2")} \u2248 5.045, '
    f'c{sub("3")} \u2248 3.130, c{sub("4")} \u2248 3.474.',
    styles['Body']))

S.append(Paragraph('3.3 Linearized Dynamics and Eigenvalues', styles['H3']))
S.append(Paragraph(
    'The linearized equations of motion near L1 in the local frame are:',
    styles['Body']))
S.append(Paragraph(
    f'x\u0308 \u2212 2y\u0307 \u2212 (1 + 2c{sub("2")})x = 0 '
    f'&nbsp;&nbsp;|&nbsp;&nbsp; '
    f'y\u0308 + 2x\u0307 + (c{sub("2")} \u2212 1)y = 0 '
    f'&nbsp;&nbsp;|&nbsp;&nbsp; '
    f'z\u0308 + c{sub("2")}\u00b7z = 0',
    styles['Formula']))
S.append(Paragraph(
    f'The in-plane characteristic equation '
    f's{sup("4")} + (2\u2212c{sub("2")})s\u00b2 + '
    f'(1\u2212c{sub("2")})(1+2c{sub("2")}) = 0 yields '
    'two pairs of eigenvalues: a real (unstable) pair s = \u00b12.897 and an imaginary '
    '(oscillatory) pair s = \u00b1i\u03bb with <b>\u03bb \u2248 2.312</b>. '
    'The out-of-plane motion has '
    f'frequency <b>\u03bd = \u221ac{sub("2")} \u2248 2.246</b>.',
    styles['Body']))
S.append(Paragraph(
    'Since \u03bb \u2260 \u03bd, the in-plane and out-of-plane oscillations have '
    'different periods. '
    'The Lindstedt\u2013Poincar\u00e9 perturbation method finds amplitude-dependent '
    'frequency corrections that bring them into 1:1 resonance \u2014 the '
    '<i>halo orbit condition</i>.',
    styles['Body']))

S.append(Paragraph('3.4 Perturbation Expansion', styles['H3']))
S.append(Paragraph(
    "Richardson's method expands the solution to 3rd order in the amplitudes "
    f'A{sub("x")} (in-plane) and A{sub("z")} (out-of-plane). The key outputs are:',
    styles['Body']))
S.append(Paragraph(
    f'<b>Amplitude ratio</b>: k = (\u03bb\u00b2 + 1 + 2c{sub("2")}) / (2\u03bb) '
    f'\u2248 3.554 \u2014 relates y-amplitude to x-amplitude in the linear solution.',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    f'<b>2nd-order coefficients</b>: a{sub("21")}, a{sub("22")}, a{sub("23")}, '
    f'a{sub("24")}, b{sub("21")}, b{sub("22")}, d{sub("21")} \u2014 '
    'correct the shape of the orbit (harmonics at 2\u03bb).',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    f'<b>3rd-order coefficients</b>: a{sub("31")}, a{sub("32")}, b{sub("31")}, '
    f'b{sub("32")}, d{sub("31")}, d{sub("32")} \u2014 '
    'further shape refinement (harmonics at 3\u03bb).',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    f'<b>Frequency corrections</b>: s{sub("1")}, s{sub("2")} \u2014 the actual orbital '
    f'frequency is \u03c9 = \u03bb(1 + s{sub("1")}A{sub("x")}\u00b2 + '
    f's{sub("2")}A{sub("z")}\u00b2).',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    f'<b>Halo constraint</b>: l{sub("1")}A{sub("x")}\u00b2 + '
    f'l{sub("2")}A{sub("z")}\u00b2 + \u0394 = 0 where '
    f'\u0394 = \u03bb\u00b2\u2212c{sub("2")}. Given A{sub("z")}, this determines '
    f'A{sub("x")}.',
    styles['BulletItem'], bulletText='\u2022'))

S.append(Spacer(1, 2 * mm))
S.append(Paragraph(
    f'For A{sub("z")} = 15,000 km, the method gives A{sub("x")} \u2248 3,211 km, '
    f'period T \u2248 283.7 h, and initial conditions (x{sub("0")}, z{sub("0")}, '
    f'vy{sub("0")}) in the simulator frame. '
    'However, as noted, these are only approximate.',
    styles['Body']))

S.append(Paragraph(
    '4. Why the Analytical Approximation Alone Fails', styles['H2']))
S.append(Paragraph(
    f'When the Richardson 3rd-order initial conditions (x{sub("0")} = 321.856 \u00d7 '
    f'10\u00b3 km, vy{sub("0")} = 0.066 km/s) are propagated in the simulator for one '
    'period (~284 hours), the resulting trajectory does <b>not</b> form a closed loop '
    'around L1. Instead, it makes a single large excursion extending far toward the Moon '
    'before looping back \u2014 resembling a transit orbit rather than a periodic halo '
    'orbit.',
    styles['Body']))
S.append(Paragraph(
    'This happens because of two compounding factors:',
    styles['Body']))
S.append(Paragraph(
    '<b>Truncation error</b>: The Richardson expansion is a 3rd-order perturbation '
    f'series in the amplitudes A{sub("x")} and A{sub("z")}. For our '
    f'A{sub("z")}/\u03b3{sub("1")}L \u2248 0.25 (not small), terms of order '
    f'A{sup("4")} and higher are '
    f'non-negligible. The velocity estimate vy{sub("0")} was off by 130% \u2014 '
    'a dramatic error despite the expansion being formally "3rd-order accurate".',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '<b>Dynamical instability</b>: The L1 point has a real (hyperbolic) eigenvalue '
    's \u2248 2.897 (in normalized units). Any deviation from the true periodic orbit '
    '\u2014 however small \u2014 excites the unstable manifold and grows exponentially as '
    f'e{sup("st")}. For the Earth\u2013Moon L1, the e-folding time is ~4 days, so after '
    'one orbital period (~12 days) the error amplifies by a factor of ~20.',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Spacer(1, 2 * mm))
S.append(Paragraph(
    'The combination is devastating: a modest analytical error feeds into exponential '
    'growth, causing the orbit to escape from L1 entirely. This is a general feature of '
    'libration-point orbits and is the reason that all real mission design workflows '
    'use numerical correction on top of analytical starting guesses.',
    styles['Body']))

S.append(Paragraph(
    '5. Stage 2 \u2014 Numerical Differential Correction', styles['H2']))

S.append(Paragraph('5.1 Periodicity Condition', styles['H3']))
S.append(Paragraph(
    'A halo orbit that crosses the xz-plane perpendicularly satisfies a symmetry: '
    f'at each xz-crossing, the state is (x, 0, z, 0, v{sub("y")}, 0) \u2014 i.e., '
    f'y = v{sub("x")} = v{sub("z")} = 0. '
    'If we start with such a state and integrate for one half-period until the next '
    f'y = 0 crossing, the orbit is periodic if and only if v{sub("x")} = 0 and '
    f'v{sub("z")} = 0 at that crossing.',
    styles['Body']))

S.append(Paragraph('5.2 Shooting Method', styles['H3']))
S.append(Paragraph(
    f'We fix z{sub("0")} (determined by the desired A{sub("z")}) and treat '
    f'x{sub("0")} and vy{sub("0")} as free variables. The algorithm iterates:',
    styles['Body']))
S.append(Paragraph(
    f'<b>1.</b> Integrate the full nonlinear CR3BP equations from '
    f'(x{sub("0")}, 0, z{sub("0")}, 0, vy{sub("0")}, 0) until the trajectory crosses '
    'y = 0 again (half-period T/2).',
    styles['BulletItem'], bulletText=' '))
S.append(Paragraph(
    f'<b>2.</b> Record the residual: (vx{sub("f")}, vz{sub("f")}) at the crossing.',
    styles['BulletItem'], bulletText=' '))
S.append(Paragraph(
    f'<b>3.</b> Compute the 2\u00d72 Jacobian '
    f'\u2202(vx{sub("f")}, vz{sub("f")}) / '
    f'\u2202(x{sub("0")}, vy{sub("0")}) via finite differences.',
    styles['BulletItem'], bulletText=' '))
S.append(Paragraph(
    f'<b>4.</b> Apply Newton\'s correction: '
    f'(\u03b4x{sub("0")}, \u03b4vy{sub("0")}) = '
    f'\u2212J{sup("\u22121")} \u00b7 (vx{sub("f")}, vz{sub("f")}).',
    styles['BulletItem'], bulletText=' '))
S.append(Paragraph(
    f'<b>5.</b> Repeat until |vx{sub("f")}| + |vz{sub("f")}| &lt; '
    f'10{sup("\u221210")} m/s.',
    styles['BulletItem'], bulletText=' '))

S.append(Spacer(1, 2 * mm))
S.append(Paragraph(
    f"The integration uses scipy's solve_ivp (RK45, adaptive step) with "
    f'rtol = 10{sup("\u221212")} '
    'and event detection for the y = 0 crossing. Each Newton iteration requires 3 '
    'integrations (nominal + 2 perturbed).', styles['Body']))

S.append(Paragraph('5.3 Convergence', styles['H3']))
S.append(Paragraph(
    'Starting from the Richardson initial guess, the method converges in '
    f'<b>8 iterations</b> to a residual of 1.8 \u00d7 10{sup("\u221211")} m/s. '
    'The corrections are significant:',
    styles['Body']))

table_data = [
    ['Parameter', 'Richardson (Stage 1)', 'Corrected (Stage 2)', '\u0394'],
    ['x\u2080 (10\u00b3 km)', '321.856', '318.188', '\u22123.668'],
    ['vy\u2080 (km/s)', '0.0660', '0.1528', '+0.0868'],
    ['T (hours)', '283.7', '293.4', '+9.7'],
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
    f'The large correction to vy{sub("0")} (+130%) explains why the Richardson-only '
    'trajectory escaped from L1 \u2014 it had insufficient tangential velocity for the '
    'true periodic orbit.',
    styles['Body']))

S.append(Paragraph('6. Final Result', styles['H2']))
S.append(Paragraph(
    f'The corrected initial conditions for an L1 halo orbit with A{sub("z")} = 15,000 km '
    f'in the Earth\u2013Moon rotating frame (barycenter at origin):', styles['Body']))

result_data = [
    ['x\u2080', '318.188 \u00d7 10\u00b3 km', '(~5,500 km sunward of L1)'],
    ['y\u2080', '0', '(xz-plane crossing)'],
    ['z\u2080', '15.228 \u00d7 10\u00b3 km', '(out-of-plane amplitude)'],
    ['vx\u2080', '0', '(perpendicular crossing)'],
    ['vy\u2080', '0.15284 km/s', '(152.8 m/s in +y direction)'],
    ['vz\u2080', '0', '(perpendicular crossing)'],
    ['Period', '293.4 hours', '(12.2 days)'],
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
    'When propagated numerically for one full period (293.4 h), the trajectory forms a '
    'closed 3D loop around L1 with visible z-excursion \u2014 a classic halo orbit shape.',
    styles['Body']))

S.append(Paragraph('7. Key Takeaway', styles['H2']))
S.append(Paragraph(
    'Analytical approximations (Richardson) are indispensable for providing a starting '
    'point, but <b>numerical differential correction is essential</b> for finding actual '
    'periodic orbits near libration points. The instability of L1 amplifies any '
    'approximation error exponentially \u2014 an orbit computed from the 3rd-order expansion '
    'alone will visibly depart from periodicity within a single revolution. The two-stage '
    'approach (analytical guess + numerical refinement) is the standard method used in '
    'mission design for SOHO, JWST, Artemis Gateway, and other libration-point missions.',
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
        'The original 3rd-order analytical approximation for halo orbits used in Stage 1. '
        'Derives all Lindstedt\u2013Poincar\u00e9 coefficients and the amplitude constraint.'
    ),
    (
        'Howell, K.C. (1984). '
        '"Three-Dimensional, Periodic, \u2018Halo\u2019 Orbits." '
        '<i>Celestial Mechanics</i>, 32(1), 53\u201371. '
        'doi:10.1007/BF01358403'
        '<br/>'
        'Systematic numerical computation of halo orbit families using differential '
        'correction (the shooting method used in Stage 2). Includes convergence analysis '
        'and orbit family continuation.'
    ),
    (
        'Koon, W.S., Lo, M.W., Marsden, J.E., Ross, S.D. (2011). '
        '<i>Dynamical Systems, the Three-Body Problem and Space Mission Design.</i> '
        'Marsden Books. '
        'ISBN 978-0-615-24095-4. '
        'Freely available at https://www.dept.aoe.vt.edu/~sdross/books/'
        '<br/>'
        'Comprehensive textbook covering CR3BP dynamics, Lagrange point geometry, '
        'Legendre coefficient derivations (Ch. 2\u20133), and halo orbit computation (Ch. 6). '
        'Primary source for the c<sub>n</sub> formula and eigenvalue analysis.'
    ),
    (
        'Thurman, R. and Worfolk, P.A. (1996). '
        '"The Geometry of Halo Orbits in the Circular Restricted Three-Body Problem." '
        '<i>University of Minnesota Geometry Center Research Report</i>, GCG95.'
        '<br/>'
        'Clear presentation of Richardson\u2019s coefficients with explicit formulas for all '
        '2nd- and 3rd-order terms. Useful companion to the original Richardson paper.'
    ),
    (
        'Farquhar, R.W. and Kamel, A.A. (1973). '
        '"Quasi-Periodic Orbits about the Translunar Libration Point." '
        '<i>Celestial Mechanics</i>, 7(4), 458\u2013473. '
        'doi:10.1007/BF01227511'
        '<br/>'
        'Early work on halo orbits in the Earth\u2013Moon system, establishing the physical '
        'basis for 3D periodic orbits near L1/L2. Proposed the ISEE-3 halo orbit mission.'
    ),
    (
        'Szebehely, V. (1967). '
        '<i>Theory of Orbits: The Restricted Problem of Three Bodies.</i> '
        'Academic Press. ISBN 978-0-12-680650-9.'
        '<br/>'
        'Classical reference for the CR3BP formulation, Lagrange points, Jacobi integral, '
        'and stability analysis. Source for the physical constants and rotating-frame '
        'equations of motion used throughout.'
    ),
]

for i, ref in enumerate(refs, 1):
    S.append(Paragraph(f'[{i}] {ref}', styles['Ref']))

doc.build(S)
print(f'PDF generated: {OUTPUT}')
