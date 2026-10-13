
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


prompt = ChatPromptTemplate.from_template("""
You are an assistant answering questions about Tamil Nadu
Government schemes.

Strict rules:
1. Use only the supplied context. Never invent facts.
2. Distinguish the scheme's overall benefits from benefits
   explicitly associated with the user's crop or beneficiary.
3. Do not present benefits for groundnut, gingelly, sunflower,
   or other crops as maize-specific benefits unless the context
   explicitly confirms that they apply to maize.
4. If a scheme description combines benefits for several crops
   and does not clearly identify which apply to the requested crop,
   state that the applicability is unclear.
5. Do not infer eligibility from a scheme name.
6. If information is missing or inconsistent, disclose this clearly.
7. Include the source URL for every scheme discussed.
8. Do not claim that a benefit is currently available; advise users
   to verify current details with the relevant department.

Context:
{context}

User question:
{question}

Provide:
- Relevant scheme names and departments
- Benefits supported by the context
- Eligibility and application details only when documented
- Any uncertainty or conflicting information
- Official source URLs


DATA ACCURACY RULES:
1. Treat each scheme as an independent record.
2. Never copy eligibility criteria from one scheme to another.
3. Include eligibility details only when explicitly supported by that scheme's own context.
4. If eligibility or financial assistance is missing, state "Not specified in the available source."
5. Do not present information as verified if the source page is inconsistent or ambiguous.
6. Keep the source URL associated with the exact scheme it describes.
7. Include every distinct scheme returned in the provided context that is relevant to the user's question.
8. Do not silently omit a retrieved scheme. If a scheme is relevant but some financial details are missing, include the scheme and state that the financial assistance is not specified in the available source.
9. Before finalizing the answer, verify that every relevant scheme in the context appears in the response exactly once.
10. For schemes covering multiple crops, explain that the scheme covers multiple crops and do not assume every listed benefit applies specifically to the crop asked about unless the source confirms it.


""")


chain = prompt | llm


def generate_answer(question, schemes):
    if not schemes:
        return "No matching schemes were found in the available data."

    context_parts = []

    for scheme in schemes:
        context_parts.append(
                f"""
    Scheme: {scheme.get('scheme', 'Not available')}
    Department: {scheme.get('department', 'Not available')}
    Funding: {scheme.get('funding') or 'Not available'}
    Description: {scheme.get('description') or 'Not available'}
    Source: {scheme.get('source_url') or 'Not available'}
    """
            )

    
    context = "\n\n".join(
        f"""
    Scheme: {scheme.get('scheme') or 'Not specified'}
    Department: {scheme.get('department') or 'Not specified'}
    Financial Assistance: {scheme.get('funding') or 'Not specified'}
    Benefits: {scheme.get('benefits') or 'Not specified'}
    Description: {scheme.get('description') or 'Not specified'}
    Eligibility: {scheme.get('eligibility') or 'Not specified in the available source'}
    Application Process: {scheme.get('application_process') or 'Not specified in the available source'}
    Source URL: {scheme.get('source_url') or 'Not available'}
    """
        for scheme in schemes
    )


    response = chain.invoke({
        "context": context,
        "question": question
    })

    return response.content
