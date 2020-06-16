#!/usr/bin/python3
"""
This is a simple script to check if SPEC already been submit into repository.
If not, it can be used to push an issue to remind the developer.
"""

import argparse
import gitee
import urllib.error
from datetime import datetime

new_issue_body = """Dear {repo} maintainer:
亲爱的 {repo} 维护者：

We found there is no spec file in this repository's master branch yet.
我们发现这个代码仓 master branch 中没有 spec 文件。

Missing spec file implies that this components will not be integtaed into latest openEuler release, and your hardworking cannot help others.
缺少 spec 文件意味着这个项目还不能被集成到 openEuler 项目中，而您的贡献还不能帮助到社区中的其他人。

We courage you submit your spec file into this repository as soon as possible.
我们鼓励您尽快提交 spec 文件到这个代码仓中.

This is a automatic advise from openEuler-Advisor. If you think the advise is not correct, please fill an issue at https://gitee.com/openeuler/openEuler-Advisor to help us improve.
这是一条由 openEuler-Advisor 自动生成的建议。如果您认为这个建议不对，请访问 https://gitee.com/openeuler/openEuler-Advisor 来帮助我们改进。

Yours openEuler Advisor.
"""

new_comment = """Dear {repo} maintainer:

We found this issue has been open for {days} days.

If you have any problems to implement it, please let the community known.

We'll try to help.

This is a automatic advise from openEuler-Advisor. If you think the advise is not correct, please fill an issue at https://gitee.com/openeuler/openEuler-Advisor to help us imporove.

Yours openEuler Advisor.
"""

if __name__ == "__main__":
    pars = argparse.ArgumentParser()
    pars.add_argument("repo", type=str, help="Repo to be checked")
    pars.add_argument("-p", "--push", help="Push the advise to gitee.com/src-openeuler", action="store_true")

    args = pars.parse_args()

    my_gitee = gitee.Gitee()
    try:
        spec_string = my_gitee.get_spec(args.repo)
    except urllib.error.HTTPError:
        spec_string = ""

    if spec_string == "":
        print("no spec file found for {repo} project".format(repo=args.repo))
        if args.push:
            issues = my_gitee.get_issues(args.repo)
            for issue in issues:
                if issue["title"] == "Submit spec file into this repository":
                    ages = datetime.now() - my_gitee.get_gitee_datetime(issue["created_at"])
                    if ages.days <= 10:
                        print("Advise has been issues only %d days ago" % ages.days)
                        print("Give developers more time to handle it.")
                        break
                    else:
                        my_gitee.post_issue_comment(args.repo, issue["number"],
                                new_comment.format(repo=args.repo, days=ages.days))
                    break
            else:
                my_gitee.post_issue(args.repo,
                        "Submit spec file into this repository",
                        new_issue_body.format(repo=args.repo))
        else:
            print("Keep this between us.")
    else:
        print("Everything's fine")

