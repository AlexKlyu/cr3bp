"""
Генерация PDF-справочника: полное описание всех пресетов CR3BP симулятора.
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
    PageBreak,
)

pdfmetrics.registerFont(TTFont('ArialUni', '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'))

OUTPUT = 'presets_summary.pdf'
FONT = 'ArialUni'

doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    leftMargin=25 * mm, rightMargin=25 * mm,
    topMargin=20 * mm, bottomMargin=20 * mm,
)

styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    'Title2', parent=styles['Title'], fontSize=20, spaceAfter=4 * mm,
    textColor=HexColor('#003366'), fontName=FONT,
))
styles.add(ParagraphStyle(
    'Subtitle', parent=styles['Normal'], fontSize=11, alignment=TA_CENTER,
    textColor=HexColor('#666666'), spaceAfter=8 * mm, fontName=FONT,
))
styles.add(ParagraphStyle(
    'H1', parent=styles['Heading1'], fontSize=16,
    textColor=HexColor('#003366'), spaceBefore=8 * mm, spaceAfter=4 * mm,
    fontName=FONT,
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
    'BodySmall', parent=styles['Normal'], fontSize=9, leading=12,
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
styles.add(ParagraphStyle(
    'Note', parent=styles['Normal'], fontSize=9, leading=12,
    leftIndent=8 * mm, rightIndent=8 * mm, spaceAfter=3 * mm,
    textColor=HexColor('#555555'), fontName=FONT,
    borderWidth=0.5, borderColor=HexColor('#cccccc'), borderPadding=4,
))


BLUE = HexColor('#003366')
GREY = HexColor('#999999')
LIGHT = HexColor('#F5F5F5')
WHITE = HexColor('#FFFFFF')


def make_table(data, col_widths):
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, -1), FONT),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, GREY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [LIGHT, WHITE]),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    return t


S = []

S.append(Paragraph(
    'CR3BP Simulator \u2014 Preset Reference Guide', styles['Title2']))
S.append(Paragraph(
    'Earth\u2013Moon Circular Restricted Three-Body Problem<br/>Complete description of all built-in scenarios',
    styles['Subtitle']))
S.append(HRFlowable(width='100%', thickness=0.5, color=BLUE))
S.append(Spacer(1, 4 * mm))

S.append(Paragraph('Overview', styles['H1']))
S.append(Paragraph(
    'The simulator includes 14 built-in presets organized in four categories:',
    styles['Body']))

overview_data = [
    ['Category', 'Presets', 'Thrust', 'Key Feature'],
    ['Lagrange Points', 'L1, L2, L3, L4, L5', 'No', 'Equilibrium positions'],
    ['Orbits', 'Earth orbit, Moon orbit', 'No', 'Stable circular orbits'],
    ['Halo Orbits', 'L1 Halo, L2 Halo (JWST)', 'No', '3D periodic orbits'],
    ['Lunar Transfers', 'Apollo-13, Direct, Thrust correction', 'No/5 N', 'Earth\u2192Moon trajectories'],
    ['TLI from Orbit', 'Orbit\u2192Moon (TLI)', '15.5 kN', 'Full transfer from orbit'],
    ['L1 Dynamics', 'L1 Escape, L1 Chaos', '0.01 N / No', 'Instability demonstrations'],
]
S.append(make_table(overview_data, [28 * mm, 42 * mm, 16 * mm, 42 * mm]))
S.append(Spacer(1, 4 * mm))

S.append(Paragraph(
    'All presets use a 500 kg spacecraft in the Earth\u2013Moon CR3BP rotating frame. '
    'Coordinates are in thousands of km (tkm), velocities in km/s, forces in Newtons. '
    'The barycenter is at the origin; Earth is at x = \u22124.67 tkm, Moon at x = 382.8 tkm.',
    styles['Body']))

S.append(PageBreak())
S.append(Paragraph('1. Lagrange Points (L1\u2013L5)', styles['H1']))

S.append(Paragraph(
    'The five Lagrange points are equilibrium positions in the rotating frame where '
    'gravitational and centrifugal forces balance. A spacecraft placed at rest at any of these '
    'points will (ideally) remain stationary.',
    styles['Body']))

lagrange_data = [
    ['Preset', 'x\u2080 (tkm)', 'y\u2080 (tkm)', 'Location', 'Stability'],
    ['L1', '323.696', '0', 'Between Earth and Moon', 'Unstable'],
    ['L2', '446.531', '0', 'Beyond Moon (far side)', 'Unstable'],
    ['L3', '\u2212386.651', '0', 'Opposite side of Earth from Moon', 'Unstable'],
    ['L4', '188.081', '332.925', '60\u00b0 ahead of Moon', 'Stable'],
    ['L5', '188.081', '\u2212332.925', '60\u00b0 behind Moon', 'Stable'],
]
S.append(make_table(lagrange_data, [14 * mm, 22 * mm, 24 * mm, 40 * mm, 20 * mm]))
S.append(Spacer(1, 3 * mm))

S.append(Paragraph(
    'All Lagrange point presets have zero velocity and zero thrust, with t<sub>End</sub> = 2400 h (100 days).',
    styles['Body']))

S.append(Paragraph('Collinear points (L1, L2, L3)', styles['H3']))
S.append(Paragraph(
    'These lie on the Earth\u2013Moon line and are <b>unstable</b>: any perturbation (even numerical '
    'round-off) will cause the spacecraft to drift away exponentially. In the simulator, L1 and L2 '
    'will show visible departure within hours to days; L3 is more weakly unstable. '
    'The instability time scale at L1 is \u03c4 \u2248 2.2 days (e-folding time).',
    styles['Body']))
S.append(Paragraph(
    'Real missions at L1/L2 (SOHO, JWST) require periodic station-keeping burns to counteract '
    'this instability \u2014 see the "L1 Escape" preset for a demonstration.',
    styles['Body']))

S.append(Paragraph('Triangular points (L4, L5)', styles['H3']))
S.append(Paragraph(
    'These form equilateral triangles with Earth and Moon and are <b>linearly stable</b> in the '
    'Earth\u2013Moon system (because the mass ratio \u03bc \u2248 0.012 is below the Routh critical value '
    'of ~0.0385). A spacecraft placed at L4 or L5 will oscillate around the point in tadpole-shaped '
    'libration orbits rather than departing. In nature, these are locations where Trojan asteroids '
    'or dust clouds could accumulate.',
    styles['Body']))

S.append(Paragraph('2. Circular Orbits', styles['H1']))

orbit_data = [
    ['Preset', 'x\u2080 (tkm)', 'v<sub>y0</sub> (km/s)', 'Orbit radius', 'Body'],
    ['\u041e\u043a\u043e\u043b\u043e\u0437\u0435\u043c\u043d\u0430\u044f \u043e\u0440\u0431\u0438\u0442\u0430',
     '45.33', '2.823', '50,000 km from Earth', 'Earth'],
    ['\u041e\u043a\u043e\u043b\u043e\u043b\u0443\u043d\u043d\u0430\u044f \u043e\u0440\u0431\u0438\u0442\u0430',
     '332.80', '0.313', '50,000 km from Moon', 'Moon'],
]
S.append(make_table(orbit_data, [30 * mm, 20 * mm, 24 * mm, 32 * mm, 18 * mm]))
S.append(Spacer(1, 3 * mm))

S.append(Paragraph(
    'Both orbits are circular, prograde, and lie in the xy-plane. The orbital velocity is computed '
    'from v = \u221a(GM/r), where r is the distance from the parent body\u2019s center. These are '
    '<b>not exact</b> circular orbits in the CR3BP (because the third body perturbs them), '
    'so over long simulation times the orbit will precess and distort slightly.',
    styles['Body']))

S.append(Paragraph(
    '<b>Earth orbit</b>: At 50,000 km from Earth center (43,629 km altitude), this is well above '
    'GEO (35,786 km) but below the Moon\u2019s distance. The orbital period is approximately '
    '2\u03c0r/v \u2248 111,300 s \u2248 31 hours. This orbit also serves as the starting point for '
    'the TLI preset.',
    styles['Body']))

S.append(Paragraph(
    '<b>Moon orbit</b>: At 50,000 km from the Moon\u2019s center (48,263 km altitude). This is a '
    'high lunar orbit; for comparison, the Apollo command modules orbited at ~110 km altitude. '
    'The much larger radius here ensures the orbit is clearly visible in the simulator\u2019s scale.',
    styles['Body']))

S.append(Paragraph('3. Halo Orbits', styles['H1']))

halo_data = [
    ['Preset', 'x\u2080 (tkm)', 'z\u2080 (tkm)', 'v<sub>y0</sub> (km/s)', 'Period', 'Near'],
    ['Гало L1', '318.188', '15.228', '0.153', '~293 h (12.2 d)', 'L1'],
    ['Орбита L2 (JWST)', '426.963', '17.601', '0.227', '~347 h (14.5 d)', 'L2'],
]
S.append(make_table(halo_data, [28 * mm, 20 * mm, 18 * mm, 22 * mm, 26 * mm, 12 * mm]))
S.append(Spacer(1, 3 * mm))

S.append(Paragraph(
    'Halo orbits are <b>three-dimensional periodic orbits</b> around the collinear Lagrange points. '
    'Unlike simple planar orbits, they have a significant out-of-plane (z) component. They were '
    'discovered by R.W. Farquhar in 1968 and are of great practical importance.',
    styles['Body']))

S.append(Paragraph(
    '<b>L1 Halo</b>: A periodic orbit near L1 with z-amplitude of ~15,200 km. The t<sub>End</sub> '
    'is set to one orbital period (293 h) so the trajectory closes on itself. Such orbits are used '
    'by solar observation missions (SOHO, DSCOVR).',
    styles['Body']))

S.append(Paragraph(
    '<b>L2 Halo (JWST)</b>: Modeled after the James Webb Space Telescope\u2019s orbit around the '
    'Sun\u2013Earth L2 point (here adapted to Earth\u2013Moon L2). JWST orbits L2 in a halo orbit '
    'with z-amplitude ~17,600 km to maintain continuous communication with Earth while staying '
    'in the shadow. Period is ~347 h (14.5 days).',
    styles['Body']))

S.append(Paragraph(
    '<i>Note</i>: These initial conditions were found via differential correction (numerical '
    'shooting) to close the orbit. They are sensitive to the integration method and timestep. '
    'Small deviations will cause the orbit to slowly diverge, which is expected since halo orbits '
    'near L1/L2 are unstable.',
    styles['Note']))

S.append(PageBreak())
S.append(Paragraph('4. Lunar Transfer Trajectories', styles['H1']))

S.append(Paragraph(
    'Three presets demonstrate different approaches to Earth\u2192Moon transfer. They form a '
    'progression from purely ballistic to fully thrust-driven:',
    styles['Body']))

comp_data = [
    ['', 'Apollo-13\nFree Return', 'Direct Transfer\n(Hohmann)', 'Thrust Correction\n(5 N)'],
    ['|v\u2080|', '10.78 km/s', '10.78 km/s', '10.71 km/s (99.3%)'],
    ['Thrust', 'None', 'None', '5 N for 3 h'],
    ['\u0394v from engine', '0', '0', '108 m/s'],
    ['Fuel', '0', '0', '18 kg (3.6%)'],
    ['Transfer time', '~166 h (7 d)', '~58 h (2.4 d)', '~72 h (3 d)'],
    ['Outcome', 'Loops Moon,\nreturns to Earth', 'Arrives at Moon\n(no return)', 'Arrives at Moon\n(with thrust)'],
    ['Departure', '(\u22129.46, \u22124.78)', '(\u22129.46, \u22124.78)', '(\u22129.33, \u22124.91)'],
]
t_comp = Table(comp_data, colWidths=[24 * mm, 36 * mm, 36 * mm, 36 * mm])
t_comp.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('BACKGROUND', (0, 1), (0, -1), HexColor('#E8EEF4')),
    ('FONTNAME', (0, 0), (-1, -1), FONT),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('GRID', (0, 0), (-1, -1), 0.5, GREY),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [LIGHT, WHITE]),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
]))
S.append(t_comp)
S.append(Spacer(1, 3 * mm))

S.append(Paragraph('4.1 Apollo-13 Free Return', styles['H2']))
S.append(Paragraph(
    'A ballistic (no thrust) trajectory that departs Earth, swings around the Moon, and returns '
    'to Earth \u2014 the classic free-return trajectory. Named after Apollo 13, which used this '
    'trajectory type after the oxygen tank explosion forced an abort. The spacecraft loops behind '
    'the Moon and uses lunar gravity to slingshot back toward Earth.',
    styles['Body']))
S.append(Paragraph(
    'The simulation runs for 166 hours (~7 days) to show the complete outbound and return legs. '
    'The initial velocity of ~10.78 km/s is precisely tuned so that the trajectory is closed \u2014 '
    'the spacecraft returns to Earth\u2019s vicinity without any course corrections.',
    styles['Body']))

S.append(Paragraph('4.2 Direct Transfer (\u041f\u0440\u044f\u043c\u043e\u0439 \u043f\u0435\u0440\u0435\u043b\u0451\u0442)', styles['H2']))
S.append(Paragraph(
    'A ballistic trajectory from nearly the same departure point as Apollo-13, but with a '
    'slightly different velocity vector that sends the spacecraft directly to the Moon without '
    'a return path. Transfer time is ~58 hours (2.4 days) \u2014 faster than the free-return '
    'because the trajectory is more direct.',
    styles['Body']))
S.append(Paragraph(
    '<b>Key difference from Apollo-13</b>: The velocity direction is adjusted '
    '(v<sub>x0</sub> = 7.626, v<sub>y0</sub> = \u22127.643 vs Apollo\u2019s 7.708, \u22127.536) '
    'so the spacecraft aims directly at the Moon rather than looping around it. The speed is '
    'nearly identical (~10.78 km/s), but the trajectory geometry is fundamentally different.',
    styles['Body']))

S.append(Paragraph('4.3 Thrust Correction (\u0417\u0435\u043c\u043b\u044f\u2192\u041b\u0443\u043d\u0430 \u0441 \u0442\u044f\u0433\u043e\u0439)', styles['H2']))
S.append(Paragraph(
    'Starts from the Apollo-13 departure position but with only 99.3% of the required velocity '
    '(10.71 km/s instead of 10.78). Without thrust, this spacecraft would fall back to Earth \u2014 '
    'it lacks the energy to reach the Moon. A gentle 5 N thruster firing for 3 hours provides '
    'the missing \u0394v \u2248 108 m/s, pushing the trajectory onto a trans-lunar path.',
    styles['Body']))
S.append(Paragraph(
    '<b>Key insight</b>: This demonstrates the <i>sensitivity</i> of orbital mechanics. '
    'A 0.7% velocity difference (108 m/s out of 10,710) is the difference between reaching the '
    'Moon and falling back to Earth. The 18 kg of fuel (3.6% of spacecraft mass) is negligible, '
    'but the trajectory change is dramatic. This is a trajectory correction scenario, '
    'not a full transfer \u2014 the engine provides a tiny "nudge" rather than the main propulsion.',
    styles['Body']))

S.append(Paragraph('5. Trans-Lunar Injection from Orbit (TLI)', styles['H1']))

S.append(Paragraph(
    'This is the most physically realistic transfer preset. Unlike the three presets above '
    '(which all start near escape velocity ~10.7 km/s), this scenario starts from a '
    '<b>natural circular orbit</b> with only the orbital velocity of 2.823 km/s. '
    'The engine must provide the entire delta-v needed to escape Earth and reach the Moon.',
    styles['Body']))

tli_data = [
    ['Parameter', 'Value', 'Notes'],
    ['x\u2080', '\u22124.67 tkm', '50,000 km orbit, 270\u00b0 position (below Earth)'],
    ['y\u2080', '\u221250.0 tkm', 'On the Earth-centered circle'],
    ['v<sub>x0</sub>', '2.823 km/s', 'Circular orbit velocity (prograde \u2192 +x here)'],
    ['v<sub>y0</sub>', '0', 'No excess velocity'],
    ['F<sub>x</sub>', '15,300 N', 'Main engine (+x toward Moon)'],
    ['F<sub>y</sub>', '2,600 N', 'Targeting component'],
    ['|F|', '15,519 N (15.5 kN)', 'Total thrust (~3.2 g acceleration)'],
    ['Burn', '120 s (2 min)', 'Short impulsive burn'],
    ['\u0394v', '3,725 m/s', 'Full TLI delta-v'],
    ['Fuel (Isp=300s)', '359 kg (72%)', 'Bipropellant chemical'],
    ['Fuel (Isp=450s)', '285 kg (57%)', 'LH\u2082/LOX (like Apollo S-IVB)'],
    ['t<sub>End</sub>', '19 h', 'Reaches Moon vicinity'],
    ['dt', '5 s (adaptive)', 'Required: dt<sub>min</sub> = 1 s'],
]
S.append(make_table(tli_data, [26 * mm, 32 * mm, 56 * mm]))
S.append(Spacer(1, 3 * mm))

S.append(Paragraph('5.1 Why Adaptive Timestepping is Required', styles['H3']))
S.append(Paragraph(
    'The 120-second burn at 15.5 kN produces ~31 m/s\u00b2 acceleration (3.2 g). With the default '
    'dt = 30 s timestep, the entire burn occupies only 4 integration steps \u2014 far too coarse '
    'to accurately capture the trajectory during the high-thrust phase. The preset sets '
    'dt = 5 s with adaptive stepping (dt<sub>min</sub> = 1 s), giving ~24+ steps during the burn. '
    'Without adaptive stepping, the trajectory misses the Moon entirely.',
    styles['Body']))

S.append(Paragraph('5.2 Comparison with the Correction Preset', styles['H3']))

comp2_data = [
    ['', 'Thrust Correction (5 N)', 'TLI from Orbit (15.5 kN)'],
    ['Starting velocity', '10.71 km/s (99.3% escape)', '2.82 km/s (circular orbit)'],
    ['Engine role', 'Tiny correction (1% of v)', 'Full propulsion (132% of v)'],
    ['Thrust', '5 N for 3 hours', '15,500 N for 2 minutes'],
    ['\u0394v', '108 m/s', '3,725 m/s'],
    ['Fuel (Isp=300s)', '18 kg (3.6%)', '359 kg (72%)'],
    ['Demonstrates', 'Trajectory sensitivity', 'Realistic TLI maneuver'],
    ['Real-world analog', 'Course correction burn', 'Apollo S-IVB TLI burn'],
]
t_comp2 = Table(comp2_data, colWidths=[28 * mm, 46 * mm, 46 * mm])
t_comp2.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('BACKGROUND', (0, 1), (0, -1), HexColor('#E8EEF4')),
    ('FONTNAME', (0, 0), (-1, -1), FONT),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('GRID', (0, 0), (-1, -1), 0.5, GREY),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [LIGHT, WHITE]),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
]))
S.append(t_comp2)
S.append(Spacer(1, 3 * mm))

S.append(Paragraph(
    '<b>Why does TLI need 3,725 m/s when escape velocity minus orbit velocity is only 1,170 m/s?</b> '
    'The thrust is constant in the rotating frame, but the optimal burn direction changes as the '
    'spacecraft moves. The F<sub>y</sub> = 2,600 N component is needed for Moon targeting, adding '
    'to the total \u0394v. A real mission would optimize the burn direction (or use multiple shorter '
    'burns at perigee) to reduce \u0394v, but the simulator\u2019s single constant-direction thrust '
    'window is less efficient.',
    styles['Body']))

S.append(Paragraph(
    '<b>Simulator limitation</b>: Only one thrust window is supported, so the preset cannot model '
    'the Lunar Orbit Insertion (LOI) braking burn. The simulation ends at t = 19 h as the '
    'spacecraft approaches the Moon. In a real mission, a second burn (~800 m/s) would slow the '
    'spacecraft into lunar orbit.',
    styles['Note']))

S.append(Paragraph('6. L1 Dynamics: Escape and Chaos', styles['H1']))

S.append(Paragraph(
    'Two presets explore the rich dynamics near the unstable L1 Lagrange point.',
    styles['Body']))

l1_data = [
    ['', 'L1 Escape', 'L1 Chaos'],
    ['Start position', 'L1 (323.696 tkm)', 'L1 (323.696 tkm)'],
    ['Start velocity', '0 (at rest)', '0.05, 0.05 km/s (small kick)'],
    ['Thrust', '0.01 N for 30 s', 'None'],
    ['\u0394v', '0.0006 m/s', '0 (ballistic)'],
    ['Mechanism', 'Micro-thrust seeds instability', 'Initial velocity seeds instability'],
    ['t<sub>End</sub>', '500 h', '2400 h'],
    ['Result', 'Departs L1 along manifold', 'Complex chaotic trajectory'],
]
t_l1 = Table(l1_data, colWidths=[24 * mm, 48 * mm, 48 * mm])
t_l1.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('BACKGROUND', (0, 1), (0, -1), HexColor('#E8EEF4')),
    ('FONTNAME', (0, 0), (-1, -1), FONT),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('GRID', (0, 0), (-1, -1), 0.5, GREY),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [LIGHT, WHITE]),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
]))
S.append(t_l1)
S.append(Spacer(1, 3 * mm))

S.append(Paragraph('6.1 L1 Escape with Micro-Thrust', styles['H2']))
S.append(Paragraph(
    'Starting exactly at L1 with zero velocity, a nearly imperceptible thrust of 0.01 N fires '
    'for just 30 seconds, imparting \u0394v \u2248 0.6 mm/s. This is 10 billion times smaller than '
    'the TLI preset\u2019s delta-v. Yet over 500 hours, the spacecraft departs L1 dramatically, '
    'swinging past the Moon and entering a complex multi-body trajectory.',
    styles['Body']))
S.append(Paragraph(
    'The instability of L1 acts as an amplifier: the tiny perturbation grows exponentially '
    '(doubling every ~1.5 days) until the spacecraft is swept away along the unstable manifold. '
    'This is the same instability that requires SOHO and JWST to perform regular station-keeping burns.',
    styles['Body']))

S.append(Paragraph('6.2 L1 Chaos', styles['H2']))
S.append(Paragraph(
    'Similar concept but without thrust: the spacecraft starts at L1 with a small initial velocity '
    '(50 m/s in both x and y). This immediately places it on the unstable manifold. Over 2400 hours '
    '(100 days), the trajectory becomes increasingly complex and chaotic \u2014 the spacecraft bounces '
    'between Earth and Moon influence zones in an unpredictable pattern.',
    styles['Body']))
S.append(Paragraph(
    'This demonstrates <b>deterministic chaos</b> in the three-body problem: the equations are '
    'fully deterministic, but the trajectory is extremely sensitive to initial conditions. A tiny '
    'change in starting velocity would produce a completely different trajectory. This sensitivity '
    'is fundamental to the three-body problem and was one of Poincar\u00e9\u2019s key discoveries.',
    styles['Body']))

S.append(PageBreak())
S.append(Paragraph('7. Quick Reference: All Preset Parameters', styles['H1']))

S.append(Paragraph(
    'Complete initial conditions for all 14 presets. All positions in tkm, velocities in km/s, '
    'forces in N, times in hours (except t<sub>dur</sub> in seconds).',
    styles['BodySmall']))

S.append(Paragraph('Table A \u2014 Position and Velocity', styles['H3']))

ref_pos = [
    ['Preset', 'x\u2080 (tkm)', 'y\u2080 (tkm)', 'z\u2080 (tkm)',
     'vx\u2080 (km/s)', 'vy\u2080 (km/s)', 'vz\u2080 (km/s)'],
    ['L1', '323.696', '0', '0', '0', '0', '0'],
    ['L2', '446.531', '0', '0', '0', '0', '0'],
    ['L3', '\u2212386.651', '0', '0', '0', '0', '0'],
    ['L4', '188.081', '332.925', '0', '0', '0', '0'],
    ['L5', '188.081', '\u2212332.925', '0', '0', '0', '0'],
    ['Earth orbit', '45.33', '0', '0', '0', '2.823', '0'],
    ['Moon orbit', '332.80', '0', '0', '0', '0.313', '0'],
    ['L1 Halo', '318.188', '0', '15.228', '0', '0.153', '0'],
    ['L2 Halo (JWST)', '426.963', '0', '17.601', '0', '0.227', '0'],
    ['Apollo-13', '\u22129.463', '\u22124.782', '0', '7.708', '\u22127.536', '0'],
    ['Direct transfer', '\u22129.463', '\u22124.782', '0', '7.626', '\u22127.643', '0'],
    ['Thrust correction', '\u22129.331', '\u22124.912', '0', '7.765', '\u22127.368', '0'],
    ['TLI from orbit *', '\u22124.67', '\u221250.0', '0', '2.823', '0', '0'],
    ['L1 Escape', '323.696', '0', '0', '0', '0', '0'],
    ['L1 Chaos', '323.696', '0', '0', '0.05', '0.05', '0'],
]
t_pos = Table(ref_pos, colWidths=[30*mm, 22*mm, 22*mm, 18*mm, 20*mm, 20*mm, 18*mm])
t_pos.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('FONTNAME', (0, 0), (-1, -1), FONT),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.4, GREY),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [LIGHT, WHITE]),
    ('TOPPADDING', (0, 0), (-1, -1), 2),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
]))
S.append(t_pos)
S.append(Spacer(1, 4 * mm))

S.append(Paragraph('Table B \u2014 Engine and Integration', styles['H3']))

ref_eng = [
    ['Preset', 'Fx (N)', 'Fy (N)', 'Burn (s)', 'tEnd (h)', 'dt (s)', 'Notes'],
    ['L1', '\u2014', '\u2014', '\u2014', '2400', '30', ''],
    ['L2', '\u2014', '\u2014', '\u2014', '2400', '30', ''],
    ['L3', '\u2014', '\u2014', '\u2014', '2400', '30', ''],
    ['L4', '\u2014', '\u2014', '\u2014', '2400', '30', ''],
    ['L5', '\u2014', '\u2014', '\u2014', '2400', '30', ''],
    ['Earth orbit', '\u2014', '\u2014', '\u2014', '2400', '30', ''],
    ['Moon orbit', '\u2014', '\u2014', '\u2014', '2400', '30', ''],
    ['L1 Halo', '\u2014', '\u2014', '\u2014', '293', '30', '1 period'],
    ['L2 Halo (JWST)', '\u2014', '\u2014', '\u2014', '347', '30', '1 period'],
    ['Apollo-13', '\u2014', '\u2014', '\u2014', '166', '30', 'Free return'],
    ['Direct transfer', '\u2014', '\u2014', '\u2014', '58', '30', 'Ballistic'],
    ['Thrust correction', '5', '\u2014', '10800', '72', '30', '\u0394v = 108 m/s'],
    ['TLI from orbit *', '15300', '2600', '120', '19', '5', 'Adaptive, dtmin=1'],
    ['L1 Escape', '0.01', '\u2014', '30', '500', '30', '\u0394v = 0.6 mm/s'],
    ['L1 Chaos', '\u2014', '\u2014', '\u2014', '2400', '30', 'v\u2080 = 50 m/s kick'],
]
t_eng = Table(ref_eng, colWidths=[30*mm, 16*mm, 14*mm, 16*mm, 16*mm, 12*mm, 36*mm])
t_eng.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('FONTNAME', (0, 0), (-1, -1), FONT),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
    ('ALIGN', (-1, 0), (-1, -1), 'LEFT'),
    ('GRID', (0, 0), (-1, -1), 0.4, GREY),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [LIGHT, WHITE]),
    ('TOPPADDING', (0, 0), (-1, -1), 2),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
]))
S.append(t_eng)
S.append(Spacer(1, 2 * mm))
S.append(Paragraph(
    '* TLI preset requires adaptive timestepping: dt = 5 s, dt<sub>min</sub> = 1 s. '
    'All other presets use default dt = 30 s. "\u2014" indicates zero / not applicable.',
    styles['BodySmall']))

S.append(Spacer(1, 6 * mm))
S.append(Paragraph('References', styles['H1']))

styles.add(ParagraphStyle(
    'Ref', parent=styles['Normal'], fontSize=9, leading=12,
    leftIndent=10 * mm, firstLineIndent=-10 * mm, spaceAfter=2 * mm,
    fontName=FONT,
))

refs = [
    'Szebehely, V. (1967). <i>Theory of Orbits: The Restricted Problem of Three Bodies.</i> '
    'Academic Press. \u2014 Classical CR3BP reference.',

    'Koon, W.S. et al. (2011). <i>Dynamical Systems, the Three-Body Problem and Space '
    'Mission Design.</i> Marsden Books. \u2014 Invariant manifolds, low-energy transfers.',

    'Farquhar, R.W. (1968). "The Control and Use of Libration-Point Satellites." '
    'NASA TR R-346. \u2014 First description of halo orbits.',

    'Racca, G.D. et al. (2002). "SMART-1 mission description." '
    '<i>Planetary and Space Science</i>, 50(14-15). \u2014 Electric propulsion lunar transfer.',

    'NASA. "Apollo by the Numbers." NASA History Division. '
    '\u2014 S-IVB TLI burn parameters, free-return trajectories.',

    'Richardson, D.L. (1980). "Analytic construction of periodic orbits about the collinear '
    'points." <i>Celestial Mechanics</i>, 22(3), 241\u2013253. \u2014 Halo orbit computation.',
]

for i, ref in enumerate(refs, 1):
    S.append(Paragraph(f'[{i}] {ref}', styles['Ref']))

doc.build(S)
print(f'PDF generated: {OUTPUT}')
