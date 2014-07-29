#!/usr/bin/env python
#
# Copyright 2013 Greg Neagle
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import glob

from autopkglib import Processor, ProcessorError


__all__ = ["ThinImageModulesSourceFinder"]



class ThinImageModulesSourceFinder(Processor):
    """Finds the root autopkg-template folder from the expanded zip archive"""
    input_variables = {
        "input_path": {
            "required": True,
            "description": "Path the zip archive was expanded to.",
        },
    }
    output_variables = {
        "pkg_path": {
            "description": "Root path of expanded archive.",
        },
    }
    description = __doc__

    def find_match(self, root_dir, match_string):
        """Finds a file or directory using shell globbing"""
        matches = glob.glob(os.path.join(root_dir, match_string))
        if matches:
            return matches[0][len(root_dir) + 1:]
        else:
            return ""

    def main(self):
        # Get root dir
        root_dir = self.env["input_path"]
        try:
            pkg_dir = self.find_match(root_dir, '*autopkg-template*')
            self.env["pkg_path"] = os.path.join(root_dir, pkg_dir)
            self.output("Found %s" % self.env["pkg_path"])
        except BaseException as err:
            raise ProcessorError(err)


if __name__ == "__main__":
    processor = ThinImageModulesSourceFinder()
    processor.execute_shell()
