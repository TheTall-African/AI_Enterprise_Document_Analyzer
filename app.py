import streamlit as st
import pandas as pd

from analyzer import analyze_document, extract_text
from chunker import chunk_text
from embeddings import create_embedding
from vector_store import(add_chunk, search_chunks, clear_collection)
from rag import generate_rag_answer

#This "if" statement is to handle the case of any docs that may still be stored in the db
if "documents_indexed" not in st.session_state:
    st.session_state.documents_indexed = False
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

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
# CLEAR BUTTON
# -------------------------------------------------
if st.button("Clear Document Index"):
    clear_collection()
    st.session_state.documents_indexed = False
    st.session_state.uploader_key += 1
    st.success("All uploaded files cleared.")
    st.rerun()

# -------------------------------------------------
# FILE UPLOAD
# -------------------------------------------------

uploaded_files = st.file_uploader(
    "Upload policy or control documents",
    type=["txt", "pdf"],
    accept_multiple_files=True, 
    key=f"document_uploader_{st.session_state.uploader_key}"
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
#  INDEX DOCUMENTS BUTTON
# -------------------------------------------------
st.divider()

st.subheader(
    "Document Search Setup"
)

if st.button("Index Documents for Search"):
    if not documents:
        st.warning("Please upload documents first.")
    else:
        total_chunks= 0

        for document_index, document in enumerate(documents):
            filename = document["filename"]
            text = document["text"]

            if not text.strip():
                continue

            #Step 1. Split document into chunks
            chunks = chunk_text(text)

            #Step 2. Process each chunk
            for chunk_index, chunk in enumerate(chunks):
                #Step 3. Convert chunk into embedding
                embedding = create_embedding(chunk)

                #Step 4. Create unique ID for chunk
                chunk_id = (f"{document_index}_"
                            f"{chunk_index}_"
                            f"{filename}"
                )

                #Step 5. Store chunk and embedding
                add_chunk(chunk_id = chunk_id,
                          text = chunk,
                          embedding = embedding,
                          filename = filename
                          )
                total_chunks += 1

        st.success(f"Indexed {total_chunks} chunks successfully.")
        st.session_state.documents_indexed = True


# -------------------------------------------------
# SEARCH BUTTON - questioning the model (most confusing feature, must understand)
# -------------------------------------------------
st.subheader("Search your documents")

user_question = st.text_input("Ask a question about the uploaded documents")
#right after this is where the search functionality will be implemented to answer the user's question

if st.button("Question Documents"):
    if not st.session_state.documents_indexed:
        st.warning("Please upload and index documents before searching.")
    elif not user_question.strip():
        st.warning("Please enter your question.")
    else:
        with st.spinner("Searching documents..."):
            question_embedding = create_embedding(user_question)

            results = search_chunks(
                question_embedding,
                number_of_results = 3
            )

        st.subheader("Most Relevant Document Chunks")

        documents_found = results.get(
            "documents", [[]]
        )[0]

        metadata_found = results.get(
            "metadatas", [[]]
        )[0]

        distances = results.get(
            "distances", [[]]
        )[0]

        if not documents_found:
            st.warning("No relevant document content was found.")
        else:
            with st.spinner("Generating answer..."):
                rag_answer = generate_rag_answer(user_question, documents_found)

            st.subheader("Answer")

            st.write(rag_answer)

            st.subheader("Sources:")

            source_files = set()

            for metadata in metadata_found:
                filename = metadata.get("filename", "Unknown")
                source_files.add(filename)

            for filename in source_files:
                st.write(f"- {filename}")

            with st.expander("View Retrieval Debug Information"):

                for index, chunk in enumerate(documents_found):
                    filename = metadata_found[index].get("filename", "Unknown")

                    st.write(f"### Result {index + 1}")

                    st.write(f"**Source:** {filename}")

                    st.write(
                        f"**Distance:** "
                        f"{distances[index]:.4f}"
                    )

                    st.write(chunk)

                    st.divider()

st.subheader("Analyze your documents")
st.write("Click the button below to pull key facts about your documents such as:")
st.write("document type, business function, major risks, controls, and other key risk information.")

# -------------------------------------------------
# ANALYZE BUTTON
# -------------------------------------------------

if st.button("Analyze"):


    # ---------------------------------------------
    # CASE 1: USER UPLOADED FILES
    # ---------------------------------------------

    if documents:

        for index, document in enumerate(documents):

            filename = document["filename"]

            text = document["text"]


            if not document["text"].strip():

                st.warning(
                    f"No readable text found in {filename}."
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
                f"{index}_{filename}"
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