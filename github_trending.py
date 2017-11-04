import requests
import datetime


def get_starting_date(period_days):
    starting_date = datetime.datetime.today()-datetime.timedelta(period_days)
    return starting_date.strftime("%Y-%m-%d")


def get_trending_repositories(top_size, period_days):
    starting_date = get_starting_date(period_days)
    url = 'https://api.github.com/search/repositories'
    parameters = {
                  'q': 'created:>{}'.format(starting_date),
                  'sort': 'stars',
                  'order': 'desc',
                  'per_page': '{}'.format(top_size),
                  }
    response = requests.get(url, parameters)
    return response.json()['items']


def get_open_issues_amount(repo_owner, repo_name):
    issue_url = "https://api.github.com/repos/{}/{}/issues".format(
       repo_owner,
       repo_name,
    )
    open_issues = requests.get(issue_url, {'state': 'open'}).json()
    return len(open_issues)


def add_issues(repositories):
    for repository in repositories:
        repository['issues'] = get_open_issues_amount(
            repository['owner']['login'],
            repository['name'],
        )
    return repositories


def print_repos_and_issues(repositories):
    print('Top repositories for the last seven days: ')
    for place, repo in enumerate(repositories, start=1):
        print(place, repo['html_url'])
        print('\t Stars = {}'.format(repo['watchers']))
        print('\t Open issues = {}'.format(repo['issues']))


if __name__ == '__main__':
    trending_repositories = get_trending_repositories(
                                                top_size=20,
                                                period_days=7,
                                                      )
    trending_repositories = add_issues(trending_repositories)
    print_repos_and_issues(trending_repositories)
