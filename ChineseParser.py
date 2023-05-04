import sys
from lark import Lark

grammar = """
start: sentence

sentence: simplesentence 
        | gosentence

subjecttime: subject time
           | time subject

simplesentence: subjecttime atplace verbphrase

gosentence: subjecttime goplace verbphrase

time: hourly 
    | weekday 
    | day 
    | weekday hourly 
    | day hourly 

hourly: "一点"      -> one
      | "二点"      -> two
      | "三点"      -> three
      | "四点"      -> four
      | "五点"      -> five
      | "六点"      -> six
      | "七点"      -> seven
      | "八点"      -> eight
      | "九点"      -> nine
      | "十点"      -> ten
      | "十一点"    -> eleven
      | "十二点"    -> twelve


weekday: "星期一" -> on_monday
       | "星期二" -> on_tuesday
       | "星期三" -> on_wednesday
       | "星期四" -> on_thursday
       | "星期五" -> on_friday
       | "星期六" -> on_saturday
       | "星期天" -> on_sunday
       | "星期日" -> on_sunday

day: "明天" -> tomorrow
   | "今天" -> today

subject: simplesubject 
       | possessivesubject 
       | pluralsubject

simplesubject: "我" -> i
             | "你" -> you
             | "他" -> he
             | "她" -> she

possessivesubject: "我的朋友"   -> my_friend
                 | "我妈妈"     -> my_mom 
                 | "我爸爸"     -> my_dad
                 | "我兄弟"     -> my_brother
                 | "我姐妹"     -> my_sister

pluralsubject: "我们" -> we
             | "你们" -> you_all
             | "他们" -> they
             | "她们" -> they
             | "它们" -> they

atplace: "在学校"   -> at_school
       | "在图书馆" -> at_the_library
       | "在宿舍"   -> at_the_dormitory
       | "在家"     -> at_home
       | "在商店"   -> at_the_store

goplace: "去学校"   -> go_to_school_to
     | "去图书馆" -> go_to_the_library_to
     | "去宿舍"   -> go_to_the_dormitory_to 
     | "去商店"   -> go_to_the_store_to
     | "去家"     -> go_home_to

verbphrase: verb object

verb: "做"      -> do
    | "看"      -> read
    | "打"      -> play
    | "买"      -> buy
    | "听"      -> listen_to
    | "学习"    -> study

object: "功课"      -> homework
      | "工作"      -> work
      | "书"        -> a_book
      | "球"        -> ball
      | "东西"      -> things
      | "音乐"      -> music
      | "电脑课"    -> computer_science
      | "中文"      -> chinese
      | "英文"      -> english

%import common.WS
%ignore WS     
"""

parser = Lark(grammar, start="start")

def translate(chinese_text):
    tree = parser.parse(chinese_text)
    sentence = []
    time_cache = []
    sentence_type = ''
    numbers = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve']
    nonterminals = ['start','sentence','atplace', 'goplace', 'subjecttime', 'subject', 'time', 'verbphrase']
    
    for node in tree.iter_subtrees_topdown():
        if node.data in nonterminals:
            continue
        elif node.data == 'simplesentence' or node.data == 'gosentence':
            sentence_type = sentence_type + node.data 
        elif node.data in numbers:
            time_cache.append('at ' + node.data + " o'clock")
        elif node.data.startswith('on_'):
            time_cache.append('on ' + node.data.removeprefix('on_').capitalize())
        elif node.data == 'today' or node.data == 'tomorrow':
            time_cache.append(node.data)
        elif node.data.startswith('my_'): 
            sentence.append('my ' + node.data.removeprefix('my_'))
        elif node.data.startswith('at_the_'): 
            sentence.append('at the ' + node.data.removeprefix('at_the_'))
        elif node.data.startswith('at_'): 
            sentence.append('at ' + node.data.removeprefix('at_'))
        elif node.data.startswith('go_to_the_'): 
            sentence.append('will go to the ' + node.data.removeprefix('go_to_the_').removesuffix('_to') + ' to')
        elif node.data.startswith('go_to_'): 
            sentence.append('will go to ' + node.data.removeprefix('go_to_').removesuffix('_to') + ' to')
        elif node.data.startswith('go_'): 
            sentence.append('will go ' + node.data.removeprefix('go_').removesuffix('_to') + ' to')
        elif node.data.startswith('a_'): 
            sentence.append('a ' + node.data.removeprefix('a_'))
        elif node.data == 'you_all':
            sentence.append('you all')
        elif node.data == 'listen_to': 
            sentence.append('listen to')
        elif node.data == 'computer_science': 
            sentence.append('computer science')
        elif node.data == 'english': 
            sentence.append('English')
        elif node.data == 'chinese': 
            sentence.append('Chinese')
        elif node.data == 'i': 
            sentence.append('I')
        else:
            sentence.append(node.data)

    if sentence_type == 'simplesentence': 
        if sentence[0] in ["my mom", "my dad", "my friend", "my sister", "my brother", "he", "she"]:
            if sentence[2] == 'buy':
                sentence[2] = 'buys'
            elif sentence[2] == 'study':
                sentence[2] = 'studies'
            elif sentence[2] == 'listen to':
                sentence[2] = 'listens to'
            elif sentence[2] == 'play':
                sentence[2] = 'plays'
            elif sentence[2] == 'do':
                sentence[2] = 'will do'            
        sentence[1], sentence[2], sentence[3] = sentence[2], sentence[3], sentence[1]
    else:     
        pass

    sentence.extend(time_cache) 

    to_capitalize = sentence[0]
    to_capitalize = to_capitalize[0].upper() + to_capitalize[1:]
    sentence[0] = to_capitalize

    return " ".join(sentence) + '.'

if __name__ == "__main__":
    if len(sys.argv) > 1:
        chinese_text = sys.argv[1]
        try:
            english_translation = translate(chinese_text)
            print(english_translation)
        except Exception as e:
            print(f"Error: Failed to parse and translate: {e}")
    else:
        print("Please provide Chinese text as a command line argument (No spaces, one sentence, anything else will be ignored).")
        print("The sentence must contain a subject, time, verb, and place to be correctly parsed.")
        print("Following valid Chinese grammar rules is also required to be correctly parsed.")
