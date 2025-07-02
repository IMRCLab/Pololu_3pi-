west build -b nrf52840dongle .
~/sw/nrfutil pkg generate --hw-version 52 --sd-req=0x00  --application build/nrf52840dongle-firmware/zephyr/zephyr.hex --application-version 1 zephyr.zip
~/sw/nrfutil device program --firmware zephyr.zip --traits nordicDfu
