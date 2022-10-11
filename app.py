import streamlit as st
import pandas as pd
import base64
import numpy as np
import random
import time
from load_css import local_css
local_css("style.css")
#from PIL import Image


######################
# Page Title
######################
#image = Image.open('jaju_logo.png')
#st.image(image, use_column_width=True)


st.title('JAJU ENGLISH')


st.sidebar.header('레벨 선택')
with st.form(key='myform', clear_on_submit=True): 
    selected_grade = st.sidebar.selectbox('학년', ("초등 3", "초등 4", "초등 5", "초등 6", "중등 1", "중등 2", "중등 3", "고등 1", "고등 2", "고등 3"))
    show_text = st.sidebar.button('지문 추출')
    question = st.sidebar.button('문제 생성')


st.sidebar.markdown('##')
st.sidebar.header('읽기 시간 측정')
video_file = open('data/timer.mp4', 'rb')
video_bytes = video_file.read()
st.sidebar.video(video_bytes)

st.sidebar.markdown('##')
st.sidebar.header('텍스트 데이터 출처')
st.sidebar.markdown("""
* [한국교육과정평가원](https://www.kice.re.kr/boardCnts/list.do?boardID=1500234&m=0403&s=suneung#;), [두산 교과서](http://www.douclass.com/gate.donga)
""")

#start_button = st.sidebar.button('시작')
#end_button = st.sidebar.button('끝')

#with st.empty():  
#    st.markdown(f'<h5 style="text-align: right;">⏳ 0시간 0분 0초 </h5>', unsafe_allow_html=True)

#    if start_button: 
#        for seconds in range(6000):
#            m, s = divmod(seconds, 60)
#            h, m = divmod(m, 60)
#            st.markdown(f'<h5 style="text-align: right;">⏳ {h}시간 {m}분 {s}초 </h5>', unsafe_allow_html=True)
#            time.sleep(1)
#    if end_button:
#        for seconds in range(6000):
#            time.sleep(1)
#            st.markdown(f'<h5 style="text-align: right;">⏳ 0시간 0분 0초 </h5>', unsafe_allow_html=True)

@st.cache(allow_output_mutation=True)
def load_data(grade):

    if str(grade) == "고등 3":
        path = "data/high_3/"
    else:
        path = "data/elementary_6/"

    random_num = random.randrange(1, 9, 1)   
    file_name = path + str(random_num) + ".txt"
    with open(file_name) as f: 
        text = f.read()
    return text

    




#MIT License

#Copyright (c) 2020 Ramsri Goutham Golla

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.


@st.cache
def generate_comphrehension_question_set(input_text):
    
    from pprint import pprint
    from Questgen import main
    payload = {"input_text": text}
    
    try:
        qg = main.QGen()
        output = qg.predict_mcq(payload)
        comprehension_question = output['questions'][0]['question_statement']
        correct = output['questions'][0]['answer']
        incorrect1 = output['questions'][0]['options'][0].lower()
        incorrect2 = output['questions'][0]['options'][1].lower()
        incorrect3 = output['questions'][0]['options'][2].lower()

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

        q2_final_set = text, comprehension_question, q2_options, q2_answer
        print(q2_final_set)

    except:
        q2_final_set = input_text, "None", "None", "None"

    return q2_final_set


@st.cache
def generate_synonym_question_set(input_text):
    import nltk
    import ssl

    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')
    nltk.download('punkt')
    nltk.download('brown')

    from nltk.corpus import brown
    from nltk.tokenize import word_tokenize
    from nltk.stem.wordnet import WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()

    from itertools import chain
    from nltk.corpus import wordnet

    freqs = nltk.FreqDist([w.lower() for w in brown.words()]) # sort wordlist by word frequency


    try: 
        tokenized = word_tokenize(input_text)
        
        noun_list = [lemmatizer.lemmatize(word, pos='n') for (word, pos) in nltk.pos_tag(tokenized) if(pos[:2] == 'NN')]

        tagged_nouns = nltk.pos_tag(noun_list)
        for (word, tag) in tagged_nouns:
            if tag == 'NNP': # If the word is a proper noun
                noun_list.remove(word)
 
        adj_list = [lemmatizer.lemmatize(word, pos='a') for (word, pos) in nltk.pos_tag(tokenized) if(pos[:2] == 'JJ')]
        
        verb_list = [lemmatizer.lemmatize(word, pos='v') for (word, pos) in nltk.pos_tag(tokenized) if(pos[:2] == 'VB')]
        verb_list = list(set(verb_list))
        if 'be' in verb_list:
            verb_list.remove('be')
        
        adv_list = [lemmatizer.lemmatize(word, pos='r') for (word, pos) in nltk.pos_tag(tokenized) if(pos[:2] == 'RB')]
        for adv in adv_list:
            if len(adv) < 5:
                adv_list.remove(adv)

        joinedlist = noun_list + adj_list + verb_list + adv_list
        joinedlist = list(set(joinedlist))
        for nava in joinedlist:
            if len(nava) < 4:
                joinedlist.remove(nava)

        joinedlist = sorted(joinedlist, key=lambda x: freqs[x.lower()], reverse=True) # Sort the list by frequency
        #joinedlist = joinedlist[:7]
        #target = random.choice(joinedlist)
        #target_list = random.sample(joinedlist, 5)

        #first_target, second_target, third_target, fourth_target = random.sample({noun_list[0], adj_list[0], verb_list[0], adv_list[0]}, 4)

        joinedlist_filtered = []
        for candidate in joinedlist:
            synonym_gen_candidate = wordnet.synsets(candidate)
            synonym_list_candidate = list(set(list(chain.from_iterable([candidate.lemma_names() for candidate in synonym_gen_candidate]))))       
            synonym_list_candidate = list(map(str.lower,synonym_list_candidate))
            synonym_list_candidate = list(set(synonym_list_candidate))

            if len(synonym_list_candidate) > 7:
                joinedlist_filtered.append(candidate) 
            else:
                continue

        target = random.choice(joinedlist_filtered) 
        target = target.lower()
        synonym_gen = wordnet.synsets(target)
        synonym_list = list(set(list(chain.from_iterable([target.lemma_names() for target in synonym_gen]))))       
        synonym_list = list(map(str.lower,synonym_list))
        synonym_list = list(set(synonym_list))
        if target in synonym_list:
            synonym_list.remove(target)

        tagged_synonyms = nltk.pos_tag(synonym_list)
        synonym_final_list = []
        for (word, tag) in tagged_synonyms: 
            if tag == nltk.pos_tag([target])[0][1]:
                synonym_final_list.append(word)
            else: 
                continue
         
        synonym_final_list = sorted(synonym_final_list, key=lambda x: freqs[x.lower()], reverse=True) # Sort the list by frequency
        #print(target, synonym_list)
        try: 
          synonym = synonym_final_list[0]
        except:
          synonym = synonym_list[0]


        wrong1 = "abc(wrong1)"
        wrong2 = "def(wrong2)"
        wrong3 = "ghi(wrong3)"     
 
        question = "Which word is closest in meaning to the highlighted word: <span class='highlight red'>" + target + "</span>?"
        
        option_list = [synonym, wrong1, wrong2, wrong3]
        option_list.sort()

        number = 0
        options = []
        for option in option_list:
          number += 1
          option = "(" + str(number) + ") " + option 
          options.append(option)
        
        for option_number in options:
            if synonym in option_number:
                option_answer = option_number

        options = ' '.join(options)

        answer = option_answer


        highlighted_text = []
        for token in tokenized:
            if target == lemmatizer.lemmatize(token.lower(), "n") or target == lemmatizer.lemmatize(token.lower(), "v"): 
                highlighted_text.append("<span class='highlight red'>" + token + "</span>")
            elif target == lemmatizer.lemmatize(token.lower(), "a") or target == lemmatizer.lemmatize(token.lower(), "r"): 
                highlighted_text.append("<span class='highlight red'>" + token + "</span>")
            else: 
                highlighted_text.append(token)

        highlighted_text = " ".join(highlighted_text)
        highlighted_text = highlighted_text.replace(" ,", ",").replace(" .", ".").replace("“ ", "“").replace("’ ", "’").replace(" ’", "’").replace(" ”", "”").replace(" !", "'").replace(" ?", "'").replace(" :", ":").replace(" ;", ";").replace("( ", "(").replace(" )", ")")
        highlighted_text = highlighted_text.replace(" .", ".")
        highlighted_text = highlighted_text.replace(" '", "'")

      
        final_set = highlighted_text, question, options, answer


    except:
        final_set = input_text, "None", "None", "None"


    return final_set



with st.empty():  
    st.subheader('Reading passage')

container_passage = st.empty()

with st.empty(): 
    st.markdown('##')
with st.empty(): 
    st.subheader('Question 1')

container_q1 = st.container()

    
with st.empty(): 
    st.subheader('Question 2')

container_q2 = st.container()


with st.empty(): 
    st.markdown('##')
with st.empty(): 
    st.markdown("""<h1 style="height:2px;border:none;color:#e5e4e2;background-color:#e5e4e2;" /> """, unsafe_allow_html=True)


text = load_data(selected_grade)

if 'count' not in st.session_state:
    st.session_state.count = 0

if show_text:
    st.session_state.count += 1
    container_passage.markdown(f'<h4 style="color:#000000; background-color: #FFFFFF; padding: 10px; border-radius: 10px; font-size: 16px;">{text}</h4>', unsafe_allow_html=True)

if question:
    if st.session_state.count < 1:
        container_passage.markdown(f'<h4 style="color:#000000; background-color: #FFFFFF; padding: 10px; border-radius: 10px; font-size: 16px;"> 문제 생성을 위해 지문 추출을 먼저 클릭해주세요. </h4>', unsafe_allow_html=True)
        st.legacy_caching.clear_cache()

    else:
        container_passage.markdown(f'<h4 style="color:#000000; background-color: #FFFFFF; padding: 10px; border-radius: 10px; font-size: 16px;">{text}</h4>', unsafe_allow_html=True)


     
        comprehension_question_set = generate_comphrehension_question_set(text)
        comprehension_question = comprehension_question_set[1]
        comprehension_options = comprehension_question_set[2]
        comprehension_answer = comprehension_question_set[3]
        container_q1.markdown(f'<h5 style="color:#000000; background-color: #FFFFFF; padding: 10px; border-radius: 10px; font-size: 16px;">{comprehension_question} <br> {comprehension_options} </h5>', unsafe_allow_html=True)

        synonym_question_set = generate_synonym_question_set(text)
        highlighted_text = synonym_question_set[0]
        synonym_question = synonym_question_set[1]
        synonym_options = synonym_question_set[2]
        synonym_answer = synonym_question_set[3]
        container_q2.markdown(f'<h2 style="color:#000000; background-color: #FFFFFF; padding: 10px; border-radius: 10px; font-size: 16px;">{synonym_question} <br>{synonym_options}  </h2>', unsafe_allow_html=True)


        container_passage.markdown(f'<h4 style="color:#000000; background-color: #FFFFFF; padding: 10px; border-radius: 10px; font-size: 16px;">{highlighted_text}</h4>', unsafe_allow_html=True)


        st.subheader('Answers')
        with st.expander("See answers"):
            st.markdown(f'<h5 style="color:#000000; background-color: #FFFFFF; padding: 10px; border-radius: 10px; font-size: 16px;"> Question 1:  {comprehension_answer} <br> Question 2:  {synonym_answer} </h5>', unsafe_allow_html=True)

        st.legacy_caching.clear_cache()

