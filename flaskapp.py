from flask import Flask, render_template, request, redirect
import json
import query
app = Flask(__name__)

@app.route("/",methods=['GET'])
def main():
    queryTerm = request.args.get("queryTerm")
    if queryTerm: # only the term is not None, run the automation script
        print("The query term  is '" + queryTerm + "'")
        query_result = json.loads(query.queryOpenHub(queryTerm))
        query_github = json.loads(query.queryGithub(queryTerm))
        #url = query_github["result"]["github_url"]
        #url = result["result"]["project_html_url"]
        #return url
        return render_template("query.html", result=query_result["result"], res=query_github["result"])
    else:
        return render_template("index.html")

@app.route('/about', methods=['GET'])
def about():
    return render_template("about.html")

@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')


if __name__ == "__main__":
    app.run(debug=True)