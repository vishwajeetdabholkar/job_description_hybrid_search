from flask import Flask, request, render_template, jsonify
import pymysql
import yaml
import time 

app = Flask(__name__)

# Load database configuration from a YAML file
db_config = yaml.safe_load(open('db.yaml'))
app.config.update(
    MYSQL_HOST=db_config['mysql_host'],
    MYSQL_USER=db_config['mysql_user'],
    MYSQL_PASSWORD=db_config['mysql_password'],
    MYSQL_DB=db_config['mysql_db']
)

# Initialize MySQL connection
connection = pymysql.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB'],
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

@app.route('/autocomplete/<field>', methods=['GET'])
def get_autocomplete_suggestions(field):
    term = request.args.get('term', '')
    if field == 'location':
        cursor = connection.cursor()
        cursor.execute('SELECT DISTINCT location FROM postings WHERE location LIKE %s LIMIT 10', ('%' + term + '%',))
        results = cursor.fetchall()
        suggestions = [row['location'] for row in results]
    # Repeat for other fields like location_type, seniority, etc.
    elif field == 'company':
        cursor = connection.cursor()
        cursor.execute('SELECT DISTINCT company_name FROM postings WHERE company_name LIKE %s LIMIT 10', ('%' + term + '%',))
        results = cursor.fetchall()
        suggestions = [row['company_name'] for row in results]
    # Add more elif blocks for other fields as needed

    return jsonify(suggestions)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    location = request.form['location']
    location_type = request.form['locationType']
    seniority = request.form['seniority']
    employment_type = request.form['employmentType']
    company = request.form['company']

    search_conditions = []
    where_conditions = []

    if keyword:
        search_conditions.append(f'(title:"{keyword}" OR description:"{keyword}")')
    if location:
        search_conditions.append(f'location:"{location}"')
    if location_type:
        where_conditions.append(f'formatted_work_type = "{location_type}"')
    if seniority:
        where_conditions.append(f'formatted_experience_level = "{seniority}"')
    if employment_type:
        where_conditions.append(f'work_type = "{employment_type.upper()}"')
    if company:
        where_conditions.append(f'company_name = "{company}"')

    search_string = ' AND '.join(search_conditions)
    where_clause = ' AND '.join(where_conditions)

    with connection.cursor() as cursor:
        sql_query = f"""
        SELECT title, company_name, location, description, application_url, job_posting_url,
               formatted_work_type, formatted_experience_level, work_type
        FROM postings
        WHERE MATCH(TABLE postings) AGAINST (%s) 
        """
        
        if where_clause:
            sql_query += f" AND {where_clause}"

        sql_query = sql_query + " limit 10;"
        print(sql_query.replace("%s", f"'{search_string}'") )
        start_time = time.time()
        cursor.execute(sql_query, (search_string,))
        results = cursor.fetchall()
        end_time = time.time()
        execution_time = end_time - start_time

    enhanced_results = []
    for result in results:
        apply_url = result['application_url'] if result['application_url'] else result['job_posting_url']
        enhanced_result = {
            "title": result['title'],
            "company_name": result['company_name'],
            "location": result['location'],
            "description": result['description'],
            "apply_url": apply_url,
            "formatted_work_type": result['formatted_work_type'],
            "formatted_experience_level": result['formatted_experience_level'],
            "work_type": result['work_type']
        }
        enhanced_results.append(enhanced_result)

    return jsonify({
        'results': enhanced_results,
        'execution_time': execution_time
    })



if __name__ == "__main__":
    app.run(debug=True)
