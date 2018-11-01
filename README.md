# SI 364 - Fall 2018 - Midterm Assignment

### Deadline: November 4, 2018 11:59 PM
### Total: 2000 points

## Instructions

We have provided a `.zip` file on Canvas (in the directory **Files > Midterm Assignment**) called `SI364midterm.zip`. This contains the file `SI364midterm.py` that includes some view functions, some models, some setup code, some comments to indicate what you may need to add and how to organize your code, a `templates` directory with 2 templates inside, and a sample `README.md` template. The `SI364midterm.py` file does NOT include all of the setup code necessary for an app to run.

You should add to the `SI364midterm.py` file and the `templates/` files to accumulate points, to fulfill the requirements listed below.

Note that some requirements are dependent upon another one being completed successfully, as in all applications!

The code we have provided is fairly basic, in that it could apply to any subject or theme. Everything else you can fill in for this midterm assignment may be of any theme or any subject you want, and involve any data (as long as it is appropriate to share with our whole class, and does not include any discriminatory content).

You may *not* earn any points for making a request to the iTunes API since we have used it so many times in class. You *may* use any other REST API, as long as you do not use code that is exactly the same as code used in lecture or section or a previous HW. (So your use of an API you've seen before must be *different* from anything we have done in class!)

*It is not enough to decide that the app you want to write does not have that type of feature -- the midterm assignment requires fulfilling all of these things for the credit that goes with them, so make your plan accordingly.*

Reading code you have been given already, written already, and looking at examples from lecture, section, and past HW is one of the *best* ways to approach this. While you can't use the code directly, it can answer a lot of possible questions and provide great examples!

I recommend writing an outline of your documentation first, and then writing a lot of comments in your `SI364midterm.py` file to subsequently translate into code.

Design will not earn you points for this assignment thoug you may certainly include it if you want -- do not prioritize it over the functionality, which is what this midterm assignment is about.

### Requirements to complete for 1800 points (90%) -- an awesome, solid app

*(I recommend treating this as a checklist and checking things off as you get them done!)*

#### Documentation Requirements (so we can grade the assignments)

* **Note:** See **To Submit** for submission instructions.
* Create a `README.md` file for your app that includes the full list of requirements from this page. The ones you have completed should be bolded. (You bold things in Markdown by using two asterisks, like this: `**This text would be bold** and this text would not be`)
* The `README.md` file should include a list of all of the routes that exist in the app and the names of the templates each one should render (e.g. `/form` -> `form.html`, like [the list we provided in the instructions for HW2](https://www.dropbox.com/s/3a83ykoz79tqn8r/Screenshot%202018-02-15%2013.27.52.png?dl=0)).
* The `README.md` file should contain at least 1 line of description of what your app is about or should do.

#### Code Requirements

**Note that many of these requirements go together!**

- [ ] Ensure that the `SI364midterm.py` file has all the setup (`app.config` values, import statements, code to run the app if that file is run, etc) necessary to run the Flask application, and the application runs correctly on `http://localhost:5000` (and the other routes you set up)
- [ ] Add navigation in `base.html` with links (using `a href` tags) that lead to every other viewable page in the application. (e.g. in the lecture examples from the Feb 9 lecture, [like this](https://www.dropbox.com/s/hjcls4cfdkqwy84/Screenshot%202018-02-15%2013.26.32.png?dl=0) )
- [ ] Ensure that all templates in the application inherit (using template inheritance, with `extends`) from `base.html` and include at least one additional `block`.
- [ ] Include at least 2 additional template `.html` files we did not provide.
- [ ] At least one additional template with a Jinja template for loop and at least one additional template with a Jinja template conditional.
    - These could be in the same template, and could be 1 of the 2 additional template files.
- [ ] At least one errorhandler for a 404 error and a corresponding template.
- [ ] At least one request to a REST API that is based on data submitted in a WTForm.
- [ ] At least one additional (not provided) WTForm that sends data with a `GET` request to a new page.
- [ ] At least one additional (not provided) WTForm that sends data with a `POST` request to the *same* page.
- [ ] At least one custom validator for a field in a WTForm.
- [ ] At least 2 additional model classes.
- [ ] Have a one:many relationship that works properly built between 2 of your models.
- [ ] Successfully save data to each table.
- [ ] Successfully query data from each of your models (so query at least one column, or all data, from every database table you have a model for).
- [ ] Query data using an `.all()` method in at least one view function and send the results of that query to a template.
- [ ] Include at least one use of `redirect`. (HINT: This should probably happen in the view function where data is posted...)
- [ ] Include at least one use of `url_for`. (HINT: This could happen where you render a form...)
- [ ] Have at least 3 view functions that are not included with the code we have provided. (But you may have more! *Make sure you include ALL view functions in the app in the documentation and ALL pages in the app in the navigation links of `base.html`.*)

### Additional Requirements for an additional 200 points (to reach 100%) -- an app with extra functionality!

* (100 points) Include an *additional* model class (to make at least 4 total in the application) with at least 3 columns. Save data to it AND query data from it; use the data you query in a view-function, and as a result of querying that data, something should show up in a view. (The data itself should show up, OR the result of a request made with the data should show up.)

* (100 points) Write code in your Python file that will allow a user to submit duplicate data to a form, but will *not* save duplicate data (like the same user should not be able to submit the exact same tweet text for HW3).


## To submit

* Commit all changes to your git repository. Should include at least the files:
    * `README.md`
    * `SI364midterm.py`
    * A `templates/` directory with a file `base.html` and `name_example.html` plus the others you have created inside it
* Create a GitHub repository called `364F18midterm` on your GitHub account. (You are NOT forking and cloning anything this time, you are creating your own repo from start to finish.)
* Submit the *link* to your GitHub repository to the **SI 364 Midterm** assignment on our Canvas site. The link should be of the form: `https://github.com/YOURGITHUBUSERNAME/364midterm` (if it doesn't look like that, you are probably linking to something specific *inside* the repo, so make sure it does look like that).

All set!

