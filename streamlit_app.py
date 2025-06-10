import streamlit as st
from app.crawler import crawl
from app.extractor import extract_clean_content
from app.analyzer import gpt_infer_structure, split_text_into_chunks
from app.cache import load_from_cache, save_to_cache
import requests
import json
import time

st.title("📘 AI-powered Documentation Extractor")

urls = st.text_area("Enter documentation URLs (one per line):").splitlines()


def merge_modules(modules):
    merged = {}
    for module in modules:
        name = module["module"]
        if name not in merged:
            merged[name] = {
                "module": name,
                "Description": module["Description"],
                "Confidence": module.get("Confidence", 0.5),
                "Submodules": dict(module["Submodules"])
            }
        else:
            merged[name]["Submodules"].update(module["Submodules"])
            merged[name]["Confidence"] = max(
                merged[name]["Confidence"],
                module.get("Confidence", 0.5)
            )
            if len(module["Description"]) > len(merged[name]["Description"]):
                merged[name]["Description"] = module["Description"]
    return list(merged.values())


if st.button("Extract Modules"):
    for url in urls:
        if url.strip() == "":
            continue

        st.markdown(f"### 🔗 {url}")
        with st.spinner("🔍 Crawling..."):
            pages = crawl(url)

        full_text = ""
        for p in pages:
            try:
                html = requests.get(p, timeout=10).text
                sections = extract_clean_content(html)
                for sec_title, subs in sections.items():
                    full_text += f"{sec_title}\n"
                    for sub in subs:
                        full_text += f"{sub['title']}\n" + "\n".join(sub['content']) + "\n\n"
            except Exception as e:
                st.warning(f"Failed to process {p}: {e}")

        if full_text.strip():
            with st.spinner("🧠 Analyzing with GPT..."):
                chunks = split_text_into_chunks(full_text, max_tokens=2000)

                partial_outputs = []
                progress_container = st.empty()

                for i, chunk in enumerate(chunks):
                    cached = load_from_cache(chunk)
                    if cached:
                        out = cached
                    else:
                        try:
                            out = gpt_infer_structure(chunk)
                            save_to_cache(chunk, out)
                            time.sleep(2)
                        except Exception as e:
                            st.warning(f"Failed to process chunk {i + 1}: {e}")
                            continue

                    if isinstance(out, list):
                        partial_outputs.extend(out)
                    else:
                        partial_outputs.append(out)

                progress_container.success("✅ GPT Analysis Complete")

            merged_output = merge_modules(partial_outputs)
            with st.expander(f"📘 Extracted Modules for {url}"):

                st.json(merged_output)
                # Convert to JSON and download
                json_str = json.dumps(merged_output, indent=2)

                # Create a unique suffix using hash of the URL
                unique_id = str(abs(hash(url)))[:8]  # Get first 8 digits of positive hash

                # Create a safe filename
                file_name = f"module_structure_{unique_id}.json"

                # Show download button with unique filename
                st.download_button(
                    label="📥 Download JSON",
                    data=json_str,
                    file_name=file_name,
                    mime="application/json",
                    key=f"download_{unique_id}"
                )



        else:
            st.warning("No valid content extracted.")
