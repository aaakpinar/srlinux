from srlinux.data import ColumnFormatter, TagValueFormatter, Border, Data, Borders, Alignment
from srlinux.mgmt.cli import CliPlugin
from srlinux.schema import FixedSchemaRoot
from srlinux.syntax import Syntax
from srlinux.location import build_path
import datetime

############################ INPUTs here... ################################ 
# fill the interfaces list in or a pattern in the uplink descriptions   
# if both given: interfaces list has precedence over the description pattern                                                                      
interfaces = []                                                         
description = "spine"
                                        
# e/iBGP group names
uplink_peer_group = "eBGP-underlay"
rr_peer_group = "to-vRR-overlay"

# network instance is typically default
uplink_network_instance = "default"
############################################################################


class Plugin(CliPlugin):
    
    def load(self, cli, **_kwargs):
        fabric = cli.show_mode.add_command(Syntax('fabric', help='shows how to give the input parameters for "show fabric" commands'))
        help = fabric.add_command(Syntax('help', help='requires uplinks, route-reflector, statistics or summary keywords'),update_location=False, callback=self._show_help)
        summary = fabric.add_command(Syntax('summary', help='shows uplinks, route-reflector and statistics all together'), update_location=False, callback=self._show_summary, schema=self._get_schema())
        platform = fabric.add_command(Syntax('platform', help='shows platform information in text'), update_location=False, callback=self._show_platform, schema=self._get_schema())
        uplink = fabric.add_command(Syntax('uplink', help='shows uplinks in a table'), update_location=False, callback=self._show_uplinks, schema=self._get_schema())
        route_reflector = fabric.add_command(Syntax('route-reflector', help='shows route-reflectors in a table'), update_location=False, callback=self._show_rr, schema=self._get_schema())
        statistics =  fabric.add_command(Syntax('statistics', help='shows statistics in a table'), update_location=False, callback=self._show_stats, schema=self._get_schema())

    def _show_help (self,state,output,**_kwargs):
        print('''
        The 'show fabric' command shows you statistics and the status of the uplinks and BGP peerings. 
        Therefore it requires some inputs that need to be added in the 'fabric.py' file.
        
        '/etc/opt/srlinux/cli/plugins/fabric.py'
        
        Example:
        interfaces = []             # fill the interfaces list in or the description pattern
        description = "spine"
        uplink_peer_group = "eBGP-underlay"
        rr_peer_group = "to-vRR-overlay"
        ''')

    def _show_summary(self, state, output, **_kwargs):

        header = f'Fabric Connectivity Report'
        result_header = self._populate_header(header)
        self._set_formatters_header(result_header)
        output.print_data(result_header)
        self._show_platform(state,output)
        self._show_uplinks(state,output)
        self._show_rr(state,output)
        self._show_stats(state,output)
    
    
    def _show_platform(self, state, output, **_kwargs):
        result_platform = Data(self._get_schema())
        self._set_formatters_platform(result_platform)
        with output.stream_data(result_platform):   
          self._populate_data_platform(result_platform, state)
    
    def _show_uplinks(self, state, output, **_kwargs):
        result = Data(self._get_schema())
        self._set_formatters_uplink(result)
        with output.stream_data(result):   
          self._populate_data_uplink(result, state)

    def _show_rr(self, state, output, **_kwargs):
        result_rr = Data(self._get_schema())
        self._set_formatters_rr(result_rr)
        with output.stream_data(result_rr):   
          self._populate_data_rr(result_rr, state)
        
    def _show_stats(self, state, output, **_kwargs):
        result_stats = Data(self._get_schema())
        self._set_formatters_stats(result_stats)
        with output.stream_data(result_stats):   
          self._populate_data_stats(result_stats, state)   
    
    def _get_header_schema(self):
        root = FixedSchemaRoot()
        root.add_child(
            'header',
            fields=['Summary']
        )
        return root

    def _get_schema(self):
        root = FixedSchemaRoot()
        platform_header = root.add_child(
            'platform_header',
            fields=['platform']
        )
        platform_header.add_child(
            'platform_child',
            key='Chassis Type',
            fields=['S/N', 'Uptime','CPU (%)','Memory (%)','Disk Partitions (%)']
        )
        uplink_header = root.add_child(
            'uplink_header',
            fields=['uplinks']
        )
        uplink_header.add_child(
            'uplink_child',
            key='Local Interface',
            fields=['Local Router', 'Link Status','eBGP Status','Remote Router', 'Remote Interface']
        )
        rr_header = root.add_child(
            'rr_header',
            fields=['Route Reflectors']
        )
        rr_header.add_child(
            'rr_child',
            key='Route Reflector Address',
            fields=['iBGP Status', 'Neighbor Description', 'Rx/Active/Tx', 'Uptime (hh:mm:ss)']
        )
        stats_header = root.add_child(
            'stats_header',
            fields=['Uplink Stats']
        )
        stats_header.add_child(
            'stats_child',
            key='Local Interface',
            fields=['Traffic Bps In/Out','Packets In/Out', 'Errored In/Out', 'FCS Err', 'CRC Err','Transceiver Volt']
        )
        return root

    def _fetch_state_platform(self, state):
        chassis_path = build_path(f'/platform/chassis')
        self.chassis_data = state.server_data_store.stream_data(chassis_path, recursive=True)
        
        # chassis_type_path = build_path(f'/platform/chassis/type')
        # self.chassis_type_data = state.server_data_store.stream_data(chassis_type_path, recursive=True)
        
        # serial_path = build_path(f'/platform/chassis/serial-number')
        # self.serial_data = state.server_data_store.stream_data(serial_path, recursive=True)       
        
        # uptime_path = build_path(f'/platform/chassis/last-booted')
        # self.uptime_data = state.server_data_store.stream_data(uptime_path, recursive=True)
        
        cpu_path = build_path(f'/platform/control[slot=*]/cpu[index=all]/total/average-5')
        self.cpu_data = state.server_data_store.stream_data(cpu_path, recursive=True)
        
        mem_path = build_path(f'/platform/control[slot=*]/memory/utilization')
        self.mem_data = state.server_data_store.stream_data(mem_path, recursive=True)

        disk_path = build_path(f'/platform/control[slot=*]/disk[name=*]/partition[name=*]/percent-used')
        self.disk_data = state.server_data_store.stream_data(disk_path, recursive=True)

    def _fetch_state_uplink(self, state, uplink, interf):
        int_oper_state_path = build_path(f'/interface[name={interf[0]}]/subinterface[index={interf[1]}]/oper-state')
        self.int_oper_state_data = state.server_data_store.stream_data(int_oper_state_path, recursive=True)
        
        sys_name_path = build_path(f'/system/name/host-name')
        self.sys_name_data = state.server_data_store.stream_data(sys_name_path, recursive=True)
        
        lldp_neighbor_path = build_path(f'/system/lldp/interface[name={interf[0]}]/neighbor')
        self.lldp_neighbor_data = state.server_data_store.stream_data(lldp_neighbor_path, recursive=True)
        
        session_state_path = build_path(f'/network-instance[name={uplink_network_instance}]/protocols/bgp/neighbor[peer-address={uplink}]')
        self.session_state_data = state.server_data_store.stream_data(session_state_path, recursive=True)
 
    def _fetch_state_rr(self, state, rr):
        rr_path = build_path(f'/network-instance[name={uplink_network_instance}]/protocols/bgp/neighbor[peer-address={rr}]')
        self.rr_data = state.server_data_store.stream_data(rr_path, recursive=True)    
        
        #time_path = build_path(f'/system/information/current-datetime')
        #self.time_data = state.server_data_store.stream_data(time_path, recursive=True) 
        
        # rr_tcp_path = build_path(f'/network-instance[name={uplink_network_instance}]/tcp/connections[remote-address={rr}]')
        # self.rr_tcp_data = state.server_data_store.stream_data(rr_tcp_path, recursive=True)        

    def _fetch_state_stats(self, state, uplink):          
        gen_path = build_path(f'/interface[name={uplink}]')
        self.gen_data = state.server_data_store.stream_data(gen_path, recursive=True)
               
    def _time_handler (self, state, dt1):
        time_path = build_path(f'/system/information/current-datetime')
        self.time_data = state.server_data_store.stream_data(time_path, recursive=True) 
        dt0 = self.time_data.system.get().information.get().current_datetime
        now = datetime.datetime(int(dt0[:4]),int(dt0[5:7]),int(dt0[8:10]),int(dt0[11:13]),int(dt0[14:16]),int(dt0[17:19]))       
        then = datetime.datetime(int(dt1[:4]),int(dt1[5:7]),int(dt1[8:10]),int(dt1[11:13]),int(dt1[14:16]),int(dt1[17:19]))       
        return (now-then)
        
    def _populate_header(self, header):
        result_header = Data(self._get_header_schema())
        data = result_header.header.create()
        data.summary = header
        return result_header

    def _populate_data_platform(self, result, state):                   
        result.synchronizer.flush_fields(result)
        data = result.platform_header.create()
        server_data = self._fetch_state_platform(state)
        chassis_type = self.chassis_data.platform.get().chassis.get().type or '<Unknown>'
        data_child = data.platform_child.create(chassis_type)
        data_child.s_n = self.chassis_data.platform.get().chassis.get().serial_number or '<Unknown>'
        data_child.uptime = self._time_handler(state, self.chassis_data.platform.get().chassis.get().last_booted)
        data_child.cpu____ = self.cpu_data.platform.get().control.get().cpu.get().total.get().average_5 or '<Unknown>'
        data_child.memory____ = self.mem_data.platform.get().control.get().memory.get().utilization or '<Unknown>'
        first = True
        for d in self.disk_data.platform.get().control.get().disk.get().partition.items():
            if first:
                first = False
                disk_util=str(self.disk_data.platform.get().control.get().disk.get("/dev/sda").partition.get(d.name).percent_used)
            else:
                disk_util+=str(f'/{self.disk_data.platform.get().control.get().disk.get("/dev/sda").partition.get(d.name).percent_used}')
            
        data_child.disk_partitions____ = disk_util

        
        data_child.synchronizer.flush_fields(data_child)
        result.synchronizer.flush_children(result.platform_header)  
        return result

    def _populate_peer_list(self, state, group):
        peer_list_path = build_path(f'/network-instance[name={uplink_network_instance}]/protocols/bgp/neighbor/peer-group')
        peer_list_data = state.server_data_store.stream_data(peer_list_path, recursive=True) 
        peer_list = []
        for peer in peer_list_data.network_instance.get().protocols.get().bgp.get().neighbor.items():
            if peer.peer_group == group :
                peer_list.append(peer.peer_address) 
        if not peer_list: print(f"No peer in <<{group}>> group! \n\n PLEASE SET THE CORRECT PARAMETERS WITH 'set-show-fabric.sh' OR DIRECTLY IN THE '/etc/opt/srlinux/cli/plugins/fabric.py' FROM THE BASH!\n")
        return peer_list
                
    def _populate_interface_list(self, state, description):
        int_list_path = build_path(f'/interface[name=*]/subinterface[index=*]/description')
        int_list_data = state.server_data_store.stream_data(int_list_path, recursive=True) 
        int_list = []
        for i in int_list_data.interface.items():
            if description in i.subinterface.get().description:
                interfaces.append(f'{i.name}.{i.subinterface.get().index}')
        if not interfaces: print(f"No interface has <<{description}>> in its description! \n\n PLEASE SET THE CORRECT PARAMETERS WITH 'set-show-fabric.sh' OR DIRECTLY IN THE '/etc/opt/srlinux/cli/plugins/fabric.py' FROM THE BASH!\n")

    def _populate_data_uplink(self, result, state):
        uplink_peer_list = self._populate_peer_list(state,uplink_peer_group)       
        result.synchronizer.flush_fields(result)
        if not interfaces: self._populate_interface_list(state,description)
        i=0
        data = result.uplink_header.create()
        for interface in interfaces:
          server_data = self._fetch_state_uplink(state, uplink_peer_list[i], interface.split('.'))
          data_child = data.uplink_child.create(interfaces[i].split('.')[0])
          data_child.local_router = self.sys_name_data.system.get().name.get().host_name or '<Unknown>'
          data_child.link_status = self.int_oper_state_data.interface.get().subinterface.get().oper_state or '<Unknown>'
          data_child.ebgp_status = self.session_state_data.network_instance.get().protocols.get().bgp.get().neighbor.get().session_state or '<Unknown>'
          data_child.remote_router = self.lldp_neighbor_data.system.get().lldp.get().interface.get().neighbor.get().system_name or '<Unknown>'
          data_child.remote_router = self.lldp_neighbor_data.system.get().lldp.get().interface.get().neighbor.get().system_name or '<Unknown>'
          data_child.remote_interface = self.lldp_neighbor_data.system.get().lldp.get().interface.get().neighbor.get().port_id or '<Unknown>'
          data_child.synchronizer.flush_fields(data_child)
          i=i+1
        result.synchronizer.flush_children(result.uplink_header)  
        return result

    def _populate_data_rr(self, result, state):                   
        rr_peer_list = self._populate_peer_list(state,rr_peer_group)
        result.synchronizer.flush_fields(result)
        i=0
        data = result.rr_header.create()
        for rr in rr_peer_list: 
          server_data = self._fetch_state_rr(state, rr)
          data_child = data.rr_child.create(rr)
          data_child.ibgp_status = self.rr_data.network_instance.get().protocols.get().bgp.get().neighbor.get().session_state or '<Unknown>'
          data_child.neighbor_description = "spine"
          data_child.rx_active_tx = f'{self.rr_data.network_instance.get().protocols.get().bgp.get().neighbor.get().evpn.get().received_routes}/'\
                                    f'{self.rr_data.network_instance.get().protocols.get().bgp.get().neighbor.get().evpn.get().active_routes}/'\
                                    f'{self.rr_data.network_instance.get().protocols.get().bgp.get().neighbor.get().evpn.get().sent_routes}' or 'Unknown'
          data_child.uptime__hh_mm_ss_ = self._time_handler(state,self.rr_data.network_instance.get().protocols.get().bgp.get().neighbor.get().last_established)
          data_child.synchronizer.flush_fields(data_child)
          i=i+1
        result.synchronizer.flush_children(result.rr_header)  
        return result

    def _populate_data_stats(self, result, state):
        uplink_peer_list = self._populate_peer_list(state,uplink_peer_group)
        result.synchronizer.flush_fields(result)
        if not interfaces: self._populate_interface_list(state,description)
        i=0
        data = result.stats_header.create()
        for interface in interfaces:
          server_data = self._fetch_state_stats(state, interface.split('.')[0])
          data_child = data.stats_child.create(interface.split('.')[0])
          data_child.traffic_bps_in_out = f'{self.gen_data.interface.get().traffic_rate.get().in_bps}/{self.gen_data.interface.get().traffic_rate.get().in_bps}'
          data_child.packets_in_out = f'{self.gen_data.interface.get().statistics.get().in_unicast_packets}/{self.gen_data.interface.get().statistics.get().out_unicast_packets or "<Unknown>"}'
          data_child.errored_in_out = f'{self.gen_data.interface.get().statistics.get().in_error_packets }/{self.gen_data.interface.get().statistics.get().out_error_packets}'
          data_child.fcs_err = self.gen_data.interface.get().statistics.get().in_fcs_error_packets
          data_child.crc_err = self.gen_data.interface.get().ethernet.get().statistics.get().in_crc_error_frames
          try: data_child.transceiver_volt =  self.gen_data.interface.get().transceiver.get().voltage.get().latest_value or 'N/A'
          except: data_child.transceiver_volt = 'N/A'
          data_child.synchronizer.flush_fields(data_child)
          i=i+1
        result.synchronizer.flush_children(result.stats_header)  
        return result
  
    def _set_formatters_header(self, data):
        data.set_formatter('/header',Border(TagValueFormatter()))  

    def _set_formatters_platform(self, data):
        data.set_formatter('/platform_header/platform_child', ColumnFormatter())  
  
    def _set_formatters_stats(self, data):
        data.set_formatter('/stats_header/stats_child', ColumnFormatter())    
    
    def _set_formatters_rr(self, data):
        data.set_formatter('/rr_header/rr_child', ColumnFormatter())

    def _set_formatters_uplink(self, data):
        data.set_formatter('/uplink_header/uplink_child', ColumnFormatter(horizontal_alignment={'Link Status':Alignment.Center}))



