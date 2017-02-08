from rest_framework import serializers

from ipam.models import IPAddress
from dcim.models import (
    CONNECTION_STATUS_CHOICES, ConsolePort, ConsolePortTemplate, ConsoleServerPort, ConsoleServerPortTemplate, Device,
    DeviceBay, DeviceBayTemplate, DeviceType, DeviceRole, IFACE_FF_CHOICES, IFACE_ORDERING_CHOICES, Interface,
    InterfaceConnection, InterfaceTemplate, Manufacturer, Module, Platform, PowerOutlet, PowerOutletTemplate, PowerPort,
    PowerPortTemplate, Rack, RackGroup, RackRole, RACK_FACE_CHOICES, RACK_TYPE_CHOICES, RACK_WIDTH_CHOICES, Site,
    STATUS_CHOICES, SUBDEVICE_ROLE_CHOICES,
)
from extras.api.serializers import CustomFieldValueSerializer
from tenancy.api.serializers import NestedTenantSerializer
from utilities.api import ChoiceFieldSerializer


#
# Sites
#

class SiteSerializer(serializers.ModelSerializer):
    tenant = NestedTenantSerializer()
    custom_field_values = CustomFieldValueSerializer(many=True)

    class Meta:
        model = Site
        fields = [
            'id', 'name', 'slug', 'tenant', 'facility', 'asn', 'physical_address', 'shipping_address', 'contact_name',
            'contact_phone', 'contact_email', 'comments', 'custom_field_values', 'count_prefixes', 'count_vlans',
            'count_racks', 'count_devices', 'count_circuits',
        ]


class NestedSiteSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='dcim-api:site-detail')

    class Meta:
        model = Site
        fields = ['id', 'url', 'name', 'slug']


class WritableSiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Site
        fields = [
            'id', 'name', 'slug', 'tenant', 'facility', 'asn', 'physical_address', 'shipping_address', 'contact_name',
            'contact_phone', 'contact_email', 'comments',
        ]


#
# Rack groups
#

class RackGroupSerializer(serializers.ModelSerializer):
    site = NestedSiteSerializer()

    class Meta:
        model = RackGroup
        fields = ['id', 'name', 'slug', 'site']


class NestedRackGroupSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='dcim-api:rackgroup-detail')

    class Meta:
        model = RackGroup
        fields = ['id', 'url', 'name', 'slug']


class WritableRackGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = RackGroup
        fields = ['id', 'name', 'slug', 'site']


#
# Rack roles
#

class RackRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = RackRole
        fields = ['id', 'name', 'slug', 'color']


class NestedRackRoleSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='dcim-api:rackrole-detail')

    class Meta:
        model = RackRole
        fields = ['id', 'url', 'name', 'slug']


#
# Racks
#


class RackSerializer(serializers.ModelSerializer):
    site = NestedSiteSerializer()
    group = NestedRackGroupSerializer()
    tenant = NestedTenantSerializer()
    role = NestedRackRoleSerializer()
    type = ChoiceFieldSerializer(choices=RACK_TYPE_CHOICES)
    width = ChoiceFieldSerializer(choices=RACK_WIDTH_CHOICES)
    custom_field_values = CustomFieldValueSerializer(many=True)

    class Meta:
        model = Rack
        fields = [
            'id', 'name', 'facility_id', 'display_name', 'site', 'group', 'tenant', 'role', 'type', 'width', 'u_height',
            'desc_units', 'comments', 'custom_field_values',
        ]


class NestedRackSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='dcim-api:rack-detail')

    class Meta:
        model = Rack
        fields = ['id', 'url', 'name', 'display_name']


class WritableRackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rack
        fields = [
            'id', 'name', 'facility_id', 'site', 'group', 'tenant', 'role', 'type', 'width', 'u_height', 'desc_units',
            'comments',
        ]


#
# Manufacturers
#

class ManufacturerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Manufacturer
        fields = ['id', 'name', 'slug']


class NestedManufacturerSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='dcim-api:manufacturer-detail')

    class Meta:
        model = Manufacturer
        fields = ['id', 'url', 'name', 'slug']


#
# Device types
#

class DeviceTypeSerializer(serializers.ModelSerializer):
    manufacturer = NestedManufacturerSerializer()
    interface_ordering = ChoiceFieldSerializer(choices=IFACE_ORDERING_CHOICES)
    subdevice_role = ChoiceFieldSerializer(choices=SUBDEVICE_ROLE_CHOICES)
    instance_count = serializers.IntegerField(source='instances.count', read_only=True)
    custom_field_values = CustomFieldValueSerializer(many=True)

    class Meta:
        model = DeviceType
        fields = [
            'id', 'manufacturer', 'model', 'slug', 'part_number', 'u_height', 'is_full_depth', 'interface_ordering',
            'is_console_server', 'is_pdu', 'is_network_device', 'subdevice_role', 'comments', 'custom_field_values',
            'instance_count',
        ]


class NestedDeviceTypeSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='dcim-api:devicetype-detail')
    manufacturer = NestedManufacturerSerializer()

    class Meta:
        model = DeviceType
        fields = ['id', 'url', 'manufacturer', 'model', 'slug']


class WritableDeviceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeviceType
        fields = [
            'id', 'manufacturer', 'model', 'slug', 'part_number', 'u_height', 'is_full_depth', 'interface_ordering',
            'is_console_server', 'is_pdu', 'is_network_device', 'subdevice_role', 'comments',
        ]


#
# Console port templates
#

class ConsolePortTemplateSerializer(serializers.ModelSerializer):
    device_type = NestedDeviceTypeSerializer()

    class Meta:
        model = ConsolePortTemplate
        fields = ['id', 'device_type', 'name']


class WritableConsolePortTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConsolePortTemplate
        fields = ['id', 'device_type', 'name']


#
# Console server port templates
#

class ConsoleServerPortTemplateSerializer(serializers.ModelSerializer):
    device_type = NestedDeviceTypeSerializer()

    class Meta:
        model = ConsoleServerPortTemplate
        fields = ['id', 'device_type', 'name']


class WritableConsoleServerPortTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConsoleServerPortTemplate
        fields = ['id', 'device_type', 'name']


#
# Power port templates
#

class PowerPortTemplateSerializer(serializers.ModelSerializer):
    device_type = NestedDeviceTypeSerializer()

    class Meta:
        model = PowerPortTemplate
        fields = ['id', 'device_type', 'name']


class WritablePowerPortTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PowerPortTemplate
        fields = ['id', 'device_type', 'name']


#
# Power outlet templates
#

class PowerOutletTemplateSerializer(serializers.ModelSerializer):
    device_type = NestedDeviceTypeSerializer()

    class Meta:
        model = PowerOutletTemplate
        fields = ['id', 'device_type', 'name']


class WritablePowerOutletTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PowerOutletTemplate
        fields = ['id', 'device_type', 'name']


#
# Interface templates
#

class InterfaceTemplateSerializer(serializers.ModelSerializer):
    device_type = NestedDeviceTypeSerializer()
    form_factor = ChoiceFieldSerializer(choices=IFACE_FF_CHOICES)

    class Meta:
        model = InterfaceTemplate
        fields = ['id', 'device_type', 'name', 'form_factor', 'mgmt_only']


class WritableInterfaceTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = InterfaceTemplate
        fields = ['id', 'device_type', 'name', 'form_factor', 'mgmt_only']


#
# Device bay templates
#

class DeviceBayTemplateSerializer(serializers.ModelSerializer):
    device_type = NestedDeviceTypeSerializer()

    class Meta:
        model = DeviceBayTemplate
        fields = ['id', 'device_type', 'name']


class WritableDeviceBayTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeviceBayTemplate
        fields = ['id', 'device_type', 'name']


#
# Device roles
#

class DeviceRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeviceRole
        fields = ['id', 'name', 'slug', 'color']


class NestedDeviceRoleSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='dcim-api:devicerole-detail')

    class Meta:
        model = DeviceRole
        fields = ['id', 'url', 'name', 'slug']


#
# Platforms
#

class PlatformSerializer(serializers.ModelSerializer):

    class Meta:
        model = Platform
        fields = ['id', 'name', 'slug', 'rpc_client']


class NestedPlatformSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='dcim-api:platform-detail')

    class Meta:
        model = Platform
        fields = ['id', 'url', 'name', 'slug']


#
# Devices
#

# Cannot import ipam.api.NestedIPAddressSerializer due to circular dependency
class DeviceIPAddressSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='ipam-api:ipaddress-detail')

    class Meta:
        model = IPAddress
        fields = ['id', 'url', 'family', 'address']


class DeviceSerializer(serializers.ModelSerializer):
    device_type = NestedDeviceTypeSerializer()
    device_role = NestedDeviceRoleSerializer()
    tenant = NestedTenantSerializer()
    platform = NestedPlatformSerializer()
    rack = NestedRackSerializer()
    face = ChoiceFieldSerializer(choices=RACK_FACE_CHOICES)
    status = ChoiceFieldSerializer(choices=STATUS_CHOICES)
    primary_ip = DeviceIPAddressSerializer()
    primary_ip4 = DeviceIPAddressSerializer()
    primary_ip6 = DeviceIPAddressSerializer()
    parent_device = serializers.SerializerMethodField()
    custom_field_values = CustomFieldValueSerializer(many=True)

    class Meta:
        model = Device
        fields = [
            'id', 'name', 'display_name', 'device_type', 'device_role', 'tenant', 'platform', 'serial', 'asset_tag',
            'rack', 'position', 'face', 'parent_device', 'status', 'primary_ip', 'primary_ip4', 'primary_ip6',
            'comments', 'custom_field_values',
        ]

    def get_parent_device(self, obj):
        try:
            device_bay = obj.parent_bay
        except DeviceBay.DoesNotExist:
            return None
        return {
            'id': device_bay.device.pk,
            'name': device_bay.device.name,
            'device_bay': {
                'id': device_bay.pk,
                'name': device_bay.name,
            }
        }


class NestedDeviceSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='dcim-api:device-detail')

    class Meta:
        model = Device
        fields = ['id', 'url', 'name', 'display_name']


class WritableDeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        fields = [
            'id', 'name', 'device_type', 'device_role', 'tenant', 'platform', 'serial', 'asset_tag', 'rack', 'position',
            'face', 'status', 'primary_ip4', 'primary_ip6', 'comments',
        ]


#
# Console server ports
#

class ConsoleServerPortSerializer(serializers.ModelSerializer):
    device = NestedDeviceSerializer()

    class Meta:
        model = ConsoleServerPort
        fields = ['id', 'device', 'name', 'connected_console']


class WritableConsoleServerPortSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConsoleServerPort
        fields = ['id', 'device', 'name', 'connected_console']


#
# Console ports
#

class ConsolePortSerializer(serializers.ModelSerializer):
    device = NestedDeviceSerializer()
    cs_port = ConsoleServerPortSerializer()

    class Meta:
        model = ConsolePort
        fields = ['id', 'device', 'name', 'cs_port', 'connection_status']


class WritableConsolePortSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConsolePort
        fields = ['id', 'device', 'name', 'cs_port', 'connection_status']


#
# Power outlets
#

class PowerOutletSerializer(serializers.ModelSerializer):
    device = NestedDeviceSerializer()

    class Meta:
        model = PowerOutlet
        fields = ['id', 'device', 'name', 'connected_port']


class WritablePowerOutletSerializer(serializers.ModelSerializer):

    class Meta:
        model = PowerOutlet
        fields = ['id', 'device', 'name', 'connected_port']


#
# Power ports
#

class PowerPortSerializer(serializers.ModelSerializer):
    device = NestedDeviceSerializer()
    power_outlet = PowerOutletSerializer()

    class Meta:
        model = PowerPort
        fields = ['id', 'device', 'name', 'power_outlet', 'connection_status']


class WritablePowerPortSerializer(serializers.ModelSerializer):

    class Meta:
        model = PowerPort
        fields = ['id', 'device', 'name', 'power_outlet', 'connection_status']


#
# Interfaces
#


class InterfaceSerializer(serializers.ModelSerializer):
    device = NestedDeviceSerializer()
    form_factor = ChoiceFieldSerializer(choices=IFACE_FF_CHOICES)
    connection = serializers.SerializerMethodField(read_only=True)
    connected_interface = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Interface
        fields = [
            'id', 'device', 'name', 'form_factor', 'mac_address', 'mgmt_only', 'description', 'connection',
            'connected_interface',
        ]

    def get_connection(self, obj):
        if obj.connection:
            return NestedInterfaceConnectionSerializer(obj.connection, context=self.context).data
        return None

    def get_connected_interface(self, obj):
        if obj.connected_interface:
            return PeerInterfaceSerializer(obj.connected_interface, context=self.context).data
        return None


class PeerInterfaceSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='dcim-api:interface-detail')
    device = NestedDeviceSerializer()

    class Meta:
        model = Interface
        fields = ['id', 'url', 'device', 'name', 'form_factor', 'mac_address', 'mgmt_only', 'description']


class WritableInterfaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interface
        fields = ['id', 'device', 'name', 'form_factor', 'mac_address', 'mgmt_only', 'description']


#
# Device bays
#

class DeviceBaySerializer(serializers.ModelSerializer):
    device = NestedDeviceSerializer()
    installed_device = NestedDeviceSerializer()

    class Meta:
        model = DeviceBay
        fields = ['id', 'device', 'name', 'installed_device']


class WritableDeviceBaySerializer(serializers.ModelSerializer):

    class Meta:
        model = DeviceBay
        fields = ['id', 'device', 'name']


#
# Modules
#

class ModuleSerializer(serializers.ModelSerializer):
    device = NestedDeviceSerializer()
    manufacturer = NestedManufacturerSerializer()

    class Meta:
        model = Module
        fields = ['id', 'device', 'parent', 'name', 'manufacturer', 'part_id', 'serial', 'discovered']


class WritableModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Module
        fields = ['id', 'device', 'parent', 'name', 'manufacturer', 'part_id', 'serial', 'discovered']


#
# Interface connections
#

class InterfaceConnectionSerializer(serializers.ModelSerializer):
    interface_a = PeerInterfaceSerializer()
    interface_b = PeerInterfaceSerializer()
    connection_status = ChoiceFieldSerializer(choices=CONNECTION_STATUS_CHOICES)

    class Meta:
        model = InterfaceConnection
        fields = ['id', 'interface_a', 'interface_b', 'connection_status']


class NestedInterfaceConnectionSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='dcim-api:interfaceconnection-detail')

    class Meta:
        model = InterfaceConnection
        fields = ['id', 'url', 'connection_status']


class WritableInterfaceConnectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = InterfaceConnection
        fields = ['id', 'interface_a', 'interface_b', 'connection_status']
