"""Tuya garage door opener"""

from zigpy.quirks.v2.homeassistant.binary_sensor import BinarySensorDeviceClass

from zhaquirks.tuya.builder import TuyaQuirkBuilder

(
    TuyaQuirkBuilder("_TZE608_fmemczv1", "TS0603")
    .tuya_onoff(dp_id=1)
    .tuya_binary_sensor(
        dp_id=3,
        device_class=BinarySensorDeviceClass.GARAGE_DOOR,
        attribute_name="garage_door",
        translation_key="garage_door",
        fallback_name="Garage door",
    )
    .skip_configuration()
    .add_to_registry()
)
