import difflib

def tax_resolve(tax, synonyms, sensitivity=0.75):
    if (not synonyms) or tax in synonyms.values(): return tax
    all_taxes = synonyms.keys() + synonyms.values()
    scores = sorted([(key, difflib.SequenceMatcher(None, tax.lower(), key.lower()).ratio()) for key in all_taxes],
                    key=lambda s: s[1], reverse=True)
    top_score = scores[0]
    if top_score[1] >= sensitivity: return synonyms[top_score[0]] if top_score[0] in synonyms.keys() else top_score[0]
    return tax
