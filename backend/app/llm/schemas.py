from pydantic import BaseModel, Field

class CriterionResult(BaseModel):
    criterion: str
    score: int = Field(ge=0, le=10)
    evidence: str = ""
    reasoning: str
    found: bool
    
class JDCriteria(BaseModel):
    criteria: list[str]