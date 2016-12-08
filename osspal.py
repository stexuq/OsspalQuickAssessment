#!/usr/local/bin/python
import urllib, urlparse, string, time
import urllib2, base64, json
from urlparse import urlparse

def queryGithub(searchTerm):
      username = 'osspal'
      password = 'Practicum2017Osspal@CMU'

      #searchTerm = raw_input('Search GitHub repo: ')
      queryURL = "https://api.github.com/search/repositories?q=" + searchTerm

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
     

if __name__ == "__main__":
      searchTerm = raw_input('Search GitHub repo: ')
      queryGithub(searchTerm)
