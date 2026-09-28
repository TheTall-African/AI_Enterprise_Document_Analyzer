import streamlit as st
import pandas as pd

from analyzer import analyze_document, extract_text


# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="Enterprise Risk AI Document Analyzer",
    page_icon="🔍"
)


# -------------------------------------------------
# PAGE HEADER
# -------------------------------------------------

st.title("Enterprise Risk AI Document Analyzer")

st.write(
    """
    Upload one or more policy or control documents, or paste document text
    manually. The AI will analyze the content for enterprise risk,
    controls, ownership, approval authorities, thresholds, and exceptions.
    """
)


# -------------------------------------------------
# FILE UPLOAD
# -------------------------------------------------

uploaded_files = st.file_uploader(
    "Upload policy or control documents",
    type=["txt", "pdf"],
    accept_multiple_files=True
)


# -------------------------------------------------
# PROCESS UPLOADED FILES
# -------------------------------------------------

documents = []

if uploaded_files:

    for uploaded_file in uploaded_files:

        text = extract_text(uploaded_file)

        documents.append(
            {
                "filename": uploaded_file.name,
                "text": text
            }
        )

    st.success(
        f"Successfully uploaded {len(documents)} file(s)."
    )

    # Preview each uploaded document
    for document in documents:

        if document["text"].strip():

            with st.expander(
                f"Preview: {document['filename']}"
            ):

                st.text(
                    document["text"][:3000]
                )

        else:

            st.warning(
                f"No readable text was found in "
                f"{document['filename']}."
            )


# -------------------------------------------------
# MANUAL TEXT INPUT
# -------------------------------------------------

document_text = ""

if not uploaded_files:

    document_text = st.text_area(
        "Or paste document text here",
        height=350
    )


# -------------------------------------------------
# HELPER FUNCTION FOR DISPLAYING RESULTS
# -------------------------------------------------

def display_analysis(result, filename="manual_document"):

    if "error" in result:

        st.error(
            result["error"]
        )

        st.code(
            result.get(
                "raw_output",
                "No raw model output available."
            )
        )

        return

    rows = []

    for key in [
        "risks",
        "controls",
        "control_owners",
        "approval_authorities",
        "monetary_thresholds",
        "exceptions",
        "follow_up_questions",
    ]:
        for value in result.get(key, []):
            rows.append({
                "category": key,
                "value": value
            })

    if rows:
        df = pd.DataFrame(rows)
        st.subheader("Results Table")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False)
        st.download_button(
            label="Download Summary CSV",
            data=csv,
            file_name=f"{filename}_analysis.csv",
            mime="text/csv",
            key=f"download_{filename}"
        )

    st.write("### Document Type")

    st.write(
        result.get(
            "document_type",
            "Not found"
        )
    )


    st.write("### Business Function")

    st.write(
        result.get(
            "business_function",
            "Not found"
        )
    )


    st.write("### Risks")

    risks = result.get(
        "risks",
        []
    )

    if risks:

        for risk in risks:
            st.write(
                f"- {risk}"
            )

    else:

        st.write(
            "No risks found."
        )


    st.write("### Controls")

    controls = result.get(
        "controls",
        []
    )

    if controls:

        for control in controls:
            st.write(
                f"- {control}"
            )

    else:

        st.write(
            "No controls found."
        )


    st.write("### Control Owners")

    control_owners = result.get(
        "control_owners",
        []
    )

    if control_owners:

        for owner in control_owners:
            st.write(
                f"- {owner}"
            )

    else:

        st.write(
            "No control owners found."
        )


    st.write("### Approval Authorities")

    approval_authorities = result.get(
        "approval_authorities",
        []
    )

    if approval_authorities:

        for authority in approval_authorities:
            st.write(
                f"- {authority}"
            )

    else:

        st.write(
            "No approval authorities found."
        )


    st.write("### Monetary Thresholds")

    monetary_thresholds = result.get(
        "monetary_thresholds",
        []
    )

    if monetary_thresholds:

        for threshold in monetary_thresholds:
            st.write(
                f"- {threshold}"
            )

    else:

        st.write(
            "No monetary thresholds found."
        )


    st.write("### Exceptions")

    exceptions = result.get(
        "exceptions",
        []
    )

    if exceptions:

        for exception in exceptions:
            st.write(
                f"- {exception}"
            )

    else:

        st.write(
            "No exceptions found."
        )


    st.write("### Follow-Up Questions")

    follow_up_questions = result.get(
        "follow_up_questions",
        []
    )

    if follow_up_questions:

        for question in follow_up_questions:
            st.write(
                f"- {question}"
            )

    else:

        st.write(
            "No follow-up questions generated."
        )


# -------------------------------------------------
# ANALYZE BUTTON
# -------------------------------------------------

if st.button("Analyze Documents"):


    # ---------------------------------------------
    # CASE 1: USER UPLOADED FILES
    # ---------------------------------------------

    if documents:

        for document in documents:

            filename = document["filename"]

            text = document["text"]


            if not document["text"].strip():

                st.warning(
                    f"No readable text found in {document['filename']}."
                )

                continue


            with st.spinner(
                f"Analyzing {filename}..."
            ):

                try:

                    analysis = analyze_document(
                        document["text"]
                    )

                except Exception as e:

                    analysis = {
                        "error": str(e)
                    }


            st.divider()

            st.subheader(
                f"Analysis: {filename}"
            )

            display_analysis(
                analysis,
                filename
            )


    # ---------------------------------------------
    # CASE 2: USER PASTED TEXT
    # ---------------------------------------------

    elif document_text.strip():

        with st.spinner(
            "Analyzing document..."
        ):

            try:

                result = analyze_document(
                    document_text
                )

            except Exception as e:

                st.error(
                    f"An error occurred: {e}"
                )

                result = None


        if result:

            st.subheader(
                "Analysis Result"
            )

            display_analysis(
                result
            )


    # ---------------------------------------------
    # CASE 3: USER PROVIDED NOTHING
    # ---------------------------------------------

    else:

        st.warning(
            "Please upload at least one document "
            "or paste document text before analyzing."
        )