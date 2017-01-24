# -*- coding: utf-8 -*-
from anchorman import annotate, clean, get_config
from utils import fix_bs4_parsing_spaces
from tests.data.dummy import LINKS


def test_annotate_settings():
    """Test annotate elements with default and manipulated config."""

    text = """<p class="first">Intel analysis shows Putin approved election hacking.</p>\n<p>Russian President Vladimir Putin told a group of <b>foreign policy experts</b> in southern Russia on Thursday that Donald Trump's "extravagant behavior" is just his way of getting his <a class="another one">message</a> across to voters.</p><p><img src="/image.png" title="Vladimir Putin"> The image shows him riding a bear in novo sibirsk.</p><p>And another paragraph about <a href="/link">Vladimir Putin</a> but there is a link already.</p>"""

    expected = """<p class="first"><a class="anchorman" href="/intel" score="33.33" type="company">Intel</a> analysis shows <a class="anchorman" href="/putin" score="100.42" type="person">Putin</a> approved election hacking.</p>\n<p>Russian President <a class="anchorman" href="/putin" score="100.42" type="person">Vladimir Putin</a> told a group of <b>foreign policy experts</b> in southern <a class="anchorman" href="/russia" score="23.12" type="place">Russia</a> on Thursday that <a class="anchorman" href="/trump" score="89.06" type="person">Donald Trump</a>'s "extravagant behavior" is just his way of getting his <a class="another one">message</a> across to voters.</p><p><img src="/image.png" title="Vladimir Putin"/> The image shows him riding a bear in novo sibirsk.</p><p>And another paragraph about <a href="/link">Vladimir Putin</a> but there is a link already.</p>"""

    # use default settings
    annotated = annotate(text, LINKS)
    assert fix_bs4_parsing_spaces(annotated) == fix_bs4_parsing_spaces(expected)

    cleaned = clean(annotated)
    assert 'class="anchorman"' not in cleaned
    assert 'a class="another one"' in cleaned

    # # ---------------------------------
    # # 1. return applied links
    number_of_links_to_apply = 3
    cfg = get_config()
    # cfg['settings']['log_level'] = 'DEBUG'

    cfg['settings']['return_applied_links'] = True
    cfg['rules']['replaces_at_all'] = number_of_links_to_apply

    annotated, applied, rest = annotate(text, LINKS, config=cfg)

    # Moscow and Election is not in rest, it is not found in the string

    assert len(applied) == number_of_links_to_apply
    assert len(rest) == len(LINKS) - number_of_links_to_apply - 2
    assert annotated.count('a class="anchorman"') == number_of_links_to_apply

    # # ---------------------------------
    # # 5.2 keyword Election in text election
    cfg['rules']['case_sensitive'] = False
    cfg['rules']['replaces_at_all'] = None

    annotated, applied_links, rest = annotate(text, LINKS, config=cfg)
    assert '<a class="anchorman" href="/election" ' in annotated
    assert len(applied_links) == 6

    # # -------------------------------
    # # 3. items replace per paragraph

    # from now on, we count all existing links also

    cfg['rules']['items_per_unit'] = 1
    annotated, applied_links, rest = annotate(text, LINKS, config=cfg)
    assert len(applied_links) == 1


    # # -------------------------------
    # # 3. items replace per paragraph
    cfg['rules']['replaces_at_all'] = None
    cfg['rules']['items_per_unit'] = None

    n = 2
    annotated, applied_links, rest = annotate(text*n, LINKS*n, config=cfg)
    assert len(applied_links) == (len(LINKS)-1)*n

    n = 10
    annotated, applied_links, rest = annotate(text*n, LINKS*n, config=cfg)
    assert len(applied_links) == (len(LINKS)-1)*n


    # # -------------------------------
    # # 3. items replace at all
    cfg['rules']['replaces_per_element'] = {"number": 1, "key": "href"}
    cfg['rules']['replaces_at_all'] = None
    cfg['rules']['items_per_unit'] = None


    text2 = """<p>Intel analysis shows Putin approved election hacking.</p>\n<p>Russian President Vladimir Putin told a group of <b>foreign policy experts</b> in southern Russia on Thursday.</p><p>Vladimir Putin bought Intel stocks.</b>"""

    links2 = [
        {
            "Vladimir Putin": {
                "href": "/putin", "type": "person", "score": 100.42
            }
        },
        {
            "Putin": {
                "href": "/putin", "type": "person", "score": 100.42
            }
        },
        {
            "Intel": {
                "href": "/intel", "type": "company", "score": 33.33
            }
        }
    ]

    annotated, applied_links, rest = annotate(text2, links2, config=cfg)
    assert len(applied_links) == 2
