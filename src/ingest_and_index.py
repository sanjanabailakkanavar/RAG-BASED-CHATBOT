import os
import fitz
import easyocr

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


# ==========================================
# CONFIG
# ==========================================

PDF_FOLDER = "data"
VECTORSTORE_PATH = "vectorstore"

# Initialize EasyOCR once
reader = easyocr.Reader(["en"], gpu=False)


# ==========================================
# PDF EXTRACTION + OCR FALLBACK
# ==========================================

def extract_text_with_ocr_fallback(pdf_path):

    documents = []

    pdf_name = os.path.basename(pdf_path)

    try:
        pdf = fitz.open(pdf_path)

    except Exception as e:
        print(f"Could not open {pdf_name}: {e}")
        return []

    print(f"\nProcessing: {pdf_name}")

    for page_num in range(len(pdf)):

        try:

            page = pdf.load_page(page_num)

            # Native text extraction
            text = page.get_text().strip()

            # OCR fallback only if page contains no extractable text
            if len(text.strip()) == 0:

                print(
                    f"OCR used -> {pdf_name} | Page {page_num + 1}"
                )

                pix = page.get_pixmap(
                    matrix=fitz.Matrix(2, 2)
                )

                image_path = f"temp_page_{page_num}.png"

                pix.save(image_path)

                try:

                    ocr_result = reader.readtext(
                        image_path,
                        detail=0
                    )

                    text = " ".join(ocr_result)

                except Exception as ocr_error:

                    print(
                        f"OCR Error on Page {page_num + 1}: "
                        f"{ocr_error}"
                    )

                finally:

                    if os.path.exists(image_path):
                        os.remove(image_path)

            # Store page if text exists
            if text:

                documents.append(
                    Document(
                        page_content=text,
                        metadata={
                            "filename": pdf_name,
                            "page": page_num + 1
                        }
                    )
                )

        except Exception as page_error:

            print(
                f"Error processing "
                f"{pdf_name} Page {page_num + 1}: "
                f"{page_error}"
            )

    return documents


# ==========================================
# LOAD ALL PDFS
# ==========================================

def load_all_documents():

    all_documents = []

    pdf_files = [
        file
        for file in os.listdir(PDF_FOLDER)
        if file.endswith(".pdf")
    ]

    print(f"\nFound {len(pdf_files)} PDFs")

    for pdf_file in pdf_files:

        pdf_path = os.path.join(
            PDF_FOLDER,
            pdf_file
        )

        docs = extract_text_with_ocr_fallback(
            pdf_path
        )

        all_documents.extend(docs)

    return all_documents


# ==========================================
# CHUNKING
# ==========================================

def create_chunks(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = splitter.split_documents(
        documents
    )

    return chunks


# ==========================================
# BUILD VECTOR STORE
# ==========================================

def build_vectorstore(chunks):

    print("\nLoading Embedding Model...")

    embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={
        "device": "cpu"
    }
)

    print("Creating FAISS Index...")

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    vectorstore.save_local(
        VECTORSTORE_PATH
    )

    print(
        f"\nFAISS Index Saved -> "
        f"{VECTORSTORE_PATH}"
    )


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    print(
        "\n========== INGESTION STARTED =========="
    )

    documents = load_all_documents()

    print(
        f"\nTotal Pages Loaded: "
        f"{len(documents)}"
    )

    chunks = create_chunks(
        documents
    )

    print(
        f"Total Chunks Created: "
        f"{len(chunks)}"
    )

    build_vectorstore(
        chunks
    )

    print(
        "\n========== INGESTION COMPLETED =========="
    )