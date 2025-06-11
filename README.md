# AI-Powered Documentation Extractor – Technical Documentation

---

## 📌 Technical Architecture Description

### 🏗️ Overall Design

This Streamlit application extracts structured information from documentation websites. It follows a modular architecture comprising four primary components:

1. **User Interface (Streamlit)**

   * Accepts one or more URLs.
   * Displays progress and outputs structured JSON results.

2. **Crawler Module (`app/crawler.py`)**

   * Recursively crawls all valid and relevant pages under the provided URL domain.
   * Handles edge cases like redirections, broken links, and duplicate visits.

3. **Extractor Module (`app/extractor.py`)**

   * Uses `BeautifulSoup` to extract main content from HTML, ignoring navigation, footer, ads, etc.
   * Parses headers (`<h1>`, `<h2>`), paragraphs (`<p>`), and lists (`<ul>`) into a structured format.

4. **Analyzer Module (`app/analyzer.py`)**

   * Sends the cleaned text content to the OpenAI GPT model.
   * Infers module/submodule hierarchy and generates meaningful descriptions.
   * Returns structured JSON in the required output format.

---

## ⚙️ Application Flow

```text
User Input (Streamlit UI) ──▶ Crawl URLs ──▶ Extract Content ──▶ GPT Inference ──▶ Display Structured JSON
```

---

## 💡 Notes on Approach

* **Content Extraction**:

  * Focuses on documentation-oriented tags (`<h1>`, `<h2>`, `<p>`, `<ul>`).
  * Filters out unrelated elements such as navigation bars, footers, and scripts.

* **Hierarchy Inference**:

  * Top-level `<h1>` elements are considered modules.
  * Nested `<h2>` tags and related content are grouped as submodules.

* **GPT-4o Integration**:

  * GPT is used to convert semi-structured HTML content into structured, human-readable JSON.
  * Input is chunked dynamically to prevent token overflow.

* **Performance**:

  * Pages are crawled sequentially, but processing each URL’s analysis begins after its crawl is complete (can be parallelized).
  * Only meaningful content is passed to the model to reduce token usage.

---

## ✅ Assumptions

1. Documentation websites are structured using semantic HTML tags.
2. Major documentation sections use `<h1>` for modules and `<h2>` for submodules.
3. OpenAI GPT model has access and sufficient quota.
4. All URLs share a consistent documentation structure within a domain.
5. Each help URL is independently valid and relevant.

---

## ⚠️ Edge Case Handling

* **Token Limitations**:

  * Input token limits are monitored. If exceeded, content is truncated or split.
  * Planned improvement: token estimation logic + chunked async processing.

* **Crawling Depth**:

  * Avoids infinite loops with visited link tracking.
  * Only processes URLs within the domain root.

* **Invalid/Unsupported URLs**:

  * Broken or redirected links are logged and skipped.

* **Non-HTML Pages**:

  * Pages with unsupported MIME types (PDFs, images) are ignored.

---

## 🧪 Testing

Tested against:

1. [https://support.neo.space/hc/en-us](https://support.neo.space/hc/en-us)
2. [https://wordpress.org/documentation/](https://wordpress.org/documentation/)
3. [https://help.zluri.com/](https://help.zluri.com/)
4. [https://www.chargebee.com/docs/2.0/](https://www.chargebee.com/docs/2.0/)

All tests successfully retrieved structured module/submodule hierarchies with GPT-generated descriptions.

---

## 📦 Deployment Notes

* Uses Streamlit for UI: `streamlit run app.py`
* Requires `.env` file with `OPENAI_API_KEY` set.
* Future improvement: Add FastAPI endpoint to serve as an API. Use Docker for easier deployment.
