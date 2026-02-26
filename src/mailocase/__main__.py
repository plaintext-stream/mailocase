import argparse
import sys

from mailocase.commands.delete import cmd_delete
from mailocase.commands.draft import cmd_draft
from mailocase.commands.init import cmd_init
from mailocase.commands.list import cmd_list
from mailocase.commands.send import cmd_send
from mailocase.render import cmd_render


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="mailocase",
        description="Local mailing list emulator and static site generator",
    )
    sub = parser.add_subparsers(dest="command", metavar="verb")

    p_init = sub.add_parser("init", help="Initialize a mailocase directory")
    p_init.add_argument("location", nargs="?", default=".", metavar="location")

    p_draft = sub.add_parser("draft", help="Create or edit a draft")
    p_draft.add_argument(
        "name", nargs="?", metavar="ts+rand_str",
        help="Existing draft filename to open (omit to create new)",
    )
    p_draft.add_argument("-a", "--send-as",  dest="send_as",   metavar="addr",
                         help="Send as address (must be listed in config addresses)")
    p_draft.add_argument("-r", "--reply-to", dest="reply_to",  metavar="hash",
                         help="Set reply-to a sent item (overwrites existing)")
    p_draft.add_argument("-c", "--cc",       dest="cc",        metavar="addr", nargs="+",
                         help="Overwrite CC recipients (space-separated)")
    p_draft.add_argument(      "--cc+",      dest="cc_add",    metavar="addr", nargs="+",
                         help="Append to CC recipients (space-separated)")
    p_draft.add_argument(      "--cc-",      dest="cc_remove", metavar="addr", nargs="+",
                         help="Remove from CC recipients (space-separated)")

    p_send = sub.add_parser("send", help="Send a draft")
    p_send.add_argument("name", metavar="ts+rand_str")
    p_send.add_argument("-a", "--send-as",  dest="send_as",   metavar="addr",
                        help="Send as address (must be listed in config addresses)")
    p_send.add_argument("-r", "--reply-to", dest="reply_to",  metavar="hash",
                        help="Set reply-to a sent item (overwrites existing)")
    p_send.add_argument("-c", "--cc",       dest="cc",        metavar="addr", nargs="+",
                        help="Overwrite CC recipients (space-separated)")
    p_send.add_argument(      "--cc+",      dest="cc_add",    metavar="addr", nargs="+",
                        help="Append to CC recipients (space-separated)")
    p_send.add_argument(      "--cc-",      dest="cc_remove", metavar="addr", nargs="+",
                        help="Remove from CC recipients (space-separated)")

    p_delete = sub.add_parser("delete", help="Delete a draft or sent mail")
    p_delete.add_argument("name", metavar="ts+rand_str or hash")

    p_render = sub.add_parser("render", help="Generate the static website")
    p_render.add_argument(
        "output", nargs="?", default="site", metavar="output_dir",
        help="Output directory (default: site/)",
    )

    p_list = sub.add_parser("list", help="Search and list emails")
    p_list.add_argument("--root",          action="store_true",
                        help="Only root messages (no In-Reply-To)")
    p_list.add_argument("--from",          dest="from_addr",     metavar="email",
                        help="Filter by from address")
    p_list.add_argument("--cc",            dest="cc_filter",     metavar="email",
                        help="Filter where this email appears in CC")
    p_list.add_argument("--subject",       metavar="regex",
                        help="Subject matches regex")
    p_list.add_argument("--content",       metavar="regex",
                        help="Any body line matches regex")
    p_list.add_argument("--include-draft", dest="include_draft", action="store_true",
                        help="Include draft/ files")

    args = parser.parse_args()

    match args.command:
        case "init":
            cmd_init(args.location)
        case "draft":
            cmd_draft(args.name, args.reply_to,
                      args.cc, args.cc_add, args.cc_remove, args.send_as)
        case "send":
            cmd_send(args.name, args.reply_to,
                     args.cc, args.cc_add, args.cc_remove, args.send_as)
        case "delete":
            cmd_delete(args.name)
        case "render":
            cmd_render(args.output)
        case "list":
            cmd_list(args.root, args.from_addr, args.cc_filter,
                     args.subject, args.content, args.include_draft)
        case _:
            parser.print_help()
            sys.exit(1)


if __name__ == "__main__":
    main()
