from pprint import pprint
from Questgen import main
#import wget
#wget.download("https://github.com/explosion/sense2vec/releases/download/v1.0.0/s2v_reddit_2015_md.tar.gz")
######################
# Page Title
######################

text = "It has been suggested that “organic” methods, defined as those in which only natural products can be used as inputs, would be less damaging to the biosphere. Large-scale adoption of “organic” farming methods, however, would reduce yields and increase production costs for many major crops. Inorganic nitrogen supplies are essential for maintaining moderate to high levels of productivity for many of the non-leguminous crop species, because organic supplies of nitrogenous materials often are either limited or more expensive than inorganic nitrogen fertilizers. In addition, there are benefits to the extensive use of either manure or legumes as “green manure” crops. In many cases, weed control can be very difficult or require much hand labor if chemicals cannot be used, and fewer people are willing to do this work as societies become wealthier. Some methods used in “organic” farming, however, such as the sensible use of crop rotations and specific combinations of cropping and livestock enterprises, can make important contributions to the sustainability of rural ecosystems."


def generate_comphrehension_question_set(input_text):
    payload = {
            "input_text": text   
            }
    try:
        qg = main.QGen()
        output = qg.predict_mcq(payload)
        comprehension_question = output['questions'][0]['question_statement']
        correct = output['questions'][0]['answer']
        incorrect1 = output['questions'][0]['options'][0]
        incorrect2 = output['questions'][0]['options'][1]
        incorrect3 = output['questions'][0]['options'][2]

        q2_option_list = [correct, incorrect1, incorrect2, incorrect3]
        q2_option_list.sort()

        q2_number = 0
        q2_options = []
        for q2_option in q2_option_list:
          q2_number += 1
          q2_option = "(" + str(q2_number) + ") " + q2_option 
          q2_options.append(q2_option)
        
        for q2_option_number in q2_options:
            if correct in q2_option_number:
                q2_option_answer = q2_option_number

        q2_options = ' '.join(q2_options)

        q2_answer = q2_option_answer

        q2_final_set = highlighted_text, comprehension_question, q2_options, q2_answer
        print(q2_final_set)
    except:
        q2_final_set = input_text, "None", "None", "None"

    return q2_final_set
    

comprehension_question_set = generate_comphrehension_question_set(text)
comprehension_question = comprehension_question_set[1]
comprehension_options = comprehension_question_set[2]
comprehension_answer = comprehension_question_set[3]




