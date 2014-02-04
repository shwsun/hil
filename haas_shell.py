import haas.command_pattern
import haas.control
import haas.er


class_name={'group':haas.er.Group,
            'vm':haas.er.VM,
            'node':haas.er.Node,
            'user':haas.er.User}

def create_group(cmd):
    '''
    do the neccessary parsing
    and call haas.control
    '''
    parts = haas.command_pattern.create_group.match(cmd)
    group_name = parts.group(1)

    #print group_name, network_id, vm_name
    haas.control.create_group(group_name)

def create_node(cmd):
    parts = haas.command_pattern.create_node.match(cmd)
    node_id= int(parts.group(1))
    haas.control.create_node(node_id)

def create_nic(cmd):
    parts = haas.command_pattern.create_nic.match(cmd)
    nic_id,mac_addr,name = parts.groups()
    nic_id = int(nic_id)
    haas.control.create_nic(nic_id,mac_addr,name)

def create_port(cmd):
    parts = haas.command_pattern.create_port.match(cmd)
    port_id, switch_id, port_no = map(int, parts.groups())
    haas.control.create_port(port_id,switch_id,port_no)
def add_nic(cmd):
    parts = haas.command_pattern.add_nic.match(cmd)
    nic_id, node_id = map(int,parts.groups())
    haas.control.add_nic(nic_id,node_id)

def create_switch(cmd):
    parts = haas.command_pattern.create_switch.match(cmd)
    switch_id, script = parts.groups()
    switch_id = int(switch_id)
    haas.control.create_switch(switch_id,script)

def connect_nic(cmd):
    parts = haas.command_pattern.connect_nic.match(cmd)
    nic_id, port_id = map(int,parts.groups())
    haas.control.connect_nic(nic_id,port_id)

def create_vlan(cmd):
    parts = haas.command_pattern.create_vlan.match(cmd)
    vlan_id = int(parts.group(1))
    haas.control.create_vlan(vlan_id)

def connect_vlan(cmd):
    parts = haas.command_pattern.connect_vlan.match(cmd)
    vlan_id,group_name,nic_name = parts.groups()
    vlan_id = int(vlan_id)
    haas.control.connect_vlan(vlan_id,group_name,nic_name)
    
    
    
def add_node(cmd):
    '''
    add one node to a group
    '''
    parts = haas.command_pattern.add_node.match(cmd)
    node_id,group_name = parts.groups()
    node_id = int(node_id)

    haas.control.add_node_to_group(node_id,group_name)

def remove_node(cmd):
    '''
    remove one node from a group
    '''
    parts = haas.command_pattern.remove.match(cmd)
    node_id = int(parts.group(1))
    group_name = parts.group(2)
    #print 'add',node_id,'to',group_name
    haas.control.remove_node_from_group(node_id,group_name)

def deploy_group(cmd):
    parts = haas.command_pattern.deploy_group.match(cmd)
    group_name = parts.group(1)
    haas.control.deploy_group(group_name)

def show_table(cmd):
    parts = haas.command_pattern.show_table.match(cmd)
    table = parts.group(1)
    if table not in class_name:
        print 'no such table'
        print 'available tables are:'
        for key in class_name:
            print key
        return
    haas.control.query_db(class_name[table])

def show_all():
    haas.control.query_db(haas.er.Node)
    haas.control.query_db(haas.er.NIC)
    haas.control.query_db(haas.er.Port)
    haas.control.query_db(haas.er.Vlan)
    haas.control.query_db(haas.er.VM)
    haas.control.query_db(haas.er.Switch)
    haas.control.query_db(haas.er.Group)
    haas.control.query_db(haas.er.User)

def auth(user_name,password):
    user = haas.control.get_entity_by_cond(haas.er.User,'user_name=="%s"'%(user_name))
    print user
    if not user:
        return False
    return user.password == password

def create_user(cmd):
    user_name,password = haas.command_pattern.create_user.match(cmd).groups()
    haas.control.create_user(user_name,password)


while True:
    user_name = raw_input('user:')
    password = raw_input("password:")
    if auth(user_name,password):
      haas.control.login_user(user_name)
      break
    print 'invalid user/password combination!'


while True:
    cmd = raw_input('haas>')
    if haas.command_pattern.create_group.match(cmd):
        create_group(cmd)
    elif cmd == 'show all':
        show_all()
    elif haas.command_pattern.deploy_group.match(cmd):
        deploy_group(cmd)
    elif haas.command_pattern.show_group.match(cmd):
        print 'show group'
    elif haas.command_pattern.show_free_table.match(cmd):
        print 'free table'
    elif haas.command_pattern.show_table.match(cmd):
        show_table(cmd)
    elif haas.command_pattern.create_vlan.match(cmd):
        create_vlan(cmd)
    elif haas.command_pattern.change_head.match(cmd):
        print 'ch head'
    elif haas.command_pattern.create_node.match(cmd):
        print 'create node'
        create_node(cmd)
    elif haas.command_pattern.create_nic.match(cmd):
        create_nic(cmd)
    elif haas.command_pattern.add_nic.match(cmd):
        add_nic(cmd)
    elif haas.command_pattern.create_port.match(cmd):
        create_port(cmd)
    elif haas.command_pattern.create_switch.match(cmd):
        create_switch(cmd)
    elif haas.command_pattern.connect_nic.match(cmd):
        connect_nic(cmd)
    elif haas.command_pattern.connect_vlan.match(cmd):
        connect_vlan(cmd)
    elif haas.command_pattern.add_node.match(cmd):
        print 'add node'
        add_node(cmd)
    elif haas.command_pattern.remove.match(cmd):
        print 'remove node'
        remove_node(cmd)
    elif haas.command_pattern.create_user.match(cmd):
        create_user(cmd)
    elif cmd == 'exit':
        #Might need check before exit
        print 'Bye for now'
        exit()
    else:
        print 'invalid command'
        print 'usage'
        print haas.command_pattern.help_text
        