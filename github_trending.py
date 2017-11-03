import requests
import datetime


def get_starting_date(days_delta):
    starting_date = datetime.datetime.today()-datetime.timedelta(days_delta)
    return starting_date.strftime("%Y-%m-%d")


def get_trending_repositories(top_size, days_delta):
    starting_date = get_starting_date(days_delta)
    url = 'https://api.github.com/search/repositories'
    parameters = {
                  'q': 'created:>{}'.format(starting_date),
                  'sort': 'stars',
                  'order': 'desc',
                  'per_page': '{}'.format(top_size),
                  }
    request = requests.get(url, parameters)
    return request.json()['items']


def get_open_issues_amount(repo_owner, repo_name):
    url_pattern = "https://api.github.com/repos/{}/{}/issues"
    url = url_pattern.format(repo_owner, repo_name)
    open_issues = requests.get(url, {'state': 'open'}).json()
    return len(open_issues)


def print_repos_and_issues(repositories):
    print('Top repositories for the last seven days: ')
    for place, repo in enumerate(repositories, start=1):
        print(place, repo['html_url'])
        print('\t Stars = {}'.format(repo['watchers']))
        issues_amount = get_open_issues_amount(
            repo['owner']['login'],
            repo['name'],
        )
        print('\t Open issues = {}'.format(issues_amount))


if __name__ == '__main__':
    trending_repositories = get_trending_repositories(
                                                top_size=20,
                                                days_delta=7,
                                                      )
    print_repos_and_issues(trending_repositories)
