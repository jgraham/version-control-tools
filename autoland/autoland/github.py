class MockGithub3(object):
    """ This class mocks out the github3 stuff we use to allow us to test
        without access to github. """

    def pull_request(self, user, repo, pullrequest):
        class PullRequest(object):
            def commits(self):
                class Commit(object):
                    sha = '05830c796e2b0e9049c9e9cd463d987f4aedf4a35'
                    def patch(self):
                        return """# HG changeset patch
# User Cthulhu <cthulhu@mozilla.com>
# Date 1428426710 14400
#      Tue Apr 07 13:11:50 2015 -0400
# Node ID 5830c796e2b0e9049c9e9cd463d987f4aedf4a35
# Parent  0000000000000000000000000000000000000000
bug 1 - did stuff

diff --git a/hello b/hello
new file mode 100644
--- /dev/null
+++ b/hello
@@ -0,0 +1,1 @@
+hello, world!"""
                return [Commit()]
        return PullRequest()

    def issue(self, user, repo, issue):
        class Issue(object):
           def create_comment(self, comment):
                return True
        return Issue()


        config = json.load(f)
        credentials = config['github']
        testing = config.get('testing', False)

    if testing:
        return MockGithub3()