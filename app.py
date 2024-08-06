from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)

df = pickle.load(open('df.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(title):
    try:
        idx = df[df['jobtitle'] == title].index[0]
        idx = df.index.get_loc(idx)
    except IndexError:
        return f"The job title '{title}' does not exist in the dataset."

    distances = sorted(list(enumerate(similarity[idx])), reverse=True, key=lambda x: x[1])[1:5]

    jobs = []
    for i in distances:
        job_details = {
            'Job Id': df.iloc[i[0]].uniq_id,
            'job title': df.iloc[i[0]].jobtitle,
            'company': df.iloc[i[0]].company,
            'Apply Link': df.iloc[i[0]].advertiserurl
        }
        jobs.append(job_details)

    return jobs

@app.route('/')
def home():
    job_titles = df['jobtitle'].unique()
    return render_template('index.html', job_titles=job_titles)

@app.route('/recommend', methods=['POST'])
def recommend_jobs():
    title = request.form.get('title')
    jobs = recommend(title)

    if isinstance(jobs, str):  # Error message
        return render_template('index.html', error_message=jobs, job_titles=df['jobtitle'].unique())

    return render_template('index.html', jobs=jobs, job_titles=df['jobtitle'].unique())

if __name__ == '__main__':
    app.run(debug=True)
