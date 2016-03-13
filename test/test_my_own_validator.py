# -*- coding: utf-8 -*-
from anchorman import annotate, clean, get_config
from anchorman.generator.candidate import data_val
from anchorman.configuration import parse_yaml

DATA = parse_yaml('data.yaml', loaded_from=__file__)


def my_validator(item, candidates, this_unit, setting):
    """Write your own validator based on this values.

    You can write your own validator function, because you get access to the
    following values. Pass values via setting if needed.

    Args:
        item (Interval): Interval(65, 68, ('dog', ('entity', {'dog': {'score': 12.0, 'type': 'animal', 'value': '/wiki/dog'}})))
        candidates (list): [Interval(21, 27, ('q\xc3\xbcick', ('entity', {'q\xc3\xbcick': {'score': 0.2, 'type': 'term', 'value': '/wiki/queick'}}))), Interval(34, 37, ('fox', ('entity', {'fox': {'score': 23.0, 'type': 'animal', 'value': '/wiki/fox'}}))), Interval(60, 64, ('lazy', ('entity', {'lazy': {'score': 5.55, 'type': 'term', 'value': '/wiki/lazy'}})))]
        this_unit (list): [Interval(60, 64, ('lazy', ('entity', {'lazy': {'score': 5.55, 'type': 'term', 'value': '/wiki/lazy'}})))]
        setting (dict): {'mode': 'highlight', 'element_identifier': 'entity', 'text_unit': {'name': 'html-paragraph', 'key': 'p', 'number_of_items': None}, 'longest_match_first': True, 'replaces_at_all': None, 'case_sensitive': True}

    Returns:
        bool: True if element is valid candidate, False otherwise.
    """

    values = data_val(item, None)
    score = values['score']
    _type = values['type']

    return True if score >= 42.0 and _type == 'city' else False


def test_annotate_own_validator_from_outside():
    """Test annotate with an own validator."""

    cfg = get_config()
    cfg['setting'].update({'mode': 'highlight'})
    two_paragraphs = DATA['two_paragraphs'].encode('utf-8')
    highlight_elements = DATA['elements']

    annotated = annotate(two_paragraphs, highlight_elements,
                         own_validator=[my_validator], config=cfg)

    expected_result = DATA['two_paragraphs_LA_annotated'].encode('utf-8')
    assert annotated == expected_result