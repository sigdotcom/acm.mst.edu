.. _tutorial-git:

===
Git
===
Git is a powerful version control system which is utilized very heavily around
the world. In almost any job, you will expected to use some form of version
control system. This tutorial will focus mainly on the basics of how to use git
with regards to GitHub, but if you're interested in learning more look at the
:ref:`references section <git-references>`.

------------------------
What is Version Control?
------------------------
When something is called 'version control' what does that mean exactly? 

The primary feature of a 'version control' system is that it keeps tracks of
'code revisions' by tracking source code changes over time. Whenever you change
your code, you have the ability to stop and takes a 'snapshot' that will create
a 'delta' between the previous file and the new file. These 'deltas' can be used
to traverse forwards or backwards through the state of the file based on when
these 'deltas' are taken.

Take this project as an example. Let's say SIG.com wants to add a new feature
that allows users to login using their GitHub accounts. As this feature is
developed, more snapshots are created until the feature is complete. For some
reason, this feature completely breaks login and no users can login anymore.
With version control, the website can be reverted all the way back to before the
feature was implemented to a know, safe state.

--------------------
Cloning a Repository
--------------------
'Cloning' a Repository is Git's way of downloading all of the snapshots and all
of the important Git data stored remotely. Using all of this data and the
snapshot 'delta' process discussed above, Git will traverse the deltas to the
latest version of the code.

.. _git-references:

----------
References
----------
`Pro Git <https://git-scm.com/book/en/v2>`_
    A very informative online book about everything Git.

`GitKraken YouTube Channel <https://www.youtube.com/gitkraken>`_
    Specific tutorials using Git with the GitKraken GUI.
