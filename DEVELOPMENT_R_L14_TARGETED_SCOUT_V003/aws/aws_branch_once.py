#!/usr/bin/env python3
"""Execute at most one authorized L14 phase on an AWS branch instance."""

import json
import os
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path


CODE_ROOT = Path(os.environ["L14_CODE_ROOT"]).resolve()
sys.path.insert(0, str(CODE_ROOT))

from branch_runner import validate_branch_result, validate_request
from durable_evidence import DurableMirror, EvidenceError, immutable_write_bytes, immutable_write_json, load_json, sha256_file


def aws(command):
    completed = subprocess.run(["aws"] + command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if completed.returncode != 0:
        raise EvidenceError("AWS command failed: {}".format(completed.stderr.strip()))
    return completed.stdout


def object_exists(bucket, key):
    completed = subprocess.run(
        ["aws", "s3api", "head-object", "--bucket", bucket, "--key", key],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    return completed.returncode == 0


def download_owner_once(bucket, key, destination):
    destination = Path(destination)
    head = json.loads(
        aws(["s3api", "head-object", "--bucket", bucket, "--key", key, "--output", "json"])
    )
    expected_sha256 = head.get("Metadata", {}).get("sha256")
    expected_bytes = int(head.get("ContentLength", -1))
    if not isinstance(expected_sha256, str) or len(expected_sha256) != 64 or expected_bytes < 0:
        raise EvidenceError("owner-once S3 object lacks authenticated metadata: {}".format(key))
    with tempfile.TemporaryDirectory(dir=str(destination.parent)) as temporary:
        staged = Path(temporary) / destination.name
        aws(["s3", "cp", "s3://{}/{}".format(bucket, key), str(staged), "--only-show-errors"])
        if staged.stat().st_size != expected_bytes or sha256_file(staged) != expected_sha256:
            raise EvidenceError("downloaded S3 object differs from authenticated metadata: {}".format(key))
        immutable_write_bytes(destination, staged.read_bytes())
    return destination


def metadata(path):
    token_request = urllib.request.Request(
        "http://169.254.169.254/latest/api/token",
        data=b"",
        method="PUT",
        headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"},
    )
    with urllib.request.urlopen(token_request, timeout=2.0) as response:
        token = response.read().decode("utf-8")
    request = urllib.request.Request(
        "http://169.254.169.254/latest/meta-data/{}".format(path),
        headers={"X-aws-ec2-metadata-token": token},
    )
    with urllib.request.urlopen(request, timeout=2.0) as response:
        return response.read().decode("utf-8")


def request_snapshot(checkpoint_root, branch, phase, run_id):
    evidence = Path(checkpoint_root) / phase / branch / "SNAPSHOT_REQUESTED.json"
    if evidence.exists():
        return
    instance_id = metadata("instance-id")
    raw = aws(
        [
            "ec2",
            "describe-volumes",
            "--filters",
            "Name=attachment.instance-id,Values={}".format(instance_id),
            "Name=attachment.device,Values=/dev/sdf",
            "--output",
            "json",
        ]
    )
    volumes = json.loads(raw).get("Volumes", [])
    if len(volumes) != 1:
        raise EvidenceError("cannot uniquely identify retained checkpoint EBS volume")
    volume_id = volumes[0]["VolumeId"]
    os.sync()
    snapshot = json.loads(
        aws(
            [
                "ec2",
                "create-snapshot",
                "--volume-id",
                volume_id,
                "--description",
                "L14 {} {} {} checkpoint".format(run_id, branch, phase),
                "--tag-specifications",
                "ResourceType=snapshot,Tags=[{Key=Project,Value=L14-Scout},{Key=RunId,Value=%s},{Key=Branch,Value=%s},{Key=Phase,Value=%s},{Key=PreserveEvidence,Value=true}]"
                % (run_id, branch, phase),
                "--output",
                "json",
            ]
        )
    )
    immutable_write_json(
        evidence,
        {
            "schema": "L14_CHECKPOINT_SNAPSHOT_REQUEST_V002",
            "run_id": run_id,
            "branch": branch,
            "phase": phase,
            "volume_id": volume_id,
            "snapshot_id": snapshot["SnapshotId"],
        },
    )


def main():
    branch = os.environ["L14_BRANCH"]
    bucket = os.environ["L14_BUCKET"]
    prefix = os.environ["L14_PREFIX"].strip("/")
    run_id = os.environ["L14_RUN_ID"]
    checkpoint_base = Path(os.environ["L14_CHECKPOINT_ROOT"]).resolve()
    kernel = Path(os.environ["L14_KERNEL_MODULE"]).resolve()
    if sha256_file(kernel) != os.environ["L14_KERNEL_SHA256"]:
        raise EvidenceError("exact kernel SHA-256 mismatch")

    phase1_output = checkpoint_base / "results" / "bridge" / branch / "BRANCH_RESULT.json"
    phase3_key = "{}/control/PHASE3_REQUEST.json".format(prefix)
    if phase1_output.exists() and not object_exists(bucket, phase3_key):
        DurableMirror("s3://{}/{}/results/bridge/{}".format(bucket, prefix, branch)).publish(
            phase1_output, "BRANCH_RESULT.json"
        )
        print("L14_AWS_WAITING_FOR_PHASE3_AUTHORIZATION", flush=True)
        return 10

    if object_exists(bucket, phase3_key):
        if not phase1_output.exists():
            raise EvidenceError("Phase 3 is present but this branch lacks authenticated Phase 1 output")
        phase = "conditional_tail"
        request_key = phase3_key
        request_name = "PHASE3_REQUEST.json"
        control_root = checkpoint_base / "control"
        control_root.mkdir(parents=True, exist_ok=True)
        gate_path = download_owner_once(bucket, "{}/control/PHASE2_GATE_REPORT.json".format(prefix), control_root / "PHASE2_GATE_REPORT.json")
        phase1_path = download_owner_once(bucket, "{}/control/PHASE1_RESULT.json".format(prefix), control_root / "PHASE1_RESULT.json")
    else:
        phase = "bridge"
        request_key = "{}/control/PHASE1_REQUEST.json".format(prefix)
        request_name = "PHASE1_REQUEST.json"

    control_root = checkpoint_base / "control"
    control_root.mkdir(parents=True, exist_ok=True)
    request_path = download_owner_once(bucket, request_key, control_root / request_name)
    request = load_json(request_path)
    validate_request(request, branch, phase)
    if request.get("run_id") != run_id:
        raise EvidenceError("AWS environment/request run-id mismatch")
    if phase == "conditional_tail":
        authorization = request.get("phase2_authorization")
        if not isinstance(authorization, dict):
            raise EvidenceError("Phase 3 authorization absent")
        if sha256_file(gate_path) != authorization.get("gate_report_sha256"):
            raise EvidenceError("Phase 2 gate report SHA-256 mismatch")
        if sha256_file(phase1_path) != authorization.get("phase1_result_sha256"):
            raise EvidenceError("Phase 1 merged result SHA-256 mismatch")

    phase_root = checkpoint_base / phase / branch
    phase_root.mkdir(parents=True, exist_ok=True)
    output = checkpoint_base / "results" / phase / branch / "BRANCH_RESULT.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        validate_branch_result(load_json(output), branch, phase, request)
    else:
        command = [
            sys.executable,
            "-B",
            str(CODE_ROOT / "branch_runner.py"),
            "--branch",
            branch,
            "--phase",
            phase,
            "--request",
            str(request_path),
            "--kernel-module",
            str(kernel),
            "--checkpoint-root",
            str(phase_root),
            "--shared-root",
            str(checkpoint_base / "shared" / branch),
            "--scratch-root",
            str(Path("/scratch/l14-v003") / run_id / branch / phase),
            "--output",
            str(output),
            "--workers",
            os.environ["L14_WORKERS"],
            "--mirror-destination",
            "s3://{}/{}/checkpoints/{}/{}".format(bucket, prefix, phase, branch),
        ]
        if (phase_root / "RUN_IDENTITY.json").exists():
            command.append("--resume")
        completed = subprocess.run(command, cwd=str(CODE_ROOT))
        if completed.returncode != 0:
            return completed.returncode

    destination = DurableMirror("s3://{}/{}/results/{}/{}".format(bucket, prefix, phase, branch))
    destination.publish(output, "BRANCH_RESULT.json")
    request_snapshot(checkpoint_base, branch, phase, run_id)
    snapshot_record = phase_root / "SNAPSHOT_REQUESTED.json"
    if snapshot_record.exists():
        destination.publish(snapshot_record, "SNAPSHOT_REQUESTED.json")
    print("L14_AWS_PHASE_COMPLETE branch={} phase={}".format(branch, phase), flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print("L14_AWS_BRANCH_FAILURE type={} message={}".format(type(error).__name__, error), file=sys.stderr, flush=True)
        raise SystemExit(2)
