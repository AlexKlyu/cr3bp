"""
Генерация PDF-заметки: демонстрация тяги в CR3BP (три пресета).
  1. Перелёт Земля→Луна с тягой (коррекция)
  2. Перелёт с орбиты к Луне (TLI)
  3. Побег от L1 с микротягой
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

OUTPUT = 'thrust_demos_note.pdf'
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


def make_table(data, col_widths):
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
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
    return t


S = []

S.append(Paragraph(
    'Thrust Demonstrations in the Earth\u2013Moon CR3BP', styles['Title2']))
S.append(Paragraph('Technical Note \u2014 March 2026', styles['Subtitle']))
S.append(HRFlowable(width='100%', thickness=0.5, color=HexColor('#003366')))
S.append(Spacer(1, 4 * mm))

S.append(Paragraph('1. Introduction', styles['H2']))
S.append(Paragraph(
    'This note describes three simulator presets that demonstrate the effect of '
    'continuous thrust in the Circular Restricted Three-Body Problem (CR3BP) '
    'Earth\u2013Moon rotating frame. Unlike the ballistic presets (Lagrange points, '
    'free-return), these scenarios use the engine force parameters (F<sub>x</sub>, '
    'F<sub>y</sub>, F<sub>z</sub>) with a finite burn time window.',
    styles['Body']))
S.append(Paragraph(
    'The CR3BP equations of motion with thrust are:',
    styles['Body']))
S.append(Paragraph(
    f'a{sub("x")} = \u03c9\u00b2x + 2\u03c9v{sub("y")} '
    f'\u2212 K{sub("E")}(x + d{sub("E")}) \u2212 K{sub("M")}(x \u2212 d{sub("M")}) '
    f'+ F{sub("x")}/m',
    styles['Formula']))
S.append(Paragraph(
    f'a{sub("y")} = \u03c9\u00b2y \u2212 2\u03c9v{sub("x")} '
    f'\u2212 (K{sub("E")} + K{sub("M")})y + F{sub("y")}/m',
    styles['Formula']))
S.append(Paragraph(
    f'a{sub("z")} = \u2212(K{sub("E")} + K{sub("M")})z + F{sub("z")}/m',
    styles['Formula']))
S.append(Paragraph(
    'where F is constant during the burn window [t<sub>On</sub>, t<sub>On</sub> + t<sub>dur</sub>] '
    'and zero otherwise. The mass m is treated as constant (no fuel depletion).',
    styles['Body']))

S.append(Paragraph('2. Preset: Earth\u2192Moon Transfer with Thrust (Correction)', styles['H2']))

S.append(Paragraph('2.1 Concept', styles['H3']))
S.append(Paragraph(
    'The spacecraft starts near Earth with a sub-escape velocity \u2014 the same departure '
    'position as the Apollo-13 free-return preset, but with only 99.3% of the required velocity. '
    'At 100% velocity (no thrust), the spacecraft completes the full free-return loop and '
    'crashes back into Earth. At 99.3% without thrust, it lacks the energy to reach the Moon '
    'and falls back toward Earth.',
    styles['Body']))
S.append(Paragraph(
    'By applying a gentle thrust of F<sub>x</sub> = 5 N in the +x direction for 3 hours at '
    'departure, the engine provides the missing \u0394v \u2248 108 m/s. This small boost is '
    'enough to push the trajectory onto a trans-lunar path. After 72 hours, the spacecraft '
    'arrives within ~2,000 km of the Moon\u2019s center.',
    styles['Body']))

S.append(Paragraph('2.2 Initial Conditions', styles['H3']))

ic1_data = [
    ['Parameter', 'Value', 'Notes'],
    ['x\u2080', '\u22129.331 \u00d7 10\u00b3 km', 'Near-Earth departure'],
    ['y\u2080', '\u22124.912 \u00d7 10\u00b3 km', '(same as Apollo-13 preset)'],
    ['v<sub>x0</sub>', '7.765 km/s', '99.3% of free-return velocity'],
    ['v<sub>y0</sub>', '\u22127.368 km/s', '(sub-escape)'],
    ['F<sub>x</sub>', '5 N', 'Gentle thrust toward Moon (+x)'],
    ['Mass', '500 kg', 'Spacecraft mass'],
    ['t<sub>On</sub>', '0 h', 'Thrust starts immediately'],
    ['t<sub>dur</sub>', '10,800 s (3 h)', 'Burn duration'],
    ['t<sub>End</sub>', '72 h', 'Arrives at Moon'],
]
S.append(make_table(ic1_data, [28 * mm, 34 * mm, 48 * mm]))
S.append(Spacer(1, 3 * mm))

S.append(Paragraph('2.3 Trajectory Description', styles['H3']))
S.append(Paragraph(
    'The trajectory proceeds in three phases:',
    styles['Body']))
S.append(Paragraph(
    '<b>Phase 1 \u2014 Powered boost (0\u20133 h)</b>: The 5 N thrust on a 500 kg spacecraft '
    'produces an acceleration of 0.01 m/s\u00b2. Over 3 hours, this imparts \u0394v \u2248 108 m/s '
    'in the +x direction \u2014 a small but critical boost.',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '<b>Phase 2 \u2014 Coasting to Moon (~3\u201370 h)</b>: After engine cutoff, the spacecraft '
    'coasts on a trans-lunar trajectory, gradually decelerating under Earth\u2019s gravity and then '
    'accelerating as lunar gravity takes over.',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '<b>Phase 3 \u2014 Lunar arrival (~72 h)</b>: The spacecraft arrives within ~2,000 km of '
    'the Moon\u2019s center \u2014 approximately 3 days after departure.',
    styles['BulletItem'], bulletText='\u2022'))

S.append(Paragraph('2.4 Physics Discussion', styles['H3']))
S.append(Paragraph(
    'The key demonstration is the critical role of even a tiny engine: the same initial '
    'conditions without thrust produce a trajectory that falls back to Earth, while '
    'just 3 hours of 5 N thrust (providing \u0394v \u2248 108 m/s) pushes the spacecraft '
    'onto a trans-lunar path. This illustrates the sensitivity of orbital mechanics \u2014 '
    'a ~0.7% velocity change leads to a qualitatively different trajectory.',
    styles['Body']))
S.append(Paragraph(
    'The initial velocity |v\u2080| \u2248 10.71 km/s is 99.3% of the Apollo-13 free-return '
    'velocity (~10.78 km/s). The 5 N thrust is comparable to a small cold-gas thruster '
    'or a single ion engine, demonstrating that even modest propulsion can enable '
    'interplanetary-scale trajectory changes when applied at the right time.',
    styles['Body']))

S.append(Paragraph('3. Preset: Orbit\u2192Moon Transfer (TLI)', styles['H2']))

S.append(Paragraph('3.1 Concept', styles['H3']))
S.append(Paragraph(
    'Unlike the previous preset (which starts near escape velocity and needs only a small '
    'correction), this scenario demonstrates a <b>full Trans-Lunar Injection (TLI)</b> from '
    'a natural circular orbit. The spacecraft begins in a 50,000 km circular orbit around '
    'Earth \u2014 the same altitude as the "Околоземная орбита" preset \u2014 with only its '
    'natural orbital velocity of 2.823 km/s. The engine must provide the entire delta-v '
    'needed to escape Earth\u2019s gravity and reach the Moon.',
    styles['Body']))
S.append(Paragraph(
    'The spacecraft is positioned at the 270\u00b0 point on its orbit (below Earth in the '
    'rotating frame), where the prograde velocity vector points in the +x direction \u2014 '
    'toward the Moon. A 15.5 kN engine fires for 2 minutes, providing \u0394v \u2248 3,725 m/s. '
    'This is comparable to the real Apollo TLI burn (~3,100 m/s from LEO by the S-IVB stage).',
    styles['Body']))
S.append(Paragraph(
    'Without thrust, the spacecraft remains in its Earth orbit indefinitely, never approaching '
    'closer than ~327,000 km to the Moon. With the TLI burn, it reaches the Moon in ~19 hours.',
    styles['Body']))

S.append(Paragraph('3.2 Initial Conditions', styles['H3']))

ic_tli = [
    ['Parameter', 'Value', 'Notes'],
    ['x\u2080', '\u22124.67 \u00d7 10\u00b3 km', '50,000 km orbit, 270\u00b0 position'],
    ['y\u2080', '\u221250.0 \u00d7 10\u00b3 km', '(below Earth in rotating frame)'],
    ['v<sub>x0</sub>', '2.823 km/s', 'Circular orbit velocity (prograde)'],
    ['v<sub>y0</sub>', '0 km/s', '(natural orbit, no excess velocity)'],
    ['F<sub>x</sub>', '15,300 N', 'Main engine thrust (+x component)'],
    ['F<sub>y</sub>', '2,600 N', 'Thrust (+y component for targeting)'],
    ['|F|', '15,519 N (15.5 kN)', 'Total thrust magnitude'],
    ['Mass', '500 kg', 'Spacecraft mass'],
    ['t<sub>On</sub>', '0 h', 'Thrust starts immediately'],
    ['t<sub>dur</sub>', '120 s (2 min)', 'Burn duration'],
    ['t<sub>End</sub>', '19 h', 'Simulation ends near Moon'],
    ['dt', '5 s', 'Base timestep (adaptive enabled)'],
    ['dt<sub>min</sub>', '1 s', 'Minimum adaptive timestep'],
]
S.append(make_table(ic_tli, [28 * mm, 36 * mm, 46 * mm]))
S.append(Spacer(1, 3 * mm))

S.append(Paragraph('3.3 Integration Settings', styles['H3']))
S.append(Paragraph(
    'This preset requires <b>adaptive timestepping</b> (dt = 5 s, dt<sub>min</sub> = 1 s). '
    'The short, intense burn (120 s at 15.5 kN) produces an acceleration of ~31 m/s\u00b2 '
    '(~3.2 g), which changes the velocity significantly within a few timesteps. The adaptive '
    'integrator automatically reduces the step size during the burn phase to maintain accuracy, '
    'then increases it during the coasting phase for efficiency.',
    styles['Body']))
S.append(Paragraph(
    'With a fixed 30 s timestep, the burn occupies only 4 integration steps, which is too '
    'coarse to accurately resolve the trajectory during the high-thrust phase. The adaptive '
    'approach provides ~24 steps during the burn (at dt \u2248 5 s or less), giving a much more '
    'accurate result.',
    styles['Body']))

S.append(Paragraph('3.4 Trajectory Description', styles['H3']))
S.append(Paragraph(
    '<b>Phase 1 \u2014 TLI burn (0\u20132 min)</b>: The 15.5 kN engine fires for 120 seconds, '
    'accelerating the spacecraft at ~3.2 g. This imparts \u0394v \u2248 3,725 m/s, boosting the '
    'velocity from 2.82 km/s (circular orbit) to ~6.5 km/s (well above escape velocity of '
    '~4.0 km/s at this altitude). The thrust direction has a small +y component for Moon targeting.',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '<b>Phase 2 \u2014 Trans-lunar coast (2 min\u201319 h)</b>: After engine cutoff, the spacecraft '
    'coasts on a trans-lunar trajectory. Earth\u2019s gravity decelerates it, then lunar gravity '
    'takes over as it approaches the Moon.',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '<b>Phase 3 \u2014 Lunar arrival (~19 h)</b>: The spacecraft arrives near the Moon. '
    'In reality, a Lunar Orbit Insertion (LOI) braking burn would be needed to enter lunar orbit; '
    'the simulator models only the TLI phase since it supports a single thrust window.',
    styles['BulletItem'], bulletText='\u2022'))

S.append(Paragraph('3.5 Physics Discussion', styles['H3']))
S.append(Paragraph(
    'This preset demonstrates a realistic TLI maneuver. Key comparisons with real missions:',
    styles['Body']))
S.append(Paragraph(
    '<b>Delta-v</b>: Our \u0394v of 3,725 m/s is comparable to the Apollo S-IVB TLI burn '
    '(~3,100 m/s from LEO). The slightly higher value reflects the non-optimal thrust direction '
    '(constant in the rotating frame) and the higher starting orbit (50,000 km vs ~185 km LEO).',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '<b>Fuel consumption</b>: Using the Tsiolkovsky rocket equation with Isp = 300 s '
    '(bipropellant), fuel mass = 500 \u00d7 (1 \u2212 e<sup>\u2212\u0394v/(Isp\u00b7g\u2080)</sup>) '
    '\u2248 359 kg (72% of spacecraft mass). With LH\u2082/LOX (Isp = 450 s), this drops to '
    '~285 kg (57%). Both are realistic for chemical propulsion.',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '<b>Thrust level</b>: 15.5 kN on 500 kg gives ~3.2 g acceleration \u2014 similar to '
    'upper-stage engines like the Apollo S-IVB (1 MN on ~130,000 kg \u2248 0.8 g) or '
    'a spacecraft main engine. This is a high-thrust, short-burn scenario (chemical propulsion), '
    'in contrast to the low-thrust electric propulsion of Preset 1.',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '<b>Without thrust</b>: The spacecraft stays in its circular Earth orbit, never approaching '
    'closer than ~327,000 km to the Moon. This dramatically illustrates the energy barrier '
    'that must be overcome for a lunar transfer.',
    styles['BulletItem'], bulletText='\u2022'))

S.append(Paragraph('4. Preset: L1 Escape with Micro-Thrust', styles['H2']))

S.append(Paragraph('4.1 Concept', styles['H3']))
S.append(Paragraph(
    'The collinear Lagrange point L1 lies at x \u2248 323.7 \u00d7 10\u00b3 km on the '
    'Earth\u2013Moon line, between the two bodies. Unlike L4 and L5 (which are linearly stable), '
    'L1 is an <i>unstable equilibrium</i>: any perturbation will cause exponential departure '
    'from the point.',
    styles['Body']))
S.append(Paragraph(
    'This preset demonstrates the instability by applying an extremely small thrust of just '
    'F<sub>x</sub> = 0.05 N for 2 hours. The resulting trajectory shows a dramatic departure '
    'from L1 \u2014 the spacecraft ends up hundreds of thousands of kilometers away, despite '
    'the perturbation being almost imperceptible initially.',
    styles['Body']))

S.append(Paragraph('4.2 Initial Conditions', styles['H3']))

ic2_data = [
    ['Parameter', 'Value', 'Notes'],
    ['x\u2080', '323.696 \u00d7 10\u00b3 km', 'L1 Lagrange point'],
    ['y\u2080, z\u2080', '0', 'On the Earth\u2013Moon line'],
    ['v<sub>x0</sub>, v<sub>y0</sub>, v<sub>z0</sub>', '0', 'Initially at rest (equilibrium)'],
    ['F<sub>x</sub>', '0.05 N', 'Micro-thrust toward Moon'],
    ['Mass', '500 kg', 'Spacecraft mass'],
    ['t<sub>On</sub>', '0 h', 'Thrust starts immediately'],
    ['t<sub>dur</sub>', '7,200 s (2 h)', 'Burn duration'],
    ['t<sub>End</sub>', '500 h', 'Long simulation to see full departure'],
]
S.append(make_table(ic2_data, [36 * mm, 34 * mm, 40 * mm]))
S.append(Spacer(1, 3 * mm))

S.append(Paragraph('4.3 Instability Analysis', styles['H3']))
S.append(Paragraph(
    'The L1 point is a saddle in the effective potential of the rotating frame. '
    'Linearizing the equations of motion about L1 yields eigenvalues with both real '
    'and imaginary parts. The positive real eigenvalue corresponds to an unstable manifold \u2014 '
    'exponential growth of perturbations along the Earth\u2013Moon line.',
    styles['Body']))
S.append(Paragraph(
    'The characteristic e-folding time at L1 is approximately:',
    styles['Body']))
S.append(Paragraph(
    f'\u03c4 \u2248 1/\u03bb \u2248 2.2 days',
    styles['Formula']))
S.append(Paragraph(
    'This means that a perturbation doubles roughly every 1.5 days. The micro-thrust '
    'of 0.05 N on 500 kg gives an acceleration of just 10\u207b\u2074 m/s\u00b2, which is '
    '~10\u2078 times weaker than Earth\u2019s surface gravity. Yet over 2 hours, it imparts '
    '\u0394v \u2248 0.36 m/s \u2014 enough to "seed" the instability.',
    styles['Body']))
S.append(Paragraph(
    'After the engine shuts off, the instability takes over. The spacecraft departs L1 along '
    'the unstable manifold, swinging past the Moon and entering a complex trajectory influenced '
    'by both Earth and Moon gravity. The final position after 500 hours is hundreds of '
    'thousands of km from L1.',
    styles['Body']))

S.append(Paragraph('4.4 Comparison: With and Without Thrust', styles['H3']))
S.append(Paragraph(
    'Without any thrust, the L1 preset shows the spacecraft remaining at L1 indefinitely '
    '(within numerical precision). Even with thrust as low as 0.01 N for 1 hour, the '
    'departure is dramatic. This sensitivity to perturbation is a hallmark of chaotic '
    'dynamics in the three-body problem and is exploited in real missions for low-energy '
    'transfers along invariant manifolds.',
    styles['Body']))

S.append(Paragraph('5. Practical Context', styles['H2']))
S.append(Paragraph(
    'These three presets span the full spectrum of thrust levels used in spaceflight:',
    styles['Body']))
S.append(Paragraph(
    '<b>High-thrust chemical propulsion (Preset 2 \u2014 TLI)</b>: The 15.5 kN engine '
    'represents a typical spacecraft main engine or upper stage. The burn is short (2 min) '
    'and impulsive, similar to the Apollo S-IVB TLI burn. Fuel consumption is high '
    '(~72% of mass at Isp = 300 s) but the transfer is fast (~19 hours to Moon).',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '<b>Low-thrust correction (Preset 1)</b>: The 5 N thruster is comparable to a cold-gas '
    'or small monopropellant system used for trajectory corrections. It provides only 108 m/s '
    'of delta-v but is sufficient because the spacecraft already has most of the required energy. '
    'Fuel use is minimal (18 kg, 3.6%).',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    '<b>Micro-thrust perturbation (Preset 3 \u2014 L1 escape)</b>: The 0.05 N thrust '
    'demonstrates how even vanishingly small forces can have dramatic effects at unstable '
    'equilibria. This principle is exploited in real station-keeping at L1/L2 (SOHO, JWST) '
    'and in manifold-assisted low-energy transfers.',
    styles['BulletItem'], bulletText='\u2022'))
S.append(Paragraph(
    'ESA\u2019s SMART-1 mission provides an interesting intermediate case: it used a 68 mN '
    'Hall-effect thruster (Isp &gt; 1,600 s) to spiral from Earth orbit to lunar orbit over '
    '13 months \u2014 extremely fuel-efficient but very slow. Such continuous low-thrust spirals '
    'are not easily demonstrated in the current simulator (which supports a single burn window), '
    'but Preset 2 shows the impulsive high-thrust alternative.',
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
        'Classical reference for CR3BP formulation and Lagrange point stability analysis.'
    ),
    (
        'Koon, W.S., Lo, M.W., Marsden, J.E., Ross, S.D. (2011). '
        '<i>Dynamical Systems, the Three-Body Problem and Space Mission Design.</i> '
        'Marsden Books. ISBN 978-0-615-24095-4.'
        '<br/>'
        'Comprehensive treatment of invariant manifolds at L1/L2 and low-energy transfers.'
    ),
    (
        'Racca, G.D. et al. (2002). '
        '"SMART-1 mission description and development status." '
        '<i>Planetary and Space Science</i>, 50(14-15), 1323\u20131337.'
        '<br/>'
        'ESA\u2019s lunar mission using solar electric propulsion for Earth\u2013Moon transfer.'
    ),
    (
        'Brophy, J.R. et al. (2014). '
        '"Development and Testing of the NEXT Ion Propulsion System." '
        '<i>AIAA Paper 2014-3899.</i>'
        '<br/>'
        'NASA\u2019s next-generation ion engine for deep-space and lunar missions.'
    ),
    (
        'NASA. "Apollo by the Numbers: S-IVB Stage." '
        '<i>NASA History Division.</i>'
        '<br/>'
        'Technical data on the S-IVB Trans-Lunar Injection burn parameters.'
    ),
]

for i, ref in enumerate(refs, 1):
    S.append(Paragraph(f'[{i}] {ref}', styles['Ref']))

doc.build(S)
print(f'PDF generated: {OUTPUT}')
