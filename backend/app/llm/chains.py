from app.llm.client import get_llm
from app.llm.prompts import criteria_prompt, rubric_prompt
from app.llm.schemas import CriterionResult, JDCriteria
from app.rag.retriever import format_context


def extract_criteria(jd_text):
    if not jd_text or not jd_text.strip():
        raise ValueError("JD text cannot be empty")
    
    llm = get_llm().with_structured_output(JDCriteria)
    chain = criteria_prompt | llm
    result = chain.invoke({"jd_text": jd_text})
    return result.criteria


def score_criterion(criterion, chunks):
    llm = get_llm().with_structured_output(CriterionResult)
    chain = rubric_prompt | llm
    return chain.invoke(
        {
            "criterion": criterion,
            "context": format_context(chunks),
        }
    )
    
    
