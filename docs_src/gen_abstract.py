"""Build the English research abstract -> public/cr3bp_theory_en.pdf

Translation of the Russian abstract (public/cr3bp_theory.pdf), which was
originally compiled with pdfTeX from a source that no longer exists.
"""
import os

from style import DocPDF, PUBLIC

TITLE = ("Numerical Integration in the Restricted Three-Body Problem: "
         "Building a Tool for Studying Motion in the Earth–Moon System")
SUBTITLE = "Research abstract"
AUTHOR = "Alexander Klyuchnikov"


def build():
    pdf = DocPDF("Numerical Integration in the Restricted Three-Body Problem")
    pdf.add_page()
    pdf.title_block(TITLE, SUBTITLE, AUTHOR)

    pdf.h1("Introduction and motivation")
    pdf.para(
        "The three-body problem is one of the fundamental problems of celestial "
        "mechanics. It describes the motion of three bodies interacting through "
        "gravity, and in the general case it has no analytical solution."
    )
    pdf.para(
        "The restricted three-body problem (RTBP) is a special case in which one "
        "considers the motion of a body of negligible mass in the gravitational "
        "field of two massive bodies — for example the Earth and the Moon — "
        "that orbit their common centre of mass on circular orbits."
    )
    pdf.para(
        "Because no exact analytical solution exists, numerical methods are the "
        "primary tool for investigating this problem. Modelling motion in the "
        "Earth–Moon system is of practical importance in astronautics, astronomy "
        "and education."
    )
    pdf.para("The project is motivated by the opportunity to:")
    pdf.bullets([
        "model spacecraft trajectories;",
        "study stable and unstable orbits;",
        "investigate the Lagrange points;",
        "present complex dynamical processes in a visual form.",
    ])

    pdf.h1("Aim and objectives")
    pdf.h2("Aim")
    pdf.para(
        "To develop a software tool for the numerical investigation of a body's "
        "motion in the Earth–Moon system within the restricted three-body problem."
    )
    pdf.h2("Objectives")
    pdf.bullets([
        "Study the theoretical foundations of the restricted three-body problem.",
        "Derive the equations of motion in a rotating reference frame.",
        "Implement numerical integration of the equations of motion.",
        "Obtain coordinates and velocities as functions of time in array form.",
        "Plot the evolution of the motion parameters.",
        "Create an interactive application for visualising the trajectory.",
    ])

    pdf.h1("Mathematical model")
    pdf.para(
        "We work in a coordinate frame rotating together with the Earth and the "
        "Moon. In this frame the equations of motion take the form:"
    )
    pdf.equation(r"$\ddot{x} - 2\omega\dot{y} = \omega^2 x"
                 r" - \frac{GM_E\,(x + d_E)}{r_E^{3}}"
                 r" - \frac{GM_M\,(x - d_M)}{r_M^{3}}$")
    pdf.equation(r"$\ddot{y} + 2\omega\dot{x} = \omega^2 y"
                 r" - \frac{GM_E\,y}{r_E^{3}} - \frac{GM_M\,y}{r_M^{3}}$")
    pdf.equation(r"$\ddot{z} = - \frac{GM_E\,z}{r_E^{3}}"
                 r" - \frac{GM_M\,z}{r_M^{3}}$")
    pdf.para("where:")
    pdf.bullets([
        "G — the gravitational constant;",
        "M_E, M_M \u2014 the masses of the Earth and the Moon;",
        "d_E, d_M \u2014 the distances from the centre of mass to the Earth and the Moon;",
        "r_E, r_M \u2014 the distances from the body to the centres of the Earth "
        "and the Moon;",
        "ω — the angular velocity of the rotating frame.",
    ])

    pdf.h1("Numerical method")
    pdf.para(
        "The system of differential equations is solved using the explicit Euler "
        "method with an integration step Δt."
    )
    pdf.h2("Velocity update")
    pdf.equation(r"$\vec{v}(t + \Delta t) = \vec{v}(t) + \vec{a}(t)\,\Delta t$")
    pdf.h2("Position update")
    pdf.equation(r"$\vec{r}(t + \Delta t) = \vec{r}(t) + \vec{v}(t)\,\Delta t"
                 r" + \frac{1}{2}\vec{a}(t)\,\Delta t^{2}$")
    pdf.para(
        "Despite its simplicity, this method makes it possible to study the "
        "qualitative dynamics of the system provided the time step is small enough."
    )

    pdf.h1("Implementation and results")
    pdf.para(
        "An interactive application was implemented using the Python programming "
        "language and the Streamlit library."
    )
    pdf.para("The application supports:")
    pdf.bullets([
        "specifying the initial conditions of the motion;",
        "numerical integration of the equations of motion;",
        "plotting coordinates and velocities against time;",
        "visualising the trajectory in three-dimensional space.",
    ])
    pdf.para(
        "The application makes it possible to examine how the initial conditions "
        "influence the character of the motion."
    )

    pdf.h1("Conclusions")
    pdf.bullets([
        "Numerical methods are the primary tool for investigating the restricted "
        "three-body problem.",
        "Even the simple Euler method allows the qualitative study of the system's "
        "dynamics.",
        "Regions of dynamical instability exist in the Earth–Moon system.",
        "Small changes in the initial conditions can lead to fundamentally "
        "different trajectories.",
        "The three-body problem demonstrates the transition from regular orbits to "
        "chaotic motion.",
    ])

    pdf.h1("Further work")
    pdf.para("The project can be extended by:")
    pdf.bullets([
        "accounting for solar perturbation (the four-body problem);",
        "using more accurate numerical methods;",
        "investigating the long-term evolution of orbits;",
        "applying the tool in physics and astronomy courses.",
    ])

    pdf.h1("References")
    pdf.bullets([
        "Murray C. D., Dermott S. F. Solar System Dynamics. Cambridge University "
        "Press, 1999.",
        "Szebehely V. Theory of Orbits: The Restricted Problem of Three Bodies. "
        "Academic Press, 1967.",
        "Vallado D. A., Crawford P., Hujsa R., Kelso T. S. Revisiting Spacetrack "
        "Report №3. AIAA, 2006.",
        "Golomb M. Lectures on Theory of Approximation. 1959.",
    ])

    out = os.path.join(PUBLIC, "cr3bp_theory_en.pdf")
    pdf.output(out)
    print(f"written: {out}")


if __name__ == "__main__":
    build()
