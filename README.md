Forked from
https://github.com/viniciuschiele/flask-rest-example

# Quick start
(requires Python3)

### Clone
git clone https://github.com/cdennison/flask-rest-example

### Setup virtualenv (optional)
Run like this on OSX

python3 -m venv env
source env/bin/activate

### Install dependencies
pip3 install -r requirements.txt

If there are still dependency issues you can try:

pip3 install -r requirements_extended.txt

### Test
python3 -m unittest discover tests

### Run
python3 run.py

Go to 
http://127.0.0.1:5000/static/index.html

Try out the APIs

#Use case and requirements
* As a teacher I want to create a test made up of multiple problems to give to a student
* I want to select from a list of existing questions and be able to add my own (add/get/update/delete a single questions, filter to get many questions)
* I want to give my student a list of questions and ids

* As a student I want to try and answer the questions correctly (solve)

# Design considerations

#### APIs implemented
•  I implemented “editing” a row using PUT and did not implement PATCH because it would be extra work and wasn’t required
•  I implemented "get a listing of all questions" as a problems/filter instead of /GET problems because I wanted to enforce a default limit
•  I named the API “problems” because each entity is a “test problem”
•  I implemented a simple “solve” API because the that seemed to be the actual use case – to try and solve a problem with the correct answer

##### UI Implementation
I could have written a custom UI from scratch using something like bootstrap/jQuery-ui but chose Swagger-UI because 1) I feel that all APIs should be documented so I would want something like Swagger UI even if I wrote my own UI 2) there was no UI logic given like “take a test of questions and report the score” which couldn’t be handled by Swagger-UI 3) I ran out of time.

Also Swagger is normally "embedded" in the code which I tried with https://github.com/rochacbruno/flasgger but there were integration issues with flask-io which I didn't have time to fix.

##### Database vs in-memory object/cache
I chose to use a database because its what you would typically use. Its possibly that using an in-memory cache would have taken less time but still would have been non-trivial to setup. It didn’t want to use a simple in-memory object because of the complexity with making it work correctly across multiple threads.

##### SQL queries I was concerned about

Paging
SELECT problems.id AS problems_id, … 
FROM problems ORDER BY problems.question DESC
 LIMIT ? OFFSET ?

Sort
SELECT problems.id AS problems_id, … 
FROM problems ORDER BY problems.question DESC

Filter (not sure why there’s an OR that could be improved)
SELECT problems.id AS problems_id, … 
FROM problems 
WHERE (problems.question LIKE '%%' || ? || '%%')

Put/Update
UPDATE problems SET question=?, answer=?, distraction1=?, distraction2=?, distraction3=?, distraction4=?, distraction5=? WHERE problems.id = ?

##### Data modeling / validation

I modeled the distractions as 5 separate columns because 1) typically on tests there is a limit to how many choices 2) it was easier than creating a second table for distractions with a 1:N relationsihp to the problems and 3) I could have used a DB column “object” type (like array, JSON, blob, text) but those are generally not performant and more difficult to work with.

##### Pagination
I implemented the pagination “state” on the client side to save time. So the client has to be careful to reuse the same filter/sort/limit and then increment the starting point of their query. A better approach would be to simply return a hash in the header for previous/next page that contains the filter/sort info (and also return a variable that says if there’s more data).

##### Production readiness
To use this code in production it would minimally need:
•  A security review and likely some type of auth
•  A webserver http://flask.pocoo.org/docs/0.12/deploying/
•  A better database e.g. Postgres
•  More performant pagination query https://stackoverflow.com/questions/34110504/optimize-query-with-offset-on-large-table
•  Integration testing
•  Performance testing
•  Negative unit tests