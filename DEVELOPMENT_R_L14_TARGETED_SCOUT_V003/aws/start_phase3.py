#!/usr/bin/env python3
"""Restart the preserved Phase-1 instances only after Phase-3 authorization."""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
CODE_ROOT = HERE.parent
sys.path.insert(0, str(CODE_ROOT))

from branch_runner import validate_request
from durable_evidence import AppendOnlyJournal, EvidenceError, load_json, sha256_file
from stage_control import stack_outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--stack-name", required=True)
    parser.add_argument("--run-root", required=True, type=Path)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--attempt-id", required=True)
    parser.add_argument("--authorize-phase3-start", required=True, metavar="RUN_ID:ATTEMPT_ID")
    args = parser.parse_args()
    config = load_json(args.config)
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,31}", args.attempt_id):
        raise EvidenceError("attempt-id is not a safe bounded identifier")
    authorization_token = "{}:{}".format(args.run_id, args.attempt_id)
    if config.get("launch_enabled") is not True or args.authorize_phase3_start != authorization_token:
        raise EvidenceError("Phase-3 paid-start authorization is absent")
    os.environ["AWS_PROFILE"] = str(config["control_profile"])
    os.environ["AWS_DEFAULT_REGION"] = str(config["region"])
    attempt_root = args.run_root / "paid_attempts" / args.attempt_id
    allocation = load_json(attempt_root / "AWS_INSTANCE_ALLOCATION.json")
    if allocation.get("run_id") != args.run_id or allocation.get("attempt_id") != args.attempt_id:
        raise EvidenceError("instance allocation run/attempt identity mismatch")
    outputs = stack_outputs(args.stack_name)
    bucket = outputs["EvidenceBucketName"]
    request_path = args.run_root / "PHASE3_REQUEST.json"
    request = load_json(request_path)
    validate_request(request, "target", "conditional_tail")
    validate_request(request, "hostile", "conditional_tail")
    if request.get("run_id") != args.run_id:
        raise EvidenceError("local Phase-3 request run-id mismatch")
    head = subprocess.run(
        ["aws", "s3api", "head-object", "--bucket", bucket, "--key", "runs/{}/control/PHASE3_REQUEST.json".format(args.run_id), "--output", "json"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if head.returncode != 0:
        raise EvidenceError("owner-once PHASE3_REQUEST.json is absent")
    remote = json.loads(head.stdout)
    if (
        remote.get("Metadata", {}).get("sha256") != sha256_file(request_path)
        or int(remote.get("ContentLength", -1)) != request_path.stat().st_size
    ):
        raise EvidenceError("owner-once PHASE3_REQUEST.json differs from local authorization")
    instance_ids = [allocation["instances"][branch]["instance_id"] for branch in ("target", "hostile")]
    described = subprocess.run(
        ["aws", "ec2", "describe-instances", "--instance-ids"] + instance_ids + ["--output", "json"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if described.returncode != 0:
        raise EvidenceError("cannot authenticate preserved instances: {}".format(described.stderr.strip()))
    instances = {
        instance["InstanceId"]: instance
        for reservation in json.loads(described.stdout).get("Reservations", [])
        for instance in reservation.get("Instances", [])
    }
    if set(instances) != set(instance_ids):
        raise EvidenceError("cannot uniquely authenticate both preserved instances")
    for branch in ("target", "hostile"):
        expected = allocation["instances"][branch]
        instance = instances[expected["instance_id"]]
        tags = {record["Key"]: record["Value"] for record in instance.get("Tags", [])}
        checkpoint = [
            record
            for record in instance.get("BlockDeviceMappings", [])
            if record.get("DeviceName") == "/dev/sdf"
        ]
        identity_ok = bool(
            instance.get("State", {}).get("Name") == "stopped"
            and instance.get("InstanceType") == config.get("instance_type")
            and instance.get("LaunchTemplate", {}).get("LaunchTemplateId") == expected["launch_template_id"]
            and tags.get("Project") == "L14-Scout"
            and tags.get("RunId") == args.run_id
            and tags.get("Branch") == branch
            and len(checkpoint) == 1
            and checkpoint[0].get("Ebs", {}).get("DeleteOnTermination") is False
        )
        if not identity_ok:
            raise EvidenceError("preserved {} instance identity failed authentication".format(branch))

    journal = AppendOnlyJournal(attempt_root / "aws_phase3_start_journal")
    started_ids = []
    for branch in ("target", "hostile"):
        instance_id = allocation["instances"][branch]["instance_id"]
        started = subprocess.run(
            ["aws", "ec2", "start-instances", "--instance-ids", instance_id],
            check=False,
        )
        if started.returncode != 0:
            journal.append("INSTANCE_START_FAILED", {"branch": branch, "instance_id": instance_id})
            raise EvidenceError("Phase-3 {} start-instances failed".format(branch))
        started_ids.append(instance_id)
        journal.append("INSTANCE_STARTED", {"branch": branch, "instance_id": instance_id})
        print("L14_PHASE3_INSTANCE_STARTED branch={} instance_id={}".format(branch, instance_id), flush=True)
    print("L14_PHASE3_INSTANCES_STARTED {}".format(started_ids))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print("L14_PHASE3_START_REFUSAL type={} message={}".format(type(error).__name__, error), file=sys.stderr)
        raise SystemExit(2)
