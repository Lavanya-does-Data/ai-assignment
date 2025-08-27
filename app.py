from flask import Flask, render_template_string, request
from deep_translator import GoogleTranslator

app = Flask(__name__)

# HTML template
HTML = """
<!doctype html>
<title>AI Assignment Demo</title>
<h2>AI Assignment Input</h2>
<form method="post">
  Project Details: <input type="text" name="project"><br><br>
  <input type="submit" value="Generate Summary">
</form>
{% if summary %}
<hr>
<h3>Summary:</h3>
<p>{{ summary }}</p>
<h3>Translations:</h3>
<p><b>Arabic:</b> {{ ar }}</p>
<p><b>Hindi:</b> {{ hi }}</p>
<p><b>Hebrew:</b> {{ he }}</p>
{% endif %}
"""

# =====================
# AGENTS (simulated)
# =====================
def search_agent(project_text):
    # Simulate searching sources for project
    return f"Found relevant info for project: {project_text[:50]}"

def summary_agent(search_results):
    # Simulate summarization
    return f"Summary based on search: {search_results[:100]}..."

def formatting_agent(summary_text):
    # Simulate formatting (e.g., adding headers, structure)
    return f"***Formatted Summary***\n{summary_text}"

def translation_agent(summary_text):
    # Translate summary into multiple languages
    ar = GoogleTranslator(source='auto', target='ar').translate(summary_text)
    hi = GoogleTranslator(source='auto', target='hi').translate(summary_text)
    he = GoogleTranslator(source='auto', target='he').translate(summary_text)
    return ar, hi, he

# =====================
# ROUTE
# =====================
@app.route("/", methods=["GET", "POST"])
def home():
    summary = ar = hi = he = None
    if request.method == "POST":
        project_text = request.form.get("project")
        
        # Multi-agent flow
        search_results = search_agent(project_text)
        summary_text = summary_agent(search_results)
        formatted_summary = formatting_agent(summary_text)
        ar, hi, he = translation_agent(formatted_summary)
        summary = formatted_summary
        
    return render_template_string(HTML, summary=summary, ar=ar, hi=hi, he=he)

# =====================
# RUN
# =====================
if __name__ == "__main__":
    app.run(debug=True)
