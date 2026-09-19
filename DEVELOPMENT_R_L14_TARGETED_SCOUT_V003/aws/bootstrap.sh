#!/usr/bin/env bash
set -euo pipefail

required=(
  L14_BRANCH L14_BUCKET L14_PREFIX L14_RUN_ID L14_SOURCE_BUNDLE_KEY
  L14_SOURCE_BUNDLE_SHA256 L14_KERNEL_RELATIVE_PATH L14_KERNEL_SHA256
  L14_WORKERS L14_RUNTIME_ADVISORY_MINUTES AWS_DEFAULT_REGION
)
for name in "${required[@]}"; do
  if [[ -z "${!name:-}" ]]; then
    echo "L14_BOOTSTRAP_FAILURE missing ${name}" >&2
    exit 2
  fi
done
if [[ ! "${L14_BRANCH}" =~ ^(target|hostile)$ ]]; then
  echo "L14_BOOTSTRAP_FAILURE invalid branch" >&2
  exit 2
fi
for value in "${L14_RUN_ID}" "${L14_PREFIX}" "${L14_SOURCE_BUNDLE_KEY}" "${L14_KERNEL_RELATIVE_PATH}"; do
  if [[ "${value}" == *..* || "${value}" == /* ]]; then
    echo "L14_BOOTSTRAP_FAILURE unsafe path value" >&2
    exit 2
  fi
done

# The pinned Amazon Linux 2023 image contains AWS CLI v2 and a system Python
# used only to authenticate and guard bootstrap. The numerical interpreter is
# the immutable CPython archive carried inside the authenticated source bundle.
command -v /usr/bin/python3 >/dev/null
command -v aws >/dev/null
command -v curl >/dev/null
command -v lsblk >/dev/null
dnf install -y xfsprogs tar gzip

# Nitro can enumerate launch-time EBS attachments under arbitrary NVMe names,
# and ebsnvme-id may render the requested mapping as either "sdf" or
# "/dev/sdf".  Resolve the stable EBS volume ID through EC2, then authenticate
# the Linux block device by the volume ID carried in its NVMe serial.  Never
# select or format a disk from size, enumeration order, or a partial match.
imds_token="$(curl -fsS -X PUT \
  -H 'X-aws-ec2-metadata-token-ttl-seconds: 21600' \
  http://169.254.169.254/latest/api/token)"
instance_id="$(curl -fsS \
  -H "X-aws-ec2-metadata-token: ${imds_token}" \
  http://169.254.169.254/latest/meta-data/instance-id)"
if [[ ! "${instance_id}" =~ ^i-[a-f0-9]+$ ]]; then
  echo "L14_BOOTSTRAP_FAILURE invalid IMDS instance identity" >&2
  exit 2
fi

ebs_volume_for_mapping() {
  local requested_mapping="$1"
  local volume_id=""
  local attempt
  for attempt in $(seq 1 20); do
    volume_id="$(aws ec2 describe-volumes \
      --region "${AWS_DEFAULT_REGION}" \
      --filters \
        "Name=attachment.instance-id,Values=${instance_id}" \
        "Name=attachment.device,Values=${requested_mapping}" \
      --query 'Volumes[0].VolumeId' \
      --output text 2>/dev/null || true)"
    if [[ "${volume_id}" =~ ^vol-[a-f0-9]+$ ]]; then
      printf '%s\n' "${volume_id}"
      return 0
    fi
    sleep 3
  done
  echo "L14_BOOTSTRAP_FAILURE cannot authenticate EBS mapping ${requested_mapping}" >&2
  return 2
}

nvme_device_for_volume() {
  local volume_id="$1"
  local expected_serial="${volume_id//-/}"
  local attempt device serial device_type normalized_serial
  local matches=()
  for attempt in $(seq 1 20); do
    matches=()
    while read -r device serial device_type; do
      [[ "${device_type}" == "disk" ]] || continue
      normalized_serial="$(printf '%s' "${serial}" | tr '[:upper:]' '[:lower:]' | tr -d '-')"
      if [[ "${normalized_serial}" == "${expected_serial}" ]]; then
        matches+=("${device}")
      fi
    done < <(lsblk -dn -o PATH,SERIAL,TYPE --raw --noheadings)
    if [[ "${#matches[@]}" -eq 1 && -b "${matches[0]}" ]]; then
      printf '%s\n' "${matches[0]}"
      return 0
    fi
    if [[ "${#matches[@]}" -gt 1 ]]; then
      echo "L14_BOOTSTRAP_FAILURE EBS volume ${volume_id} maps to multiple block devices" >&2
      return 2
    fi
    sleep 3
  done
  echo "L14_BOOTSTRAP_FAILURE EBS volume ${volume_id} has no authenticated NVMe device" >&2
  return 2
}

checkpoint_volume_id="$(ebs_volume_for_mapping /dev/sdf)"
scratch_volume_id="$(ebs_volume_for_mapping /dev/sdg)"
if [[ "${checkpoint_volume_id}" == "${scratch_volume_id}" ]]; then
  echo "L14_BOOTSTRAP_FAILURE checkpoint and scratch resolve to the same EBS volume" >&2
  exit 2
fi
checkpoint_device="$(nvme_device_for_volume "${checkpoint_volume_id}")"
scratch_device="$(nvme_device_for_volume "${scratch_volume_id}")"
echo "L14_EBS_AUTHENTICATED role=checkpoint mapping=/dev/sdf volume=${checkpoint_volume_id} device=${checkpoint_device}"
echo "L14_EBS_AUTHENTICATED role=scratch mapping=/dev/sdg volume=${scratch_volume_id} device=${scratch_device}"

readonly checkpoint_label="L14_CKPT"
readonly scratch_label="L14_SCRATCH"
for filesystem_label in "${checkpoint_label}" "${scratch_label}"; do
  if (( ${#filesystem_label} > 12 )); then
    echo "L14_BOOTSTRAP_FAILURE XFS label exceeds 12 bytes: ${filesystem_label}" >&2
    exit 2
  fi
done

if ! blkid "${checkpoint_device}" >/dev/null 2>&1; then
  mkfs.xfs -f -L "${checkpoint_label}" "${checkpoint_device}"
fi
mkdir -p /checkpoint
checkpoint_uuid="$(blkid -s UUID -o value "${checkpoint_device}")"
if ! grep -q "UUID=${checkpoint_uuid}" /etc/fstab; then
  echo "UUID=${checkpoint_uuid} /checkpoint xfs defaults,nofail 0 2" >> /etc/fstab
fi
mountpoint -q /checkpoint || mount /checkpoint

if ! blkid "${scratch_device}" >/dev/null 2>&1; then
  mkfs.xfs -f -L "${scratch_label}" "${scratch_device}"
fi
mkdir -p /scratch
scratch_uuid="$(blkid -s UUID -o value "${scratch_device}")"
if ! grep -q "UUID=${scratch_uuid}" /etc/fstab; then
  echo "UUID=${scratch_uuid} /scratch xfs defaults,nofail 0 2" >> /etc/fstab
fi
mountpoint -q /scratch || mount /scratch
chmod 0700 /checkpoint /scratch

mkdir -p /opt/l14/releases
bundle=/opt/l14/source.tar.gz
aws s3 cp "s3://${L14_BUCKET}/${L14_SOURCE_BUNDLE_KEY}" "${bundle}" --only-show-errors
echo "${L14_SOURCE_BUNDLE_SHA256}  ${bundle}" | sha256sum -c -
release="/opt/l14/releases/${L14_SOURCE_BUNDLE_SHA256}"
if [[ ! -d "${release}" ]]; then
  mkdir "${release}"
  tar -xzf "${bundle}" -C "${release}" --strip-components=1
fi
ln -sfn "${release}" /opt/l14/current
/usr/bin/python3 -B /opt/l14/current/aws/verify_bundle.py --root /opt/l14/current
runtime=/opt/l14/runtimes/${L14_SOURCE_BUNDLE_SHA256}
if [[ ! -f "${runtime}/.READY" ]]; then
  if [[ -e "${runtime}" ]]; then
    echo "L14_BOOTSTRAP_FAILURE incomplete exact runtime exists at ${runtime}" >&2
    exit 2
  fi
  mkdir -p /opt/l14/runtimes
  runtime_staging="$(mktemp -d "/opt/l14/runtimes/.${L14_SOURCE_BUNDLE_SHA256}.XXXXXX")"
  python_archive="$(/usr/bin/python3 -B -c 'import json; print(json.load(open("/opt/l14/current/BUNDLE_MANIFEST.json"))["runtime"]["python_archive_path"])')"
  tar -xzf "/opt/l14/current/${python_archive}" -C "${runtime_staging}"
  mv "${runtime_staging}" "${runtime}"
  "${runtime}/python/bin/python3" -m venv --copies "${runtime}/venv"
  "${runtime}/venv/bin/python" -m pip install \
    --disable-pip-version-check \
    --no-index \
    --require-hashes \
    --find-links /opt/l14/current/runtime/wheelhouse \
    -r /opt/l14/current/runtime/requirements.lock
  "${runtime}/venv/bin/python" -B /opt/l14/current/aws/verify_bundle.py \
    --root /opt/l14/current \
    --verify-runtime
  printf '%s\n' "${L14_SOURCE_BUNDLE_SHA256}" >"${runtime}/.READY"
fi
"${runtime}/venv/bin/python" -B /opt/l14/current/aws/verify_bundle.py \
  --root /opt/l14/current \
  --verify-runtime
kernel="/opt/l14/current/${L14_KERNEL_RELATIVE_PATH}"
echo "${L14_KERNEL_SHA256}  ${kernel}" | sha256sum -c -

install -d -m 0700 "/checkpoint/${L14_RUN_ID}" "/checkpoint/${L14_RUN_ID}/runtime_ledger"
install -d -m 0700 "/scratch/${L14_RUN_ID}"
cat >/etc/l14-scout.env <<EOF
L14_BRANCH=${L14_BRANCH}
L14_BUCKET=${L14_BUCKET}
L14_PREFIX=${L14_PREFIX}
L14_RUN_ID=${L14_RUN_ID}
L14_CODE_ROOT=/opt/l14/current
L14_KERNEL_MODULE=${kernel}
L14_KERNEL_SHA256=${L14_KERNEL_SHA256}
L14_WORKERS=${L14_WORKERS}
L14_RUNTIME_ADVISORY_MINUTES=${L14_RUNTIME_ADVISORY_MINUTES}
L14_CHECKPOINT_ROOT=/checkpoint/${L14_RUN_ID}
L14_SCRATCH_ROOT=/scratch/${L14_RUN_ID}
L14_PYTHON=${runtime}/venv/bin/python
PYTHONPATH=/opt/l14/current
L14_EXPECTED_LOGICAL_CPUS=192
L14_EXPECTED_PHYSICAL_CORES=192
L14_MIN_MEMORY_MIB=1500000
AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION}
PYTHONDONTWRITEBYTECODE=1
PYTHONHASHSEED=0
OMP_NUM_THREADS=1
MKL_NUM_THREADS=1
OPENBLAS_NUM_THREADS=1
NUMEXPR_NUM_THREADS=1
VECLIB_MAXIMUM_THREADS=1
OMP_DYNAMIC=FALSE
MKL_DYNAMIC=FALSE
MALLOC_ARENA_MAX=2
EOF
chmod 0600 /etc/l14-scout.env

cat >/etc/systemd/system/l14-branch.service <<'EOF'
[Unit]
Description=L14 independent numerical branch
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
EnvironmentFile=/etc/l14-scout.env
WorkingDirectory=/opt/l14/current
ExecStartPre=-/usr/bin/python3 -B /opt/l14/current/aws/runtime_guard.py
ExecStartPre=-/opt/l14/current/aws/run_performance_preflight.sh
ExecStart=/opt/l14/current/aws/run_branch_once.sh
KillSignal=SIGTERM
TimeoutStartSec=infinity
TimeoutStopSec=infinity
SuccessExitStatus=0 10 75
Nice=-5
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
EOF

cat >/etc/systemd/system/l14-runtime-guard.service <<'EOF'
[Unit]
Description=L14 persistent runtime advisory ledger

[Service]
Type=oneshot
EnvironmentFile=/etc/l14-scout.env
WorkingDirectory=/opt/l14/current
ExecStart=/usr/bin/python3 -B /opt/l14/current/aws/runtime_guard.py
EOF

cat >/etc/systemd/system/l14-runtime-guard.timer <<'EOF'
[Unit]
Description=Record L14 runtime progress and advisory state every minute

[Timer]
OnBootSec=30
OnUnitActiveSec=60
AccuracySec=1
Persistent=true

[Install]
WantedBy=timers.target
EOF

systemctl daemon-reload
systemctl enable --now l14-runtime-guard.timer
systemctl enable --now l14-branch.service
echo "L14_BOOTSTRAP_COMPLETE branch=${L14_BRANCH} run_id=${L14_RUN_ID}"
