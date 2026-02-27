from typing import Union, List, Dict
from contract_extractor.core.pipeline import ExtractionPipeline

_pipeline = ExtractionPipeline()


def extract(
    pdf: Union[str, bytes],
    query: str,
    output_type: str,
    examples: List[Dict] = None
) -> Dict:
    return _pipeline.run(pdf, query, output_type)
