"""
Генерация PDF-заметки: круговые орбиты в CR3BP (околоземная и окололунная).
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

OUTPUT = 'orbits_note.pdf'
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
    'Circular Orbits in the Earth\u2013Moon CR3BP', styles['Title2']))
S.append(Paragraph('Technical Note \u2014 March 2026', styles['Subtitle']))
S.append(HRFlowable(width='100%', thickness=0.5, color=HexColor('#003366')))
S.append(Spacer(1, 4 * mm))

S.append(Paragraph('1. Overview', styles['H2']))
S.append(Paragraph(
    'The simulator provides two circular orbit presets that demonstrate the simplest '
    'periodic motions in the CR3BP rotating frame: an orbit around Earth '
    '(\u043e\u043a\u043e\u043b\u043e\u0437\u0435\u043c\u043d\u0430\u044f, '
    '<i>e_orbit</i>) and an orbit around the Moon '
    '(\u043e\u043a\u043e\u043b\u043e\u043b\u0443\u043d\u043d\u0430\u044f, '
    '<i>m_orbit</i>). These presets illustrate how Keplerian circular motion is modified '
    'by the rotating frame and the gravitational influence of the second body.',
    styles['Body']))
S.append(Paragraph(
    'In a two-body problem, a circular orbit requires v = \u221a(GM/r). In the CR3BP '
    'rotating frame, the velocity must be corrected for the frame rotation and the '
    'perturbation from the second body. For orbits close to one primary (the "restricted" '
    'regime), the correction is small and the orbit remains nearly circular.',
    styles['Body']))

S.append(Paragraph('2. Near-Earth Orbit (e_orbit)', styles['H2']))
S.append(Paragraph(
    'The near-Earth orbit preset places a spacecraft in a roughly circular orbit around '
    'Earth, far enough from the surface to be interesting in the CR3BP context but well '
    'inside the Earth\u2019s Hill sphere.',
    styles['Body']))

S.append(Paragraph('2.1 Initial Conditions', styles['H3']))

e_orbit_data = [
    ['Parameter', 'Value', 'Notes'],
    ['x\u2080', '45.33 \u00d7 10\u00b3 km', 'Distance from barycenter'],
    ['y\u2080', '0', 'Starting on x-axis'],
    ['vx\u2080', '0', 'No radial velocity'],
    ['vy\u2080', '2.823 km/s', 'Circular velocity (prograde)'],
    ['r from Earth', '~49,900 km', '~7.8 Earth radii'],
    ['t\u2082\u2099\u2084', '100 h', 'Integration time'],
]
t1 = Table(e_orbit_data, colWidths=[24 * mm, 38 * mm, 48 * mm])
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

S.append(Paragraph('2.2 Circular Velocity Derivation', styles['H3']))
S.append(Paragraph(
    'For a circular orbit of radius r around Earth in the inertial frame, the Keplerian '
    'circular velocity is:',
    styles['Body']))
S.append(Paragraph(
    f'v{sub("circ")} = \u221a(GM{sub("E")}/r)',
    styles['Formula']))
S.append(Paragraph(
    f'For r \u2248 49,900 km, v{sub("circ")} \u2248 2.826 km/s. In the rotating frame, the '
    f'velocity must be adjusted by subtracting the frame rotation velocity at that point: '
    f'v{sub("rot")} = \u03c9 \u00d7 |x| \u2248 2.662 \u00d7 10{sup("\u22126")} '
    f'\u00d7 45,330 km \u2248 0.121 km/s. The preset value vy\u2080 = 2.823 km/s is '
    f'close to v{sub("circ")} \u2212 v{sub("rot")} \u2248 2.705 km/s, with the difference '
    f'accounted for by the Moon\u2019s gravitational perturbation.',
    styles['Body']))

S.append(Paragraph('3. Near-Moon Orbit (m_orbit)', styles['H2']))
S.append(Paragraph(
    'The near-Moon orbit preset places a spacecraft in a roughly circular orbit around '
    'the Moon. Because the Moon\u2019s mass is much smaller than Earth\u2019s '
    f'(M{sub("M")}/M{sub("E")} \u2248 1/81.3), orbital velocities near the Moon are '
    'correspondingly lower.',
    styles['Body']))

S.append(Paragraph('3.1 Initial Conditions', styles['H3']))

m_orbit_data = [
    ['Parameter', 'Value', 'Notes'],
    ['x\u2080', '332.8 \u00d7 10\u00b3 km', 'Near Moon (at 382.8 tkm)'],
    ['y\u2080', '0', 'Starting on x-axis'],
    ['vx\u2080', '0', 'No radial velocity'],
    ['vy\u2080', '0.313 km/s', 'Circular velocity (prograde)'],
    ['r from Moon', '~50,000 km', '~28.8 Moon radii'],
    ['t\u2082\u2099\u2084', '400 h', 'Integration time'],
]
t2 = Table(m_orbit_data, colWidths=[24 * mm, 38 * mm, 48 * mm])
t2.setStyle(TableStyle([
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
S.append(t2)
S.append(Spacer(1, 3 * mm))

S.append(Paragraph('3.2 Lunar Circular Velocity', styles['H3']))
S.append(Paragraph(
    f'The Keplerian circular velocity at r \u2248 50,000 km from the Moon is:',
    styles['Body']))
S.append(Paragraph(
    f'v{sub("circ")} = \u221a(GM{sub("M")}/r) = '
    f'\u221a(4.905 \u00d7 10{sup("12")} / 50 \u00d7 10{sup("6")}) \u2248 0.313 km/s',
    styles['Formula']))
S.append(Paragraph(
    'This is much smaller than the Earth orbit velocity because of the Moon\u2019s low mass. '
    'The rotating frame correction at the Moon\u2019s distance is \u03c9 \u00d7 d{sub("M")} '
    '\u2248 1.02 km/s, but since the orbit is centered on the Moon (not the barycenter), '
    'the local correction nearly cancels.'.replace(
        '{sub("M")}', '<sub>M</sub>'),
    styles['Body']))

S.append(Paragraph('4. Coriolis Effects on Orbital Motion', styles['H2']))
S.append(Paragraph(
    'In the rotating frame, the Coriolis acceleration '
    f'<b>a{sub("Cor")}</b> = \u22122<b>\u03c9</b> \u00d7 <b>v</b> acts perpendicular to the '
    'velocity. For a circular orbit, the Coriolis force modifies the effective centripetal '
    'balance:',
    styles['Body']))
S.append(Paragraph(
    f'a{sub("Cor,x")} = +2\u03c9v{sub("y")}, &nbsp;&nbsp; '
    f'a{sub("Cor,y")} = \u22122\u03c9v{sub("x")}',
    styles['Formula']))
S.append(Paragraph(
    'For the near-Earth orbit (vy \u2248 2.8 km/s), the Coriolis acceleration is '
    f'~1.5 \u00d7 10{sup("\u22125")} m/s\u00b2, which is small compared to the gravitational '
    f'acceleration (~1.6 \u00d7 10{sup("\u22121")} m/s\u00b2) but causes slow precession of '
    'the orbital plane and orbit shape over many revolutions.',
    styles['Body']))
S.append(Paragraph(
    'For the near-Moon orbit, the Coriolis effect is relatively stronger because the '
    'gravitational acceleration is much weaker. This makes lunar orbits in the CR3BP '
    'deviate more noticeably from perfect circles, especially over long integration times.',
    styles['Body']))

S.append(Paragraph('5. Comparison of Orbital Periods', styles['H2']))

period_data = [
    ['Property', 'e_orbit (Earth)', 'm_orbit (Moon)'],
    ['Orbital radius', '~50,000 km', '~50,000 km'],
    ['Central body mass', '5.972 \u00d7 10\u00b2\u2074 kg', '7.342 \u00d7 10\u00b2\u00b2 kg'],
    ['Keplerian period', '~31.1 h', '~284 h'],
    ['v\u2080 (rotating frame)', '2.823 km/s', '0.313 km/s'],
    ['Orbits in t\u2082\u2099\u2084', '~3.2 orbits', '~1.4 orbits'],
    ['Stability', 'Very stable', 'Perturbed by Earth'],
]
t3 = Table(period_data, colWidths=[32 * mm, 38 * mm, 40 * mm])
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
    'The Keplerian period scales as T = 2\u03c0\u221a(r\u00b3/GM). At the same orbital '
    'radius of ~50,000 km, the lunar orbit period is \u221a(M{sub("E")}/M{sub("M")}) '
    '\u2248 9\u00d7 longer than the Earth orbit period because of the mass ratio.'.replace(
        '{sub("E")}', '<sub>E</sub>').replace('{sub("M")}', '<sub>M</sub>'),
    styles['Body']))

S.append(Paragraph(
    'The near-Earth orbit is highly stable over the integration window because the '
    'spacecraft is deep inside Earth\u2019s Hill sphere (radius ~60,000 km). The '
    'near-Moon orbit, while also inside the Moon\u2019s Hill sphere (~61,500 km), '
    'experiences stronger tidal perturbations from Earth and may show visible '
    'precession or shape distortion over many orbits.',
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
        'Classical reference for the CR3BP, including the rotating frame equations '
        'and pseudo-forces (Coriolis and centrifugal).'
    ),
    (
        'Koon, W.S., Lo, M.W., Marsden, J.E., Ross, S.D. (2011). '
        '<i>Dynamical Systems, the Three-Body Problem and Space Mission Design.</i> '
        'Marsden Books. ISBN 978-0-615-24095-4.'
        '<br/>'
        'Treatment of periodic orbits in the CR3BP, including nearly circular orbits '
        'around the primaries and their stability.'
    ),
    (
        'Battin, R.H. (1999). '
        '<i>An Introduction to the Mathematics and Methods of Astrodynamics.</i> '
        'Revised edition. AIAA Education Series. ISBN 978-1-56347-342-5.'
        '<br/>'
        'Comprehensive derivation of circular orbit velocities, period calculations, '
        'and perturbation theory for near-Keplerian orbits.'
    ),
    (
        'Roy, A.E. (2005). '
        '<i>Orbital Motion.</i> 4th edition. '
        'CRC Press. ISBN 978-0-7503-1015-3.'
        '<br/>'
        'Detailed treatment of Hill spheres, tidal perturbations on satellite orbits, '
        'and long-term orbital stability in multi-body systems.'
    ),
]

for i, ref in enumerate(refs, 1):
    S.append(Paragraph(f'[{i}] {ref}', styles['Ref']))

doc.build(S)
print(f'PDF generated: {OUTPUT}')
