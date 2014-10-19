#!/usr/bin/env python
#
# Copyright 2014 chris.gerke@gmail.com
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

import os.path
import subprocess
import shutil

from glob import glob
from autopkglib import Processor, ProcessorError

__all__ = ["PkgDistributionCreator"]

class PkgDistributionCreator(Processor):
    description = ("Creates a distribution style package. ")
    input_variables = {
        "distribution_file": {
            "required": True,
            "description": ("Path to a distribution file. "),
        },
        "resources_path": {
            "required": True,
            "description": ("Path to a resources. "),
        },
        "source_path": {
            "required": True,
            "description": ("Path to a pkg. "),
        },
        "destination_file": {
            "required": True,
            "description": ("File to be created "),
        },
    }
    output_variables = {
    }

    __doc__ = description
    source_path = None

    def pkgConvert(self):
        if os.path.exists('/usr/bin/productbuild'):
            try:
                self.output("Found binary %s" % '/usr/bin/productbuild')
            except OSError as e:
                raise ProcessorError(
                    "Can't find binary %s: %s" % ('/usr/bin/productbuild', e.strerror))
        try:
            pbcmd = ["/usr/bin/productbuild",
                      "--distribution", self.env['distribution_file'],
                      "--resources", self.env['resources_path'],
                      "--package-path", self.env['source_path'],
                      self.env['destination_file']]
            p = subprocess.Popen(pbcmd,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            (out, err) = p.communicate()
        except OSError as e:
            raise ProcessorError("cmmac execution failed with error code %d: %s"
                % (e.errno, e.strerror))
        if p.returncode != 0:
            raise ProcessorError("cmmac conversion of %s failed: %s"
                % (self.env['source_path'], err))
                
    def main(self):
        if os.path.exists(self.env['source_path']):
            try:
                self.output("Found %s" % self.env['source_path'])
            except OSError as e:
                raise ProcessorError(
                    "Can't find %s" % (self.env['source_path'], e.strerror))
        if os.path.exists(self.env['destination_file']):
            try:
                self.output("Found %s" % self.env['destination_file'])
            except OSError as e:
                raise ProcessorError(
                    "Can't find %s" % (self.env['destination_file'], e.strerror))
        if os.path.exists(self.env['distribution_file']):
            try:
                self.output("Found %s" % self.env['distribution_file'])
                self.pkgConvert()
            except OSError as e:
                raise ProcessorError(
                    "Can't find %s" % (self.env['distribution_file'], e.strerror))

if __name__ == '__main__':
    processor = PkgDistributionCreator()
    processor.execute_shell()
