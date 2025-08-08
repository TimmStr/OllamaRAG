from langchain_core.documents import Document

from utils.nlp_utils import filter_stop_words, filter_signs, clean_text, chunk_text


def test_filter_stop_words():
    text = "Hallo mein Name ist Karl und ich lebe in Frankfurt."
    assert filter_stop_words(text) == "hallo name karl lebe frankfurt."


def test_filter_signs():
    text = "Hi there. I &hope /the \\weather! is fine."
    assert filter_signs(text) == "Hi there I hope the weather is fine"


def test_clean_text():
    doc = Document(page_content="Hello! This is a test. @#€%&123456")
    assert clean_text(doc) == Document(page_content="hello this is a test. €%123456")


def test_chunk_text():
    text = """Hat der alte Hexenmeister Sich doch einmal wegbegeben! Und nun sollen seine Geister
    Auch nach meinem Willen leben. Seine Wort’ und Werke
    Merkt’ ich und den Brauch, Und mit Geistesstärke
    Tu’ ich Wunder auch. 
    Walle! walle Manche Strecke,
    Daß zum Zwecke Wasser fließe,
    Und mit reichem, vollem Schwalle Zu dem Bade sich ergieße!
    Und nun komm, du alter Besen! Nimm die schlechten Lumpenhüllen!
    Bist schon lange Knecht gewesen; Nun erfülle meinen Willen!
    Auf zwei Beinen stehe, Oben sei ein Kopf,
    Eile nun und gehe Mit dem Wassertopf!"""
    result = chunk_text(text, chunk_size=10, overlap=2)
    expected = ['Hat der alte Hexenmeister Sich doch einmal wegbegeben!',
                'einmal wegbegeben! Und nun sollen seine Geister Auch nach meinem Willen leben.',
                'Willen leben. Seine Wort’ und Werke Merkt’ ich und den Brauch, Und mit Geistesstärke Tu’ ich Wunder auch.',
                'Wunder auch. Walle!',
                'auch. Walle! walle Manche Strecke, Daß zum Zwecke Wasser fließe, Und mit reichem, vollem Schwalle Zu dem Bade sich ergieße!',
                'sich ergieße! Und nun komm, du alter Besen!', 'alter Besen! Nimm die schlechten Lumpenhüllen!',
                'schlechten Lumpenhüllen! Bist schon lange Knecht gewesen; Nun erfülle meinen Willen!',
                'meinen Willen! Auf zwei Beinen stehe, Oben sei ein Kopf, Eile nun und gehe Mit dem Wassertopf!']
    assert result == expected
