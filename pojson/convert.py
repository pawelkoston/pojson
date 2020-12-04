import simplejson
import polib
import os
import argparse

def po2dict(po, skip_headers=False, flat=False, keep=False):
    """Convert po object to dictionary data structure (ready for JSON).
    """
    result = {}
    if not skip_headers:
        result[''] = po.metadata.copy()
    if flat:
        for entry in po:
            result[entry.msgid] = entry.msgstr
        return result

    for entry in po:
        if entry.obsolete and not keep:
            continue

        if entry.msgctxt:
            key = u'{0}\x04{1}'.format(entry.msgctxt, entry.msgid)
        else:
            key = entry.msgid

        if entry.msgstr:
            result[key] = [None, entry.msgstr]
        elif entry.msgstr_plural:
            plural = [entry.msgid_plural]
            result[key] = plural
            ordered_plural = sorted(entry.msgstr_plural.items())
            for order, msgstr in ordered_plural:
                plural.append(msgstr)
    return result

def convert(po_file, encoding=None, pretty_print=False, skip_headers=False, flat=False, keep=False):
    if encoding is None:
        po = polib.pofile(po_file,
                          autodetect_encoding=True)
    else:
        po = polib.pofile(po_file,
                          autodetect_encoding=False,
                          encoding=encoding)

    data = po2dict(po, skip_headers, flat, keep)

    if not pretty_print:
        result = simplejson.dumps(data, ensure_ascii=False, sort_keys=True)
    else:
        result = simplejson.dumps(data, sort_keys=True, indent=4 * ' ',
                                  ensure_ascii=False)
    return result


