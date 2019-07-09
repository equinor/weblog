#!/usr/bin/env python
"""wlog is a lightweight thin logger that logs against a logger service.

"""

import web_log


def wlog():
    import sys

    args = sys.argv
    if len(args) > 1 and args[1] == "-v":
        print("wlog %s" % web_log.WEBLOG_VERSION)
        exit(0)
    if len(args) < 3:
        exit("Usage: wlog application event [extra]\n       wlog -v")
    extra = ""
    application = args[1]
    event = args[2]
    extra = " ".join(args[3:])
    web_log.log(application, event, extra_info=extra)


if __name__ == "__main__":
    main()
