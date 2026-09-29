def chunk_text(text, chunk_size=1200, overlap=250):
    """
    Splits text into chunks while trying to preserve paragraph boundaries.
    """

    paragraphs = text.split("\n\n")

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:

        paragraph = paragraph.strip()

        if not paragraph:
            continue

        # If adding this paragraph still keeps us
        # within the desired chunk size, add it.
        if len(current_chunk) + len(paragraph) <= chunk_size:

            if current_chunk:
                current_chunk += "\n\n"

            current_chunk += paragraph

        else:

            # Save current chunk before starting another
            if current_chunk:
                chunks.append(current_chunk)

            # Preserve some overlap from the previous chunk
            overlap_text = current_chunk[-overlap:] if current_chunk else ""

            current_chunk = overlap_text + "\n\n" + paragraph

    # Add final remaining chunk
    if current_chunk:
        chunks.append(current_chunk)

    return chunks