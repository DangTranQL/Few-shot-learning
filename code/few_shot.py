import openai 
import pandas as pd
import time
import os
from embed import get_embeddings, get_most_similar
import csv

openai.api_key = "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"
openai.Model.list()

questions_per_course = 22
#Will use this many few-shot examples if possible: (if fewer are solved, use as many as possible)
codex_engine = "code-davinci-002"
engine_temperature = 0
engine_topP = 0
few_shot_max_tokens = 512
codex_time_delay = 3
course_location = 'C:/Users/ADMIN/Desktop/mathQ/code/csv/hw2.csv'
embeddings_location = 'C:/Users/ADMIN/Desktop/mathQ/code/embed_data.json'
columns = ["Id", "Question", "Solution", "ChatGPT Answer", "Grade 0/1", "List of questions from most to least similar (do this only for 0s and list only 1s)", "Few-shot answer"]

def execute_few_shot(questions_per):
    all_embeddings = get_embeddings(embeddings_location)
    results = pd.read_csv(course_location, encoding='ANSI')
    rows = []
    for i in range(questions_per):
        row = []
        r = []
        row = [results.iloc[i]["Id"], results.iloc[i]["Question"], results.iloc[i]["Solution"], results.iloc[i]["ChatGPT Answer"], results.iloc[i]["Grade 0/1"]]
        most_similar_questions = get_most_similar(all_embeddings, i+1)
        # print(most_similar_questions)
        for t in most_similar_questions:
            if results.iloc[t-1]['Grade 0/1'] == 0:
                r.append(t)
        for r1 in r:
            most_similar_questions.remove(r1)
        row += [most_similar_questions]   
        few_shot_input = ''
        print('doing few-shot for ' + 'hw2' + ' question ' + str(i+1) + '...')
        few_shot_input += 'Q: ' + results.iloc[most_similar_questions[0]-1]['Question'] + '\n'
        few_shot_input += 'S: ' + results.iloc[most_similar_questions[0]-1]['Solution'] + '\n'
        few_shot_input += 'A: ' + results.iloc[most_similar_questions[0]-1]['ChatGPT Answer'] + '\n\n'
        few_shot_input += 'Q: ' + results.iloc[i]['Question'] + '\n'
        few_shot_input += 'S: ' + results.iloc[i]['Solution']
        start = time.time()
        time.sleep(codex_time_delay) #to avoid an openai.error.RateLimitError
        few_shot_output = openai.Completion.create(engine = codex_engine, 
                                                    prompt = few_shot_input, 
                                                    max_tokens = few_shot_max_tokens, 
                                                    temperature = engine_temperature, 
                                                    top_p = engine_topP)['choices'][0]['text']
        print('Codex API call time: ' + str(time.time()-start) + '\n')
        row += [few_shot_output]
        rows.append(row)
    info = pd.DataFrame(rows, columns=columns)
    info.to_csv(course_location, index=False, encoding='ANSI')

if __name__ == "__main__":
    execute_few_shot(questions_per_course)