# 0-100
# data source node --> edge node
DSNODE_REGISTER = 1

# data source node <-- edge node


# 100-200
# data source node --> edge node


# data source node <-- edge node





# 200-300
# edge node --> cloud
SEND_DATA_REQ = 201
SEND_DATA = 4

# edge node <-- cloud
SEND_DATA_CFM = 202


def dump_send_data_req():
    pass
def load_send_data_req():
    pass

MSG_DIC = {
    SEND_DATA_REQ:[dump_send_data_req,load_send_data_req],
    SEND_DATA_CFM:[]

}

