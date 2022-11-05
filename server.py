import os
from bottle import route, run, template, get, post, request
from scraper import scrap, get_dropdown_choices

index_html = '''My first web app! By <strong>{{ author }}</strong>.'''


@route('/')
def index():



    return template(index_html, author='Real Python')

@route('/name/<name>')
def name(name):
    return template(index_html, author=name)

@get('/plot')
def form():

    global categories
    categories = get_dropdown_choices()

    print(categories)

    options = ""
    for key, value in enumerate(categories):
        options += f"<option value='{key}'>{value}</option>"

    print('options', options)

    #return_string =

    '''
    <h2>Choose your Coursera category:</h2>
              <form method="POST" action="/plot">
                Category: <input name="category" type="text" /><br/>
                <input type="submit" />
    '''

    return '''
              <form method="post" action="/plot">
              <label for="cars">Choose a car:</label>
              <select name="cars">''' + options + '</select><input type="submit"/></form>'

@post('/plot')
def submit():
    # grab data from form
    category = request.forms.get('cars')
    print(category)

    #check the input



    results = scrap(category)
    print('FINAL FINAL FINAL ', len(results))

    response = len(results)

    if response:

        html_result = f"""<table style="width:100%">
                              <tr>
                                <th>Category Name</th>
                                <th>Course Name</th>
                                <th>First Instructor Name</th>
                                <th>Course Description</th>
                                <th># of Students Enrolled</th>
                                <th># of Ratings</th>
                              </tr>
                              <tr>
                                <td>Alfreds Futterkiste</td>
                                <td>Maria Anders</td>
                                <td>Germany</td>
                                <td>Germany</td>
                                <td>Germany</td>
                              </tr>
                              <tr>
                                <td>Centro comercial Moctezuma</td>
                                <td>Francisco Chang</td>
                                <td>Mexico</td>
                              </tr>
                        </table>
        """

        return template('''
            <h1>Congrats!</h1>
            <div>
              Number of courses: {{response}}
            </div>
            ''',
            response=response
        )


run(host='0.0.0.0', port=8080)

"""
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    run(host='0.0.0.0', port=port, debug=True)
"""