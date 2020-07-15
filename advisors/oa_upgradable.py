#!/usr/bin/python3
"""
This is a script to check upgradable information against upstream
"""
from pyrpm.spec import Spec, replace_macros

import yaml
import json
import datetime
import sys
import os
import argparse

import urllib.error

import gitee
import check_upstream
import version_recommend


def get_ver_tags(gt, repo, d_path=None):
    """
    Get version tags of given package
    """
    repo_yaml = ""
    if d_path:
        try:
            repo_yaml = open(os.path.join(d_path, repo + ".yaml")).read()
        except FileNotFoundError:
            print("Failed to get YAML info from default path.")

    if not repo_yaml:
        try:
            repo_yaml = gt.get_yaml(repo)
        except urllib.error.HTTPError:
            print("Failed to get YAML info for {pkg}".format(pkg=repo))
            return None

    pkg_info = yaml.load(repo_yaml, Loader=yaml.Loader)

    vc_type = pkg_info["version_control"]
    if vc_type == "hg":
        tags = check_upstream.check_hg(pkg_info)
    elif vc_type == "github":
        tags = check_upstream.check_github(pkg_info)
    elif vc_type == "git":
        tags = check_upstream.check_git(pkg_info)
    elif vc_type == "gitlab.gnome":
        tags = check_upstream.check_gnome(pkg_info)
    elif vc_type == "svn":
        tags = check_upstream.check_svn(pkg_info)
    elif vc_type == "metacpan":
        tags = check_upstream.check_metacpan(pkg_info)
    elif vc_type == "pypi":
        tags = check_upstream.check_pypi(pkg_info)
    else:
        print("Unsupport version control method {vc}".format(vc=vc_type))
        return None
    
    return tags


if __name__ == "__main__":
    parameters = argparse.ArgumentParser()
    parameters.add_argument("-p", "--push", action="store_true",
            help="Push the version bump as an issue to src-openeuler repository") 
    parameters.add_argument("-d", "--default", type=str, default=os.getcwd(),
            help="The fallback place to look for YAML information")
    parameters.add_argument("repo", type=str,
            help="Repository to be checked for upstream version info") 

    args = parameters.parse_args()

    user_gitee = gitee.Gitee()
    spec_string = user_gitee.get_spec(args.repo)
    if not spec_string:
        print("{pkg}.spec can't be found on the master branch".format(pkg=args.repo))
        sys.exit(1)

    spec_file = Spec.from_string(spec_string)
    cur_version = replace_macros(spec_file.version, spec_file)

    print("Checking ", args.repo)
    print("current version is ", cur_version)

    pkg_tags = get_ver_tags(user_gitee, args.repo, args.default)
    if pkg_tags is None:
        sys.exit(1)
    ver_rec = version_recommend.VersionRecommend(pkg_tags, cur_version, 0)

    print("known release tags :", pkg_tags)
    print("Latest version is ", ver_rec.latest_version)
    print("Maintain version is", ver_rec.maintain_version)
