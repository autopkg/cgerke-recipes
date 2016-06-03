#!/usr/bin/env python
#
# FileZillaURLProvider
# Copyright 2013 Samuel Keeley, derived from BarebonesURLProvider by Timothy Sutton
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

import urllib2
import re

from autopkglib import Processor, ProcessorError

__all__ = ["FileZillaURLProvider"]

update_url = "http://update.filezilla-project.org/updatecheck.php?platform=i686-apple-darwin9&version=3.0.0&osversion=12"

prods = {"FileZilla": "release",
         "FileZilla_release": "release",
         "FileZilla_beta": "beta",
         "FileZilla_nightly": "nightly"
         }


class FileZillaURLProvider(Processor):
    description = "Provides a version and compressed download for the FileZilla product given."
    input_variables = {
        "product_name": {
            "required": True,
            "description": "Product to fetch URL for. One of 'FileZilla', 'FileZilla_release', 'FileZilla_beta', 'FileZilla_nightly'.",
        },
    }
    output_variables = {
        "version": {
            "description": "Version of the product.",
        },
        "url": {
            "description": "Download URL.",
        }
    }

    __doc__ = description

    def main(self):

        valid_prods = prods.keys()
        prod = self.env.get("product_name")
        if prod not in valid_prods:
            raise ProcessorError(
                "product_name %s is invalid; it must be one of: %s" %
                (prod, valid_prods))

        try:
            manifest_str = urllib2.urlopen(update_url).read()
            # print manifest_str
        except BaseException as e:
            raise ProcessorError(
                "Unexpected error retrieving product manifest: '%s'" %
                e)

        version = None
        url = None

        if prod == "FileZilla_beta":
            for item in manifest_str.split("\n"):
                if "beta" in item:
                    item_strip = item.strip()
                    line_split = item_strip.split()
                    url = line_split[2]
                    version = line_split[1]
        elif prod == "FileZilla_nightly":
            for item in manifest_str.split("\n"):
                if "nightly" in item:
                    item_strip = item.strip()
                    line_split = item_strip.split()
                    url = line_split[2]
                    version = line_split[1]
        elif prod == "FileZilla" or prod == "FileZilla_release":
            for item in manifest_str.split("\n"):
                if "release" in item:
                    item_strip = item.strip()
                    line_split = item_strip.split()
                    url = line_split[2]
                    version = line_split[1]

        if not version or not url:
            raise ProcessorError("Version or URL not found")

        self.env["version"] = version
        self.env["url"] = url
        self.output("Found URL %s" % self.env["url"])

if __name__ == "__main__":
    processor = FileZillaURLProvider()
    processor.execute_shell()
