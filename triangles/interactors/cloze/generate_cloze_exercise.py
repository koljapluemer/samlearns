import string
from typing import Dict


def generate_cloze_exercise(template_string:str, correct_answer_string:str) -> Dict[str, str]:
    # return both the template with "___" replacing the correct answer
    # and the correct answer itself
    # important: the correct_answer_string may contain punctuation at the beginning or end
    # this punctuation should NOT be included in the returned correct answer
    # it should also NOT be replaced in the template
    # so ("I love dogs.", "dogs.") should return {"template": "I love ___.", "answer": "dogs"}
    
    # Find the correct answer in the template
    if correct_answer_string not in template_string:
        raise ValueError("Correct answer string must be present in template string")
    
    # Strip punctuation from the correct answer
    stripped_answer = correct_answer_string.strip(string.punctuation)
    
    # Replace the full correct answer (with punctuation) with "___"
    modified_template = template_string.replace(correct_answer_string, "___")
    
    return {"template": modified_template, "answer": stripped_answer} 