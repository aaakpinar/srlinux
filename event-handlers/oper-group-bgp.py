import sys
import json

# count_up_uplinks returns the number of monitored uplinks that have oper-state=up
def count_up_uplinks(paths):
    up_cnt = 0
    for path in paths:
        if path.get("value", "down") == "up":
            up_cnt = up_cnt + 1
    return up_cnt

# required_up_uplinks returns the value of the `required-up-uplinks` option
def required_up_uplinks(options):
    return int(options.get("required-up-uplinks", 1))

# main entry function for event handler
def event_handler_main(in_json_str):
    # parse input json string passed by event handler
    in_json = json.loads(in_json_str)
    paths = in_json["paths"]
    options = in_json["options"]

    num_up_uplinks = count_up_uplinks(paths)
    downlinks_new_state = (
        "down" if num_up_uplinks < required_up_uplinks(options) else "up"
    )

    # add `debug="true"` option to event-handler configuration to output parsed parameters
    if options.get("debug") == "true":
        print(
            f"num of required up uplinks = {required_up_uplinks(options)}\n\
detected num of up uplinks = {num_up_uplinks}\n\
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
