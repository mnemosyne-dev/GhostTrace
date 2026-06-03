try:
    from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image
)
    from reportlab.lib.styles import getSampleStyleSheet
except ImportError:
    raise ImportError(
        "reportlab is required to generate PDF reports. Install with: pip install reportlab"
    )

from datetime import datetime

from sympy import content


def create_pdf_report(data):

    filename = "GhostTrace_Report.pdf"

    pdf = SimpleDocTemplate(
        filename
    )

    styles = getSampleStyleSheet()

    content = []


    # TITLE
    content.append(
        Paragraph(
            "GhostTrace Privacy Audit Report",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1,20)
    )


    # DATE
    content.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]))


    content.append(
        Spacer(1,20)
    )


    # SUMMARY
    summary = f"""
    <b>SCAN SUMMARY</b><br/><br/>

    Files Scanned: {data["files"]}<br/>
    Risky Files: {data["risky"]}<br/>
    Threats Found: {data["threats"]}<br/>
    Risk Score: {data["score"]}/1000<br/>
    Risk Level: {data["level"]}<br/>
    """


    content.append(
        Paragraph(
            summary,
            styles["Normal"]
        )
    )


    content.append(
        Spacer(1,20)
    )


    # RECOMMENDATION

    recommendation = """
    <b>SECURITY RECOMMENDATIONS</b>
    <br/><br/>

    - Rotate leaked passwords and API keys<br/>
    - Remove exposed sensitive documents<br/>
    - Use encrypted storage<br/>
    - Avoid storing credentials in plain text<br/>
    - Review privacy exposure regularly<br/>
    """


    content.append(
        Paragraph(
            recommendation,
            styles["Normal"]
        )
    )

    if "risk_graph" in data:
        content.append(
            Paragraph(
                "Risk Overview Graph",
                styles["Heading2"]
            )
        )

        content.append(
            Image(
                data["risk_graph"],
                width=300,
                height=200
            )
        )

    if "threat_graph" in data:
        content.append(
            Paragraph(
                "Threat Analysis Graph",
                styles["Heading2"]
            )
        )

        content.append(
            Image(
                data["threat_graph"],
                width=300,
                height=200
            )
        )

    pdf.build(
        content
    )

    return filename