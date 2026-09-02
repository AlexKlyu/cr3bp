"""Build the English talk outline -> public/plan_2503_en.pdf

Translation of the Russian outline (public/plan_2503.pdf), which was
originally printed to PDF from a browser; no source survived.
"""
import os

from style import DocPDF, PUBLIC

SECTIONS = [
    ("Title slide", [
        "Introduce myself.",
        "Project title: Numerical integration in the restricted three-body "
        "problem. Building a tool for studying motion in the Earth–Moon system.",
        "A year ago I watched Apollo 13.",
        "Formulas are just symbols on paper.",
        "PhET, Desmos and Universe Sandbox do not model spacecraft motion with "
        "Lagrange points, thrust and accuracy control.",
        "So I decided to build it myself.",
    ]),
    ("Introduction to the topic", [
        "The three-body problem is a classical problem of mechanics.",
        "I consider a simplification of it.",
        "This gives the circular restricted three-body problem (CR3BP).",
        "A rotating frame centred on the system's barycentre.",
    ]),
    ("Relevance and existing tools", [
        "Comparison with existing tools.",
        "None of them models motion in the CR3BP in 3D with thrust and accuracy "
        "control via the Jacobi integral.",
    ]),
    ("rocketlauncher.space", [
        "Please try the tool.",
    ]),
    ("Aim and objectives", [
        "The aim of my work is to create an educational web simulator.",
    ]),
    ("Mathematical model", [
        "Here are the equations of motion.",
        "The term 2ω × v.",
        "It depends on velocity.",
        "Remember this.",
    ]),
    ("Scope of applicability", [
        "The model has a scope of applicability.",
        "Not for computing trajectories of real missions.",
        "For understanding the dynamics.",
    ]),
    ("Three integrators", [
        "Poincaré proved that no analytical solution exists.",
        "Numerical integration.",
        "The Euler method is the simplest approach.",
        "First setback: the computational error accumulated to 20–30% over 30 days.",
        "I was not consistent with units (velocity in km/s, everything else in SI).",
        "The error still accumulated, but over the same period it stayed below 5%.",
        "That was still not good enough.",
        "Euler is a first-order method (acceleration evaluated once per step). "
        "Halve the step and the error halves.",
        "The Verlet method is second order (acceleration evaluated twice per step).",
        "I will come back later to the Verlet method with iterative velocity "
        "correction shown on this slide.",
    ]),
    ("The Jacobi integral", [
        "Used for accuracy control.",
        "The Jacobi integral is the only quantity conserved in the CR3BP.",
        "Its drift is a measure of the error.",
    ]),
    ("Log-log convergence", [
        "The most unexpected setback.",
        "I plotted a log-log graph for Euler and Verlet (the red and yellow lines).",
        "Verlet — a method that should be second order — behaves like a first-order one.",
        "The slope on the graph is 1, not 2.",
        "The Coriolis force.",
        "Explicit Verlet assumes acceleration depends only on position.",
        "The Coriolis force depends on velocity.",
        "Verlet substitutes an approximate velocity and loses its order of accuracy.",
        "The solution: Verlet with iterative velocity correction.",
        "Three iterations per step refine the velocity. The result is on the graph. "
        "At a step of 30 seconds: Euler's error is 8 kilometres; Verlet with "
        "iterative velocity correction, 13 centimetres. A factor of 58,000.",
    ]),
    ("Adaptive step", [
        "There are terms of the form 1/r.",
        "Close to a planet r drops sharply, and the force and acceleration grow.",
        "A small inaccuracy turns into an enormous error.",
        "Approaching the Earth or the Moon, dt is reduced in proportion to velocity.",
    ]),
    ("Lagrange points L1–L5: graphical solution", [
        "The Lagrange points are five points where a spacecraft can hang motionless.",
        "Set the velocities and accelerations in the equations of motion to zero.",
        "From the z equation we get z = 0.",
        "I plotted the x and y equations in Desmos.",
        "The intersections of the two graphs.",
        "I started zooming in.",
        "At one place the acceleration changes sign.",
    ]),
    ("Lagrange points L1–L5: numerical solution", [
        "I decided to search for that point automatically — halve the interval and "
        "see where the sign changes.",
        "I wrote the algorithm. It found L1 to an accuracy of 10⁻¹⁸.",
        "Later I learned this method is called bisection.",
        "I arrived at it myself, from the Desmos graph.",
    ]),
    ("Personal contribution", [
        "Derivation of the equations of motion.",
        "Implementation of the Jacobi integral as an accuracy-checking tool.",
        "Three integrators.",
        "A series of 7 computational experiments for quantitative verification.",
        "Locating the Lagrange points L1–L5.",
        "The 3D web simulator.",
    ]),
    ("Directions for development", [
        "Account for the eccentricity of the Moon's orbit (solve the elliptic RTBP).",
        "Add the Sun.",
        "Implement halo-orbit station keeping.",
        "Create laboratory exercises (a set of assignments).",
    ]),
    ("Conclusions", [
        "All six objectives have been completed.",
        "The aim of the work — to create an educational web simulator — has been achieved.",
        "Verlet with iterative velocity correction is 58 thousand times more "
        "accurate than Euler.",
    ]),
    ("Demonstration", [
        "I will demonstrate how my tool works.",
        "At the bottom are the 7 numerical experiments (appendices) and the "
        "materials for the talk.",
        "Two trajectories meet, starting at the Lagrange point L1 with equal "
        "speeds directed in opposite directions.",
        "We can choose scenarios.",
        "We can create our own flight scenario.",
        "Several bodies can be added for comparison.",
        "Every flight and visualisation parameter can be changed.",
    ]),
    ("Thank you", [
        "Thank you for your attention. I am ready to answer any questions.",
    ]),
]

OBJECTIVES = [
    "Study the fundamentals of the CR3BP.",
    "Derive the equations of motion in a rotating reference frame.",
    "Implement trajectory computation using the Euler method.",
    "Implement the Verlet method and compare its accuracy with Euler.",
    "Find the Lagrange points L1–L5 numerically.",
    "Create an interactive 3D web simulator.",
]

ASSUMPTIONS = [
    "A circular orbit for the Moon.",
    "Negligible spacecraft mass.",
    "The influence of the Sun is not taken into account.",
]

TOOLS = [
    "The 3D web simulator.",
    "Its initial version.",
    "The tool for locating the Lagrange points.",
]


def build():
    pdf = DocPDF("Talk outline")
    pdf.add_page()
    pdf.title_block("Talk Outline",
                    "Numerical integration in the restricted three-body problem",
                    "Alexander Klyuchnikov")

    for heading, points in SECTIONS:
        pdf.h1(heading)
        pdf.bullets(points)
        if heading == "Aim and objectives":
            pdf.h2("Six objectives")
            pdf.bullets(OBJECTIVES, numbered=True)
        elif heading == "Scope of applicability":
            pdf.h2("Three assumptions")
            pdf.bullets(ASSUMPTIONS, numbered=True)
        elif heading == "Demonstration":
            pdf.h2("At the very top, three tools")
            pdf.bullets(TOOLS, numbered=True)

    out = os.path.join(PUBLIC, "plan_2503_en.pdf")
    pdf.output(out)
    print(f"written: {out}")


if __name__ == "__main__":
    build()
