from so import get_jobs as get_so_jobs
from save import save_to_file
from flask import Flask, render_template, request, redirect, send_file
from wwr import get_jobs as get_wwr_jobs
from remoteok import get_jobs as get_remoteok_jobs

db = {}
app = Flask("Job Search")


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/search')
def searchJobs():
    term = request.args.get("term")
    if term:
        jobs = []
        term = term.lower()
        existingJobs = db.get(term)
        if existingJobs:
            jobs = existingJobs
        else:
            jobs += get_so_jobs(term)
            jobs += get_wwr_jobs(term)
            jobs += get_remoteok_jobs(term)
            db[term] = jobs
    else:
        return redirect("/")
    return render_template("search.html",
                           jobs=jobs,
                           searchingBy=term,
                           resultsNumber=len(jobs))


@app.route("/export")
def export():
    try:
        term = request.args.get('term')
        if not term:
            print("term error")
            raise Exception()
        term = term.lower()
        jobs = db.get(term)
        if not jobs:
            print("jobs error")
            raise Exception()
        save_to_file(jobs)
        return send_file("jobs.csv")
    except:
        return redirect('/')


app.run(host="127.0.0.1")
