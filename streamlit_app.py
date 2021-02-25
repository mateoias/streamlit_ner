
#install dependencies
import os
import streamlit as st
import pandas as pd
import spacy
from spacy import displacy
nlp = spacy.load('en_core_web_md')
# use the beta model with BERT for better results
# zh_nlp = spacy.load('zh_core_web_trf')
zh_nlp = spacy.load('zh_core_web_sm')

# set the environment as huggingface (new) 3.0 throws an error
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Run the following to use Spacy's built in visualizer instead of returning raw text 
def header():
	st.title("Named Entity Checker")
	st.subheader("Named Entity Recognition with Spacy. Enter the text you would like to analyze. The app will detect and identify proper nouns; people, places, movies, etc.")
	st.write("The Chinese model is using a smaller version to save resources, so the Chinese version is less effective.")
def choose_language():
	option = ""
	option = st.selectbox('What language would you like to analyze?',
            ('', 'English', 'Chinese'))
	return option

def analyze_text(text, option):
	if option == 'English':
		return nlp(text)
	elif option == 'Chinese':
		return zh_nlp(text)


def label_explainer():
	st.header("Meanings of the labels")
	entity_labels = ["PERSON", "NORP", "FAC", "ORG",
                  "GPE", "LOC", "PRODUCT", "EVENT", "WORK_OF_ART",
                  "LANGUAGE", "MONEY", "LAW"]
	label_definitions = ["Person's name", "religious/political/national group names",
                      "Buildings, airports, bridges etc.", "companies and organizations",
                      "Countries, cities, states", "locations(mountains, lakes, etc", "Products", "named events(history, war, sports, etc.",
                      "Titles of movies, books, etc.", "any named language",
                      "names of money (dollar, etc.)", "names of laws and regulations"]
	label_dataframe = pd.DataFrame({'entity_labels': entity_labels})
	label_dataframe['label_definitions'] = label_definitions
	st.write(label_dataframe)


def main():
	"""Summarizer Streamlit App"""
	header()
	option = choose_language()
	labels = {"ents": ["PERSON", "NORP", "FAC", "ORG",
                    "GPE", "LOC", "PRODUCT", "EVENT", "WORK_OF_ART",
                    "LANGUAGE", "MONEY", "LAW"]}
	raw_text = st.text_area("Enter Text Here and press the Analyze button",  height=400)
	if st.button("Analyze"):
		doc = analyze_text(raw_text, option)
		html = displacy.render(doc, style="ent", options = labels)
		html = html.replace("\n\n", "\n")
		st.write(HTML_WRAPPER.format(html), unsafe_allow_html=True)
	label_explainer()



HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""
	

if __name__ == '__main__':
	main()
