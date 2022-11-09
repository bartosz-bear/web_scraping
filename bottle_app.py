import os
from bottle import run, template, get, post, request
from scraper import scrap, get_dropdown_choices

@get('/get_courses')
def form():

    global course_categories
    course_categories = get_dropdown_choices()

    select_input_options = ""
    for key, value in course_categories.items():
        select_input_options += f"<option value='{value}'>{key}</option>"

    selection_form = ''' <form method="post" action="/get_courses">
                          <p><b>It will take up to 2 minutes to scrap data and create a CSV file.
                           After you press the button, do not refresh the page.</b><p>
                          <label for="course_category">Choose a course category:</label>
                          <select name="course_category">''' + select_input_options + '''</select><input type="submit"/></form>'''

    return selection_form

@post('/get_courses')
def submit():

    chosen_course_category = request.params.get('course_category')
    scrapping_results = scrap(chosen_course_category)
    number_of_courses = len(scrapping_results)

    html_string = ''' <h3><b>Congrats!</b></h3>
                      <a href='https://www.pythonanywhere.com/user/bartoszbear/files/home/bartoszbear/courses_final.csv'>Your CSV is here</a>
                      <div>
                        <br>Number of courses: {{number_of_courses}}
                      </div>
                  '''

    return template(html_string, number_of_courses=number_of_courses)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    run(host='0.0.0.0', port=port, debug=True)
