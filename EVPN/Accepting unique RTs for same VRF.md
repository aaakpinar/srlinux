Workaround to accept EVPN updates coming for a VNI but with different RT. (Similar to import-as in Juniper)

1. First, let's filter out the VNI:

```
community-set target:vni-1 {
    member [
        target:.*:1
    ]
}
```
This community set uses a regular expression to match any route target community where:
- `(.*)` matches any ASN number
- `:1` matches specifically the value 1 (typically the VNI)
- So it would match communities like target:4200000001:1, target:4200000002:1, etc.

```
community-set target:marker {
    member [
        target:64496:64496
    ]
}
```
This creates a marker community (target:64496:64496) that will be used to mark routes that matched our first criteria.

2. The peer import policy:
```
policy import_peer_target_vni_1 {
    statement 10 {
        match {
            family [
                evpn
            ]
            bgp {
                community-set target:vni-1
            }
        }
        action {
            policy-result accept
            bgp {
                communities {
                    add target:marker
                }
            }
        }
    }
}
```
This policy:
- Matches EVPN routes that have a route target matching our regex pattern (any ASN with :1)
- For matching routes, it accepts them and adds the marker community (target:64496:64496)
- This is applied at the BGP peer level to process incoming routes

3. The VRF import policy:
```
policy import_vrf_target:anyRT {
    statement 10 {
        match {
            family [
                evpn
            ]
            bgp {
                community-set target:marker
            }
        }
        action {
            policy-result accept
        }
    }
}
```
This policy:
- Matches EVPN routes that have our marker community (target:64496:64496)
- Simply accepts these routes
- This is applied at the VRF level to import routes into the VRF

The overall workflow is:
1. EVPN routes come in from peers with different ASNs but all ending in :1
2. The peer import policy matches these routes using the regex and adds the marker community
3. The VRF import policy then matches the dummy community to import these routes into the VRF

This is a workaround for the limitation that extended community regex matching isn't supported directly in VRF import policies. Instead, it uses the peer import policy to mark matching routes with a marker community, which can then be matched exactly (no regex needed) in the VRF import policy.
