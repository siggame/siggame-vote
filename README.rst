Vote
====

A stupid web app to allow SIG-Game devs to vote using GitHub's OAUTH
stuff.

Deployment Reminders
--------------------

If you're an idiot like Wisely, you're going to need to remember to 
check the following:

* Make sure nginx is configured properly
* Make sure you run ``syncdb``
* Make sure you run ``collectstatic`` if nginx is configured to serve
  out of vote/var/static
* Make sure the GitHub application is configured properly. It may not
  always point to megaminerai.com.


Github Organization Checking
----------------------------

The app uses the ``user:email`` and ``repo`` OAuth scopes from the 
GitHub API. They don't provide very fine-grained access controls, so 
we have to request read/write tokens for user repos. It's a consequence
of some users being private members of the organization.

If a member is on a private MegaMinerAI SIG-Game GitHub team, they are 
a private member of the organization. Meaning, their membership in the 
organization isn't dispayed publicly on their profile. To see whether
they're a member of a SIG-Game team (and hence the oraganization), we 
need to have access to their private repos. The only way to see that is
by using the ``repo`` scope, which allows read-write to all public
and private repositories.

Them's the breaks.
