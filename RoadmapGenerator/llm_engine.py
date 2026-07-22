from ollama import chat

def stream_response(model_nameL: str, system_prompt: str, student_data: dict) -> None:
    """
    *purpose*: generates the llm response on given student data in chunks
    
    *inputs*:
    1. model_name: (string) = name of LLM to be used
    2. system_prompt: (string) = custom system prompt for LLM
    3. student_data: (dictionary) = input student data

    *output*: streaming llm text
    """

    stream = chat(
        model=model_nameL,
        messages=[
            {'role':'system', 'content': system_prompt},
            {'role': 'user',
            'content': f"Provide the detailed roadmap by analyzing given student data:\n {student_data}"}],
        stream=True,
    )

    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)