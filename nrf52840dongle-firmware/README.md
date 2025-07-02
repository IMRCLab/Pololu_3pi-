# Setup

- In vscode, install the nrf connect SDK.
- For SDK and toolkit, use the latest version (we tested with v3.0.2)
- Attach the dongle via USB and put in bootloader mode by pressing the reset button (this button is horizontal, next to the more obvious vertical button). The red LED should blink
- Open a nrf SDK terminal and then execute `./build_and_flash.sh`

Note that the code needs to be changed to change the address and each robot gets a separate address.
