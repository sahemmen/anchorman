# -*- coding: utf-8 -*-
import logging
import re
import time
from bs4 import BeautifulSoup
logger = logging.getLogger('anchorman')

try:
    from line_profiler import LineProfiler

    def do_profile(follow=[]):
        def inner(func):
            def profiled_func(*args, **kwargs):
                try:
                    profiler = LineProfiler()
                    profiler.add_function(func)
                    for f in follow:
                        profiler.add_function(f)
                    profiler.enable_by_count()
                    return func(*args, **kwargs)
                finally:
                    profiler.print_stats()
            return profiled_func
        return inner

except ImportError:
    def do_profile(follow=[]):
        "Helpful if you accidentally leave in production!"
        def inner(func):
            def nothing(*args, **kwargs):
                return func(*args, **kwargs)
            return nothing
        return inner


def timeit(method):
    def timed(*args, **kw):
        bench = []
        for r in xrange(3):
            ts = time.time()
            result = method(*args, **kw)
            te = time.time()
            bench.append(te - ts)
        print '%r \t\t%2.4f sec' % (method.__name__, sum(bench) / len(bench))
        return result
    return timed


def disabled(f):
    return f

timeit = disabled


def create_tag(c, d, rest_markup):
    tag = rest_markup.get('tag')
    return "<{}{}>{}</{}>".format(tag, ' x ', c, tag)


def log(msg, level=None, logger=logger):
    """Project logger.

    :param msg: Error message string.
    """
    # print logging._levelNames[logger.level] == 'INFO'
    # if logger.isEnabledFor(logging.DEBUG):
    if level == 'INFO':
        logger.info(msg)
    else:
        logger.debug(msg)


def set_and_log_level(log_level, logger=logger):
    """Log the global level via INFO at start."""
    logger.setLevel(logging.getLevelName('INFO'))
    log('log_level {}'.format(log_level), level='INFO')
    logger.setLevel(logging.getLevelName(log_level))


def tokens_as_re(elements, case_sensitive):
    """Generate a regex for all tokens."""
    def allforms(t):
        return list({t, t.lower(), t.upper(), t.title()})

    tokens = [e.keys()[0].encode('utf-8') for e in elements]
    forms = [[t] if case_sensitive else allforms(t) for t in tokens]
    patterns = [r"\b{0}\b".format(f) for form in forms for f in form]
    return "|".join(patterns)


def check_tags(a_tag, the_tag_str, filter_tags, soup_str):
    """ """
    if a_tag.name in filter_tags:
        try:
            _from = soup_str.index(the_tag_str)
            return (_from, _from + len(the_tag_str), a_tag.text)
        except ValueError as e:
            log("substring not found: {}, {}".format(a_tag, e))
    return None


def check_classes(a_tag, the_tag_str, filter_classes, soup_str):
    """ """
    try:
        _from = soup_str.index(the_tag_str)
        tag_classes = dict(a_tag.attrs).get('class', '')
        return [(_from, _from + len(the_tag_str), None)
                for fclass in filter_classes
                for tclass in tag_classes
                if fclass in tclass]
    except ValueError as e:
        log("substring not found: {}, {}".format(a_tag, e))
    return []


def sort_em(sort_by_item_value, elements, index):
    """ """
    if sort_by_item_value:
        key = sort_by_item_value['key']
        default = sort_by_item_value['default']
        return sorted(elements,
                      key=lambda tup: tup[index].get(key, default),
                      reverse=True)
    return elements


def saturated_unit(items_per_unit, old_links, u_from, u_to, unit_candidates):
    if items_per_unit:
        if len(unit_candidates) == items_per_unit:
            return True
        # check against the old_links in this unit
        if old_links:
            count_old_links = len(unit_candidates)
            for k, v in old_links.iteritems():
                _f, _t = v
                if u_from < _f and _t < u_to:
                    count_old_links += 1
            if count_old_links >= items_per_unit:
                return True

    return False


def soup_it(text, settings):

    soup = BeautifulSoup(text, settings.get('parser', 'lxml'))
    soup_str = str(soup)
    prettify = False
    # clean up automated augmentation and we do not use prettify for now
    if prettify:
        # this totally change the input representation to indented structure
        # better to read, but may to much
        soup_str = soup.prettify()
        if soup_str.startswith('<html>\n <body>'):
            soup_str = soup_str[15:-16]
    else:
        # we lose all multiple whitespaces, there is no indentation finally
        # if there was in the input
        if soup_str.startswith('<html><body>'):
            soup_str = soup_str[12:-14]
    return soup, soup_str
