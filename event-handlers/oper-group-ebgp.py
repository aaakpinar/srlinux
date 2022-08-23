import sys
import json

# count_ebgp_sessions_established returns the number of monitored eBGP sessions that are established  {established=up}
def count_ebgp_sessions_established(paths):
    up_cnt = 0
    for path in paths:
        if path.get("value") == "established":
            up_cnt = up_cnt + 1
    return up_cnt


# required_ebgp_sessions_established returns the value of the `required-ebgp-sessions-established` option
def required_ebgp_sessions_established(options):
    return int(options.get("required-ebgp-sessions-established", 1))


# main entry function for event handler
def event_handler_main(in_json_str):
    # parse input json string passed by event handler
    in_json = json.loads(in_json_str)
    paths = in_json["paths"]
    options = in_json["options"]

    num_up_ebgp_sessions = count_ebgp_sessions_established(paths)
    downlinks_new_state = (
        "down" if num_up_ebgp_sessions < required_ebgp_sessions_established(options) else "up"
    )

    if options.get("debug") == "true":
        print(
            f"\nnum of required eBGP sessions established = {required_ebgp_sessions_established(options)}\n\
detected num of eBGP sessions established = {num_up_ebgp_sessions}\n\
downlinks new state = {downlinks_new_state}"
        )

    response_actions = []

    for downlink in options.get("down-links", []):
        response_actions.append(
            {
                "set-ephemeral-path": {
                    "path": f"interface {downlink} oper-state",
                    "value": downlinks_new_state,
                }
            }
        )

    response = {"actions": response_actions}
    return json.dumps(response)
