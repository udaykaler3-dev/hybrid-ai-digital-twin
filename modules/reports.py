"""
=========================================================
GASONET DIGITAL TWIN
DIGITAL TWIN ENGINEERING REPORT
=========================================================
"""

# ==========================================================
# IMPORTS
# ==========================================================

import streamlit as st

from io import BytesIO

from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image
)

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.units import inch

from styles.theme import load_theme


# ==========================================================
# REPORTS PAGE
# ==========================================================

def reports():

    # ------------------------------------------------------
    # Load Theme
    # ------------------------------------------------------

    load_theme()

    # ------------------------------------------------------
    # Header
    # ------------------------------------------------------

    st.title("Digital Twin Engineering Report")

    st.caption(
        "Engineering report generated from the latest Digital Twin prediction."
    )

    st.divider()

    # ------------------------------------------------------
    # Validate Prediction
    # ------------------------------------------------------

    if "twin" not in st.session_state:

        st.warning(
            "Run a Manual Prediction first."
        )

        return

    twin = st.session_state["twin"]

        # ==========================================================
    # ENGINEERING ALARMS
    # ==========================================================

    st.subheader("Engineering Alarms")

    warnings = twin.get("warnings", [])

    if len(warnings) == 0:

        st.success(
            "✓ No active engineering alarms detected."
        )

    else:

        for i, warning in enumerate(warnings, start=1):

            st.error(
                f"ALM-{i:03d} : {warning}"
            )

    st.divider()

    # ==========================================================
    # MAINTENANCE RECOMMENDATIONS
    # ==========================================================

    st.subheader("Maintenance Recommendations")

    recommendations = twin.get(
        "recommendations",
        []
    )

    if len(recommendations) == 0:

        st.success(
            "✓ Continue normal compressor operation."
        )

    else:

        for i, recommendation in enumerate(
            recommendations,
            start=1
        ):

            st.info(
                f"{i}. {recommendation}"
            )

    st.divider()
        # ==========================================================
    # GENERATE PDF REPORT
    # ==========================================================

    st.subheader("Generate Engineering Report")

    if st.button(
        "Generate PDF Report",
        use_container_width=True
    ):

        pdf_buffer = BytesIO()

        doc = SimpleDocTemplate(
            pdf_buffer,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        styles = getSampleStyleSheet()

        story = []

        # ------------------------------------------------------
        # Logo
        # ------------------------------------------------------

        logo = Image("assets/gasonet_logo.png")

        logo.drawWidth = 2.2 * inch
        logo.drawHeight = 0.9 * inch
        logo.hAlign = "CENTER"

        story.append(logo)
        story.append(Spacer(1, 20))

        # ------------------------------------------------------
        # Title
        # ------------------------------------------------------

        story.append(
            Paragraph(
                "Digital Twin Engineering Report",
                styles["Title"]
            )
        )

        story.append(
            Paragraph(
                f"Generated on {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
                styles["BodyText"]
            )
        )

        story.append(Spacer(1, 20))

        # ------------------------------------------------------
        # Prediction Summary
        # ------------------------------------------------------

        story.append(
            Paragraph(
                "<b>Prediction Summary</b>",
                styles["Heading2"]
            )
        )

        story.append(
            Paragraph(
                f"""
                Health : {twin['health']:.1f}%<br/>
                Hybrid Power : {twin['predicted_power']:.2f} kW<br/>
                Predicted Energy : {twin['predicted_energy']:.2f} kWh<br/>
                Model Difference : {twin['model_difference']:.2f} kW
                """,
                styles["BodyText"]
            )
        )

        story.append(Spacer(1, 20))

        # ------------------------------------------------------
        # Engineering Alarms
        # ------------------------------------------------------

        story.append(
            Paragraph(
                "<b>Engineering Alarms</b>",
                styles["Heading2"]
            )
        )

        if len(warnings) == 0:

            story.append(
                Paragraph(
                    "No active engineering alarms detected.",
                    styles["BodyText"]
                )
            )

        else:

            for warning in warnings:

                story.append(
                    Paragraph(
                        f"• {warning}",
                        styles["BodyText"]
                    )
                )

        story.append(Spacer(1, 20))

        # ------------------------------------------------------
        # Maintenance Recommendations
        # ------------------------------------------------------

        story.append(
            Paragraph(
                "<b>Maintenance Recommendations</b>",
                styles["Heading2"]
            )
        )

        if len(recommendations) == 0:

            story.append(
                Paragraph(
                    "Continue normal compressor operation.",
                    styles["BodyText"]
                )
            )

        else:

            for recommendation in recommendations:

                story.append(
                    Paragraph(
                        f"• {recommendation}",
                        styles["BodyText"]
                    )
                )

        story.append(Spacer(1, 20))

        # ------------------------------------------------------
        # Footer
        # ------------------------------------------------------

        story.append(
            Paragraph(
                "Generated by Gasonet Digital Twin",
                styles["Italic"]
            )
        )

        doc.build(story)

        pdf_data = pdf_buffer.getvalue()

        pdf_buffer.close()

        st.success(
            "Engineering Report Generated Successfully."
        )

        st.download_button(
            "Download PDF Report",
            data=pdf_data,
            file_name="Digital_Twin_Engineering_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    