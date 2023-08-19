#!/usr/bin/env bash
#
# this runs a local redis-server and accepts run|start|stop|status args;
# use the run command to leave redis in the foreground.
# note: the default command is status

set -euo pipefail

failures=0
trap 'failures=$((failures+1))' ERR

VERBOSE="false"  # set to "true" for extra output

CMD_ARG=${1:-status}
PORT=${PORT:-0}
export RIPC_RUNTIME_DIR=${RIPC_RUNTIME_DIR:-/tmp/redis-ipc}
[[ -d $RIPC_RUNTIME_DIR ]] || mkdir -p $RIPC_RUNTIME_DIR

echo "Using socket runtime dir: ${RIPC_RUNTIME_DIR}"

if [[ "${CMD_ARG}" = "status" ]]; then
    [[ "${VERBOSE}" = "true" ]]  && echo "pinging redis-server on local socket..."
    redis-cli -s ${RIPC_RUNTIME_DIR}/socket ping
fi

if [[ "${CMD_ARG}" = "start" ]]; then
    [[ "${VERBOSE}" = "true" ]]  && echo "starting redis-server on local socket..."
    redis-server --port ${PORT} --pidfile ${RIPC_RUNTIME_DIR}/redis.pid --unixsocket ${RIPC_RUNTIME_DIR}/socket --unixsocketperm 600 &
    sleep 1
    redis-cli -s ${RIPC_RUNTIME_DIR}/socket config set save ""
fi

if [[ "${CMD_ARG}" = "run" ]]; then
    [[ "${VERBOSE}" = "true" ]]  && echo "starting redis-server in foreground..."
    redis-server --port ${PORT} --pidfile ${RIPC_RUNTIME_DIR}/redis.pid --unixsocket ${RIPC_RUNTIME_DIR}/socket --unixsocketperm 600
fi

if [[ "${CMD_ARG}" = "stop" ]]; then
    [[ "${VERBOSE}" = "true" ]]  && echo "killing redis-server on local socket in 1 sec..."
    sleep 1
    cat ${RIPC_RUNTIME_DIR}/redis.pid | xargs kill
    sleep 1
    rmdir $RIPC_RUNTIME_DIR
fi

if ((failures == 0)); then
    echo "Success"
else
    echo "Something went wrong"
    exit 1
fi
