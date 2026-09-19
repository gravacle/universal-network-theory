#!/usr/bin/env python3
"""Explicitly gated paid launch of the two Phase-1 EC2 instances.

Preparation and validation never call this file.  It requires both a production
config with launch_enabled=true and an exact command-line authorization token.
"""

import argparse
import base64
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from decimal import Decimal
from pathlib import Path


HERE = Path(__file__).resolve().parent
CODE_ROOT = HERE.parent
sys.path.insert(0, str(CODE_ROOT))

from branch_runner import validate_request
from durable_evidence import (
    AppendOnlyJournal,
    EvidenceError,
    immutable_write_bytes,
    immutable_write_json,
    load_json,
    sha256_bytes,
    sha256_file,
)
from readiness import verify_aws, verify_local
from stage_control import stack_outputs


def aws_json(command):
    completed = subprocess.run(["aws"] + command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if completed.returncode != 0:
        raise EvidenceError("AWS command failed: {}".format(completed.stderr.strip()))
    return json.loads(completed.stdout)


def authenticate_object(bucket, key, expected_sha256, expected_bytes=None, version_id=None):
    command = ["s3api", "head-object", "--bucket", bucket, "--key", key]
    if version_id:
        command.extend(["--version-id", version_id])
    command.extend(["--output", "json"])
    head = aws_json(command)
    metadata = head.get("Metadata", {})
    if metadata.get("sha256") != expected_sha256:
        raise EvidenceError("S3 object SHA-256 metadata mismatch: {}".format(key))
    if expected_bytes is not None and int(head.get("ContentLength", -1)) != int(expected_bytes):
        raise EvidenceError("S3 object byte-size mismatch: {}".format(key))
    if version_id and head.get("VersionId") != version_id:
        raise EvidenceError("S3 object version mismatch: {}".format(key))


def authenticate_override_assets(evidence_path, stack_name, run_id, config, bucket):
    evidence = load_json(evidence_path)
    if (
        evidence.get("schema") != "L14_NO_COMPUTE_ASSET_STAGING_V003"
        or evidence.get("run_id") != run_id
        or evidence.get("account_id") != config.get("account_id")
        or evidence.get("region") != config.get("region")
        or evidence.get("stack_name") != stack_name
    ):
        raise EvidenceError("override-asset evidence identity mismatch")
    objects = evidence.get("objects", {})
    for name in ("bootstrap", "source_bundle"):
        record = objects.get(name, {})
        if record.get("bucket") != bucket:
            raise EvidenceError("override-asset bucket mismatch: {}".format(name))
        authenticate_object(
            bucket,
            str(record.get("s3_key")),
            str(record.get("sha256")),
            int(record.get("bytes", -1)),
            str(record.get("version_id")),
        )
    return evidence


def launch_template_user_data(template_id, version):
    response = aws_json(
        [
            "ec2",
            "describe-launch-template-versions",
            "--launch-template-id",
            template_id,
            "--versions",
            str(version),
            "--output",
            "json",
        ]
    )
    versions = response.get("LaunchTemplateVersions", [])
    if len(versions) != 1:
        raise EvidenceError("AWS did not return exactly one launch-template version")
    encoded = versions[0].get("LaunchTemplateData", {}).get("UserData")
    if not encoded:
        raise EvidenceError("launch-template version has no user data")
    try:
        return base64.b64decode(encoded, validate=True)
    except Exception as error:
        raise EvidenceError("launch-template user data is not valid base64: {}".format(error))


def corrected_user_data(template_id, version, stack_input_evidence, override_assets, config):
    data = launch_template_user_data(template_id, version)
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise EvidenceError("launch-template user data is not UTF-8: {}".format(error))
    parameters = {
        record["ParameterKey"]: record["ParameterValue"]
        for record in stack_input_evidence.get("parameters", [])
    }
    objects = override_assets["objects"]
    old_minutes = str(parameters["RuntimeAdvisoryMinutes"])
    new_minutes = str(config["runtime_advisory_after_minutes"])
    substitutions = (
        (parameters["BootstrapKey"], objects["bootstrap"]["s3_key"]),
        (parameters["BootstrapSha256"], objects["bootstrap"]["sha256"]),
        (parameters["SourceBundleKey"], objects["source_bundle"]["s3_key"]),
        (
            "L14_RUNTIME_ADVISORY_MINUTES='{}'".format(old_minutes),
            "L14_RUNTIME_ADVISORY_MINUTES='{}'".format(new_minutes),
        ),
    )
    for old, new in substitutions:
        if text.count(old) != 1:
            raise EvidenceError("expected exactly one launch-payload token: {}".format(old))
        text = text.replace(old, new, 1)
    return data, text.encode("utf-8")


def aws_dry_run(command):
    completed = subprocess.run(
        ["aws"] + command + ["--dry-run"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    diagnostic = completed.stdout + completed.stderr
    if "DryRunOperation" not in diagnostic:
        raise EvidenceError("AWS launch dry-run failed: {}".format(diagnostic.strip()))


def authenticate_stack_and_assets(stack_name, evidence_path, run_root, run_id, config, outputs):
    evidence = load_json(evidence_path)
    if (
        evidence.get("schema") != "L14_NO_COMPUTE_STACK_INPUTS_V002"
        or evidence.get("run_id") != run_id
        or evidence.get("account_id") != config.get("account_id")
        or evidence.get("region") != config.get("region")
    ):
        raise EvidenceError("no-compute stack-input evidence identity mismatch")
    template = evidence.get("cloudformation_template", {})
    if sha256_file(CODE_ROOT / "aws" / "cloudformation.yaml") != template.get("sha256"):
        raise EvidenceError("deployed-template evidence does not match reviewed template")

    deployed_template = aws_json(
        ["cloudformation", "get-template", "--stack-name", stack_name, "--template-stage", "Original", "--output", "json"]
    ).get("TemplateBody")
    if not isinstance(deployed_template, str):
        raise EvidenceError("CloudFormation did not return the original template body as text")
    deployed_template_sha256 = hashlib.sha256(deployed_template.encode("utf-8")).hexdigest()
    local_template_bytes = (CODE_ROOT / "aws" / "cloudformation.yaml").read_bytes()
    local_template_sha256 = hashlib.sha256(local_template_bytes).hexdigest()
    if deployed_template_sha256 != local_template_sha256:
        raise EvidenceError("deployed CloudFormation template body differs from reviewed bytes")
    if outputs.get("ReviewedTemplateSha256") != local_template_sha256:
        raise EvidenceError("deployed template-hash output differs from reviewed bytes")

    description = aws_json(
        ["cloudformation", "describe-stacks", "--stack-name", stack_name, "--output", "json"]
    )
    stacks = description.get("Stacks", [])
    if len(stacks) != 1 or stacks[0].get("StackStatus") not in ("CREATE_COMPLETE", "UPDATE_COMPLETE"):
        raise EvidenceError("no-compute stack is absent or not complete")
    actual_parameters = {
        record["ParameterKey"]: record["ParameterValue"]
        for record in stacks[0].get("Parameters", [])
    }
    expected_parameters = {
        record["ParameterKey"]: record["ParameterValue"]
        for record in evidence.get("parameters", [])
    }
    if actual_parameters != expected_parameters:
        raise EvidenceError("deployed CloudFormation parameters differ from authenticated inputs")

    bucket = outputs["EvidenceBucketName"]
    bootstrap = evidence.get("bootstrap", {})
    source_bundle = evidence.get("source_bundle", {})
    authenticate_object(
        bucket,
        str(bootstrap.get("s3_key")),
        str(bootstrap.get("sha256")),
        int(bootstrap.get("bytes", -1)),
    )
    authenticate_object(
        bucket,
        str(source_bundle.get("s3_key")),
        str(source_bundle.get("sha256")),
        int(source_bundle.get("bytes", -1)),
    )

    request_path = run_root / "PHASE1_REQUEST.json"
    request = load_json(request_path)
    validate_request(request, "target", "bridge")
    validate_request(request, "hostile", "bridge")
    if request.get("run_id") != run_id:
        raise EvidenceError("local Phase-1 request run-id mismatch")
    request_key = "runs/{}/control/PHASE1_REQUEST.json".format(run_id)
    authenticate_object(bucket, request_key, sha256_file(request_path), request_path.stat().st_size)
    return evidence


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--stack-name", required=True)
    parser.add_argument("--run-root", required=True, type=Path)
    parser.add_argument("--stack-input-evidence", required=True, type=Path)
    parser.add_argument("--override-assets-evidence", type=Path)
    parser.add_argument("--launch-template-version", default="$Latest")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--attempt-id", required=True)
    parser.add_argument("--authorize-paid-launch", required=True, metavar="RUN_ID:ATTEMPT_ID")
    parser.add_argument("--bindings", type=Path, default=CODE_ROOT / "KERNEL_BINDINGS_RELEASE_V003R3.json")
    args = parser.parse_args()
    config = load_json(args.config)
    if config.get("schema") != "L14_AWS_RUN_CONFIG_V002" or config.get("launch_enabled") is not True:
        raise EvidenceError("production config does not explicitly enable launch")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,31}", args.attempt_id):
        raise EvidenceError("attempt-id is not a safe bounded identifier")
    authorization_token = "{}:{}".format(args.run_id, args.attempt_id)
    if args.authorize_paid_launch != authorization_token:
        raise EvidenceError("paid-launch authorization token must exactly equal run-id:attempt-id")
    checks = []
    blockers = []
    bindings = load_json(args.bindings)
    verify_local(config, bindings, checks, blockers)
    observations = verify_aws(config, checks, blockers)
    if blockers:
        raise EvidenceError("mandatory production readiness failed: {}".format(",".join(blockers)))

    os.environ["AWS_PROFILE"] = str(config["control_profile"])
    os.environ["AWS_DEFAULT_REGION"] = str(config["region"])
    outputs = stack_outputs(args.stack_name)
    bucket = outputs["EvidenceBucketName"]
    run_root = args.run_root.expanduser().resolve()
    attempt_root = run_root / "paid_attempts" / args.attempt_id
    if attempt_root.exists():
        raise EvidenceError("paid-attempt evidence root already exists")
    stack_input_evidence = authenticate_stack_and_assets(
        args.stack_name,
        args.stack_input_evidence.expanduser().resolve(),
        run_root,
        args.run_id,
        config,
        outputs,
    )
    override_assets = None
    if args.override_assets_evidence:
        if not str(args.launch_template_version).isdigit():
            raise EvidenceError("asset override requires an exact numeric launch-template version")
        override_assets = authenticate_override_assets(
            args.override_assets_evidence.expanduser().resolve(),
            args.stack_name,
            args.run_id,
            config,
            bucket,
        )
    quota = aws_json(
        [
            "service-quotas",
            "get-service-quota",
            "--service-code",
            "ec2",
            "--quota-code",
            "L-1216C47A",
            "--output",
            "json",
        ]
    )
    if Decimal(str(quota["Quota"]["Value"])) < Decimal(str(config["required_standard_on_demand_vcpus"])):
        raise EvidenceError("Standard On-Demand vCPU quota is insufficient")

    prepared_user_data = {}
    launch_template_version = str(args.launch_template_version)
    with tempfile.TemporaryDirectory(prefix="l14-launch-") as temporary_directory:
        temporary_root = Path(temporary_directory)
        for branch, output_key in (
            ("target", "TargetLaunchTemplateId"),
            ("hostile", "HostileLaunchTemplateId"),
        ):
            template_id = outputs[output_key]
            if override_assets:
                original, user_data = corrected_user_data(
                    template_id,
                    launch_template_version,
                    stack_input_evidence,
                    override_assets,
                    config,
                )
            else:
                original = launch_template_user_data(template_id, launch_template_version)
                user_data = original
            temporary_path = temporary_root / "{}_user_data.sh".format(branch)
            temporary_path.write_bytes(user_data)
            command = [
                "ec2",
                "run-instances",
                "--launch-template",
                "LaunchTemplateId={},Version={}".format(template_id, launch_template_version),
                "--user-data",
                "fileb://{}".format(temporary_path),
                "--count",
                "1",
                "--client-token",
                "{}-{}-{}-phase1".format(args.run_id, args.attempt_id, branch),
            ]
            aws_dry_run(command)
            prepared_user_data[branch] = {
                "bytes": user_data,
                "original_sha256": sha256_bytes(original),
                "sha256": sha256_bytes(user_data),
                "launch_template_id": template_id,
            }

    attempt_root.mkdir(parents=True, exist_ok=False)
    journal = AppendOnlyJournal(attempt_root / "aws_launch_journal")
    allocations = {}
    for branch, output_key in (
        ("target", "TargetLaunchTemplateId"),
        ("hostile", "HostileLaunchTemplateId"),
    ):
        template_id = outputs[output_key]
        user_data_path = attempt_root / "AWS_USER_DATA_{}.sh".format(branch)
        immutable_write_bytes(user_data_path, prepared_user_data[branch]["bytes"])
        response = aws_json(
            [
                "ec2",
                "run-instances",
                "--launch-template",
                "LaunchTemplateId={},Version={}".format(template_id, launch_template_version),
                "--user-data",
                "fileb://{}".format(user_data_path),
                "--count",
                "1",
                "--client-token",
                "{}-{}-{}-phase1".format(args.run_id, args.attempt_id, branch),
                "--output",
                "json",
            ]
        )
        instances = response.get("Instances", [])
        if len(instances) != 1:
            raise EvidenceError("AWS did not return one {} instance".format(branch))
        instance_id = instances[0]["InstanceId"]
        allocations[branch] = {
            "instance_id": instance_id,
            "launch_template_id": template_id,
            "launch_template_version": launch_template_version,
            "user_data_sha256": prepared_user_data[branch]["sha256"],
        }
        journal.append("INSTANCE_ALLOCATED", {"branch": branch, "instance_id": instance_id, "launch_template_id": template_id})
        immutable_write_json(
            attempt_root / "AWS_INSTANCE_ALLOCATION_{}.json".format(branch),
            {
                "schema": "L14_AWS_BRANCH_ALLOCATION_V003",
                "run_id": args.run_id,
                "attempt_id": args.attempt_id,
                "branch": branch,
                "instance_id": instance_id,
                "launch_template_id": template_id,
                "launch_template_version": launch_template_version,
                "user_data_sha256": prepared_user_data[branch]["sha256"],
                "original_user_data_sha256": prepared_user_data[branch]["original_sha256"],
            },
        )
        print("L14_AWS_INSTANCE branch={} instance_id={}".format(branch, instance_id), flush=True)

    record = {
        "schema": "L14_AWS_INSTANCE_ALLOCATION_V003",
        "run_id": args.run_id,
        "attempt_id": args.attempt_id,
        "region": config["region"],
        "instance_type": config["instance_type"],
        "instances": allocations,
        "runtime_advisory_minutes": config["runtime_advisory_after_minutes"],
        "estimated_compute_cost_usd": config["estimated_compute_cost_usd"],
        "readiness_checks": checks,
        "aws_observations": observations,
        "stack_input_evidence": {
            "path": str(args.stack_input_evidence.expanduser().resolve()),
            "sha256": sha256_file(args.stack_input_evidence.expanduser().resolve()),
        },
        "override_assets_evidence": (
            {
                "path": str(args.override_assets_evidence.expanduser().resolve()),
                "sha256": sha256_file(args.override_assets_evidence.expanduser().resolve()),
            }
            if args.override_assets_evidence
            else None
        ),
        "stack_parameters": stack_input_evidence["parameters"],
    }
    immutable_write_json(attempt_root / "AWS_INSTANCE_ALLOCATION.json", record)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print("L14_PAID_LAUNCH_REFUSAL type={} message={}".format(type(error).__name__, error), file=sys.stderr)
        raise SystemExit(2)
