"""
Генерация PDF-заметки: демонстрация хаоса вблизи точки L1.
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

OUTPUT = 'l1_chaos_note.pdf'
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
    'Chaos Demonstration Near the L1 Lagrange Point', styles['Title2']))
S.append(Paragraph('Technical Note \u2014 March 2026', styles['Subtitle']))
S.append(HRFlowable(width='100%', thickness=0.5, color=HexColor('#003366')))
S.append(Spacer(1, 4 * mm))

S.append(Paragraph('1. Concept', styles['H2']))
S.append(Paragraph(
    'This preset demonstrates the <i>chaotic sensitivity</i> of the CR3BP near the L1 '
    'Lagrange point. A test particle is placed exactly at L1 (the unstable equilibrium '
    'between Earth and Moon) with a tiny initial velocity of 50 m/s. Over the course of '
    '2,400 hours (~100 days), the particle wanders chaotically between the Earth and Moon '
    'regions, following an unpredictable and non-repeating path.',
    styles['Body']))
S.append(Paragraph(
    'The L1 point is a <i>saddle point</i> of the effective potential in the rotating '
    'frame. It is the gateway between the Earth and Moon gravitational domains. The '
    'slightest perturbation causes the particle to fall toward one body, only to be '
    'deflected back through the L1 neck toward the other \u2014 generating complex, '
    'chaotic dynamics.',
    styles['Body']))

S.append(Paragraph('2. Initial Conditions', styles['H2']))

ic_data = [
    ['Parameter', 'Value', 'Notes'],
    ['x\u2080', '323,696 km', 'At the L1 point'],
    ['y\u2080', '0', 'On the Earth\u2013Moon axis'],
    ['z\u2080', '0', 'Planar motion'],
    ['vx\u2080', '0.05 km/s', '50 m/s in x-direction'],
    ['vy\u2080', '0.05 km/s', '50 m/s in y-direction'],
    ['vz\u2080', '0', 'Planar motion'],
    ['|v\u2080|', '0.0707 km/s', '~70.7 m/s total (tiny!)'],
    ['t\u2082\u2099\u2084', '2,400 h', '100 days integration'],
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

S.append(Paragraph('3. L1 Instability: The Saddle Point', styles['H2']))
S.append(Paragraph(
    'The L1 Lagrange point is an unstable equilibrium \u2014 specifically, a saddle point '
    'of the effective potential (also called the Jacobi potential or pseudo-potential):',
    styles['Body']))
S.append(Paragraph(
    f'U{sub("eff")}(x, y) = \u2212\u00bd\u03c9\u00b2(x\u00b2 + y\u00b2) '
    f'\u2212 GM{sub("E")}/r{sub("E")} \u2212 GM{sub("M")}/r{sub("M")}',
    styles['Formula']))
S.append(Paragraph(
    'At L1, the potential is a local maximum along the x-axis (the Earth\u2013Moon line) '
    'and a local minimum in the perpendicular direction. This saddle geometry means:',
    styles['Body']))
S.append(Paragraph(
    '<b>Along x-axis:</b> any displacement grows exponentially. The particle accelerates '
    'toward Earth (if displaced Earthward) or toward Moon (if displaced Moonward).',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '<b>Perpendicular to x-axis:</b> the particle oscillates, but the Coriolis force '
    'couples the two directions, creating a complex spiral instability.',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Spacer(1, 2 * mm))
S.append(Paragraph(
    'Linearizing the equations of motion around L1, the eigenvalues of the state '
    f'transition matrix have the form \u00b1\u03bb (real) and \u00b1i\u03c9{sub("p")} '
    '(imaginary). The real eigenvalue \u03bb gives the exponential divergence rate. '
    f'For the Earth\u2013Moon L1, \u03bb \u2248 2.9 \u00d7 10{sup("\u22126")} s{sup("\u22121")}, '
    'corresponding to a characteristic divergence time of ~4 days.',
    styles['Body']))

S.append(Paragraph('4. Sensitivity to Initial Conditions', styles['H2']))
S.append(Paragraph(
    'The hallmark of chaos is <i>sensitive dependence on initial conditions</i>: '
    'infinitesimally small changes in the starting state lead to exponentially diverging '
    'trajectories. Near L1, this sensitivity is extreme.',
    styles['Body']))

S.append(Paragraph('4.1 Dramatic Example', styles['H3']))
S.append(Paragraph(
    'Consider two particles starting at L1 with nearly identical velocities:',
    styles['Body']))

sens_data = [
    ['Case', 'vy\u2080', 'Outcome'],
    ['A', '+0.01 km/s (+10 m/s)', 'Wanders to Moon-side orbit'],
    ['B', '\u22120.01 km/s (\u221210 m/s)', 'Wanders to Earth-side orbit'],
    ['\u0394vy', '0.02 km/s (20 m/s)', 'Opposite hemispheres!'],
]
t2 = Table(sens_data, colWidths=[18 * mm, 42 * mm, 50 * mm])
t2.setStyle(TableStyle([
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
S.append(t2)
S.append(Spacer(1, 3 * mm))

S.append(Paragraph(
    'A difference of just 20 m/s in the initial y-velocity \u2014 about the speed of a '
    'brisk bicycle ride \u2014 sends the two particles to completely different regions of '
    'the Earth\u2013Moon system. After 100 days, one orbits near the Moon while the other '
    'orbits near Earth. This is a vivid illustration of deterministic chaos: the equations '
    'are perfectly deterministic, yet the outcome is practically unpredictable.',
    styles['Body']))

S.append(Paragraph('4.2 Exponential Divergence', styles['H3']))
S.append(Paragraph(
    'If two trajectories start with separation \u03b4\u2080, the separation grows as:',
    styles['Body']))
S.append(Paragraph(
    '\u03b4(t) ~ \u03b4\u2080 \u00d7 e\u207b\u1d50\u1d43\u02e3 \u00b7 t',
    styles['Formula']))
S.append(Paragraph(
    'where \u03bb{sub("max")} is the largest Lyapunov exponent. Near L1 in the '
    'Earth\u2013Moon system, \u03bb{sub("max")} is on the order of the unstable eigenvalue '
    '(~3 \u00d7 10{sup("\u22126")} s{sup("\u22121")}), meaning separations double roughly '
    'every 2\u20133 days.'.replace(
        '{sub("max")}', '<sub>max</sub>').replace(
        '{sup("\u22126")}', '<sup>\u22126</sup>').replace(
        '{sup("\u22121")}', '<sup>\u22121</sup>'),
    styles['Body']))

S.append(Paragraph('5. Lyapunov Exponents', styles['H2']))
S.append(Paragraph(
    'The <i>Lyapunov exponent</i> quantifies the average rate of exponential divergence '
    'of nearby trajectories. For a dynamical system with state vector '
    f'<b>x</b> \u2208 \u211d{sup("n")}, the maximal Lyapunov exponent is defined as:',
    styles['Body']))
S.append(Paragraph(
    f'\u03bb{sub("max")} = lim(t\u2192\u221e) (1/t) ln(|\u03b4<b>x</b>(t)| / |\u03b4<b>x</b>(0)|)',
    styles['Formula']))
S.append(Paragraph(
    'A positive maximal Lyapunov exponent is the mathematical signature of chaos. For '
    'the CR3BP near L1:',
    styles['Body']))
S.append(Paragraph(
    f'\u03bb{sub("max")} &gt; 0: the system is chaotic (nearby orbits diverge exponentially)',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    'The Lyapunov time T{sub("L")} = 1/\u03bb{sub("max")} gives the timescale over '
    'which predictions break down. For Earth\u2013Moon L1, T{sub("L")} ~ 4 days, meaning '
    'trajectory predictions beyond ~2 weeks are unreliable without extremely precise '
    'initial conditions.'.replace('{sub("L")}', '<sub>L</sub>').replace(
        '{sub("max")}', '<sub>max</sub>'),
    styles['BulletItem'], bulletText='\u2022'))
S.append(Spacer(1, 2 * mm))

S.append(Paragraph(
    '6. The Three-Body Problem and Poincar\u00e9', styles['H2']))
S.append(Paragraph(
    'The chaotic behavior near L1 is a specific manifestation of the general chaos '
    'inherent in the three-body problem, first recognized by Henri Poincar\u00e9 in '
    'the 1890s. Poincar\u00e9 showed that the three-body problem is <i>non-integrable</i>: '
    'unlike the two-body problem (which has a complete analytical solution via Kepler\u2019s '
    'laws), no closed-form solution exists for three or more gravitating bodies.',
    styles['Body']))
S.append(Paragraph(
    'Key insights from Poincar\u00e9\u2019s work relevant to this demonstration:',
    styles['Body']))
S.append(Paragraph(
    '<b>Homoclinic tangles:</b> the stable and unstable manifolds of L1 intersect '
    'transversally, creating an infinitely complex web of trajectories that shuttle '
    'between Earth and Moon regions.',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '<b>Non-periodicity:</b> a generic orbit near L1 never exactly repeats. The '
    'trajectory fills a region of phase space ergodically rather than closing on itself.',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '<b>Deterministic unpredictability:</b> the equations of motion are completely '
    'deterministic (given exact initial conditions, the future is uniquely determined), '
    'yet in practice, finite measurement precision makes long-term prediction impossible.',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Spacer(1, 2 * mm))
S.append(Paragraph(
    'This demonstration near L1 is, in essence, a modern visualization of what '
    'Poincar\u00e9 discovered analytically over a century ago: the three-body problem is '
    'a paradigmatic example of deterministic chaos, and the region near the collinear '
    'Lagrange points is where this chaos is most clearly visible.',
    styles['Body']))

S.append(Paragraph('7. Practical Implications', styles['H2']))
S.append(Paragraph(
    'The chaos near L1 has both challenges and opportunities for space missions:',
    styles['Body']))
S.append(Paragraph(
    '<b>Station-keeping:</b> spacecraft at L1 (like SOHO at Sun\u2013Earth L1) require '
    'regular stationkeeping maneuvers (~1 m/s/year) because the instability causes '
    'exponential drift.',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '<b>Low-energy transfers:</b> the same unstable manifolds that cause chaos also '
    'provide low-energy pathways between Earth and Moon orbits. The Interplanetary '
    'Superhighway concept (Lo and Ross, 2001) exploits these manifolds for fuel-efficient '
    'trajectory design.',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '<b>Trajectory design:</b> the extreme sensitivity means that tiny thrust maneuvers '
    'near L1 can redirect a spacecraft to very different final destinations \u2014 a form of '
    'gravitational leverage.',
    styles['BulletItem'], bulletText='\u2022'))

S.append(Paragraph('References', styles['H2']))

styles.add(ParagraphStyle(
    'Ref', parent=styles['Normal'], fontSize=9, leading=12,
    leftIndent=10 * mm, firstLineIndent=-10 * mm, spaceAfter=2 * mm,
    fontName=FONT,
))

refs = [
    (
        'Poincar\u00e9, H. (1892\u20131899). '
        '<i>Les M\u00e9thodes Nouvelles de la M\u00e9canique C\u00e9leste.</i> '
        'Gauthier-Villars, Paris. 3 volumes.'
        '<br/>'
        'Foundational work establishing the non-integrability of the three-body problem '
        'and the existence of homoclinic tangles \u2014 the mathematical basis of chaos.'
    ),
    (
        'Szebehely, V. (1967). '
        '<i>Theory of Orbits: The Restricted Problem of Three Bodies.</i> '
        'Academic Press. ISBN 978-0-12-680650-9.'
        '<br/>'
        'Comprehensive treatment of the CR3BP including the stability analysis of '
        'Lagrange points and the saddle-point geometry of L1, L2, L3.'
    ),
    (
        'Koon, W.S., Lo, M.W., Marsden, J.E., Ross, S.D. (2011). '
        '<i>Dynamical Systems, the Three-Body Problem and Space Mission Design.</i> '
        'Marsden Books. ISBN 978-0-615-24095-4.'
        '<br/>'
        'Modern treatment of invariant manifolds near Lagrange points, homoclinic/'
        'heteroclinic connections, and their application to trajectory design.'
    ),
    (
        'Strogatz, S.H. (2015). '
        '<i>Nonlinear Dynamics and Chaos.</i> 2nd edition. '
        'Westview Press. ISBN 978-0-8133-4910-7.'
        '<br/>'
        'Accessible introduction to chaos theory, Lyapunov exponents, and sensitive '
        'dependence on initial conditions.'
    ),
    (
        'Lo, M.W. and Ross, S.D. (2001). '
        '"The Lunar L1 Gateway: Portal to the Stars and Beyond." '
        '<i>AIAA Space 2001 Conference</i>, AIAA-2001-4768.'
        '<br/>'
        'The Interplanetary Superhighway concept: exploiting chaotic dynamics near '
        'Lagrange points for low-energy space mission design.'
    ),
    (
        'Ott, E. (2002). '
        '<i>Chaos in Dynamical Systems.</i> 2nd edition. '
        'Cambridge University Press. ISBN 978-0-521-01084-9.'
        '<br/>'
        'Rigorous mathematical treatment of Lyapunov exponents, strange attractors, '
        'and chaos in Hamiltonian systems including celestial mechanics.'
    ),
]

for i, ref in enumerate(refs, 1):
    S.append(Paragraph(f'[{i}] {ref}', styles['Ref']))

doc.build(S)
print(f'PDF generated: {OUTPUT}')
