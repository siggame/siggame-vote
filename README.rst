Vote
====

A stupid web app to allow SIG-Game devs to vote using GitHub's OAUTH
stuff.


Wisely's Thoughts.
------------------

From what I can tell, it's not possible for a user to see what teams
they're on. It's the responsibility of the Organization Owners to see
place users on teams and manage their access.

We could just save the access_token for a team owner, but that seems
like a bad idea. We can still figure out if the user's on a team by
keeping a little data. Namely, the team's ``id``.

Here's how to enforce team-wise permissions:

1. Organization owner pulls up django admin interface to make a new 
   voting topic

   * GitHub uses owner's token to list possible teams by hitting
     ``/orgs/siggame/teams``. This may require ``user`` scope. ::

        {
         "name": "MegaMinerAI 11",
         "id": 335202,
         "slug": "megaminerai-11",
         ...
        },


2. Owner fills out the form, chooses the team, and lists some choices
   to vote on

   * Voting app saves the chosen team and its corresponding id

3. User tries to access a ballot

   * Voting app hits ``/teams/:id/members``, where ``:id`` is the team's id 
     which was saved in step 1.
   * If the user is a member, we get an HTTP 200 back. Otherwise, they're
     not a member, so redirect them away
