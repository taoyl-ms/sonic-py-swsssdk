Schema data is defined in ABNF [RFC5234](https://tools.ietf.org/html/rfc5234) syntax.

### Definitions of common tokens
    name                    = 1*DIGIT/1*ALPHA
    ref_hash_key_reference  = "[" hash_key "]" ;The token is a refernce to another valid DB key.
    hash_key                = name ; a valid key name (i.e. exists in DB)

### DEVICE_METADATA table

### BGP_NEIGHBOR table

    ; Stores BGP session information
    bgp_neighbor_key    = IPPrefix       ; IP address of BGP neighbor
    asn                 = 1*5DIGIT       ; remote ASN
    admin_status        = "down" / "up"  ; admin status
    name                = 1*64VCHAR      ; neighbor host name
    peer_addr           = IPPrefix       ; local address used to peer with neighbor

    ;QOS Mappings
    map_dscp_to_tc  = ref_hash_key_reference
    map_tc_to_queue = ref_hash_key_reference

    Example:
    127.0.0.1:6379[4]> keys BGP_NEIGHBOR:*
     1) "BGP_NEIGHBOR:10.0.0.31"
     2) "BGP_NEIGHBOR:10.0.0.39"
     3) "BGP_NEIGHBOR:10.0.0.11"
     4) "BGP_NEIGHBOR:10.0.0.7"
     5) "BGP_NEIGHBOR:10.0.0.15"
     6) "BGP_NEIGHBOR:10.0.0.45"
     7) "BGP_NEIGHBOR:10.0.0.35"
     8) "BGP_NEIGHBOR:10.0.0.51"
     9) "BGP_NEIGHBOR:10.0.0.1"
    10) "BGP_NEIGHBOR:10.0.0.43"
    11) "BGP_NEIGHBOR:10.0.0.3"
    12) "BGP_NEIGHBOR:10.0.0.21"
    13) "BGP_NEIGHBOR:10.0.0.55"
    14) "BGP_NEIGHBOR:10.0.0.17"
    15) "BGP_NEIGHBOR:10.0.0.19"
    16) "BGP_NEIGHBOR:10.0.0.25"
    17) "BGP_NEIGHBOR:10.0.0.63"
    18) "BGP_NEIGHBOR:10.0.0.41"
    19) "BGP_NEIGHBOR:10.0.0.29"
    20) "BGP_NEIGHBOR:10.0.0.33"
    21) "BGP_NEIGHBOR:10.0.0.5"
    22) "BGP_NEIGHBOR:10.0.0.23"
    23) "BGP_NEIGHBOR:10.0.0.13"
    24) "BGP_NEIGHBOR:10.0.0.27"
    25) "BGP_NEIGHBOR:10.0.0.57"
    26) "BGP_NEIGHBOR:10.0.0.47"
    27) "BGP_NEIGHBOR:10.0.0.37"
    28) "BGP_NEIGHBOR:10.0.0.53"
    29) "BGP_NEIGHBOR:10.0.0.49"
    30) "BGP_NEIGHBOR:10.0.0.9"
    31) "BGP_NEIGHBOR:10.0.0.61"
    32) "BGP_NEIGHBOR:10.0.0.59"
    127.0.0.1:6379[4]> hgetall BGP_NEIGHBOR:10.0.0.13
    1) "admin_status"
    2) "up"
    3) "peer_addr"
    4) "10.0.0.12"
    5) "asn"
    6) "65200"
    7) "name"
    8) "ARISTA07T2"

