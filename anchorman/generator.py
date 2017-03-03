# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
from anchorman.utils import log


def create_element(candidate, config):
    """Create the element that will be inserted in the text.

    :param item:
    :param config:
    """
    exclude_keys = config['markup'].get('exclude_keys', [])
    attr = config['markup'].get('attributes', {}).items()

    _from, _to, token, element = candidate
    attr += element.items()
    attributes = None
    try:
        attributes = ['{}="{}"'.format(key, val)
                      for key, val in sorted(attr)
                      if key not in exclude_keys]
    except Exception as e:
        log("{}: {}".format(attr, e))

    anchor = '<{tag}{attributes}>{text}</{tag}>'.format(
        tag=config['markup']['tag'],
        attributes=' '+' '.join(attributes) if attributes else '',
        text=token)

    return _from, _to, token, anchor


def remove_elements(text, config):
    """Remove elements of text based on the markup specifications.

    :param config:
    :param text:
    """
    text_soup = BeautifulSoup(text, config['settings'].get('parser', 'lxml'))

    # use markup info to specify the element you want to find
    found = text_soup.findAll
    attributes = config['markup'].get('attributes')
    tag = config['markup'].get('tag')
    anchors = found(tag, attributes) if attributes else found(tag)

    for anchor in anchors:
        anchor_text = anchor.text.encode('utf-8')
        key, value = specified_or_guess(config['markup'], attributes)
        fuzzy_re = "<{0}[^>]*?{1}=\"{2}[^>]*?>{3}<\/{0}>".format(
            tag, key, value, anchor_text)
        # use re.sub vs replace to prevent encoding issues
        text = re.sub(fuzzy_re, anchor_text, text)

    return text


def specified_or_guess(markup, attributes):
    """"""
    identifier = markup.get('identifier')
    key, value = identifier.items()[0] if identifier else attributes.items()[0]
    return key, value #'{}="{}"'.format(key, value)


def augment_result(text, to_be_applied):
    """Augment the text with the elements in to be applied.

    :param text:
    :param to_be_applied:
    """
    to_be_applied = sorted(to_be_applied, reverse=True)
    log(str(to_be_applied))

    for _from, _to, token, anchor in to_be_applied:
        log("appling: {} {} {}".format(_from, _to, token))
        text = "{}{}{}".format(text[:_from], anchor, text[_to:])

    return text
