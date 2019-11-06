from flask import Flask, render_template,request,redirect,escape,session,copy_current_request_context,jsonify
#from vsearch import search4letters
#from DBcm import UseDatabase,ConnectionError,CredentialsError,SQLError
from checker import check_logged_in
from threading import Thread
from time import sleep
import scoreboard
import re
'''
def search4letters(phrase:str,letters:str='aeiou')->set:
    """Return a aet of the 'letters' found in 'phrase'."""
    return set(letters).intersection(set(phrase))
'''

app=Flask(__name__)
app.secret_key='YouWillNeverGuess'
'''
app.config['dbconfig']={'host':'127.0.0.1',
                        'user':'vsearch',
                        'password':'vsearchpasswd',
                        'database':'vsearchlogDB',}
'''

@app.route('/search4',methods=['POST'])
def do_search() -> 'html':
    session['Cycle']=session['Cycle']+1
    instructions=request.form['instruction_stream']
    instruction=instructions.split('\n')
    session['instructions']=instructions
    session['instruction']=instruction
    for i in range(0, len(instruction)):
        instruction[i]=instruction[i].replace('\r', '')
    ins_Table,_func,_reg=scoreboard.goto_cycle(session['Cycle'],instruction)
    return render_template('results.html',
                           the_title='Here are your results',
                           Instruction_Stream=instructions,
                           insTable=ins_Table,
                           func=_func,
                           reg=_reg,)

@app.route('/cycle',methods=['POST'])
def next_search():
    session['Cycle']=session['Cycle']+1
    instruction=session['instruction']
    ins_Table,_func,_reg=scoreboard.goto_cycle(session['Cycle'],instruction)
    res=dict()
    res['ins_Table']=ins_Table
    res['func']=_func
    res['reg']=_reg
    res['Cycle']=session['Cycle']
    return  jsonify(res)

@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    session['Cycle']=0
    return render_template('entry.html',the_title='ScoreBoard Algorithm')
 
if __name__=='__main__':
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app=ProxyFix(app.wsgi_app)
    app.run()