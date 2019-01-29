"""
Copyright 2018 Skyscanner Ltd

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""


from cfripper.model.rule_processor import Rule


class IAMRoleWildcardActionOnPermissionsPolicyRule(Rule):

    REASON = "IAM role {} should not allow * action on its permissions policy {}"
    MONITOR_MODE = False

    def invoke(self, resources, parameters):
        for resource in resources.get("AWS::IAM::Role", []):
            for policy in resource.policies:
                if policy.policy_document.wildcard_allowed_actions(pattern=r"^(\w*:){0,1}\*$"):
                    self.add_failure(
                        type(self).__name__,
                        self.REASON.format(
                            resource.logical_id,
                            policy.policy_name,
                        ),
                    )
