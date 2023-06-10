import subprocess
import os
import argparse
from typing import Optional, Sequence
from collections import OrderedDict
import math


#CMD = ['rm', '-rf']
CMD = ['test', '-n']

class Cleanup:
    """remove files sorted on disk usage"""

    def __init__(self, path: str, limit: int, days: str, ftype: str, brief: bool, check: bool, force: bool) -> None:
        """search for find, sort them on size and optionaly remove them"""
        self.path = path
        self.limit = limit
        self.days = "+" + days
        self.ftype = ftype
        self.brief = brief
        self.check = check
        self.force = force
        self.count = 0
        self.total_rm = 0
        self.warning = '\033[93m'
        self.okblue =  '\033[94m'
        self.okcyan = '\033[96m'
        self.endc = '\033[0m'

        if dir_list := self._get_dirs():
            if dir_details := self._get_dir_size(dirs=dir_list):
                if top_dirs := self._sort_dirs(dir_dict=dir_details):
                    print(f"Files in {self.path}: {len(top_dirs)}\nResult limit is: {self.limit}\n")
                    for key, val in top_dirs.items():
                        self.count += 1
                        active = False
                        if self.count <= self.limit:
                            if self.brief:
                                print(key)
                            else:
                                print(f"file: {key}\ntype: {subprocess.run(['file', '-b',key], stdout=subprocess.PIPE, text=True).stdout}size: {self._convert(size_bytes=val)}\n")
                            if not self.force:
                                active = input(self.warning + "delete item? (y/n)? " + self.endc).lower() == "y"
                            if active and not self.check or self.force and not self.check:
                                self._rm_dirs(key)
                                if not self.force:
                                    print(self.okblue + "Removed!\n" + self.endc)
                            if self.check and active:
                                print(self.okblue + "Not removed! (check mode)\n" + self.endc)
                            if not active and not self.force:
                                print(self.okcyan + "Skipping\n" + self.endc)
                            self.total_rm += val
                    total_rm_gb = self._convert(size_bytes=self.total_rm)
                    print(f"Total removed: {total_rm_gb}")



    def _convert(self, size_bytes:int):
        """Convert bytes to human readable format
        
        Args:
            int:

        Returns:
            str: Filesize in reasonable units
        """

        if size_bytes == 0:
            return "0B"
        i = int(math.floor(math.log(size_bytes, 1024)))
        a = {0: "b",1: "k", 2: "m", 3: "g", 4: "t", 5: "p", 6: "e"}
        r = size_bytes / (1024**i)
        return "%s%s" % (round(r, 2), (a[i]))

    def _get_dirs(self):
        """Return a list of files in given path

        Returns:
            list: Files found
        """

        proc = subprocess.Popen(['find', self.path, '-maxdepth', '1', '-mindepth','1','-mtime', self.days, '-type', self.ftype], stdout=subprocess.PIPE, text=True)
        return proc.stdout.read().splitlines()

    def _get_dir_size(self, dirs:list):
        """Get disk usage of files 
        
        Args:
            list: list of files

        Returns:
            dict: filename and filesize as k, v 
        """
        
        dir_details = {}
        for dir in dirs:
            du = subprocess.run(['du', '-b', '-d 0', dir], capture_output=True, text=True).stdout.strip()
            single_dir = du.split("\t")[:2]
            dir_details[single_dir[1]] = single_dir[0]
        return dir_details

    def _sort_dirs(self, dir_dict: dict):
        """Sort files on disk usage 
        
        Args:
            dict: unsorted dict with filename and filesize

        Returns:
            dict: sorted dict with filename and filesize
        """

        return {k: int(v) for k, v in sorted(dir_dict.items(),key=lambda item: int(item[1]), reverse=True)}

    def _rm_dirs(self, key: str):
        """Remove files 
        
        Args:
            dict: sorted dict with filename and filesize
        """
        
        run_rm = subprocess.run([CMD[0],CMD[1],key])


def get_argparser(argv: Optional[Sequence[str]] = None):
    parser = argparse.ArgumentParser(
        description="List directories ordered on disk usage and optionaly remove them.",
    )
    parser.add_argument("path", help="Directory to scan")
    parser.add_argument(
        "-l",
        "--limit",
        metavar="\b",
        default=5,
        type=int,
        help="Number of files to return (default %(default)s)",
    )
    parser.add_argument(
        "-d",
        "--days",
        metavar="\b",
        default="0",
        help='Amount of days file is not modified (default "%(default)s")',
    )
    parser.add_argument(
        "-t",
        "--filetype",
        metavar="\b",
        default="f,d",
        help='File is of type (default "%(default)s")',
    )
    parser.add_argument(
        "-b",
        "--brief",
        default=False,
        action=argparse.BooleanOptionalAction,
        help="Dont show file details",
    )
    parser.add_argument(
        "-c",
        "--check",
        metavar="\b",
        default=False,
        action=argparse.BooleanOptionalAction,
        help="Run without making any changes",
    )
    parser.add_argument(
        "-f",
        "--force",
        default=False,
        action=argparse.BooleanOptionalAction,
        help="Do not prompt before removal",
    )

    return parser


if __name__ == "__main__":
    parser = get_argparser()
    args = parser.parse_args()

    Cleanup(path=args.path, limit=args.limit, days=args.days, ftype=args.filetype, brief=args.brief, check=args.check, force=args.force)


