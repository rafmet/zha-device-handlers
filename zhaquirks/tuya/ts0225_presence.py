"""TS0225 presence sensor."""

from zigpy.quirks import CustomCluster
from zigpy.quirks.v2 import EntityType
from zigpy.quirks.v2.homeassistant import UnitOfLength, UnitOfTime
from zigpy.quirks.v2.homeassistant.number import NumberDeviceClass
from zigpy.quirks.v2.homeassistant.sensor import SensorDeviceClass, SensorStateClass
from zigpy.zcl.foundation import BaseAttributeDefs, Status, ZCLAttributeDef, ZCLHeader
from zigpy.zcl.clusters.measurement import IlluminanceMeasurement
from zhaquirks.tuya.builder import TuyaQuirkBuilder
import zigpy.types as t

class TS0225IlluminanceMeasurement(CustomCluster, IlluminanceMeasurement):
    """Custom Illuminance Measurement Cluster that handles attribute 0x0000."""

    def deserialize(self, data: bytes) -> tuple[ZCLHeader, ...]:
        return super().deserialize(data[:-2])

class TS0225Config(CustomCluster):
    """TS0225 specific cluster."""

    cluster_id = 0xE002

    class AttributeDefs(BaseAttributeDefs):
        """Attribute Definitions."""

        presence_keep_time = ZCLAttributeDef(
            id=0xE001, type=t.uint16_t, is_manufacturer_specific=False
        )
        motion_detection_sensitivity = ZCLAttributeDef(
            id=0xE004, type=t.uint8_t, access="rw", is_manufacturer_specific=False
        )
        static_detection_sensitivity = ZCLAttributeDef(
            id=0xE005, type=t.uint8_t, access="rw", is_manufacturer_specific=False
        )
        led_indicator = ZCLAttributeDef(
            id=0xE009, type=t.uint8_t, access="rw", is_manufacturer_specific=False
        )
        target_distance = ZCLAttributeDef(
            id=0xE00A, type=t.uint16_t, is_manufacturer_specific=False
        )
        motion_detection_distance = ZCLAttributeDef(
            id=0xE00B, type=t.uint16_t, access="rw", is_manufacturer_specific=False
        )

    async def write_attributes(self, attributes, manufacturer=None):
        res = await super().write_attributes(attributes, manufacturer=manufacturer)

        for record in res[0]:
            if record.attrid == 0xE009 and record.status == Status.INVALID_DATA_TYPE:
                record.status = Status.SUCCESS

        return res

(
    TuyaQuirkBuilder("_TZ3218_t9ynfz4x", "TS0225")
    .adds(TS0225IlluminanceMeasurement)
    .replaces(TS0225Config)
    .sensor(
        TS0225Config.AttributeDefs.target_distance.name,
        TS0225Config.cluster_id,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.DISTANCE,
        unit=UnitOfLength.CENTIMETERS,
        entity_type=EntityType.STANDARD,
        translation_key="target_distance",
        fallback_name="Target distance",
    )
    .sensor(
        TS0225Config.AttributeDefs.presence_keep_time.name,
        TS0225Config.cluster_id,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.DURATION,
        unit=UnitOfTime.MINUTES,
        entity_type=EntityType.STANDARD,
        translation_key="presence_time",
        fallback_name="Presence Time",
    )
    .number(
        TS0225Config.AttributeDefs.motion_detection_sensitivity.name,
        TS0225Config.cluster_id,
        min_value=0,
        max_value=5,
        step=1,
        translation_key="motion_sensitivity",
        fallback_name="Motion sensitivity",
    )
    .number(
        TS0225Config.AttributeDefs.static_detection_sensitivity.name,
        TS0225Config.cluster_id,
        min_value=0,
        max_value=5,
        step=1,
        translation_key="motionless_sensitivity",
        fallback_name="Motionless detection sensitivity",
    )
    .number(
        TS0225Config.AttributeDefs.motion_detection_distance.name,
        TS0225Config.cluster_id,
        device_class=NumberDeviceClass.DISTANCE,
        unit=UnitOfLength.CENTIMETERS,
        min_value=75,
        max_value=600,
        step=75,
        translation_key="motion_detection_distance",
        fallback_name="Motion detection distance",
    )
    .tuya_number(
        dp_id=101,
        attribute_name="fading_time",
        type=t.uint16_t,
        min_value=10,
        max_value=10000,
        step=1,
        unit=UnitOfTime.SECONDS,
        fallback_name="Fading time",
        translation_key="fading_time",
    )
    .switch(
        TS0225Config.AttributeDefs.led_indicator.name,
        TS0225Config.cluster_id,
        translation_key="led_indicator",
        fallback_name="LED indicator",
    )
    .tuya_enchantment()
    .skip_configuration()
    .add_to_registry()
)
