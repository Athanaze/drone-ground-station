make GCC_PATH=/home/sacha/tempyStuffRandom/project_usb/usb/gcc-arm-none-eabi-8-2019-q3-update/bin
echo "================"
echo "================"
echo "================"
echo "================"
st-flash write build/usb.bin 0x8000000
