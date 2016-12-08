# query openhub and github
import requests
from bs4 import BeautifulSoup
import json
import xml.etree.ElementTree as ET

import urllib, urlparse, string, time
import urllib2, base64, json
from urlparse import urlparse

def queryGithub(searchTerm):
      username = 'osspal'
      password = 'Practicum2017Osspal@CMU'

      #searchTerm = raw_input('Search GitHub repo: ')
      qs = {'q': searchTerm}
      qsEncoded = urllib.urlencode(qs)
      queryURL = "https://api.github.com/search/repositories?o=desc&sort=stars&" + qsEncoded

      # e.g. 'https://api.github.com/search/repositories?q=electron'
      searchReq = urllib2.Request(queryURL)
      base64string = base64.b64encode('%s:%s' % (username, password))
      searchReq.add_header("Authorization", "Basic %s" % base64string)
      searchRes = urllib2.urlopen(searchReq)
      jsonSearch = json.loads(searchRes.read())

      githubURL =  'http://github.com/' + jsonSearch['items'][0]['full_name']

      print 'Top result: ', githubURL

      parsedURL = urlparse(githubURL)
      owner = parsedURL.path.split('/')[1]
      repoName = parsedURL.path.split('/')[2]

      # e.g. 'https://github.com/electron/electron'
      basicReq = urllib2.Request("https://api.github.com/repos/" + owner + "/" + repoName)
      base64string = base64.b64encode('%s:%s' % (username, password))
      basicReq.add_header("Authorization", "Basic %s" % base64string)   
      basicRes = urllib2.urlopen(basicReq)

      # e.g. 'https://api.github.com/repos/electron/electron/releases/latest '
      latestJson = ''
      try:
            latestReq = urllib2.Request("https://api.github.com/repos/" + owner + "/" + repoName + "/releases/latest")
            latestReq.add_header("Authorization", "Basic %s" % base64string)
            latestRes = urllib2.urlopen(latestReq)
            latestJson = latestRes.read();
      except urllib2.HTTPError as err:
            if err.code == 404:
                  #print 'Unable to retrive latest release info.'     
                  latestJson = '{"published_at":"NA"}'

      # e.g. 'https://api.github.com/repos/$owner/$repoName/license'
      licenseJson = ''
      try:
            licenseReq = urllib2.Request("https://api.github.com/repos/" + owner + "/" + repoName + "/license")
            licenseReq.add_header("Authorization", "Basic %s" % base64string)
            licenseRes = urllib2.urlopen(licenseReq)
            licenseJson = licenseRes.read()
      except urllib2.HTTPError as err:
            if err.code == 404:
                  #print 'Unable to retrive license info.'
                  licenseJson = '{"license":{"name":"NA"}}'

      # parsed json responses
      jsonBasic = json.loads(basicRes.read())
      jsonLatest = json.loads(latestJson)
      jsonLicense = json.loads(licenseJson)

      print '# of stars: ', jsonBasic['watchers_count']
      print '# of forks: ', jsonBasic['forks_count']
      print 'latest release publish date: ', jsonLatest['published_at']
      print 'Licesne: ', jsonLicense['license']['name']
      print 'Open Issues Count: ', jsonBasic['open_issues_count']
      print 'Subscribers Count: ', jsonBasic['subscribers_count']

      map={}
      map["github_url"] = githubURL
      map["number_of_starts"] = jsonBasic['watchers_count']
      map["number_of_forks"] = jsonBasic['forks_count']
      map["latest_release_publish_date"] = jsonLatest['published_at']
      map["licesne"] = jsonLicense['license']['name']
      map["open_issues_count"] = jsonBasic['open_issues_count']
      map["subscribers_count"] = jsonBasic['subscribers_count']
      return json.dumps({"result": map})


def queryOpenHub(queryTerm):
    api_key = "85690631252ec7681f0e7ac7f46725c4fcc8b56cd2f6c38cb4a7cf7961512f98"
    #query_term = "electron"
    page_num = "1"
    url = "https://www.openhub.net/projects.xml?api_key=" + api_key + "&query=" + queryTerm + "&page=" + page_num
    resp = requests.get(url,verify=False)
    print url
    soup = BeautifulSoup(resp.content, "html.parser")
    # we use beautiful soup to get the #1 rank project id & url on Openhub
    project_id = soup.find('id').get_text()
    print project_id
    project_html_url = soup.find('html_url').get_text()
    print project_html_url

    project_query_url = "https://www.openhub.net/projects/" + str(project_id) + ".xml?api_key=" + api_key
    print project_query_url

    openhub_resp_content = requests.get(project_query_url,verify=False).content

    openhub_soup = BeautifulSoup(openhub_resp_content, "html.parser")
    project_twelve_month_contributor_count = openhub_soup.find('twelve_month_contributor_count').get_text()
    project_total_contributor_count = openhub_soup.find('total_contributor_count').get_text()
    project_twelve_month_commit_count = openhub_soup.find('twelve_month_commit_count').get_text()
    project_total_commit_count = openhub_soup.find('total_commit_count').get_text()
    project_total_code_lines = openhub_soup.find('total_code_lines').get_text()
    project_main_language_name = openhub_soup.find('main_language_name').get_text()
    project_license = openhub_soup.find('license').find('name').get_text()
    project_project_activity_index_description = openhub_soup.find('project_activity_index').find('description').get_text()

    map={}
    map["project_html_url"] = project_html_url
    map["project_twelve_month_contributor_count"] = project_twelve_month_contributor_count
    map["project_total_contributor_count"] = project_total_contributor_count
    map["project_twelve_month_commit_count"] = project_twelve_month_commit_count
    map["project_total_commit_count"] = project_total_commit_count
    map["project_total_code_lines"] = project_total_code_lines
    map["project_main_language_name"] = project_main_language_name
    map["project_license"] = project_license
    map["project_project_activity_index_description"] = project_project_activity_index_description

    return json.dumps({"result": map})

    # print project_twelve_month_contributor_count
    # print project_total_contributor_count
    # print project_twelve_month_commit_count
    # print project_total_commit_count
    # print project_total_code_lines
    # print project_main_language_name
    # print project_license
    # print project_project_activity_index_description



if __name__ == "__main__":
    searchTerm = raw_input('Search GitHub repo: ')
    queryOpenHub(searchTerm)
    #queryGithub(searchTerm)