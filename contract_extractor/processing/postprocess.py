import ast

class ValuesExtractor:
    def value_extractor(self, value, docs):
        if isinstance(value, str):
            try:
                dictt = ast.literal_eval(value)
                final_answer = dictt.get("answer", None)
                page_no = int(dictt.get("page_number", '0'))
                confidence_score = float(dictt.get("confidence_score", '0'))
                snippet = ''.join([l.get('content', '') for l in list(filter(lambda d: d['page_number'] == page_no, docs))])
                return final_answer, page_no, snippet, confidence_score
            except (ValueError, SyntaxError):
                return value, None, None, None
