#!/bin/bash

# Environment check
source .env
# If migrating from localhost, set this to localhost
if [[ ! $SOURCE_HOST_ADDRESS ]]
then
  echo "Please set the current host address in SOURCE_HOST_ADDRESS"
  exit 1
fi

# If migrating from localhost, set this to $USER
if [[ ! $SOURCE_HOST_USER ]]
then
  echo "Please set the current host user in SOURCE_HOST"
  exit 1
fi

# If migrating to localhost, set this to localhost
if [[ ! $TARGET_HOST_ADDRESS ]]
then
  echo "Please set the new host address in TARGET_HOST_ADDRESS"
  exit 1
fi

# If migrating to localhost, set this to $USER
if [[ ! $TARGET_HOST_USER ]]
then
  echo "Please set the new host user in TARGET_HOST_USER"
  exit 1
fi

# Argument check

if [[ ! $1 ]]
then
  echo "Please supply a docker volume name, as displayed by the command 'docker volume ls'"
  exit 1
fi
volume_name=$1

# Export the volume from the current instance

echo "Exporting volume $volume_name on $SOURCE_HOST_ADDRESS"
ssh "$SOURCE_HOST_USER"@"$SOURCE_HOST_ADDRESS" "\
mkdir -p \$HOME/docker-volume-backup
docker run \
  --rm \
  -v $volume_name:/volume-backup-source \
  -v \$HOME/docker-volume-backup:/volume-backup-target \
  busybox \
  sh -c 'cd /volume-backup-source && tar cf /volume-backup-target/backup.tar .' \
"


# Transfer the exported volume to the new address

echo "Transferring exported volume $volume_name from $SOURCE_HOST_ADDRESS to $TARGET_HOST_ADDRESS"
ssh "$TARGET_HOST_USER"@"$TARGET_HOST_ADDRESS" "mkdir -p \$HOME/docker-volume-backup"
scp -3 "$SOURCE_HOST_USER"@"$SOURCE_HOST_ADDRESS":./docker-volume-backup/backup.tar \
  "$TARGET_HOST_USER"@"$TARGET_HOST_ADDRESS":./docker-volume-backup/backup.tar


# Restore the backup

echo "Creating volume $volume_name on $TARGET_HOST_ADDRESS"
ssh "$TARGET_HOST_USER"@"$TARGET_HOST_ADDRESS" "\
docker volume create $volume_name \
&& docker run \
  --rm \
  -v $volume_name:/volume-backup-target \
  -v \$HOME/docker-volume-backup/:/volume-backup-source \
  busybox \
  sh -c 'cd /volume-backup-target && tar xf /volume-backup-source/backup.tar .' \
"

# Clean up residual files

echo "Cleaning up unnecessary files"
ssh "$SOURCE_HOST_USER"@"$SOURCE_HOST_ADDRESS" "rm -rf \$HOME/docker-volume-backup"
ssh "$TARGET_HOST_USER"@"$TARGET_HOST_ADDRESS" "rm -rf \$HOME/docker-volume-backup"

echo "Successfully migrated docker volume $volume_name from $SOURCE_HOST_ADDRESS to $TARGET_HOST_ADDRESS"
