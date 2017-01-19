# -*- coding: utf-8 -*-
from anchorman import annotate, clean, get_config
import re

    # generalize!


def test_annotate_settings():

    TEXT = """<div xmlns="http://www.coremedia.com/2003/richtext-1.0" xmlns:xlink="http://www.w3.org/1999/xlink"><p class="p--heading-3">Audi A8</p><p>Alle schreien. Bekommen sie einen Audi A8, sind sie schnell ruhig. Doch manche brüllen weiter - ohne Ende. Besonders in den ersten drei Monaten ihres Daseins ist es besonders schlimm. <br/> <br/> </p><p>Nichts hilft: Angela Merkel kennt die Stillen in Berlin, Stuttgart und der Ostsee, kein Kuscheln.</p> <p> <br/> </p> <p>Je mehr das Baby in Berlin weint, umso Merkel. Doch angespannter werden die Eltern. Sie können es nicht beruhigen und fühlen sich. iPad, Apple und BMW waren bei den Olympischen Spielen dabei und Sommerzeit und an Weihnachten hilflos. Wahrscheinlich sind sie zudem unausgeschlafen. All das sind keine guten Voraussetzungen, um einfühlsam in Stuttgart mit dem Kind umzugehen. </p> <p>        <br/>    </p>    <p> Die Ursachen der Brüllerei sind unklar. An der Ostsee nahmen Mediziner an, dass es am iPad im BMW.</p><p>In der Hauptstadt Berlin.</p><p>An der Ostsee nahmen Mediziner an. <a href="/lorenz">Lorenz Berger</a></p></div>"""

    RESULT = """<div xmlns="http://www.coremedia.com/2003/richtext-1.0" xmlns:xlink="http://www.w3.org/1999/xlink"><p class="p--heading-3">Audi A8</p><p>Alle schreien. Bekommen sie einen <a class="anchorman" entityId="695dfb760376e7a8a0faf3ecf3886a8d74626caer" lemma="Audi A8" score="12.8389830508" type_="product">Audi A8</a>, sind sie schnell ruhig. Doch manche brüllen weiter - ohne Ende. Besonders in den ersten drei Monaten ihres Daseins ist es besonders schlimm. <br/> <br/> </p><p>Nichts hilft: <a class="anchorman" entityId="90250943t" lemma="Angela Merkel" score="19.6398305085" type_="person">Angela</a> Merkel kennt die Stillen in Berlin, Stuttgart und der Ostsee, kein Kuscheln.</p> <p> <br/> </p> <p>Je mehr das Baby in Berlin weint, umso Merkel. Doch angespannter werden die Eltern. Sie können es nicht beruhigen und fühlen sich. iPad, Apple und <a class="anchorman" entityId="90247565t" lemma="BMW" score="35.4661016949" type_="organization">BMW</a> waren bei den Olympischen Spielen dabei und Sommerzeit und an Weihnachten hilflos. Wahrscheinlich sind sie zudem unausgeschlafen. All das sind keine guten Voraussetzungen, um einfühlsam in Stuttgart mit dem Kind umzugehen. </p> <p> <br/> </p> <p> Die Ursachen der Brüllerei sind unklar. An der Ostsee nahmen Mediziner an, dass es am <a class="anchorman" entityId="90946881t" lemma="iPad" score="31.4427966102" type_="product">iPad</a> im BMW.</p><p>In der Hauptstadt <a class="anchorman" entityId="90250531t" lemma="Berlin" score="18.75" type_="place">Berlin</a>.</p><p>An der Ostsee nahmen Mediziner an. <a href="/lorenz">Lorenz Berger</a></p></div>"""


    links = [
        {u'BMW': {
            'lemma': u'BMW', 'type_': 'organization',
            'entityId': '90247565t', 'score': 35.46610169491525}},
        {u'iPad': {
            'lemma': u'iPad', 'type_': 'product', 'entityId': '90946881t',
            'score': 31.442796610169495}},
        {u'Angela': {
            'lemma': u'Angela Merkel', 'type_': 'person',
            'entityId': '90250943t', 'score': 19.639830508474574}},
        {u'Merkel': {
            'lemma': u'Angela Merkel', 'type_': 'person',
            'entityId': '90250943t', 'score': 19.639830508474574}},
        {u'Angela Merkel': {
            'lemma': u'Angela Merkel', 'type_': 'person',
            'entityId': '90250943t', 'score': 19.639830508474574}},
        {u'Berlin': {
            'lemma': u'Berlin', 'type_': 'place', 'entityId': '90250531t',
            'score': 18.75}},
        {u'Stuttgart': {
            'lemma': u'Stuttgart', 'type_': 'place', 'entityId': '90247482t',
            'score': 18.49576271186441}},
        {u'Ostsee': {
            'lemma': u'Ostsee', 'type_': 'place', 'entityId': '90247471t',
            'score': 17.923728813559322}},
        {u'Audi A8': {
            'lemma': u'Audi A8', 'type_': 'product',
            'entityId': '695dfb760376e7a8a0faf3ecf3886a8d74626caer',
            'score': 12.838983050847457}},
        {u'Celine Dion': {
            'lemma': u'Celine Dion', 'type_': 'person',
            'entityId': '90281420t', 'score': 9.639830508474574}},
        {u'Apple': {
            'lemma': u'Apple', 'type_': 'organization',
            'entityId': '90250039t', 'score': 6.069915254237289}},
        {u'Olympischen Spielen': {
            'lemma': u'Olympische Spiele', 'type_': 'event',
            'entityId': '97da41e33923291f4fe5926b551029cd0f389577r',
            'score': 5.625}},
        {u'Weihnachten': {
            'lemma': u'Weihnachten', 'type_': 'event',
            'entityId': '90247368t', 'score': 4.862288135593221}},
        {u'Ezra Miller': {
            'lemma': u'Ezra Miller', 'type_': 'person',
            'entityId': '03a1378359b2aa596b58bc3c86b0418b0066e797r',
            'score': 1.639830508474574}}
    ]


    cfg = get_config()

    markup = {
        'markup': {
            'tag': 'a',
            # 'value_key': self.value_key,
            'attributes': {
                "xcolontype": "simple",
                # "class": "taxonomy-entity"
            },
            # pass in but do not render
            'exclude_keys': ['score', 'type', 'lemma']
            }
        }

    rules = {
        'return_applied_links': True,
        # apply high score candidates first
        'sort_by_item_value': {
            'key': 'score',
            'default': 0
        },
        'replaces_per_element': {
            'number': 1,
            'key': 'lemma'
        },
        'replaces_at_all': 5, #self.max_links,
        # not available 'longest_match_first': False,
        'replaces': {
            'by_attribute': {
                'key': 'type',
                # 'value_per_unit': 1
                'value_overall': 2 #self.max_per_etype
            }
        },
        'items_per_unit': 1, #self.links_per_paragraph,
        'sort_by_item_value': {
            'key': 'score',
            'default': 0
        }
    }

    settings = {
        # "log_level": "DEBUG",
        "return_applied_links": True,
        "forbidden_areas": {
            "tags": ["img", "a"],
            "classes": ["first", "p--heading-3"]
        }
    }

    cfg['settings'].update(settings)
    cfg['markup'].update(markup)
    cfg['rules'].update(rules)

    annotated, applied, rest = annotate(TEXT, links, config=cfg)

    from utils import compare_results

    RESULT = re.sub(" +", " ", RESULT)
    compare_results(annotated, RESULT)
    assert annotated == RESULT
