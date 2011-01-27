#!/usr/bin/python

'''A restricted environment to allow users to execute commands by way of ssh,
restricted by their public key. Enable by making this the target of the
command="..." argument in .ssh/authorized_keys for the key to be restricted.
Example:

    in .ssh/sendmail_or_sleep.py:

        #!/usr/bin/python
        from datagrok.misc.sshrestrictor import run
        run(valid = [(re.compile(x), c) for (x, c) in [

            # User may call sendmail
            (r'(?:/usr/sbin/)?sendmail [a-zA-Z0-9. -]*$', '/usr/sbin/sendmail'),

            # Or just sleep a bit, useful for establishing tunnels.
            (r'(?:/bin/)?sleep \d?\d?\d$', '/bin/sleep'),

        ]])

    in .ssh/authorized_keys:

        command="~/.ssh/sendmail_or_sleep.py" ssh-rsa AAAAB3za...LiPk== user@example.net

To do: support optional re-writing of arguments instead of passing them
directly to validated executable.

'''
__author__ = 'Michael F. Lamb <mike@datagrok.org>'
__date__ = 'Wed, 27 Feb 2008 03:12:54 -0400'

import os
import re


def main(valid):
    """Match requested command against list of patterns, first to match is
    executed. Otherwise exit with nonzero status.

    valid is a list of (re, path) 2-tuples where:

        re is a compiled regular expression object (or any other object with a
        .match(string) method accepting one argument).

        path is the full path to the acutal executable to be run.

    """

    # TODO: make 'valid' more robust, so that it might accept (string, string)
    # pairs in addition to (re_object, string) pairs. Similar to django's URL
    # matching mechanism.

    try:
        cmd = os.environ['SSH_ORIGINAL_COMMAND']
    except KeyError:
        raise SystemExit("Permission denied for interactive shell.")

    for rx, c in valid_re:
        if rx.match(cmd):
            # TODO: support a mechanism for rewriting arguments
            os.execvp(c, cmd.split())
            # os.execvp replaces this process with new; script essentially ends
            # here. Imagine a call to sys.exit().

    raise SystemExit("Permission denied for that command.")
