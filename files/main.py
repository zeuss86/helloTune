"""
main.py - Streamlit front end for the Audio and Document Converter.

Run with:  python -m streamlit run main.py
"""

import shutil

import streamlit as st

import converters as cv
from styles import CSS, EMPTY_MP3, EMPTY_PDF, MASTHEAD, READY_NOTE

st.set_page_config(
    page_title="Audio and Document Converter", page_icon="🎧", layout="wide"
)
st.markdown(CSS, unsafe_allow_html=True)

LONG_TEXT_CHARS = 100_000  # beyond this, speech generation takes several minutes


# --------------------------------------------------------------------------- #
# Small helpers
# --------------------------------------------------------------------------- #
def file_signature(uploaded) -> str:
    """Identify an upload so we only re-process it when the file changes."""
    return f"{uploaded.name}:{uploaded.size}"


def file_stem(name: str) -> str:
    return name.rsplit(".", 1)[0] if "." in name else name


def progress_bar(label: str):
    """Return (bar, update). `update(fraction)` is passed to the converters."""
    bar = st.progress(0.0, text=label)

    def update(fraction: float) -> None:
        bar.progress(min(max(fraction, 0.0), 1.0), text=label)

    return bar, update


def format_duration(seconds) -> str:
    if not seconds:
        return "Unknown"
    minutes, secs = divmod(int(seconds), 60)
    return f"{minutes}:{secs:02d}"


def status_line(ok: bool, ready_text: str, missing_text: str) -> str:
    state = "on" if ok else "off"
    return f'<div class="status {state}"><span></span>{ready_text if ok else missing_text}</div>'


# --------------------------------------------------------------------------- #
# Sidebar
# --------------------------------------------------------------------------- #
def render_sidebar() -> None:
    with st.sidebar:
        st.markdown("### How it works")
        st.write(
            "PDF to MP3 reads a document aloud. MP3 to Text transcribes a "
            "recording. Files are processed in memory and are not saved."
        )

        st.markdown("### Privacy")
        st.write(
            "Whisper runs entirely on this machine. Speech generation and the "
            "Google transcription engine send content to Google's services."
        )

        st.markdown("### Components")
        st.markdown(
            status_line(
                cv.whisper_available(),
                "Whisper is installed",
                "Whisper is not installed",
            )
            + status_line(
                bool(shutil.which("ffmpeg")),
                "ffmpeg is installed",
                "ffmpeg not found (Google engine only)",
            ),
            unsafe_allow_html=True,
        )


# --------------------------------------------------------------------------- #
# Tab 1: PDF to MP3
# --------------------------------------------------------------------------- #
def generate_audio(text: str, lang: cv.Language, slow: bool, source_name: str) -> None:
    bar, update = progress_bar("Generating speech")
    try:
        with st.spinner(
            "Converting text to speech. Long documents can take a few minutes."
        ):
            audio = cv.text_to_mp3(text, lang.tts, slow, update)
        st.session_state["tts_result"] = {
            "audio": audio,
            "name": f"{file_stem(source_name)}.mp3",
            "language": lang.name,
        }
    except cv.ConversionError as exc:
        st.error(str(exc))
    finally:
        bar.empty()


def render_pdf_to_mp3() -> None:
    left, right = st.columns(2, gap="large")

    with left, st.container(key="card_pdf_input"):
        st.subheader("Upload a PDF")
        pdf = st.file_uploader(
            "PDF file",
            type=["pdf"],
            key="pdf_upload",
            label_visibility="collapsed",
            help=f"Drag and drop, or browse. Up to {cv.MAX_UPLOAD_MB} MB.",
        )

        ready = False
        if pdf is None:
            # File removed: forget everything derived from it.
            for key in ("pdf_sig", "tts_result"):
                st.session_state.pop(key, None)
        else:
            signature = file_signature(pdf)
            if st.session_state.get("pdf_sig") != signature:
                st.session_state.pop("tts_result", None)
                bar, update = progress_bar("Reading pages")
                try:
                    text, pages = cv.extract_pdf_text(pdf.getvalue(), update)
                    if not text:
                        raise cv.ConversionError(
                            "No selectable text was found. Scanned PDFs are images, "
                            "so they need OCR before they can be read aloud."
                        )
                    st.session_state.update(
                        pdf_sig=signature, pdf_text=text, pdf_pages=pages
                    )
                except cv.ConversionError as exc:
                    st.session_state.pop("pdf_sig", None)
                    st.error(str(exc))
                finally:
                    bar.empty()
            ready = st.session_state.get("pdf_sig") == signature

        if ready:
            current = st.session_state["pdf_text"]
            col1, col2, col3 = st.columns(3)
            col1.metric("Pages", st.session_state["pdf_pages"])
            col2.metric("Words", f"{len(current.split()):,}")
            col3.metric("Characters", f"{len(current):,}")

            pick, slow_col = st.columns([3, 2], vertical_alignment="bottom")
            lang = pick.selectbox(
                "Voice language",
                cv.LANGUAGES,
                format_func=lambda l: l.name,
                key="tts_lang",
            )
            slow = slow_col.checkbox("Speak slowly", key="tts_slow")

            if len(current) > LONG_TEXT_CHARS:
                st.warning(
                    "This is a long document. Generating the audio may take several minutes."
                )

            if st.button("Generate MP3", type="primary"):
                generate_audio(st.session_state["pdf_text"], lang, slow, pdf.name)

            with st.expander("Review or edit the text"):
                st.text_area(
                    "Text to be read aloud",
                    key="pdf_text",
                    height=260,
                    label_visibility="collapsed",
                )

    with right, st.container(key="card_pdf_output"):
        st.subheader("Your audio")
        result = st.session_state.get("tts_result")
        if result:
            st.markdown(
                READY_NOTE.format("Your audio is ready."), unsafe_allow_html=True
            )
            st.audio(result["audio"], format="audio/mp3")
            col1, col2 = st.columns(2)
            col1.metric("Voice", result["language"])
            col2.metric("File size", f"{len(result['audio']) / 1024:,.0f} KB")
            st.download_button(
                "Download MP3",
                result["audio"],
                file_name=result["name"],
                mime="audio/mpeg",
                type="primary",
            )
        else:
            st.markdown(EMPTY_PDF, unsafe_allow_html=True)


# --------------------------------------------------------------------------- #
# Tab 2: MP3 to Text
# --------------------------------------------------------------------------- #
def render_mp3_to_text() -> None:
    left, right = st.columns(2, gap="large")

    with left, st.container(key="card_mp3_input"):
        st.subheader("Upload an MP3")
        mp3 = st.file_uploader(
            "MP3 file",
            type=["mp3"],
            key="mp3_upload",
            label_visibility="collapsed",
            help=f"Drag and drop, or browse. Up to {cv.MAX_UPLOAD_MB} MB.",
        )

        data = None
        if mp3 is None:
            for key in ("mp3_sig", "stt_result"):
                st.session_state.pop(key, None)
        else:
            signature = file_signature(mp3)
            if st.session_state.get("mp3_sig") != signature:
                st.session_state.pop(
                    "stt_result", None
                )  # new file, old transcript is stale
                st.session_state["mp3_sig"] = signature
            try:
                data = mp3.getvalue()
                cv.validate_upload(data, "mp3")
                st.audio(data, format="audio/mp3")  # preview of the uploaded file
            except cv.ConversionError as exc:
                data = None
                st.error(str(exc))

        whisper_ok = cv.whisper_available()
        engines = ["Whisper (runs on this machine)", "Google Web Speech (online)"]
        engine = st.radio(
            "Transcription engine",
            engines,
            index=0 if whisper_ok else 1,
            help="Whisper is more accurate and private. Google Web Speech is lighter but needs internet and ffmpeg.",
        )
        use_whisper = engine == engines[0]

        if use_whisper and not whisper_ok:
            st.warning(
                "Whisper is not installed. Run `pip install faster-whisper`, or choose Google Web Speech."
            )

        options = ([None] if use_whisper else []) + cv.LANGUAGES
        language = st.selectbox(
            "Spoken language",
            options,
            format_func=lambda l: "Detect automatically" if l is None else l.name,
        )

        model_size = "base"
        if use_whisper:
            with st.expander("Advanced settings"):
                model_size = st.selectbox(
                    "Model size",
                    ["tiny", "base", "small", "medium"],
                    index=1,
                    help="Larger models are more accurate but slower. The first run downloads the model.",
                )

        can_run = data is not None and not (use_whisper and not whisper_ok)
        if st.button("Transcribe audio", type="primary", disabled=not can_run):
            bar, update = progress_bar("Transcribing")
            try:
                with st.spinner(
                    "Transcribing. This can take a while for long recordings."
                ):
                    if use_whisper:
                        result = cv.transcribe_whisper(
                            data, model_size, language, update
                        )
                    else:
                        result = cv.transcribe_google(data, language, update)
                st.session_state["stt_result"] = {
                    "transcript": result,
                    "name": file_stem(mp3.name),
                }
                st.session_state["stt_text"] = result.text
            except cv.ConversionError as exc:
                st.error(str(exc))
            finally:
                bar.empty()

    with right, st.container(key="card_mp3_output"):
        st.subheader("Your transcript")
        saved = st.session_state.get("stt_result")
        if saved:
            transcript = saved["transcript"]
            current = st.session_state["stt_text"]

            st.markdown(
                READY_NOTE.format("Your transcript is ready. You can edit it below."),
                unsafe_allow_html=True,
            )
            col1, col2, col3 = st.columns(3)
            col1.metric("Language", transcript.language)
            col2.metric("Words", f"{len(current.split()):,}")
            col3.metric("Length", format_duration(transcript.duration))

            text = st.text_area(
                "Transcript", key="stt_text", height=300, label_visibility="collapsed"
            )

            txt_col, docx_col = st.columns(2)
            txt_col.download_button(
                "Download .txt",
                text.encode("utf-8"),
                file_name=f"{saved['name']}.txt",
                mime="text/plain",
                type="primary",
            )
            try:
                docx_col.download_button(
                    "Download .docx",
                    cv.text_to_docx(text, saved["name"]),
                    file_name=f"{saved['name']}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
            except cv.ConversionError as exc:
                docx_col.caption(str(exc))
        else:
            st.markdown(EMPTY_MP3, unsafe_allow_html=True)


# --------------------------------------------------------------------------- #
# Page layout
# --------------------------------------------------------------------------- #
render_sidebar()
st.markdown(MASTHEAD, unsafe_allow_html=True)
tab_pdf, tab_mp3 = st.tabs(["PDF to MP3", "MP3 to Text"])
with tab_pdf:
    render_pdf_to_mp3()
with tab_mp3:
    render_mp3_to_text()
