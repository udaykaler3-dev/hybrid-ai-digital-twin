import streamlit as st

from io import BytesIO

from datetime import datetime


from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)


from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib import colors

from reportlab.lib.units import inch



def pdf_generator():


    st.title(
        "Export Engineering Report"
    )


    st.subheader(
        "AI Digital Twin Compressor Assessment Report"
    )


    st.caption(
        "Generate a professional engineering summary report."
    )


    st.divider()


    # =====================================================
    # CHECK DIGITAL TWIN DATA
    # =====================================================


    if "twin" not in st.session_state:


        st.warning(
            "Run Manual Prediction before generating report."
        )


        return



    twin = st.session_state["twin"]


    if not twin["valid"]:


        st.error(
            "Prediction data is invalid."
        )


        return



    # =====================================================
    # EXTRACT DATA
    # =====================================================


    inputs = twin["inputs"]

    warnings = twin["warnings"]

    recommendations = twin["recommendations"]


    report_date = datetime.now().strftime(
        "%d-%m-%Y"
    )


    report_time = datetime.now().strftime(
        "%H:%M:%S"
    )
        # =====================================================
    # GENERATE REPORT BUTTON
    # =====================================================


    generate = st.button(
        "Generate Engineering Report",
        use_container_width=True
    )


    if not generate:

        return



    # =====================================================
    # CREATE PDF DOCUMENT
    # =====================================================


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



    # =====================================================
    # GASONET LOGO
    # =====================================================


    logo = Image(
        "assets/gasonet_logo.png"
    )


    logo.drawWidth = 2.2 * inch

    logo.drawHeight = 0.9 * inch

    logo.hAlign = "CENTER"


    story.append(
        logo
    )


    story.append(
        Spacer(1,20)
    )



    # =====================================================
    # TITLE SECTION
    # =====================================================


    story.append(

        Paragraph(

            "AI DIGITAL TWIN ENGINEERING REPORT",

            styles["Title"]

        )

    )


    story.append(
        Spacer(1,15)
    )


    story.append(

        Paragraph(

            "Booster Compressor Health Prediction System",

            styles["Heading2"]

        )

    )


    story.append(
        Spacer(1,20)
    )



    story.append(

        Paragraph(

            "<b>Company:</b> Gasonet",

            styles["BodyText"]

        )

    )


    story.append(

        Paragraph(

            f"<b>Date:</b> {report_date}",

            styles["BodyText"]

        )

    )


    story.append(

        Paragraph(

            f"<b>Time:</b> {report_time}",

            styles["BodyText"]

        )

    )


    story.append(

        Spacer(1,25)

    )
        # =====================================================
    # EXECUTIVE SUMMARY
    # =====================================================


    story.append(

        Paragraph(

            "1. Executive Summary",

            styles["Heading1"]

        )

    )


    summary = f"""

The AI Digital Twin evaluated the Booster Compressor
operating condition using a Hybrid AI approach combining
Machine Learning prediction and Physics-Based Engineering
analysis.

<br/><br/>

Equipment Health : <b>{twin['health']:.1f}%</b>

<br/>

Prediction Confidence : <b>{twin['confidence']:.1f}%</b>

<br/>

Anomaly Status : <b>{twin['anomaly']}</b>

<br/>

Severity Level : <b>{twin['severity']}</b>

"""


    story.append(

        Paragraph(

            summary,

            styles["BodyText"]

        )

    )


    story.append(

        Spacer(1,20)

    )



    # =====================================================
    # PERFORMANCE SUMMARY
    # =====================================================


    story.append(

        Paragraph(

            "2. Compressor Performance Summary",

            styles["Heading1"]

        )

    )



    performance_data = [

        [
            "Parameter",
            "Value"
        ],

        [
            "Predicted Power",
            f"{twin['predicted_power']:.2f} kW"
        ],

        [
            "Predicted Energy",
            f"{twin['predicted_energy']:.2f} kWh"
        ],

        [
            "Equipment Health",
            f"{twin['health']:.1f}%"
        ],

        [
            "AI Confidence",
            f"{twin['confidence']:.1f}%"
        ],

    ]



    table = Table(

        performance_data,

        colWidths=[
            3 * inch,
            3 * inch
        ]

    )



    table.setStyle(

        TableStyle(

            [

                (
                    "BACKGROUND",
                    (0,0),
                    (-1,0),
                    colors.darkblue
                ),

                (
                    "TEXTCOLOR",
                    (0,0),
                    (-1,0),
                    colors.white
                ),

                (
                    "GRID",
                    (0,0),
                    (-1,-1),
                    0.5,
                    colors.black
                ),

                (
                    "ALIGN",
                    (0,0),
                    (-1,-1),
                    "CENTER"
                ),

            ]

        )

    )



    story.append(
        table
    )


    story.append(

        Spacer(1,25)

    )
        # =====================================================
    # OPERATING CONDITIONS
    # =====================================================


    story.append(

        Paragraph(

            "3. Operating Conditions",

            styles["Heading1"]

        )

    )


    operating_data = [

        [
            "Parameter",
            "Value"
        ],

        [
            "Suction Pressure",
            f"{inputs['suction']:.2f} bar"
        ],

        [
            "Discharge Pressure",
            f"{inputs['discharge']:.2f} bar"
        ],

        [
            "Voltage",
            f"{inputs['voltage']:.2f} V"
        ],

        [
            "Current",
            f"{inputs['current']:.2f} A"
        ],

        [
            "Flow Rate",
            f"{inputs['flow']:.2f} SCMH"
        ],

        [
            "Running Hours",
            f"{inputs['hmr']:.2f} hr"
        ]

    ]


    table = Table(

        operating_data,

        colWidths=[
            3 * inch,
            3 * inch
        ]

    )


    table.setStyle(

        TableStyle(

            [

                (
                    "BACKGROUND",
                    (0,0),
                    (-1,0),
                    colors.darkgreen
                ),

                (
                    "TEXTCOLOR",
                    (0,0),
                    (-1,0),
                    colors.white
                ),

                (
                    "GRID",
                    (0,0),
                    (-1,-1),
                    0.5,
                    colors.black
                ),

                (
                    "ALIGN",
                    (0,0),
                    (-1,-1),
                    "CENTER"
                )

            ]

        )

    )


    story.append(table)


    story.append(
        Spacer(1,25)
    )



    # =====================================================
    # HYBRID AI ANALYSIS
    # =====================================================


    story.append(

        Paragraph(

            "4. Hybrid AI Analysis",

            styles["Heading1"]

        )

    )


    hybrid_data = [

        [
            "Model",
            "Prediction"
        ],

        [
            "Machine Learning Model",
            f"{twin['ml_power']:.2f} kW"
        ],

        [
            "Physics-Based Model",
            f"{twin['physics_power']:.2f} kW"
        ],

        [
            "Model Difference",
            f"{twin['model_difference']:.2f} kW"
        ]

    ]


    table = Table(

        hybrid_data,

        colWidths=[
            3 * inch,
            3 * inch
        ]

    )


    table.setStyle(

        TableStyle(

            [

                (
                    "BACKGROUND",
                    (0,0),
                    (-1,0),
                    colors.darkblue
                ),

                (
                    "TEXTCOLOR",
                    (0,0),
                    (-1,0),
                    colors.white
                ),

                (
                    "GRID",
                    (0,0),
                    (-1,-1),
                    0.5,
                    colors.black
                ),

                (
                    "ALIGN",
                    (0,0),
                    (-1,-1),
                    "CENTER"
                )

            ]

        )

    )


    story.append(table)


    story.append(

        Spacer(1,25)

    )
        # =====================================================
    # ENGINEERING ALARMS
    # =====================================================


    story.append(

        Paragraph(

            "5. Engineering Alarms",

            styles["Heading1"]

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


        for i, alarm in enumerate(
            warnings,
            start=1
        ):


            story.append(

                Paragraph(

                    f"ALM-{i:03d} | {alarm}",

                    styles["BodyText"]

                )

            )


    story.append(

        Spacer(1,20)

    )



    # =====================================================
    # MAINTENANCE RECOMMENDATIONS
    # =====================================================


    story.append(

        Paragraph(

            "6. Maintenance Recommendations",

            styles["Heading1"]

        )

    )


    if len(recommendations) == 0:


        story.append(

            Paragraph(

                "No maintenance action is currently required.",

                styles["BodyText"]

            )

        )


    else:


        for recommendation in recommendations:


            story.append(

                Paragraph(

                    recommendation,

                    styles["BodyText"]

                )

            )



    story.append(

        Spacer(1,20)

    )



    # =====================================================
    # FINAL DIGITAL TWIN ASSESSMENT
    # =====================================================


    story.append(

        Paragraph(

            "7. Final Digital Twin Assessment",

            styles["Heading1"]

        )

    )


    if twin["health"] >= 90:


        conclusion = """

The Booster Compressor is operating under healthy conditions.

The AI Digital Twin indicates stable operation with no immediate
maintenance requirement.

"""


    elif twin["health"] >= 75:


        conclusion = """

The Booster Compressor is operating within acceptable limits.

Preventive maintenance monitoring is recommended.

"""


    else:


        conclusion = """

The Booster Compressor health is below the recommended limit.

Maintenance inspection should be scheduled.

"""


    story.append(

        Paragraph(

            conclusion,

            styles["BodyText"]

        )

    )



    story.append(

        Spacer(1,25)

    )



    # =====================================================
    # REPORT FOOTER
    # =====================================================


    story.append(

        Paragraph(

            "Generated by Gasonet AI Digital Twin Platform",

            styles["Heading2"]

        )

    )


    story.append(

        Paragraph(

            f"Report generated on {report_date} at {report_time}",

            styles["BodyText"]

        )

    )



    # =====================================================
    # BUILD PDF
    # =====================================================


    doc.build(story)


    pdf_data = pdf_buffer.getvalue()


    pdf_buffer.close()



    st.success(

        "Engineering Report Generated Successfully."

    )



    st.download_button(

        label="Download Engineering Report",

        data=pdf_data,

        file_name=f"Gasonet_AI_Digital_Twin_Report_{report_date}.pdf",

        mime="application/pdf",

        use_container_width=True

    )