import json
import pandas as pd
import os
import glob

from os.path import join, dirname, abspath, exists, isdir

# relevant paths
home_path = dirname(dirname(dirname(abspath(__file__))))
output_ims_dir_path = join(home_path, "data", "images")

# list of csv files in current directory
datafiles = [f for f in os.listdir(dirname(__file__)) if (f.endswith('csv') and f != "MATH.csv")]

# json fields
question  =  {
    'Id': None,
    'Question': None,
    'Solution' : None,
    'ChatGPT Answer' : None,
    'Grade 0/1' : None,
}

# COURSES_TO_PROCESS = [
#     "18.01",
#     "18.02",
#     "18.03",
#     "18.05",
#     "18.06",
#     "6.042",
#     "COMS3251"
#     ]

# def get_codex_input(sheet, i):
#     """
#     retrieve the codex input for a given problem from a course
#     """
#     field = sheet['Codex Input'][i]
#     if field == sheet['Question'][i] or field == '':
#         return 'Same as original question'
#     else:
#         return field

def get_program_solution(sheet, i, course_code):
    """
    retrieve the solution to a given problem from a course, in the form of text or path to image when applicable
    """
    output_plot_fname = join(output_ims_dir_path, course_code + "-q" + str(i+1) + "-codex-output-plot.png")
    if exists(output_plot_fname): # the question produces an image output; return file path
        path = "data/images/" + course_code + "-q" + str(i+1) + "-codex-output-plot.png"
        return path
    else: # otherwise return solution as in csv
        return sheet['Solution'][i]

def get_file_q_num(n):
    """
    returns 2-digit string representing a given number n
    """
    if n < 10:
        return "0" + str(n)
    else:
        return str(n)

if __name__ == "__main__":
    # Writing to jsons
    for filename in datafiles:
        course_name = filename[: -4].strip() # format of: "<course_code>""

        # read in sheet
        sheet = pd.read_csv(join(dirname(__file__),  filename))

        # set up file output directory
        out_dir_path = join(home_path, "data", course_name)
        # if isdir(out_dir_path): # make course directory if DNE
        #     os.makedirs(out_dir_path)
        # else:
        #     for f in glob.glob(out_dir_path + "/*"): # clear directory if exists before writing in new files
        #         os.remove(f)

        for i in range(1,23):
            question['Id'] = str(sheet['Id'][i-1])
            question['Question'] = sheet['Question'][i-1]
            question['Solution'] = str(sheet['Solution'][i-1])
            question['ChatGPT Answer'] = sheet['ChatGPT Answer'][i-1]
            question['Grade 0/1'] = str(sheet['Grade 0/1'][i-1])

        
            json_object = json.dumps(question, indent = 7)
            fname = join(out_dir_path, course_name +'_'+'Question'+'_'+get_file_q_num(int(sheet['Id'][i-1]))+'.json')
            with open(fname, "w") as outfile:
                outfile.write(json_object)
